from serial import Serial

UART = Serial('/dev/ttyAMA0', baudrate=460800, timeout=1)


if __name__ = "__main__":
	while True:
		try:
			print(UART.read(1))
		except Exception as e:
			print(e + '/n')