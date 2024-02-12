#!/usr/bin/python

import psycopg2
from src.nibe.config import Configuration


class PostgresTasks:
    config = Configuration()

    def create_table_nibe(self) -> None:
        """create table nibe in the PostgreSQL database (database specified in config.py), saves common inverter data"""
        command = """
        CREATE TABLE nibe (
            data_id SERIAL PRIMARY KEY,
            time TIMESTAMP NOT NULL,
            aktuelle_aussenlufttemperatur FLOAT4, 
            aktuelle_vorlauftemperatur FLOAT4, 
            aktuelle_ruecklauftemperatur FLOAT4, 
            eintritt_waermequellenmedium FLOAT4, 
            austritt_waermequellenmedium FLOAT4, 
            brauchwasser_oben FLOAT4, 
            brauchwasserbereitung FLOAT4, 
            roomsensor FLOAT4, 
            berechneter_vorlauf FLOAT4, 
            volumenstrommesser FLOAT4, 
            gradminuten FLOAT4, 
            verdichterfrequenz_istwert FLOAT4, 
            verdichterstarts FLOAT4, 
            gesamtbetriebszeit_verdichter FLOAT4, 
            momentan_verwendete_leistung FLOAT4, 
            brauchwasser_nur_verdichter FLOAT4, 
            heizung_nur_verdichter FLOAT4, 
            aktueller_status FLOAT4, 
            umschaltventil_brauchwasser FLOAT4
              )
        """

        conn = None
        try:
            # read the connection parameters
            params = PostgresTasks.config.postgresql_config()
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # create table one by one
            cur.execute(command)
            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

    def insert_nibe(
        self,
        aktuelle_aussenlufttemperatur: float,
        aktuelle_vorlauftemperatur: float,
        aktuelle_ruecklauftemperatur: float,
        eintritt_waermequellenmedium: float,
        austritt_waermequellenmedium: float,
        brauchwasser_oben: float,
        brauchwasserbereitung: float,
        roomsensor: float,
        berechneter_vorlauf: float,
        volumenstrommesser: float,
        gradminuten: float,
        verdichterfrequenz_istwert: float,
        verdichterstarts: float,
        gesamtbetriebszeit_verdichter: float,
        momentan_verwendete_leistung: float,
        brauchwasser_nur_verdichter: float,
        heizung_nur_verdichter: float,
        aktueller_status: float,
        umschaltventil_brauchwasser: float,
    ) -> int:
        """insert a new data row into the nibe table"""
        sql = """INSERT INTO nibe(time, aktuelle_aussenlufttemperatur, aktuelle_vorlauftemperatur, aktuelle_ruecklauftemperatur, eintritt_waermequellenmedium, austritt_waermequellenmedium, brauchwasser_oben, brauchwasserbereitung, roomsensor, berechneter_vorlauf, volumenstrommesser, gradminuten, verdichterfrequenz_istwert, verdichterstarts, gesamtbetriebszeit_verdichter, momentan_verwendete_leistung, brauchwasser_nur_verdichter, heizung_nur_verdichter, aktueller_status, umschaltventil_brauchwasser)
                VALUES(NOW()::TIMESTAMP, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING data_id;"""
        conn = None
        data_id = None
        try:
            # read database configuration
            params = PostgresTasks.config.postgresql_config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(
                sql,
                (
                    aktuelle_aussenlufttemperatur,
                    aktuelle_vorlauftemperatur,
                    aktuelle_ruecklauftemperatur,
                    eintritt_waermequellenmedium,
                    austritt_waermequellenmedium,
                    brauchwasser_oben,
                    brauchwasserbereitung,
                    roomsensor,
                    berechneter_vorlauf,
                    volumenstrommesser,
                    gradminuten,
                    verdichterfrequenz_istwert,
                    verdichterstarts,
                    gesamtbetriebszeit_verdichter,
                    momentan_verwendete_leistung,
                    brauchwasser_nur_verdichter,
                    heizung_nur_verdichter,
                    aktueller_status,
                    umschaltventil_brauchwasser,
                ),
            )
            # get the generated id back
            data_id = cur.fetchone()[0]
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return data_id


# to test a specific function via "python postgresql_tasks.py" in the powershell
if __name__ == "__main__":
    postgres_task = PostgresTasks()
    postgres_task.create_table_nibe()
#   postgres_task.insert_nibe(84, 1734796.1200000001)
