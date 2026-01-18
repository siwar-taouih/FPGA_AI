[matmul.cpp](/src/hls/matmul.cpp)

- Function definitions for matrix multiplication, activiation layers, and combined neural network.


[matmul.hpp](/src/hls/matmul.hpp)

- Header file with function, neural network weight, and constant declarations.


[matmul_tb.cpp](/src/hls/matmul_tb.cpp)

- Testbench used in HLS to verify program behavior with C-synthesis.

**Compile & Run C Simulation**

g++ -o matmul_test matmul.cpp matmul_tb.cpp -I. -std=c++11

**Run C simulation to verify the design with updated weights**

./matmul_test

>> Test image 1: Prediction = 1 

Total of 3 images tested

**Run C Synthesis (Requires Vitis HLS)**

To run C synthesis, you need Xilinx Vitis HLS installed. Use the provided TCL script:

```bash
vitis_hls run_hls.tcl
```

Or run interactively on AMD

```bash
vitis_hls
# In Vitis HLS GUI:
# 1. Create new project
# 2. Add matmul.cpp and matmul.hpp as design files
# 3. Add matmul_tb.cpp as testbench
# 4. Set top function: nn_inference
# 5. Create solution with target device (e.g., xc7z020clg484-1)
# 6. Set clock period: 10ns (100MHz)
# 7. Run C Synthesis
```

**Synthesis Configuration:**
- **Top Function:** `nn_inference`
- **Target Device:** Xilinx Zynq-7020 (xc7z020clg484-1)
- **Clock Period:** 8ns (125MHz) - Optimized for floating-point operations
  - Alternative: 10ns (100MHz) for safer timing closure
  - Alternative: 6.67ns (150MHz) for aggressive performance
- **Optimization:** High effort scheduling with DSP full register enabled

**Expected Synthesis Outputs:**

After running synthesis, check the reports in `nn_inference_hls/solution1/syn/report/`:

1. **nn_inference_csynth.rpt** - Main synthesis report containing:
   - **Timing Summary:** Latency, Interval, Pipeline depth
   - **Resource Utilization:** 
     - BRAM_18K (Block RAM for weight storage)
     - DSP48E (DSP slices for multiply-accumulate)
     - FF (Flip-flops)
     - LUT (Look-up tables)
   - **Interface Summary:** Port protocols and bit-widths
   
2. **Resource Estimates** (typical for this design):
   - DSP48E: ~32-64 (for parallel multiply-accumulate)
   - BRAM: ~10-20 (for storing 100x32 + 32x16 + 16x10 weights)
   - LUT: ~5000-15000 (control logic, activation functions)
   - FF: ~3000-8000 (pipeline registers)

**Generated RTL Files:**

The synthesis will generate Verilog/VHDL files in `nn_inference_hls/solution1/syn/verilog/` or `vhdl/`

