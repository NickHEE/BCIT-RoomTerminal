// lock.sv - ELEX 7660 final project, this module's purpose is to 
// control the door lock 


module roomterminal ( output logic [3:0] kpc,  // column select, active-low
					(* altera_attribute = "-name WEAK_PULL_UP_RESISTOR ON" *)
					input logic  [3:0] kpr,  // rows, active-low w/ pull-ups
					output logic [8:0] LED, // active-low LED segments 
					output logic lock_output,
					output logic TxD,  // column select, active-low
					//output logic locktest,
					output logic test,
					 input logic available,
					 input logic  reset_n,
					 input logic FPGA_CLK1_50,
					input logic unavailable);
              
		  
	logic TxD_start;
	logic [7:0] TxD_data;
	
	
			  
			  
 
	keypad keypad_0(.*);		 
	UART UART_0 (.*);		  
				
	
	
endmodule


