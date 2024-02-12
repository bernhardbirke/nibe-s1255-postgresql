import os
import yaml
from configparser import ConfigParser
from dev.definitions import ROOT_DIR


class Configuration:
    def __init__(
        self,
        url_to_database: str = os.path.join(ROOT_DIR, "database.ini"),
        url_yaml_config: str = os.path.join(ROOT_DIR, "nibe-s1255-register.yaml"),
    ):
        self.url_to_database = url_to_database
        self.url_yaml_config = url_yaml_config

    def nibe_config(self, section: str = "nibe") -> dict:
        """define the details of a connection to the nibe modbus tcp/ip based on database.ini"""
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.url_to_database)

        # get section
        nibe_con = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                nibe_con[param[0]] = param[1]
        else:
            raise Exception(
                f"Section {section} not found in the {self.url_to_database} file"
            )

        return nibe_con

    def postgresql_config(self, section: str = "postgresql") -> dict:
        """define the details of a database connection based on database.ini"""
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.url_to_database)

        # get section
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception(
                f"Section {section} not found in the {self.url_to_database} file"
            )

        return db

    def yaml_config(self) -> dict:
        """creates and returns a python object based on the defined yaml file."""
        with open(self.url_yaml_config) as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    def data_names_yaml(self) -> dict:
        """creates data names based on the titel of yaml file and returns the whole yaml_dict"""
        yaml_dict: dict = self.yaml_config()
        for id, entry in yaml_dict.items():
            yaml_dict[id]["name"] = (
                entry["titel"].replace(",", "").replace(" ", "_").lower()
            )
        return yaml_dict
