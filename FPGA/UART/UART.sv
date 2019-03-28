module UART (input logic clk,
			 output logic TxD);

clockDivider clockDivider0 (.*);
async_transmitter async_transmitter0(.*);
testDataGen testDataGen0 (.*);

endmodule