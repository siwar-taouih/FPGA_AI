-- ==============================================================
-- Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
-- Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
-- ==============================================================
library ieee; 
use ieee.std_logic_1164.all; 
use ieee.std_logic_unsigned.all;

entity nn_inference_nn_inference_Pipeline_col_layer2_weights_28 is 
    generic(
             DataWidth     : integer := 32; 
             AddressWidth     : integer := 4; 
             AddressRange    : integer := 16
    ); 
    port (
          address0      : in std_logic_vector(AddressWidth-1 downto 0); 
          ce0       : in std_logic; 
          q0         : out std_logic_vector(DataWidth-1 downto 0);
          reset     : in std_logic;
          clk       : in std_logic
    ); 
end entity; 


architecture rtl of nn_inference_nn_inference_Pipeline_col_layer2_weights_28 is 

signal address0_tmp : std_logic_vector(AddressWidth-1 downto 0); 
type mem_array is array (0 to AddressRange-1) of std_logic_vector (DataWidth-1 downto 0); 
signal mem : mem_array := (
    0 => "10111101000011000010101111110011", 
    1 => "00111111001100100111101100001000", 
    2 => "00111111001110010001101010011010", 
    3 => "10111101011001101000000111101010", 
    4 => "00111111001011110101111011011000", 
    5 => "10111111010111001000000111010111", 
    6 => "00111111010101010001000100000100", 
    7 => "00111111000000101100010101100100", 
    8 => "10111111000111000010101111111110", 
    9 => "10111101000011011010000010000011", 
    10 => "00111111010001110111010000010000", 
    11 => "10111011101010000000111000100101", 
    12 => "00111111011001001100101010001011", 
    13 => "00111111000000110011101011110111", 
    14 => "00111111010011110001010111111000", 
    15 => "00111101111111010011011111100100" );


begin 


memory_access_guard_0: process (address0) 
begin
      address0_tmp <= address0;
--synthesis translate_off
      if (CONV_INTEGER(address0) > AddressRange-1) then
           address0_tmp <= (others => '0');
      else 
           address0_tmp <= address0;
      end if;
--synthesis translate_on
end process;

p_rom_access: process (clk)  
begin 
    if (clk'event and clk = '1') then
        if (ce0 = '1') then 
            q0 <= mem(CONV_INTEGER(address0_tmp)); 
        end if;
    end if;
end process;

end rtl;

