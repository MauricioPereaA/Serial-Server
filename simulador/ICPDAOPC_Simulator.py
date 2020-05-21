import socket, serial, time, threading , os, json, random
from _thread import *
import sys

STATUS_SERVER = True
DEVICES = []

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
	global DEVICES
	for device in DEVICES['device']:
		if device['id'] == id:
			print(device['name'])
			return device['name']


def ReadInputSingle(id, input):
	global DEVICES
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)

	command = '@{:02x}\r'.format(int(id))
	try:
		print('write Data: {}'.format(command))

		for device in DEVICES['device']:
			if device['id'] == id:
				response = device['input_state']

		print('read data: {}'.format(response))

	except Exception as e1:
		print('error comunication...: {}'.format(e1))
		print_lock.release()
		return 'Error Comunication'

	response = hex(int(response))
	response = response[2:]
	if '7055' in nameDevice:
		response = '00' + response
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
		response = '00' + response
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
	global DEVICES
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)

	command = '@{:02x}\r'.format(int(id))
	try:
		print('write Data: {}'.format(command))

		for device in DEVICES['device']:
			if device['id'] == id:
				response = device['input_state']

		print('read data: {:04x}'.format(int(response)))

	except Exception as e1:
		print('error comunication...: {}'.format(e1))
		print_lock.release()
		return 'Error Comunication'


	response = hex(int(response))
	response = response[2:]
	if '7055' in nameDevice:
		response = '00' + response
		print_lock.release()
		return str(int(response[2:], 16))
	elif '7051' in nameDevice:
		print_lock.release()
		return str(int(response, 16))
	elif '7060' in nameDevice:
		response = '00' + response
		print_lock.release()
		return str(int(response[2:], 16))
	elif '7058' in nameDevice:
		print_lock.release()
		return str(int(response[:2], 16))
	else:
		print_lock.release()
		return '-4'


def SetOutputSingle(id, output, value):
	global DEVICES
	print_lock.acquire()
	command = '#{:02x}1{}{:02x}\r'.format(int(id), int(output), int(value))
	try:
		print('write Data: {}'.format(command))

		print('read data: {}'.format('>'))

		print_lock.release()
		return '0'
	except Exception as e1:
		print('error comunication...: {}'.format(e1))
		print_lock.release()
		return 'Error Comunication'


def SetOutputPort(id, value):
	global DEVICES
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)

	if '7055' in nameDevice:
		command = '@{:02x}{:02x}\r'.format(int(id), int(value))
	elif '7060' in nameDevice:
		command = '@{:02x}{:01x}\r'.format(int(id), int(value))
	elif '7067' in nameDevice:
		command = '@{:02x}{:02x}\r'.format(int(id), int(value))
	else:
		return '-3'

	try:

		print('write Data: {}'.format(command))

		for device in DEVICES['device']:
			if device['id'] == id:
				device.update({'output_state': value})
				print(device)
				break
		with open('devices.txt', 'w') as outfile:
			json.dump(DEVICES, outfile, indent=4)

		print('read data: {}'.format('>'))

		print_lock.release()
		return '0'
	except Exception as e1:
		print('error comunication...: {}'.format(e1))
		print_lock.release()
		return 'Error Comunication'



def ReadOutputPort(id):
	global DEVICES
	print_lock.acquire()
	nameDevice = ReadNameDevice(id)

	command = '@{:02x}\r'.format(int(id))
	try:
		print('write Data: {}'.format(command))

		for device in DEVICES['device']:
			if device['id'] == id:
				response = device['output_state']

		print('read data: {:04x}'.format(int(response)))

	except Exception as e1:
		print('error comunication...: {}'.format(e1))
		print_lock.release()
		return 'Error Comunication'


	response = hex(int(response))
	response = response[2:]
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

	command = '#{:02x}{:01x}\r'.format(int(id), int(channel))
	try:
		print('write Data: {}'.format(command))
		response = random.randint(0, 65535)
		print('read data: {}'.format(str(response)))
		print_lock.release()
		return str(response)
	except Exception as e1:
		print('error comunication...: {}'.format(e1))
		print_lock.release()
		return 'Error Comunication'


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
	global STATUS_SERVER, DEVICES

	with open('devices.txt') as json_file:
		DEVICES = json.load(json_file)

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
			os.system('taskkill /IM "ICPDAOPC_Simulator.exe" /F')
			break
		if len(data.decode()) > 2 and STATUS_SERVER:
			response = serial_connection(data.decode())
			print(response)
			c.sendall(response.encode())
			time.sleep(.05)
			#c.close()
			#break
		if len(data.decode()) <= 2:
			c.sendall(b'Perro')
			c.close()
			break


def main():
	global STATUS_SERVER, DEVICES

	host = "127.0.0.1"
	port = 10001
	tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpServer.bind((host, port))

	tcpServer.listen(5)
	print('Socket binded to port', port)

	while True:
		print("Server Multiconexion : Esperando conexion de los clientes..")
		c, addr = tcpServer.accept()
		#print_lock.acquire()

		print('Connected to: ', addr[0], ':', addr[1])

		start_new_thread(threaded, (c, addr))
		#t1 = threading.Thread(target=threaded, args=(c, addr))
		#t1.start()
		#t1.join()
		#if STATUS_SERVER == False:
		#	sys.exit()


if __name__ == '__main__':
	main()