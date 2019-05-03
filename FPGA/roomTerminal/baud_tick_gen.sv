/*
baud_tick_gen.sv - Generate a clock (tick) at the baud rate specified in 'parameters.h'
Created by: https://github.com/CatherineH , 2016-11-15
Modified by: Nicholas Huttemann, 2019-04-08
*/

module baud_tick_gen(input FPGA_CLK1_50, enable,
					 output tick);  
	// output tick: generate a tick at the specified baud rate * oversampling

	`include "parameters.h"
	parameter ClkFrequency = CLK_FREQUENCY;
	parameter Baud = BAUD_RATE;
	parameter Oversampling = 1; // Only using UART for TX. No need to oversample
	
	// Define a log base 2 function for calculating bit length of AccWidth
	function integer log2(input integer v); begin 
		log2=0; 
		while(v>>log2) 
			log2=log2+1; 
	end endfunction

	localparam AccWidth = log2(ClkFrequency/Baud)+8;  // +/- 2% max timing error over a byte
	logic [AccWidth:0] Acc = 0;
	localparam ShiftLimiter = log2(Baud*Oversampling >> (31-AccWidth));  // this makes sure Inc calculation doesn't overflow
	localparam Inc = ((Baud*Oversampling << (AccWidth-ShiftLimiter))+(ClkFrequency>>(ShiftLimiter+1)))/(ClkFrequency>>ShiftLimiter);

	
	always @(posedge clk) begin
		if(enable) 
			Acc <= Acc[AccWidth-1:0] + Inc[AccWidth:0]; 
		else 
			Acc <= Inc[AccWidth:0];
	end

	assign tick = Acc[AccWidth];

endmodule