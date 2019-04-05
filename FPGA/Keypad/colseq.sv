// colseq.sv - ELEX 7660 final project, this module's purpose is to 
// to cycle through the 4 columns on the keypad


module colseq ( input logic [3:0] kpr,     // the input is a 4 bit called kpr, the rows
		input logic 	clk,			// the single digit input, the clk 
		input logic 	reset_n,        // the single digit input, reset 
		output logic [3:0] kpc); 		// the 4 bit output that controls the cycle of columns 

	always_ff @(posedge clk ,negedge reset_n) begin  // using always ff to push it into the register
		
	if (~reset_n ) 						// if the reset command is given, start from the left most column (3rd)
		kpc = 'b0111;					// the 3rd column, which is the left most column
	else if ( kpr == 'b1111)			// if no key is pressed ( wasn't detected by the row (kpr), cycle, 
		case (kpc)						// or else, do nothing. 
			'b0111 : kpc = 'b1011;		// the cases to assign the next state determined by the previous state
			'b1011 : kpc = 'b1101;
			'b1101 : kpc = 'b1110;
			'b1110 : kpc = 'b0111;
		default : kpc = 'b0111;			// assign a state when kpc is in none of the state mentioned above 
	
	
		endcase				
	end 

endmodule 