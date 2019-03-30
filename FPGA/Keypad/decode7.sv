// decode 7.sv - ELEX 7660 pre- lab 2, this module's purpose is to 
// to decode the number that is pressed to the 7-segment LED display.
// Hsiao Yi, Lu (Ian Lu A00984995)  2019-1-24

module decode7 ( input logic [3:0] num, output logic [7:0]LED); 
			// 4 bit input num, and 8 bit output LEDS
			
	always_comb begin 
	
	
	//leds = 8'b00000000;
	//LED[2] = 'b1;  
	//LED = 'b10010001; 
	//LED[4] = 'b1; 
	
		case (num)
			0 : LED = 8'b00000001;		
			1 : LED = 8'b00000010;		
			2 : LED = 8'b00000100;
			3 : LED = 8'b00001000;
			4 : LED = 8'b00010000;
			5 : LED = 8'b00100000;
			6 : LED = 8'b01000000;	
			7 : LED = 8'b10000000;
			/*
			8 : LED = 8'b10000000;
			9 : LED = 8'b10010000;
			10 : LED = 8'b10001000;
			11 : LED = 8'b10000011;
			12 : LED = 8'b11000110;
			13 : LED = 8'b10100001;
			14 : LED = 8'b10000110;
			15 : LED = 8'b10001110;
			*/
			default : begin 
					
					LED = 'b11111111; 
					// if it's in none of the above state, 
					end 			// turn off all LEDs
		endcase
		
		end
endmodule 