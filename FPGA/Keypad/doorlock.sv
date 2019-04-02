// lock.sv - ELEX 7660 final project, this module's purpose is to 
// control the door lock 


module doorlock ( 
					//input logic lock, 
					input logic PB_state,
					//input logic  unlock,
					output logic lock_output); 
			// 4 bit input num, and 8 bit output LEDS
	
	always_comb begin 
	
		if (PB_state)
			lock_output = 1; 
		else //if( unlock) 
			lock_output = 0; 
	
	
	end 
		
endmodule 