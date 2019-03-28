module clockDivider( input logic clk,
					 output logic divClk);

	logic [24:0] counter;
	parameter DIVISOR = 25000000; //50Mhz Clk -> 2Hz

	assign divClk = (counter < DIVISOR/2) ? 0 : 1; // 50% duty cycle

	always @(posedge clk) begin
		counter <= counter + 1;
		if (counter >= (DIVISOR - 1))
			counter <= 0;
	end

endmodule