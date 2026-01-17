-- ==============================================================
-- Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
-- Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
-- ==============================================================
library ieee; 
use ieee.std_logic_1164.all; 
use ieee.std_logic_unsigned.all;

entity nn_inference_nn_inference_Pipeline_col_layer2_weights_18 is 
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


architecture rtl of nn_inference_nn_inference_Pipeline_col_layer2_weights_18 is 

signal address0_tmp : std_logic_vector(AddressWidth-1 downto 0); 
type mem_array is array (0 to AddressRange-1) of std_logic_vector (DataWidth-1 downto 0); 
signal mem : mem_array := (
    0 => "00111101001110010000000001001101", 
    1 => "00111111000010001101011010010111", 
    2 => "00111111001110100001100000011000", 
    3 => "10111111101010110110101100010111", 
    4 => "00111110111100001110110110111000", 
    5 => "10111111100001100111011010001001", 
    6 => "00111111000110101100001101011100", 
    7 => "10111110100100001111101011111010", 
    8 => "10111110100110001111111001110100", 
    9 => "10111111011001001110111011000111", 
    10 => "00111011101000010000001010010001", 
    11 => "10111111001111100110000101111001", 
    12 => "10111101111011011011011101001111", 
    13 => "00111111101010101001000111000000", 
    14 => "10111111010010110100000011110000", 
    15 => "00111111001011000001110110101111" );


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

