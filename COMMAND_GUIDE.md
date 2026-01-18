# FPGA Deployment Guide - Vivado + Pynq-Z2 Board
## Steps to Run Neural Network on Physical FPGA Hardware

This guide covers **only what runs on Vivado with the FPGA board connected**.

---

## Prerequisites

### Required Hardware
- **Pynq-Z2 FPGA Board**
- **USB cable** (micro-USB to computer)
- **Power supply** for board

### Required Software (Must be installed on Linux/Windows machine)
- **Vivado 2021.1** or later
- **Vitis 2021.1** or later
- Pre-generated RTL files (already in `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/nn_inference/hdl/`)

### Python for Testing (on your Mac)
```bash
pip3 install pyserial opencv-python numpy
```

---

## STEP 1: Create Vivado Project

### Launch Vivado
```bash
# On Linux/Windows machine with Vivado installed:
vivado
```

### Create Project in Vivado GUI

**1. Create New Project**
   - File -> Project -> New
   - Project name: `fpga_nn_project`
   - Location: `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/vivado`
   - ✓ Create project subdirectory
   - Click **Next**

**2. Project Type**
   - Select: **RTL Project**
   - ✗ Do not specify sources at this time
   - Click **Next**

**3. Add VHDL Sources**
   - Click **Add Directories**
   - Browse to: `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/src/vhdl/`
   - Select all `.vhd` files:
     - `fix_address.vhd`
     - `not_gate.vhd`
     - `nn_ctrl.vhd`
   - Click **Next**

**4. Add Constraints** (skip for now)
   - Click **Next**

**5. Select Board**
   - Click **Boards** tab
   - Search: `pynq-z2`
   - Select: **pynq-z2**
   - Click **Next** -> **Finish**

---

## STEP 2: Add Pre-Generated Neural Network IP

**6. Add IP Repository**
   - Tools -> Settings -> IP -> Repository
   - Click **+** (Add)
   - Browse to: `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/nn_inference/`
   - Click **Select**
   - Click **OK**
   - You should see: "1 repository added"

---

## STEP 3: Create Block Design

**7. Create Block Design**
   - Flow Navigator -> IP INTEGRATOR -> **Create Block Design**
   - Name: `design_1`
   - Click **OK**

**8. Add ZYNQ Processor**
   - In diagram window: Right-click -> **Add IP**
   - Search: `ZYNQ7 Processing System`
   - Double-click to add
   - Click **Run Block Automation** (green banner)
   - Click **OK**

**9. Configure ZYNQ**
   - Double-click **ZYNQ7 Processing System** block
   - Go to: **Peripheral I/O Pins**
   - **Uncheck all** except **UART 0**
   - Click **OK**

**10. Add BRAM Controller**
   - Right-click -> **Add IP**
   - Search: `AXI BRAM Controller`
   - Double-click to add
   - Click **Run Block Automation**
   - Click **OK**

**11. Configure BRAM**
   - Double-click **axi_bram_ctrl_0**
   - Set **Number of BRAM interfaces**: `1`
   - Click **OK**

**12. Add Neural Network IP**
   - Right-click -> **Add IP**
   - Search: `nn_inference`
   - Double-click to add
   - **DO NOT** run block automation

**13. Add VHDL Control Modules**
   - From **Sources** panel, drag into block design:
     - `fix_address`
     - `not_gate`
     - `nn_ctrl`

**14. Make Connections**
   - Connect ports by clicking and dragging:
     - ZYNQ → BRAM Controller (AXI connections)
     - BRAM Controller → nn_inference (data paths)
     - nn_ctrl → nn_inference (control signals)
     - fix_address → address buses
     - not_gate → control logic
   
   *(Refer to original project diagram for exact connections)*

**15. Create External LED Port**
   - Right-click on `led_ctrl` output from `nn_ctrl`
   - Select **Make External**
   - This creates output port for LEDs

**16. Validate Design**
   - Tools -> **Validate Design** (or press **F6**)
   - Should show: "Validation successful"

---

## STEP 4: Generate Bitstream

