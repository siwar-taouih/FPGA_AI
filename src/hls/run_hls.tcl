# Vitis HLS TCL Script for Neural Network Synthesis
# This script creates an HLS project and runs C synthesis
# Optimized for MNIST Neural Network Inference on FPGA

# Set project name and top function
set project_name "nn_inference_hls"
set top_function "nn_inference"
set solution_name "solution1"

# Create new project (remove if exists)
open_project -reset $project_name

# Add design files
add_files matmul.cpp
add_files matmul.hpp

# Add testbench files (not synthesized, only for verification)
add_files -tb matmul_tb.cpp

# Set top function
set_top $top_function

# Create solution with target device and clock period
open_solution -reset $solution_name

# Set target device - Xilinx Zynq-7020 (common for neural network applications)
# Alternative devices:
#   - xc7z020clg484-1 (Zynq-7020, lower cost)
#   - xc7z045ffg900-2 (Zynq-7045, more resources)
#   - xczu9eg-ffvb1156-2-e (Zynq UltraScale+, high performance)
set_part {xc7z020clg484-1}

# Create clock constraint
# 8ns = 125MHz - Optimized for floating-point operations on Zynq-7000
# This provides good balance between performance and timing closure
# Adjust if needed: 10ns=100MHz (safer), 6.67ns=150MHz (aggressive)
create_clock -period 8 -name default

# Configure synthesis options
config_compile -name_max_length 80
config_schedule -effort high
config_schedule -enable_dsp_full_reg

# Configure interface synthesis
config_interface -m_axi_addr64

# Run C simulation (optional - uncomment to verify before synthesis)
# csim_design -clean

# Run C synthesis
puts "========================================="
puts "Starting C Synthesis..."
puts "Target Device: xc7z020clg484-1"
puts "Clock Period: 8ns (125MHz)"
puts "========================================="
csynth_design

# Co-simulation (optional - uncomment to verify RTL)
# cosim_design -rtl verilog -trace_level all

# Export RTL design (uncomment to generate IP for Vivado)
# export_design -format ip_catalog -description "MNIST Neural Network Inference" -vendor "user" -version "1.0"

# Export RTL as Verilog/VHDL (uncomment to generate standalone RTL)
# export_design -rtl verilog -format syn_dcp

# Print synthesis summary
puts "========================================="
puts "C Synthesis Complete!"
puts "Check reports in: nn_inference_hls/solution1/syn/report/"
puts "  - nn_inference_csynth.rpt (main synthesis report)"
puts "  - Resource utilization (LUTs, FFs, DSPs, BRAMs)"
puts "  - Timing analysis (latency, interval, clock)"
puts "========================================="

exit
