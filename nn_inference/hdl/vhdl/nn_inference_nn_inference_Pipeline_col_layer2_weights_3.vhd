-- ==============================================================
-- Vitis HLS - High-Level Synthesis from C, C++ and OpenCL v2021.1 (64-bit)
-- Copyright 1986-2021 Xilinx, Inc. All Rights Reserved.
-- ==============================================================
library ieee; 
use ieee.std_logic_1164.all; 
use ieee.std_logic_unsigned.all;

entity nn_inference_nn_inference_Pipeline_col_layer2_weights_3 is 
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


architecture rtl of nn_inference_nn_inference_Pipeline_col_layer2_weights_3 is 

signal address0_tmp : std_logic_vector(AddressWidth-1 downto 0); 
type mem_array is array (0 to AddressRange-1) of std_logic_vector (DataWidth-1 downto 0); 
signal mem : mem_array := (
    0 => "10111111000010101101101000100111", 
    1 => "10111111110010010110100111110001", 
    2 => "10111111100100111001100011101101", 
    3 => "00111111001001011110001000101000", 
    4 => "00111110110000111001100010011000", 
    5 => "00111111101101001110110000010100", 
    6 => "00111110100100111010011001001100", 
    7 => "00111101110110101110001011100000", 
    8 => "10111100001100010110111001011000", 
    9 => "00111111011100100111010110001001", 
    10 => "10111111010100010010111010111100", 
    11 => "00111111011111011101101111001001", 
    12 => "10111111000101101011011100101100", 
    13 => "00111111000011101011101000100010", 
    14 => "10111110101010111101011010010100", 
    15 => "00111111101110011001011010110100" );


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

