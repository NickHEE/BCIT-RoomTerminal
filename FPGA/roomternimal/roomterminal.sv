module roomterminal ( output logic [3:0] kpc,  // column select, active-low
		      (* altera_attribute = "-name WEAK_PULL_UP_RESISTOR ON" *)
		      input logic  [3:0] kpr,  // rows, active-low w/ pull-ups
		      output logic [8:0] LED, // active-low LED segments 
		      output logic lock_output, TxD, test,
		      input logic available, reset_n, FPGA_CLK1_50, unavailable);
	  
	logic TxD_start;
	logic [7:0] TxD_data;

	keypad keypad_0(.*);		 
	UART UART_0 (.*);	
	
endmodule


