// lock.sv - ELEX 7660 final project, this module's purpose is to 
// control the door lock 


module doorlock ( 	input logic FPGA_CLK1_50
					input logic available,
					input logic unavailable,
					input logic unlock_signal
					output logic lock_output); 
			// 4 bit input num, and 8 bit output LEDS
	
	logic roomIsAvailable;
	logic unlockState;
	logic [28:0] div;
	
	always_comb begin
		if (available)
			roomIsAvailable = 1;
		if (unavailable)
			roomIsAvailable = 0;
	end 

always_ff @ ( posedge FPGA_CLK1_50 ) begin
	case (unlockState)
		0 : begin lock_output <= 0; div = 0; if (unlock_signal && roomIsAvailable ) unlockState <= 1 end //Locked Idle State
		1 : begin lock_output <= 1; div <= div + 1; if (div >= 150000000) unlockState <= 0; end          //Unlock and wait 3 seconds
		default : unlockState <= 0;
end	
	
		
			