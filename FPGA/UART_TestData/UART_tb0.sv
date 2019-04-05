module UART_tb;

	logic clk = 0;
	logic TxD_start;
	logic [7:0] TxD_data = 'b01001001;
	logic TxD, TxD_busy;
	
	
	async_transmitter DUT (.*);
	
	initial begin
		TxD_start = 1;
		repeat(1) @(negedge clk);
		TxD_start = 0;
		while (TxD_busy) begin 
			repeat(1) @(posedge clk);
		end
		$stop;
	end
	
	always
		#500ns clk = ~clk; 
		
endmodule