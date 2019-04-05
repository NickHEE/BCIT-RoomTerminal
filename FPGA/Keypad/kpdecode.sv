// kpdecode.sv - ELEX 7660 final project, this module's purpose is to 
// to decode the position that is pressed on the keypad, and determine the 
// correct number
// num 11 is used as the state when no key is pressed. 
// can't use num 0 because num 0 is a valid data when 0 is pressed 

module kpdecode ( input logic [3:0] kpc,   // 4 bit input kpc
		input logic [3:0] kpr,			// 4 bit input kpr
		output logic kphit,			// 1 bit output if any of the key is pressed
		output logic [3:0] num );		// 4 bit output num to assign number pressed
		
always_comb begin
	
	/*
	//if ( kpr == 'b1111) 		// if no key is pressed,
	//	num = 0;				// output "no key is pressed"
	//else 
		//num = 1;    // or else the a key is pressed
		
	if ( kpr == 'b1011) 
		num = 3;                // works when I physically connect 1011 to [3:0} kpr 
	//else if (kpc == 'b1011)
		//num = 4 ;
	//else if (kpc == 'b1101)
		//num = 5;
	else num = 0;
		*/
		
	if ( kpr == 'b1111) 		// if no key is pressed,
		kphit = 0;				// output "no key is pressed"
	else 
		kphit = 1;    // or else the a key is pressed
		
	if ( kpc == 'b0111) 	// if the left most column (3rd) is pressed 
		 case (kpr)			// to decode the position of key press
			'b0111 : num = 1;	// 1st row
			'b1011 : num = 4;	// 2nd row
			'b1101 : num = 7;	// 3rd row
			'b1110 : num = 14;	// 4th row
			default : num = 11;		
								
		endcase
	
	else if (kpc == 'b1011) // if the 2nd column is pressed 
		 case (kpr)
			'b0111 : num = 2;  // 1st row
			'b1011 : num = 5;
			'b1101 : num = 8;
			'b1110 : num = 0;
		default : num =11;
		endcase
	
	else if (kpc == 'b1101) // if the 2nd column is pressed 
		 case (kpr)
			'b0111 : num = 3; // 1st row
			'b1011 : num = 6;
			'b1101 : num = 9;
			'b1110 : num = 15;
		default : num =11;
		endcase

	else if (kpc == 'b1110) // if the 2nd column is pressed 
		 case (kpr)
			'b0111 : num = 10; // 1st row
			'b1011 : num = 11;
			'b1101 : num = 12;
			'b1110 : num = 13;
		default : num =11;
		endcase	
	else 
		num =11;                 
	
	end


	
endmodule 




