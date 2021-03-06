module clockDivider( input logic clk,
					 output logic divClk);

	logic [24:0] counter = 0;
	parameter DIVISOR = 25000000; //50Mhz Clk -> 2Hz 25,000,000
	// 500,000 100Hz

	assign divClk = (counter < DIVISOR/2) ? 0 : 1; // 50% duty cycle

	always @(posedge clk) begin
		counter <= counter + 1;
		if (counter >= (DIVISOR - 1))
			counter <= 0;
	end

endmodule