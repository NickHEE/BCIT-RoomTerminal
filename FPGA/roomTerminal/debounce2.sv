// debounce2.sv - ELEX 7660 final project, this module's purpose is to 
// debounce the keypad input "kphit" , and send the clean output " PB_state" 

module debounce2(
    input clk, //
    input kphit,  //this is the input to be debounced
    output reg PB_state  //this is the debounced switch
);

// Synchronize the switch input to the clock
reg PB_sync_0;
always @(posedge clk) PB_sync_0 <= kphit; 
reg PB_sync_1;
always @(posedge clk) PB_sync_1 <= PB_sync_0;

// Debounce the switch
reg [15:0] PB_cnt;
always @(posedge clk)
if(PB_state==PB_sync_1)
    PB_cnt <= 0;
else
begin
    PB_cnt <= PB_cnt + 1'b1;  
    if(PB_cnt == 16'hffff) PB_state <= ~PB_state;  
end
endmodule