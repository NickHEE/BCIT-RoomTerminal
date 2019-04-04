module testDataGen ( input logic clk, divClk, TxD_busy,
					 output logic TxD_start,
					 output logic [7:0] TxD_data);

	logic [4:0][7:0] data  = {{8'b01101000},
							  {8'b01100101},
							  {8'b01101100},
							  {8'b01101100},
							  {8'b01101111}};
	logic [2:0] char;
	logic [3:0] state;
	logic [19:0] div;
	logic [1:0] aaaa;
	
	
	always_ff @(posedge clk) begin
		case (state)
			0 : begin      char <= 1;  state <= 1; TxD_data <= data[char]; TxD_start <= 1; div <= 0; end
			1 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 2; end
			2 : begin      char <= 2;  state <= 3; TxD_data <= data[char]; TxD_start <= 1; div <= 0; end
			3 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 4; end
			4 : begin      char <= 3;  state <= 5; TxD_data <= data[char]; TxD_start <= 1; div <= 0; end
			5 : begin TxD_start <= 0;  if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 6; end
			6 : begin      char <= 4;  state <= 7; TxD_data <= data[char]; TxD_start <= 1; div <= 0; end
			7 : begin TxD_start <= 0;	if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 8; end		
			8 : begin      char <= 0;  state <= 9; TxD_data <= data[char]; TxD_start <= 1; div <= 0; end
			9 : begin TxD_start <= 0;	if (~TxD_busy) div <= div + 1; if (div >= 1000000) state <= 0; end		
			default: begin TxD_start <= 0;  state <= 0; div <= 0; end
		endcase	
	end
   	
endmodule