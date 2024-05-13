import sys
import time
import serial
import csv
import config

def validate(byteArray):
    if len(byteArray) != 18:
        return False
    if byteArray[0] != '02':
        return False
    if byteArray[16] != '0d':
        return False
    return True

def weight(byteArray):
    weightString = ""
    for i in range(5, 10):
        weightString += intValue(byteArray[i])
    return weightString

def intValue(byteString):
    return chr(int(byteString, 16))

def parse(line):
    bytes = line.split(":")
    if validate(bytes):
        return weight(bytes)
    return ""

def write_to_csv(time, weight, unit):
    with open('weights.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([time, weight, unit])

while True:
    with serial.Serial(
            config.serial_port,
            bytesize=serial.SEVENBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_TWO,
            baudrate=4800,
            timeout=1
        ) as ser:
        line = ser.read(18)
        formattedLine = ":".join("{:02x}".format(byte) for byte in line)
        formattedWeight = parse(formattedLine)
        if formattedWeight:
            print("{} ::: {} ::: {}".format(time.time(), formattedWeight, config.unit))
            write_to_csv(time.time(), formattedWeight, config.unit)
            sys.stdout.flush()
