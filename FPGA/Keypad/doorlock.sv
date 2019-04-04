// lock.sv - ELEX 7660 final project, this module's purpose is to 
// control the door lock 


module doorlock ( 
					input unlock_signal,
					input logic lock, 
					input logic PB_state, 
					input logic  unlock,  // need to be edge 
					output logic lock_output); 
			// 4 bit input num, and 8 bit output LEDS
	
	logic room_state; 
	
	always_comb begin 
	
		if (unlock_signal==1 && (room_state ==1)) 
			lock_output = 1; 
			
			
			
			
	
	
	
	
	
		//if (PB_state)
			//lock_output = 1; 
		//else //if( unlock) 
			//lock_output = 0; 
	
	
	end 
		
endmodule 


always_ff @ ( posedge available ) begin

		
		if ( unlock_signal )
			lock_output =1;
		
	

	


	//  the program check is the room booked, if the room is booked, we can't do anything for now, 
	// if the room is not booked, the student can pressed unlock to open the door 
	
	// at posedge book, telling the system that the room is booked and posedge clock of not_booked, 