module UART_tb;

	logic clk = 0;
	logic TxD;
	
	
	UART UART0 (.*);
	
	initial begin
		#2s $stop;
	end
	
	always
		#10ns clk = ~clk; 
		
endmodule