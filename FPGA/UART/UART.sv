/*
UART.sv - Top level module that, for normal operation, only instantiates
and asynchronous transmitter. A test data generator and clock divider can
be uncommented and use for testing if a keypad is not available.
Created by: Nicholas Huttemann, 2019-04-08 
*/

module UART (input logic FPGA_CLK1_50,
			 output logic TxD);

	logic TxD_start;
	logic [7:0] TxD_data;
	logic divClk;
	logic TxD_busy;

// Test Modules can be used in place of a keypad
// clockDivider clockDivider0 (.*);
// testDataGen testDataGen0 (.*);

	async_transmitter async_transmitter0(.*);

endmodule