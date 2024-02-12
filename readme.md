#nibe-s1255-postgresql
#readme.md

## create virtual environment

python3 -m venv ./venv
source ./venv/bin/activate

## install necessary modules

module to parse `nibe-s1255-register.yaml`:

    $ pip install pyyaml

module to establish a Modbus TCP/IP connection:

    $ pip install pyModbusTCP

Module to run the tests

    $ pip install pytest

Module to use postgreSQL

    $ pip install psycopg2 or pip install psycopg2-binary

## start the scripts

    python -m src.nibe.__main__

## Simple way to request a data point

Make sure to turn on ModbusTCP in the settings of the S1255 heat pump.
There's also an option to export the registers of your specific heat pump to a csv file (via USB device)

```
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host="IP_OF_HEAT_PUMP", port=502, auto_open=True)
c.read_input_registers(7) #returns a value for the data point
c.read_holding_registers(0, 2) #returns a value for the data point

```
