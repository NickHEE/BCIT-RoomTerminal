// the testbench for vendingMachine.sv, it resets at the start
// written by Hsiao Yi, Lu (Ian) A00984995 Set 6T on Feb.6.2019

module debounce2_tb;

	logic clk='1; //this is a 50MHz clock provided on FPGA pin PIN_Y2
    logic PB;  //this is the input to be debounced
    logic PB_state;  //this is the debounced switch
	
	//////

	debounce2 debouncethis (.*); 
    	// 
	initial begin

	
    	PB <= 1;
		repeat(1) @(posedge clk) ;
		PB <= 0;
		repeat(2) @(posedge clk) ;
		PB <= 1;
		repeat(1) @(posedge clk) ;
		PB <= 0;
		repeat(2) @(posedge clk) ;
		PB <= 1;
		repeat(1) @(posedge clk) ;
		PB <= 0;
		repeat(100) @(posedge clk) ;
     		$stop ;     
   	end

  	always
     	#500ns clk = ~clk ;  // setting the clock period to be 500 ns
endmodule 