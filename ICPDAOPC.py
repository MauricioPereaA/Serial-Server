import socket, serial, time, threading , os
from _thread import *
import sys

STATUS_SERVER = True

print_lock = threading.Lock()


def WaitInput(id, input, value, timeout):
	start_time = time.time()
	while True:
		statusIn = ReadInputSingle(id,input)
		if value == statusIn:
			return '0'
		if (time.time() - start_time) >= int(timeout):
			return '-3'
		time.sleep(0.1)


def SimpleAction(id_out, output, value_out, id_in, in_put, value_in, timeout):
	statusOut = SetOutputSingle(id_out, output, value_out)
	print('StatusOut', statusOut)
	if statusOut == '0':
		start_time = time.time()
		while True:
			statusIn = ReadInputSingle(id_in, in_put)
			print('Status In', statusIn)
			if value_in == statusIn:
				return '0'
			if (time.time() - start_time) >= int(timeout):
				return '-3'
			time.sleep(0.1)
	else:
		return '-4'


def DoubleAction(id_out1, output1, id_out2, output2, id_in1, input1, id_in2, input2, timeout):
	statusOut1 = SetOutputSingle(id_out1, output1, '1')
	statusOut2 = SetOutputSingle(id_out2, output2, '0')
	if (statusOut1 == '0') and (statusOut2 == '0'):
		start_time = time.time()
		while True:
			statusIn1 = ReadInputSingle(id_in1, input1)
			statusIn2 = ReadInputSingle(id_in2, input2)
			if (statusIn1 == '1') and (statusIn2 == '0'):
				return '0'
			if (time.time() - start_time) >= int(timeout):
				return '-3'
			time.sleep(0.1)
	else:
		return '-4'


def ReadErrorCode():
	pass


def ReadNameDevice(id):
	print('Create conection to ICPDA')
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		command = '${:02x}M\r'.format(int(id))
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if len(response) > 2:
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'

			ser.close()

			return response.decode()
		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		return 'Cannot_Open_Serial_Port'


def ReadInputSingle(id, input):
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)
	nameDevice = nameDevice[3:]
	print('Create conection to ICPDA')
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		command = '@{:02x}\r'.format(int(id))
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if len(response) > 2:
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'
			ser.close()
		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			print_lock.release()
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		print_lock.release()
		return 'Cannot_Open_Serial_Port'

	response = response.decode()
	response = response[1:]
	print(response)
	if '7055' in nameDevice:
		response = response[2:]
		responseHex = int(response, 16)
		responseBin = bin(responseHex)
		responseBin = responseBin[2:]
		responseBinRev = responseBin[::-1]
		if responseBinRev == '0':
			responseBinRev = '00000000'
		try:
			if responseBinRev[int(input)] == '1':
				print_lock.release()
				return '1'
			else:
				print_lock.release()
				return '0'
		except Exception:
			print_lock.release()
			return '-1'
	elif '7051' in nameDevice:
		responseHex = int(response, 16)
		responseBin = bin(responseHex)
		responseBin = responseBin[2:]
		trama1 = responseBin[:-8]
		trama1 = trama1[2:]
		trama2 = responseBin[-8:]
		responseBinRev = trama2[::-1] + trama1[::-1]
		if responseBinRev == '0':
			responseBinRev = '0000000000000000'
		try:
			if responseBinRev[int(input)] == '1':
				print_lock.release()
				return '1'
			else:
				print_lock.release()
				return '0'
		except Exception:
			print_lock.release()
			return '-1'
	elif '7060' in nameDevice:
		response = response[2:]
		responseHex = int(response, 16)
		responseBin = bin(responseHex)
		responseBin = responseBin[2:]
		responseBinRev = responseBin[::-1]
		if responseBinRev == '0':
			responseBinRev = '00000000'
		try:
			if responseBinRev[int(input)] == '1':
				print_lock.release()
				return '1'
			else:
				print_lock.release()
				return '0'
		except Exception:
			print_lock.release()
			return '-1'
	elif '7058' in nameDevice:
		response = response[:2]
		responseHex = int(response, 16)
		responseBin = bin(responseHex)
		responseBin = responseBin[2:]
		responseBinRev = responseBin[::-1]
		if responseBinRev == '0':
			responseBinRev = '00000000'
		try:
			if responseBinRev[int(input)] == '1':
				print_lock.release()
				return '1'
			else:
				print_lock.release()
				return '0'
		except Exception:
			print_lock.release()
			return '-1'
	else:
		print_lock.release()
		return '-4'


def ReadInputPort(id):
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)
	nameDevice = nameDevice[3:]
	print('Create conection to ICPDA')
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		command = '@{:02x}\r'.format(int(id))
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if len(response) > 2:
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'

			ser.close()

		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			print_lock.release()
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		print_lock.release()
		return 'Cannot_Open_Serial_Port'

	response = response.decode()
	response = response[1:]
	if '7055' in nameDevice:
		print_lock.release()
		return str(int(response[2:], 16))
	elif '7051' in nameDevice:
		print_lock.release()
		return str(int(response, 16))
	elif '7060' in nameDevice:
		print_lock.release()
		return str(int(response[2:], 16))
	elif '7058' in nameDevice:
		print_lock.release()
		return str(int(response[:2], 16))
	else:
		print_lock.release()
		return '-4'


def SetOutputSingle(id, output, value):
	print_lock.acquire()
	print('Create conection to ICPDA')
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		command = '#{:02x}1{}{:02x}\r'.format(int(id), int(output), int(value))
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if '>' in response.decode():
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'
			ser.close()
			print_lock.release()
			return '0'
		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			print_lock.release()
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		print_lock.release()
		return 'Cannot_Open_Serial_Port'


