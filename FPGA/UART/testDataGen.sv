module testDataGen ( input logic clk, divClk, TxD_busy,
					 output logic TxD_start,
					 output logic [7:0] TxD_data);

	logic [4:0][7:0] data  = {{8'b01101000},
							  {8'b01100101},
							  {8'b01101100},
							  {8'b01101100},
							  {8'b01101111}};
	logic [2:0] char;

	always_ff @(negedge clk) begin
		if (TxD_busy) TxD_start <= 0;
	end

	always_ff @(posedge divClk) begin
		case (char)
			0 : begin char <= 1; TxD_data <= data[char]; TxD_start <= 1; end
			1 : begin char <= 2; TxD_data <= data[char]; TxD_start <= 1; end
			2 : begin char <= 3; TxD_data <= data[char]; TxD_start <= 1; end
			3 : begin char <= 4; TxD_data <= data[char]; TxD_start <= 1; end
			4 : begin char <= 0; TxD_data <= data[char]; TxD_start <= 1; end
			default: begin char <= 0; TxD_data <= data[char]; TxD_start <= 1; end
		endcase
	end	
endmodule