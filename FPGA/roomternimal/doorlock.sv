// lock.sv - ELEX 7660 final project, this module's purpose is to 
// control the door lock 


module doorlock ( 	input logic FPGA_CLK1_50,
					input logic available,
					input logic unavailable,
					input logic unlock_signal,
					output logic lock_output
					//output logic test); 
					);
			// 4 bit input num, and 8 bit output LEDS
	
	logic roomIsAvailable;
	logic unlockState = 0;
	logic [28:0] div;
	/*
	always_comb begin
		//test = 0; 
		roomIsAvailable =0 ;
		if (available)
			//roomIsAvailable = 1;
			//test =1; 
		if (unavailable)
			//roomIsAvailable = 0;
			//test = 0;                   // it's going in 
	end 
*/
		
		
always_ff @ ( posedge unavailable , posedge available ) begin

	if (available)
			begin
			roomIsAvailable <= 1;
			//test <=1;
			end
			
			
	if (unavailable) begin
			roomIsAvailable <= 0;
			//test<=0;
			end
			
	

end 

always_ff @ ( posedge FPGA_CLK1_50 ) begin
	case (unlockState)
		0 : begin lock_output <= 0; div = 0; if (unlock_signal && roomIsAvailable ) unlockState <= 1 ;end //Locked Idle State
		1 : begin lock_output <= 1; div <= div + 1; if (div >= 150000000) unlockState <= 0; end          //Unlock and wait 3 seconds
		default : unlockState <= 0;
	endcase
end	
	
endmodule 
	


	//  the program check is the room booked, if the room is booked, we can't do anything for now, 
	// if the room is not booked, the student can pressed unlock to open the door 
	
	// at posedge book, telling the system that the room is booked and posedge clock of not_booked, 