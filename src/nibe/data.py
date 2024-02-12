# coding: utf-8
import logging
import sys
from time import sleep
from typing import Any
from pyModbusTCP.client import ModbusClient


from src.nibe.config import Configuration
from src.nibe.postgresql_tasks import PostgresTasks

from src.nibe.exceptions import (
    WrongData,
    DataCollectionError,
    UnknownRegisterTypeError,
    NoConnectionError,
)


class NibeToPostgres:

    def __init__(
        self,
        config: Configuration,
        client: PostgresTasks,
    ) -> None:
        self.config = config
        self.client = client
        self.BACKOFF_INTERVAL: int = 30  # minimum interval between calls in seconds

    def connect_modbus(self) -> ModbusClient:
        """establishes ModbusClient connection and returns it"""
        nibe_con = self.config.nibe_config()
        con = ModbusClient(
            host=nibe_con["nibe_ip"], port=nibe_con["nibe_port"], auto_open=True
        )
        if con:
            return con
        else:
            logging.error("No Connection available", exc_info=True)
            raise NoConnectionError(
                "No connection established. Check nibe_ip and nibe_port."
            )

    @staticmethod
    def get_response(con: ModbusClient, register_no: int, registertype: str) -> int:
        """uses con to read register data and returns the raw data as int"""
        if registertype == "MODBUS_INPUT_REGISTER":
            return int(con.read_input_registers(register_no))
        elif registertype == "MODBUS_HOLDING_REGISTER":
            return int(con.read_holding_registers(register_no))
        else:
            logging.error(f"Unknown register type: {registertype}", exc_info=True)
            raise UnknownRegisterTypeError("Registertype unknown")

    @staticmethod
    def process_value(
        raw_value, division_factor, register_name, other_param=0
    ) -> float:
        """modifies raw_value and returns processed data ready to store into database"""
        if register_name == "gradminuten":  # calculation for singnedint
            raw_value = raw_value - 2**16 if raw_value > 2**15 else raw_value
        if (
            register_name == "heizung_nur_verdichter"
            or register_name == "brauchwasser_nur_verdichter"
        ):  # calculation for 32 bit integer
            raw_value = raw_value + 2**16 * other_param
        return raw_value / division_factor

    def run(self) -> None:
        try:
            logging.info(f"Application started")
            yaml_config = self.config.data_names_yaml()
            while True:
                try:
                    con = self.connect_modbus()
                    processed: dict = {}  # to store processed values
                    for reg_dict in yaml_config.values():
                        raw_value = self.get_response(
                            con, reg_dict["register"], reg_dict["registertyp"]
                        )
                        logging.debug(f"Nibe Modbus TPC/IP Response: {raw_value}")
                        try:
                            other_param = reg_dict["faktor32bit"]
                        except KeyError:
                            other_param = 0

                        processed_value = self.process_value(
                            raw_value,
                            reg_dict["divisionsfaktor"],
                            reg_dict["name"],
                            other_param,
                        )
                        processed[reg_dict["name"]] = processed_value

                    con.close()
                    logging.debug(f"collected data: {processed}")
                    # insert data to database
                    data_id = self.client.insert_nibe(
                        processed["aktuelle_aussenlufttemperatur"],
                        processed["aktuelle_vorlauftemperatur"],
                        processed["aktuelle_ruecklauftemperatur"],
                        processed["eintritt_waermequellenmedium"],
                        processed["austritt_waermequellenmedium"],
                        processed["brauchwasser_oben"],
                        processed["brauchwasserbereitung"],
                        processed["roomsensor"],
                        processed["berechneter_vorlauf"],
                        processed["volumenstrommesser"],
                        processed["gradminuten"],
                        processed["verdichterfrequenz_istwert"],
                        processed["verdichterstarts"],
                        processed["gesamtbetriebszeit_verdichter"],
                        processed["momentan_verwendete_leistung"],
                        processed["brauchwasser_nur_verdichter"],
                        processed["heizung_nur_verdichter"],
                        processed["aktueller_status"],
                        processed["umschaltventil_brauchwasser"],
                    )
                    logging.info(f"Data written. Data id: {data_id}")
                    sleep(self.BACKOFF_INTERVAL)

                except ConnectionError:
                    logging.error("No Connection available", exc_info=True)
                    sleep(10)
                    logging.info("Waited 10 seconds for connection")
                except Exception as e:
                    logging.error("Exception: {}".format(e), exc_info=True)
                    sys.exit(1)

        except KeyboardInterrupt:
            logging.info("Stopping program.")
