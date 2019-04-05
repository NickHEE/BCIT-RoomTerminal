module UART (	input logic TxD_start,
				input logic [7:0] TxD_data,
				input logic FPGA_CLK1_50,
			 output logic TxD);

	//logic TxD_start;
	//logic [7:0] TxD_data;
	logic divClk;
	logic TxD_busy;


async_transmitter async_transmitter0(.*);

endmodule