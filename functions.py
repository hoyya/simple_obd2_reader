import obd
import data_set
import sys
import string
import time

elm327 = obd.OBD()

data = data_set.data_set()

last_torque=0
last_power=0

def parse_input(input):
	parts = input.split(':')

	try:
		# parse the user's input
		command = None

		if len(input) == 2:
			command = obd.commands[int(input, 16)]
		elif len(parts) == 2:
			mode = int(parts[0], 16)
			pid = int(parts[1], 16)
			command = obd.commands[mode][pid]

		# send command and print result
		if command is not None and elm327.has_command(command):
			r = elm327.query(command)
			sys.stdout.write("\nDecoded Result:\n%s\n" % str(r))
		else:
			sys.stdout.write("Unsupported command: %s" % str(command))
			
		return command

	except:
		sys.stdout.write("Could not parse command\n")


def scan():
	
	data.rpm = to_int(str(elm327.query(parse_input("01:0C"))))
	data.speed = to_int(str(elm327.query(parse_input("01:0D"))))
	data.intake_temp = to_int(str(elm327.query(parse_input("01:0F"))))
	data.oil_temp = to_int(str(elm327.query(parse_input("01:5C"))))
	data.coolant_temp = to_int(str(elm327.query(parse_input("01:05"))))
	global last_torque
	last_torque = data.torque
	data.torque = to_int(str(elm327.query(parse_input("01:63"))))
	if torque > last_torque:
		data.max_torque = torque
	data.fuel_rate = to_int(str(elm327.query(parse_input("01:5E"))))
	global last_power
	last_power = data.power
	data.power = calc_power(torque, rpm)
	if data.power > last_power:
		data.max_power = power
		
def to_int(string):
	try:
	
		n = int(filter(lambda x: x.isdigit(), string))		
		return n
		
	except:
		return 0

def calc_power(torque, rpm):
	p = (torque * rpm) / 5252
	return p
	
def timer():
	start = time.time()
	under100 = True
	while under100:
		if int(filter(lambda x: x.isdigit(), speed)) >= 100:
			end = time.time()
			under100 = False
	global t
	t = end - start
		
	
def get_fault_codes():
	codes = elm327.query(parse_input("03"))
	return codes
	
def clear_fault_codes():
	elm327.query(parse_input("04"))

	
	