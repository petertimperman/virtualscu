from enum import Enum 
import time
import serial

class Status(Enum):
	STOPPED = 'S'
	JOGGINGFORWARD ='F'
	JOGGINGREVERSE= 'R'
	PAUSED = 'P'
	ERROR = 'E'

class ProtcolMessage(Enum):
    ENQ = chr(133)  # <ENQ> in acsii + 128
    NULL = chr(128)  # <Null>: 0 + 128
    ACK = chr(134)  # 6 + 128
    CR = chr(141)  # 13 + 128
    #CR = chr(13)

class CommandCode(Enum):
    SCAN = "G"
    PAUSE = "P"
    STOP = "S"
    HOME = "H"
    SLEW = '9'
    JOGFORWARD = "F"
    JOGREVERSE = "R"
    FASTERJOG = "Q"
    SLOWERJOG = "Z"
    SCANMODE = "B"
    UNITS = "U"
    BURSTFIRE = "L"
    NEXTPOSITION = "N"
    SHGRETURN = "C"
    SHGALIGN = "K"
    SHGFORWARD = "D"
    SHGREVERSE = "E"
    SHGJOGCRYSTAL = "I"
    SHGJOGPRISM = "J"


class SCU():
	def __init__(self):
		self.units=["W","D","N"]
		self.unit = "W" #wavenumbers
		self.position = 15000 #Start at 15000
		self.status = "S" #Start as stopped 

	def slew(self, new_position):
		if new_position < self.position:
			self.status = Status.JOGGINGREVERSE
			while new_position != self.position and self.status != Status.STOPPED:
				self.position  -= 1
				time.sleep(.1)
		else:
			self.status = Status.JOGGINGFORWARD
			while new_position != self.position and self.status != Status.STOPPED:
				self.position  += 1
				time.sleep(.1) 
		self.status = Status.STOPPED
	
	def jog_forward(self):
		self.status = Status.JOGGINGFORWARD
		while new_position != self.position and self.status != Status.STOPPED:
				self.position  += 1
				time.sleep(.1) 
		self.status = Status.STOPPED

	def jog_reverse(self):
		self.status = Status.JOGGINGREVERSE
		while new_position != self.position and self.status != Status.STOPPED:
				self.position  -= 1
				time.sleep(.1) 
		self.status = Status.STOPPED
	def to_status(self):
		return self.status+self.unit+str(self.position)
	def change_unit(self):
		next_index = self.units.index(self.unit) +1 
		if next_index == 3:
			next_index = 0
		self.unit = self.units[next_index]
class SerialParser():
	def __init__(self):
		self.ser = serial.Serial(port="/dev/ttyS0", baudrate=9600, timeout = .01
                   , bytesize=serial.EIGHTBITS, stopbits=2, rtscts=True)
		self.scu = SCU()
		self.poll()

	def poll(self):
		null_count = 0 
		while True:
			
			self.ser.flushInput()
			
			if null_count == 45:
				print "Writing enq"
				self.ser.write(ProtcolMessage.ENQ.value)
				response_counter = 0
				command_buffer = list()
				while response_counter <100: #Limit to 100 characters recieved 
					recieved = self.ser.read()
					
					if recieved != ProtcolMessage.CR.value and recieved != ProtcolMessage.ACK.value :
						command_buffer.append(recieved)
						response_counter += 1	
					else:
						if recieved == ProtcolMessage.ACK.value:
							command = ProtcolMessage.ACK.value
						else:
							command = self.parse_command(command_buffer)
						self.execute_command(command)
						print command_buffer 
						break
				null_count = 0
			else:
				self.ser.write(ProtcolMessage.NULL.value)
				null_count += 1
	def parse_command(self, command_buffer):
			command = command_buffer[0]
			print command
			return command

	def execute_command(self,command, message=None):
		print "Command-->"+str(command)
		if command ==  ProtcolMessage.ACK.value or command == "0":
			print "Ack recieved"
			message = self.scu.to_status()+"CS" + ProtcolMessage.CR.value
			self.return_status()
		elif command = "U":
			self.scu.change_unit()
			self.return_status()
		else:
			self.return_error()
			
	def return_status(self):
		self.ser.write(self.scu.to_status()+"CS" + ProtcolMessage.CR.value)
	def return_error(self):
		self.ser.write("EE00000"+ProtcolMessage.CR.value)
ser_parse = SerialParser()
