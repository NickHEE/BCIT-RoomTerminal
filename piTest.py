import serial

UART = serial.Serial('/dev/ttyAMA0',stopbits=serial.STOPBITS_TWO, baudrate=115200, timeout=2)


if __name__ == "__main__":
	while True:
		try:
			print(UART.read(1))
		except Exception as e:
			print(e + '/n')