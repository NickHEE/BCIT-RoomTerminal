// lock.sv - ELEX 7660 final project, this module's purpose is to 
// control the door lock 


module doorlock ( 
					input logic lock, 
					input logic PB_state, 
					input logic  unlock,  // need to be edge 
					output logic lock_output); 
			// 4 bit input num, and 8 bit output LEDS
	
	always_comb begin 
	
		if (PB_state)
			lock_output = 1; 
		else //if( unlock) 
			lock_output = 0; 
	
	
	end 
		
endmodule 



	//  the program check is the room booked, if the room is booked, we can't do anything for now, 
	// if the room is not booked, the student can pressed unlock to open the door 
	
	// at posedge book, telling the system that the room is booked and posedge clock of not_booked, 