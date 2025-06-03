from lib.umodbus.serial import Serial as ModbusRTUMaster
from machine import Pin

Corresponding_direction ={
    0: "N", 1: "NE", 2: "E", 3: "SE", 4: "S", 5: "SW", 6: "W", 7: "NW", 8: "N", -1: "??"
}

# Define the pins for Modbus communication
rtu_pins = (Pin(0), Pin(1))

# Define the starting address to read from
starting_address = 0

# Define the quantity of registers to read
qty = 5

# Initialize Modbus RTU Master
host = ModbusRTUMaster(baudrate=4800, data_bits=8, stop_bits=1, parity=None, pins=rtu_pins, uart_id=0)

def read_registers():
    return  host.read_holding_registers(slave_addr=1, starting_addr=starting_address, register_qty=qty, signed=False)