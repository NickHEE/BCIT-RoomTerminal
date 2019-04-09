/*
testDataGen.sv - Emulates a keypad by sending 'hello' char by char 
in an ascii format with delays in between. Used to test async_transmitter.sv
Created by: Nicholas Huttemann, 2019-04-08
*/

module testDataGen ( input logic clk, divClk, TxD_busy,
					 output logic TxD_start,
					 output logic [7:0] TxD_data);

	logic [4:0][7:0] data  = {{8'b01101000},  // h
							  {8'b01100101},  // e
							  {8'b01101100},  // l
							  {8'b01101100},  // l
							  {8'b01101111}}; // o
	logic [2:0] char;  // data index
	logic [3:0] state; // state machine vector
	logic [19:0] div;  // large vector to divide 50Mhz clk
	
	/*
	This state machine works as follows:
	1. Select a char from data array and put at TxD_data output
	2. Assert TxD_start, then wait for async_transmitter to tx the char
	Repeat
	*/
	always_ff @(posedge clk) begin
		case (state)
			0 : begin      char <= 1;  state <= 1; TxD_data <= data[char]; TxD_start <= 1; div <= 0;  end
			1 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 2; end
			2 : begin      char <= 2;  state <= 3; TxD_data <= data[char]; TxD_start <= 1; div <= 0;  end
			3 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 4; end
			4 : begin      char <= 3;  state <= 5; TxD_data <= data[char]; TxD_start <= 1; div <= 0;  end
			5 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 6; end
			6 : begin      char <= 4;  state <= 7; TxD_data <= data[char]; TxD_start <= 1; div <= 0;  end
			7 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 8; end		
			8 : begin      char <= 0;  state <= 9; TxD_data <= data[char]; TxD_start <= 1; div <= 0;  end
			9 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 0; end		
			default: begin TxD_start <= 0;  state <= 0; div <= 0; end
		endcase	
	end
   	
endmodule