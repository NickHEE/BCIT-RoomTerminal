import serial

UART = serial.Serial('/dev/ttyS0', baudrate=115200, timeout=2)


if __name__ == "__main__":
	while True:
		try:
			#print(bin(ord(UART.read(1))))
			print(UART.read(1))
		except Exception as e:
			print(e + '/n')