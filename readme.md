# nibe-s1255-postgresql

This python script requests data from the heatpump nibe S1255 via Modbus TCP/IP and saves it to a postgresql database.

## create virtual environment

	python3 -m venv ./venv
	source ./venv/bin/activate

## install necessary modules

module to parse `nibe-s1255-register.yaml`:

    pip install pyyaml

module to establish a Modbus TCP/IP connection:

    pip install pyModbusTCP

Module to run the tests

    pip install pytest

Module to use postgreSQL

    pip install psycopg2 or pip install psycopg2-binary

## necessary additional files

to establish a connection to the nibe heatpump and the postgresql database add a file `database.ini` with the following content to the root directory of the project.

```
[postgresql]
host=localhost
database=my_database
user=my_username
password=my_postgresql_pw

[nibe]
nibe_port = 502
nibe_ip = xxx.xxx.xxx.xx
```

The file `nibe-s1255-register.yaml` specifies all the necessary registers and probably has to be adapted.

## start the scripts
In the root directory of the project run:

    python -m src.nibe.__main__

## Simple way to request a data point

Make sure to turn on ModbusTCP in the settings of the S1255 heat pump.
There's also an option to export the registers of your specific heat pump to a csv file (via USB device)

```
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host="IP_OF_HEAT_PUMP", port=502, auto_open=True)
c.read_input_registers(7) #returns a value for the data point
c.read_holding_registers(0) #returns a value for the data point
c.close()

```
