// decode 7.sv - ELEX 7660 final project, this module's purpose is to 
// decode the button pressed into ASCI code to be sent as "data" 


module decode7 ( input logic [3:0] num, 
					input logic FPGA_CLK1_50,
					input logic PB_state , 
					output logic [7:0]LED,
					output logic [7:0] data, 
					output logic start); 
			// 4 bit input num, and 8 bit output LEDS
			
	logic [2:0] startState  =0; 	
	
	always_comb begin 
	
	/*
	//leds = 8'b00000000;
	//LED[2] = 'b1;  
	//LED = 'b10010001; 
	//LED[4] = 'b1; 
	if ( PB_state ==1) begin
		start = 1; 
		LED = 8'b11111111;             ///////////////////for testing 
		end   							/// for testing
		
	else begin 
	LED = 8'b00000000;
	start = 0;
	end 
	
	*/
		if ( PB_state ==1) begin
		//start = 1; 
		case (num)
			0 : LED = 8'b00110000;		
			1 : LED = 8'b00110001;		
			2 : LED = 8'b00110010;
			3 : LED = 8'b00110011;
			4 : LED = 8'b00110100;
			5 : LED = 8'b00110101;
			6 : LED = 8'b00110110;	
			7 : LED = 8'b00110111;
			8 : LED = 8'b00111000;
			9 : LED = 8'b00111001;
			//10 : LED = 8'b10001000;
			11 : LED = 8'b00000000;              // assigning number 11 to be the state when no key is pressed
			//12 : LED = 8'b11000110;
			//13 : LED = 8'b10100001;
			//14 : LED = 8'b10000110;
			//15 : LED = 8'b10001110;
			
			default : begin 
					
					LED = 'b00000000; 
					// if it's in none of the above state, 
					end 			// turn off all LEDs
		endcase
		data = LED;   // output data 
		
		end 
	
	else begin 
		LED = 'b00000000; 
		//start = 0; 
		data = LED; 
		end
		
	end  // end the always_comb
	
	
	
	always_ff @ ( posedge FPGA_CLK1_50) begin
	
		case (startState) 
			0: begin 
				if (PB_state) begin 
					startState <=1; 
					start <= 1; 
					end
				end // waiting for push 
			1: begin
				startState <= 2; 
				end
			2: begin
				startState <= 3; 
				end
			3: begin
				startState <= 4; 
				end
			4: begin start <=0;
				startState <= 5; 
				end
			5: if (~PB_state) 
				startState <=0; // wait for release 
		endcase
	end 
	
	
	
endmodule 