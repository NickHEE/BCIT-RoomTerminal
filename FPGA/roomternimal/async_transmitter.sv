////////////////////////////////////////////////////////
// RS-232 RX and TX module
// (c) fpga4fun.com & KNJN LLC - 2003 to 2016

// The RS-232 settings are fixed
// TX: 8-bit data, 2 stop, no-parity
// RX: 8-bit data, 1 stop, no-parity (the receiver can accept more stop bits of course)

//`define SIMULATION   // in this mode, TX outputs one bit per clock cycle
                       // and RX receives one bit per clock cycle (for fast simulations)

////////////////////////////////////////////////////////
module async_transmitter(
	input FPGA_CLK1_50,
	input TxD_start,
	input [7:0] TxD_data,
	output TxD,
	output TxD_busy
);


	// Assert TxD_start for (at least) one clock cycle to start transmission of TxD_data
	// TxD_data is latched so that it doesn't have to stay valid while it is being sent

	////////////////////////////////
	`ifdef SIMULATION
	logic BitTick = 1'b1;  // output one bit per clock cycle
	`else
	logic BitTick;
	baud_tick_gen tickgen(.FPGA_CLK1_50(FPGA_CLK1_50), .enable(TxD_busy), .tick(BitTick));
	`endif

	logic [3:0] TxD_state = 0;
	logic TxD_ready; 
	logic [7:0] TxD_shift = 0;
	
	assign TxD_ready = (TxD_state==0);
	assign TxD_busy = ~TxD_ready;
	
	always @(posedge FPGA_CLK1_50)
	begin
		if(TxD_ready & TxD_start)
			TxD_shift <= TxD_data;
		else
		if(TxD_state[3] & BitTick)
			TxD_shift <= (TxD_shift >> 1);

		case(TxD_state)
			4'b0000: if(TxD_start) TxD_state <= 4'b0100;
			4'b0100: if(BitTick) TxD_state <= 4'b1000;  // start bit
			4'b1000: if(BitTick) TxD_state <= 4'b1001;  // bit 0
			4'b1001: if(BitTick) TxD_state <= 4'b1010;  // bit 1
			4'b1010: if(BitTick) TxD_state <= 4'b1011;  // bit 2
			4'b1011: if(BitTick) TxD_state <= 4'b1100;  // bit 3
			4'b1100: if(BitTick) TxD_state <= 4'b1101;  // bit 4
			4'b1101: if(BitTick) TxD_state <= 4'b1110;  // bit 5
			4'b1110: if(BitTick) TxD_state <= 4'b1111;  // bit 6
			4'b1111: if(BitTick) TxD_state <= 4'b0010;  // bit 7
			4'b0010: if(BitTick) TxD_state <= 4'b0000;  // stop1
			default: if(BitTick) TxD_state <= 4'b0000;
		endcase
	end

	assign TxD = (TxD_state<4) | (TxD_state[3] & TxD_shift[0]);  // put together the start, data and stop bits
	endmodule