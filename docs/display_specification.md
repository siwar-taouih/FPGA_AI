# FPGA Monitor Display Specification
## MNIST Digit Recognition - Visual Output System

### Display Overview

This document describes the graphical display system for showing meaningful output on a monitor connected to the Zynq FPGA board.

---

## Screen Layout (640x480 VGA/HDMI)

```
┌────────────────────────────────────────────────────────────┐
│  MNIST Digit Recognition - FPGA Hardware Accelerator       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ┌─────────────────┐         ┌──────────────────────┐    │
│  │  Input Image    │         │   Prediction Result   │    │
│  │                 │         │                       │    │
│  │   [10x10 grid]  │         │   Digit:    7         │    │
│  │   (scaled 20x)  │         │   Confidence: 95.3%   │    │
│  │   200x200 px    │         │                       │    │
│  │                 │         │   Processing Time:    │    │
│  │                 │         │   0.026 ms            │    │
│  └─────────────────┘         │   (3,250 cycles)      │    │
│                              └──────────────────────┘    │
│                                                            │
│  ┌────────────────────────────────────────────────────┐   │
│  │  Confidence Distribution (Bar Graph)               │   │
│  │                                                    │   │
│  │  0: ████░░░░░░  12%                               │   │
│  │  1: ██░░░░░░░░   5%                               │   │
│  │  2: ███░░░░░░░   8%                               │   │
│  │  3: ██░░░░░░░░   4%                               │   │
│  │  4: ███░░░░░░░   7%                               │   │
│  │  5: ████░░░░░░  11%                               │   │
│  │  6: ███░░░░░░░   9%                               │   │
│  │  7: ██████████  95% ← PREDICTION                  │   │
│  │  8: ████░░░░░░  10%                               │   │
│  │  9: ███░░░░░░░   6%                               │   │
│  └────────────────────────────────────────────────────┘   │
│                                                            │
│  Status: Ready  |  Images Processed: 42  |  Accuracy: 98% │
└────────────────────────────────────────────────────────────┘
```

---

## Display Components

### 1. Header Bar
- **Title:** "MNIST Digit Recognition - FPGA Hardware Accelerator"
- **Background:** Dark blue (#1E3A8A)
- **Text:** White, bold, 24px font
- **Position:** Top of screen, full width

### 2. Input Image Display
- **Size:** 200x200 pixels (10x10 image scaled 20x)
- **Position:** Left side, centered vertically
- **Border:** 2px white border
- **Content:** Grayscale visualization of the 100 input pixels
- **Label:** "Input Image" above the display

### 3. Prediction Panel
- **Size:** 250x200 pixels
- **Position:** Right of input image
- **Background:** Light gray (#F3F4F6)
- **Border:** 2px border
- **Contents:**
  - **Predicted Digit:** Large (72px), bold, centered
  - **Confidence:** Percentage with 1 decimal place
  - **Processing Time:** In milliseconds and clock cycles
  - **Color coding:** 
    - Green if confidence > 90%
    - Yellow if 70-90%
    - Red if < 70%

### 4. Confidence Distribution Graph
- **Type:** Horizontal bar chart
- **Size:** 600x250 pixels
- **Position:** Bottom section
- **Bars:** One for each digit (0-9)
- **Colors:** 
  - Predicted digit: Green (#10B981)
  - Other digits: Gray (#9CA3AF)
- **Labels:** Digit number + percentage value

### 5. Status Bar
- **Position:** Bottom of screen
- **Height:** 30px
- **Background:** Dark gray (#374151)
- **Text:** White
- **Information:**
  - Current status (Ready/Processing/Error)
  - Total images processed
  - Overall accuracy percentage

---

## Color Scheme

```
Primary Background:   #FFFFFF (White)
Header:              #1E3A8A (Dark Blue)
Panel Background:    #F3F4F6 (Light Gray)
Border:              #D1D5DB (Gray)
Text Primary:        #111827 (Almost Black)
Text Secondary:      #6B7280 (Medium Gray)
Success/High Conf:   #10B981 (Green)
Warning/Med Conf:    #F59E0B (Yellow)
Error/Low Conf:      #EF4444 (Red)
Accent:              #3B82F6 (Blue)
```

---

## Implementation Options

### Option A: Simple VGA Controller (Recommended for beginners)
- **Resolution:** 640x480 @ 60Hz
- **Color depth:** 8-bit (256 colors) or 12-bit (4096 colors)
- **Memory:** Frame buffer in BRAM (307,200 bytes for 640x480x8bit)
- **Interface:** VGA connector on FPGA board

### Option B: HDMI Output (More advanced)
- **Resolution:** 1280x720 or 1920x1080
- **Color depth:** 24-bit RGB
- **Interface:** HDMI encoder IP core
- **Requires:** More FPGA resources

### Option C: Software Display via ARM (Easiest)
- **Method:** ARM processor generates display using Linux framebuffer
- **Graphics:** Use Qt, SDL, or simple framebuffer writes
- **Advantage:** Easier to program, flexible
- **Disadvantage:** Not pure hardware solution

---

## Data Flow

```
┌──────────────────┐
│  Test Image      │
│  (100 floats)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Neural Network  │
│  (FPGA Hardware) │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Results:        │
│  - Prediction    │
│  - Confidence    │
│  - Timing        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Display Driver  │
│  (ARM or FPGA)   │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  VGA/HDMI        │
│  Monitor Output  │
└──────────────────┘
```

---

## Recommended Implementation Path

### Phase 1: Basic Text Display (Quickest)
Use ARM processor with simple UART or framebuffer to display:
- Predicted digit
- Confidence percentage
- Processing time

### Phase 2: Add Graphics
Implement VGA controller to show:
- Scaled input image
- Prediction with color coding
- Basic bar graph

### Phase 3: Full GUI
Complete implementation with:
- All visual elements
- Real-time updates
- Multiple test images cycling

---

## Files to Create

1. **display_controller.v** - VGA timing and control logic
2. **frame_buffer.v** - Memory for storing display data
3. **graphics_engine.v** - Draws shapes, text, bars
4. **display_driver.c** - ARM software to update display
5. **font_rom.v** - Character font data for text display

---

## Performance Requirements

- **Update Rate:** 30-60 FPS for smooth display
- **Latency:** < 1ms from prediction to display update
- **Memory:** ~300KB for frame buffer (640x480x8bit)
- **FPGA Resources:** 
  - ~1000 LUTs for VGA controller
  - ~10 BRAMs for frame buffer
  - Minimal impact on neural network resources

---

## Next Steps

Choose your implementation approach:

**A. Quick Software Display (Recommended to start)**
   - Use ARM processor with Linux
   - Display via HDMI using Qt or framebuffer
   - Fastest to implement and test

**B. Hardware VGA Display**
   - Implement VGA controller in FPGA
   - More educational, pure hardware solution
   - Requires additional Verilog coding

**C. Hybrid Approach**
   - ARM generates graphics
   - FPGA handles VGA timing
   - Good balance of flexibility and performance
