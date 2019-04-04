module UART (input logic clk,
			 output logic TxD);

	logic TxD_start;
	logic [7:0] TxD_data;
	logic divClk;
	logic TxD_busy;

clockDivider clockDivider0 (.*);
async_transmitter async_transmitter0(.*);
testDataGen testDataGen0 (.*);

endmodule