**17. Create HDL Wrapper**
   - In Sources panel: Right-click `design_1.bd`
   - Select **Create HDL Wrapper**
   - Choose: **Let Vivado manage wrapper**
   - Click **OK**

**18. Run Synthesis**
   - Flow Navigator -> SYNTHESIS -> **Run Synthesis**
   - Click **OK**
   - **Wait 10-30 minutes**

**19. Open Synthesized Design**
   - When synthesis completes, click **Open Synthesized Design**

**20. Assign LED Pins**
   - Window -> **I/O Ports**
   - Set LED pin assignments (6 LEDs):
     - `led_ctrl[0]`: **R14**, I/O Std: **LVCMOS33**  (LD0)
     - `led_ctrl[1]`: **P14**, I/O Std: **LVCMOS33**  (LD1)
     - `led_ctrl[2]`: **N16**, I/O Std: **LVCMOS33**  (LD2)
     - `led_ctrl[3]`: **M14**, I/O Std: **LVCMOS33**  (LD3)
     - `led_ctrl[4]`: **M15**, I/O Std: **LVCMOS33**  (LD4)
     - `led_ctrl[5]`: **G14**, I/O Std: **LVCMOS33**  (LD5)
   - Press **Ctrl+S** to save constraints

**21. Run Implementation**
   - Flow Navigator -> IMPLEMENTATION -> **Run Implementation**
   - Click **OK**
   - **Wait 20-40 minutes**

**22. Generate Bitstream**
   - Flow Navigator -> PROGRAM AND DEBUG -> **Generate Bitstream**
   - Click **OK**
   - **Wait 30-60 minutes**

**23. Export Hardware**
   - File -> Export -> **Export Hardware**
   - ✓ **Include bitstream**
   - Click **Next**
   - Location: `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/hardware`
   - Click **Finish**

---

## STEP 5: Create Vitis Software Application

**24. Launch Vitis**
```bash
# On Linux/Windows machine:
vitis -workspace /Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/vitis_workspace
```

**25. Create Platform Project**
   - File -> New -> **Platform Project**
   - Name: `fpga_nn_platform`
   - Click **Next**
   - Click **Browse** -> Select: `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/hardware/design_1_wrapper.xsa`
   - Click **Finish**

**26. Create Application Project**
   - File -> New -> **Application Project**
   - Click **Next**
   - Select platform: `fpga_nn_platform`
   - Click **Next**
   - Application name: `nn_app`
   - Click **Next**
   - Domain: **standalone on ps7_cortexa9_0**
   - Click **Next**
   - Template: **Hello World**
   - Click **Finish**

**27. Replace Application Code**
   - In Project Explorer: `nn_app -> src -> helloworld.c`
   - Delete all content
   - Copy code from: `/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/src/vitis/helloworld.c`
   - Paste into `helloworld.c`
   - Press **Ctrl+S** to save

**28. Build Application**
   - Right-click `nn_app`
   - Select **Build Project**
   - **Wait 1-5 minutes**

---

## STEP 6: Connect and Program FPGAoard

**29. Connect Pynq-Z2 Board**
   - Connect **micro-USB cable** from board to computer
   - Connect **power supply** to board
   - Set **boot mode jumpers** to **JTAG mode**:
     - JP4: Set to JTAG position
   - **Power on** the board

**30. Program FPGA**
   - In Vitis: Right-click `nn_app`
   - Select **Run As** -> **Launch Hardware (System Debugger)**
   - Vitis will:
     - Program the FPGA with bitstream
     - Load software onto ARM processor
     - Start execution