def SetOutputPort(id, value):
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)
	nameDevice = nameDevice[3:]

	if '7055' in nameDevice:
		command = '@{:02x}{:02x}\r'.format(int(id), int(value))
	elif '7060' in nameDevice:
		command = '@{:02x}{:01x}\r'.format(int(id), int(value))
	elif '7067' in nameDevice:
		command = '@{:02x}{:02x}\r'.format(int(id), int(value))
	else:
		return '-3'
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if '>' in response.decode():
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'
			ser.close()
			print_lock.release()
			return '0'
		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			print_lock.release()
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		print_lock.release()
		return 'Cannot_Open_Serial_Port'


def ReadOutputPort(id):
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)
	nameDevice = nameDevice[3:]
	print('Create conection to ICPDA')
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		command = '@{:02x}\r'.format(int(id))
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if len(response) > 2:
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'

			ser.close()
		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			print_lock.release()
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		print_lock.release()
		return 'Cannot_Open_Serial_Port'

	response = response.decode()
	response = response[1:]
	if '7055' in nameDevice:
		print_lock.release()
		return str(int(response[:2], 16))
	elif '7060' in nameDevice:
		print_lock.release()
		return str(int(response[:2], 16))
	elif '7067' in nameDevice:
		print_lock.release()
		return str(int(response[:2], 16))
	else:
		print_lock.release()
		return '-4'


def ReadAnalog(id, channel):
	print_lock.acquire()
	print('Create conection to ICPDA')
	ser = serial.Serial(
		port='COM3',
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout=0
	)

	if ser.isOpen():
		command = '#{:02x}{:01x}\r'.format(int(id), int(channel))
		try:
			ser.flushInput()
			ser.flushOutput()
			ser.write(command.encode())
			print('write Data: {}'.format(command))
			time.sleep(0.05)

			timeStart = time.time()

			while True:
				response = ser.readline()
				if len(response) > 2:
					print('read data: {}'.format(response))
					break
				if (time.time() - timeStart) >= 1.0:
					return '-2'

			ser.close()
			response = response.decode()
			response = response[1:]
			print_lock.release()
			return response
		except Exception as e1:
			print('error comunication...: {}'.format(e1))
			print_lock.release()
			return 'Error Comunication'
	else:
		print('cannot open serial port')
		print_lock.release()
		return 'Cannot_Open_Serial_Port'


def serial_connection(message: str):

	message = message.replace('\r\n', '')
	messagelist = message.split(',')

	ICPDAResponse = ''
	if messagelist[0] == 'ReadInputSingle':
		ICPDAResponse = ReadInputSingle(messagelist[1], messagelist[2])
	elif messagelist[0] == 'ReadInputPort':
		ICPDAResponse = ReadInputPort(messagelist[1])
	elif messagelist[0] == 'SetOutputSingle':
		ICPDAResponse = SetOutputSingle(messagelist[1], messagelist[2], messagelist[3])
	elif messagelist[0] == 'SetOutputPort':
		ICPDAResponse = SetOutputPort(messagelist[1], messagelist[2])
	elif messagelist[0] == 'ReadOutputPort':
		ICPDAResponse = ReadOutputPort(messagelist[1])
	elif messagelist[0] == 'ReadAnalog':
		ICPDAResponse =ReadAnalog(messagelist[1], messagelist[2])
	elif messagelist[0] == 'WaitInput':
		ICPDAResponse = WaitInput(messagelist[1], messagelist[2], messagelist[3], messagelist[4])
	elif messagelist[0] == 'SimpleAction':
		ICPDAResponse = SimpleAction(messagelist[1], messagelist[2], messagelist[3], messagelist[4], messagelist[5], messagelist[6], messagelist[7])
	elif messagelist[0] == 'DoubleAction':
		ICPDAResponse = DoubleAction(messagelist[1], messagelist[2], messagelist[3], messagelist[4], messagelist[5], messagelist[6], messagelist[7], messagelist[8], messagelist[9])
	else:
		ICPDAResponse = '-10'
	return ICPDAResponse


def threaded(c, addr):
	global STATUS_SERVER
	while True:
		print('waiting for message.')
		data = c.recv(1024)
		print(data)
		if not data.decode():
			c.close()
			break
		if 'exit' in data.decode():
			print('Bye')
			c.sendall('Bye'.encode())
			STATUS_SERVER = False
			os.system('taskkill /IM "ICPDAOPC.exe" /F')
			break
		if len(data.decode()) > 2 and STATUS_SERVER:
			response = serial_connection(data.decode())
			print(response)
			c.sendall(response.encode())
			#c.close()
			#break
		if len(data.decode()) <= 2:
			c.sendall(b'Perro')
			c.close()
			break


def main():
	global STATUS_SERVER
	host = "127.0.0.1"
	port = 10001
	tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpServer.bind((host, port))

	tcpServer.listen(5)
	print('Socket binded to port', port)

	while True:
		print("Server Multiconexion : Esperando conexion de los clientes..")
		c, addr = tcpServer.accept()

		print('Connected to: ', addr[0], ':', addr[1])

		start_new_thread(threaded, (c, addr))
		#t1 = threading.Thread(target=threaded, args=(c, addr))
		#t1.start()
		#t1.join()
		#if STATUS_SERVER == False:
		#	sys.exit()


if __name__ == '__main__':
	main()