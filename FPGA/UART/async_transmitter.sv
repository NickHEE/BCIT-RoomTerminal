// async_transmitter.sv - Transmits in RS-232 format. 8 data bits, 1 start, 1 stop, no parity.
// Created by: (c) fpga4fun.com & KNJN LLC - 2003 to 2016
// Modified by: Nicholas Huttemann, 2019-04-08

//`define SIMULATION   // in this mode, TX outputs one bit per clock cycle
                       

module async_transmitter(
	input FPGA_CLK1_50,
	input TxD_start,
	input [7:0] TxD_data,
	output TxD,
	output TxD_busy
);


	// Assert TxD_start for (at least) one clock cycle to start transmission of TxD_data
	// TxD_data is latched so that it doesn't have to stay valid while it is being sent

	`ifdef SIMULATION
	logic BitTick = 1'b1;  // output one bit per clock cycle
	`else
	logic BitTick;
	baud_tick_gen tickgen(.clk(clk), .enable(TxD_busy), .tick(BitTick));
	`endif

	logic [3:0] TxD_state = 0;
	logic TxD_ready; 
	logic [7:0] TxD_shift = 0;
	
	assign TxD_ready = (TxD_state==0);
	assign TxD_busy = ~TxD_ready;
	
	always @(posedge clk)
	begin
		if(TxD_ready & TxD_start)  // Start signal received, begin transmission
			TxD_shift <= TxD_data;
		else
		if(TxD_state[3] & BitTick) // Data finished, transmit stop bit
			TxD_shift <= (TxD_shift >> 1);

		case(TxD_state)
			4'b0000: if(TxD_start) TxD_state <= 4'b0100; // idle
			4'b0100: if(BitTick) TxD_state <= 4'b1000;   // start bit
			4'b1000: if(BitTick) TxD_state <= 4'b1001;   // bit 0
			4'b1001: if(BitTick) TxD_state <= 4'b1010;   // bit 1
			4'b1010: if(BitTick) TxD_state <= 4'b1011;   // bit 2
			4'b1011: if(BitTick) TxD_state <= 4'b1100;   // bit 3
			4'b1100: if(BitTick) TxD_state <= 4'b1101;   // bit 4
			4'b1101: if(BitTick) TxD_state <= 4'b1110;   // bit 5
			4'b1110: if(BitTick) TxD_state <= 4'b1111;   // bit 6
			4'b1111: if(BitTick) TxD_state <= 4'b0010;   // bit 7
			4'b0010: if(BitTick) TxD_state <= 4'b0000;   // stop bit
			default: if(BitTick) TxD_state <= 4'b0000;   // idle
		endcase
	end

	assign TxD = (TxD_state<4) | (TxD_state[3] & TxD_shift[0]);  // put together the start, data and stop bits
	endmodule