**31. Verify LEDs**
   - LEDs on board should light up showing 6-bit binary pattern
   - Pattern represents neural network prediction (0-9)
   
   **LED Pattern Reference:**
   | Digit | Binary   | LD5 | LD4 | LD3 | LD2 | LD1 | LD0 |
   |-------|----------|-----|-----|-----|-----|-----|-----|
   | 0     | 001010   | ⚫  | ⚫  | 🟢  | ⚫  | 🟢  | ⚫  |
   | 1     | 000001   | ⚫  | ⚫  | ⚫  | ⚫  | ⚫  | 🟢  |
   | 2     | 000010   | ⚫  | ⚫  | ⚫  | ⚫  | 🟢  | ⚫  |
   | 3     | 000011   | ⚫  | ⚫  | ⚫  | ⚫  | 🟢  | 🟢  |
   | 4     | 000100   | ⚫  | ⚫  | ⚫  | 🟢  | ⚫  | ⚫  |
   | 5     | 000101   | ⚫  | ⚫  | ⚫  | 🟢  | ⚫  | 🟢  |
   | 6     | 000110   | ⚫  | ⚫  | ⚫  | 🟢  | 🟢  | ⚫  |
   | 7     | 000111   | ⚫  | ⚫  | ⚫  | 🟢  | 🟢  | 🟢  |
   | 8     | 001000   | ⚫  | ⚫  | 🟢  | ⚫  | ⚫  | ⚫  |
   | 9     | 001001   | ⚫  | ⚫  | 🟢  | ⚫  | ⚫  | 🟢  |

---

## STEP 7: Test with UART (from your Mac)

**32. Find USB Serial Port**
```bash
# On Mac:
ls /dev/tty.usbserial*

# On Linux:
ls /dev/ttyUSB*

# Example output: /dev/tty.usbserial-1234
```

**33. Run Test Script**
```bash
# On your Mac:
cd /Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/src/python

# Run test (replace with your actual port):
python3 uart_test_nn.py -port /dev/tty.usbserial-1234

# Expected output:
# Sending test image...
# Prediction: 7
# [LEDs on board show: 0111 in binary = 7]
```

---

## Quick Reference

| Step | Tool | Duration | Output |
|------|------|----------|--------|
| 1-3. Vivado Project Setup | Vivado GUI | 15 min | Block design |
| 4. Synthesis | Vivado | 10-30 min | Synthesized design |
| 4. Implementation | Vivado | 20-40 min | Placed & routed design |
| 4. Bitstream | Vivado | 30-60 min | `.bit` file |
| 5. Vitis Software | Vitis GUI | 5-10 min | `.elf` executable |
| 6. Program FPGA | Vitis | 1-2 min | Running on hardware |
| 7. Test | Python script | Instant | UART predictions |

---

## File Locations

```
/Users/siwartaouih/uOttaHack_FPGA/FPGA_AI/
├── nn_inference/hdl/           # Pre-generated RTL (use this)
│   ├── verilog/                # Neural network Verilog files
│   └── ip/                     # IP catalog files
├── src/
│   ├── vhdl/                   # Control logic (add to Vivado)
│   │   ├── fix_address.vhd
│   │   ├── not_gate.vhd
│   │   └── nn_ctrl.vhd
│   ├── vitis/                  # ARM processor code
│   │   └── helloworld.c        # Copy to Vitis project
│   └── python/                 # Testing scripts (run on Mac)
│       └── uart_test_nn.py
├── vivado/                     # Vivado project (created)
├── hardware/                   # Exported .xsa file (created)
└── vitis_workspace/            # Vitis workspace (created)
```

---

## Troubleshooting

### Board Not Detected
```bash
# Check USB connection:
lsusb | grep Xilinx

# Check JTAG mode jumpers (JP4)
```

### Bitstream Generation Failed
- Check Vivado log: `vivado/fpga_nn_project/fpga_nn_project.runs/impl_1/runme.log`
- Verify all connections in block design
- Re-validate design (F6)

### LEDs Not Working
- Verify pin constraints were saved
- Check UART output for errors
- Verify power supply is connected

---

## Summary

This workflow requires:
1. **Vivado** (Linux/Windows) - for FPGA design and bitstream generation
2. **Vitis** (Linux/Windows) - for ARM software compilation
3. **Pynq-Z2 board** - physical hardware
4. **Python scripts** (Mac/Linux/Windows) - for testing via UART

**Total time:** ~2-3 hours (mostly waiting for synthesis/implementation)
