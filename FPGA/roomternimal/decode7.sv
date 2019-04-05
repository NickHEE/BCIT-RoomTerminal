// decode 7.sv - ELEX 7660 final project, this module's purpose is to 
// decode the button pressed into ASCI code to be sent as "TxD_data" 


module decode7 ( input logic [3:0] num, 
					input logic FPGA_CLK1_50,
					input logic PB_state , 
					output logic [8:0]LED,
					output logic [7:0] TxD_data, 
					output logic unlock_signal,
					output logic test,
					//output logic locktest,
					output logic TxD_start); 
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
		if ( PB_state ==1) begin      // key is pressed 
		//start = 1; 
		case (num)
			0 : begin LED = 8'b00110000; unlock_signal = 0;  end // the MSB bit is the unlock_signal
			1 : begin LED = 8'b00110001;	unlock_signal = 0;end 
			2 : begin LED = 8'b00110010;unlock_signal = 0;	end 
			3 : begin LED = 8'b00110011;unlock_signal = 0;		end 
			4 : begin LED = 8'b00110100;	unlock_signal = 0;end 
			5 : begin LED = 8'b00110101;	unlock_signal = 0;end 
			6 : begin LED = 8'b00110110;		unlock_signal = 0;end 
			7 :begin  LED = 8'b00110111;	unlock_signal = 0;end 
			8 : begin LED = 8'b00111000;	unlock_signal = 0;end 
			9 : begin LED = 8'b00111001;	unlock_signal = 0;end 
			//10 : LED = 8'b10001000;
			11 :begin  LED = 8'b00000000; 	unlock_signal = 0;    end   // assigning number 11 to be the state when no key is pressed
			//12 : LED = 8'b11000110;
			13 : begin  LED = 8'b00110111; 	unlock_signal = 1;end 
			14 : begin LED = 8'b01000001;   unlock_signal = 0;    end
			//15 : LED = 8'b10001110;
			
			default : begin 
					//unlock_signal =0;
					LED = 8'b00000000; 
					unlock_signal = 0;
					// if it's in none of the above state, 
					end 			// turn off all LEDs
		endcase
		//data = LED[7:0];   // output data 
		//unlock_signal =LED[8];
		end 
	
	else begin     // no key is pressed 
		LED = 8'b00000000; 
		unlock_signal = 0;
		//TxD_start = 0; 
		//data = LED[7:0]; 
		//unlock_signal =LED[8];
		end
		
	end  // end the always_comb
	
	assign  TxD_data = LED[7:0];   // output TxD_data 
	//assign  unlock_signal =lock;
	//assign  test = LED[8];
	
	always_ff @ ( posedge FPGA_CLK1_50) begin
	
		case (startState) 
			0: begin 
				if (PB_state) begin 
					startState <=1; 
					TxD_start <= 1; 
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
			4: begin TxD_start <=0;
				startState <= 5; 
				end
			5: if (~PB_state) 
				startState <=0; // wait for release 
		endcase
	end 
	
	
	
endmodule 