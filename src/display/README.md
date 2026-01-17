# FPGA Monitor Display System

This directory contains software for displaying meaningful output on a monitor connected to your Zynq FPGA board.

## What Will Be Displayed

Your monitor will show:

1. **Input Image** - Visual representation of the 10x10 digit image (scaled up to 200x200 pixels)
2. **Prediction Result** - Large display of the predicted digit (0-9)
3. **Confidence Level** - Percentage confidence with color coding:
   - Green: > 90% confidence
   - Yellow: 70-90% confidence
   - Red: < 70% confidence
4. **Processing Time** - How long the FPGA took to process (in milliseconds and clock cycles)
5. **Confidence Distribution** - Bar graph showing confidence for all 10 digits
6. **Statistics** - Total images processed and accuracy percentage

## Display Options

### Option 1: Python GUI (display_gui.py)
**Best for:** Development PC or Zynq with Linux + Python + Tkinter

**Features:**
- Full graphical interface
- Real-time updates
- Bar charts and visualizations

**Requirements:**
```bash
sudo apt-get install python3-tk python3-numpy
```

**Run:**
```bash
python3 display_gui.py
```

### Option 2: Terminal Display (display_terminal.py)
**Best for:** Any system with Python, no GUI needed

**Features:**
- Text-based visualization
- ASCII art representation of digit
- Works over SSH/serial console

**Requirements:**
```bash
pip3 install numpy
```

**Run:**
```bash
python3 display_terminal.py
```

### Option 3: Web Interface (Coming Soon)
**Best for:** Remote monitoring via web browser

**Features:**
- Access from any device with a browser
- Real-time updates via WebSocket
- Mobile-friendly

## Integration with FPGA

### On Zynq Platform:

1. **FPGA Side (PL - Programmable Logic):**
   - Neural network hardware processes images
   - Returns prediction via AXI interface

2. **ARM Side (PS - Processing System):**
   - Loads test images
   - Sends to FPGA via AXI
   - Receives results
   - Updates display

### Data Flow:

```
Test Images → ARM Processor → AXI Bus → FPGA NN → Results → Display Software → Monitor
```

## Quick Start

### For Development (on your Mac):

```bash
cd /Users/siwartaouih/FPGA_AI/src/display
python3 display_terminal.py
```

This will show a demo of what the display will look like.

### For FPGA Deployment:

1. Copy display software to Zynq board
2. Integrate with your FPGA driver code
3. Run display application
4. Connect monitor via HDMI/VGA

## Display Specification

See `../../docs/display_specification.md` for complete visual design and technical details.

## Files

- **display_gui.py** - Full graphical interface (requires Tkinter)
- **display_terminal.py** - Terminal-based display (works anywhere)
- **display_specification.md** - Complete design document
- **README.md** - This file

## Example Output

```
╔════════════════════════════════════════════════════════════╗
║  MNIST Digit Recognition - FPGA Hardware Accelerator       ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  Input Image (10x10):          Prediction: 7              ║
║                                                            ║
║  ░░░░░░░░░░                    Confidence: 95.3%          ║
║  ░░██████░░                    Status: ✓ Correct          ║
║  ░░░░░░██░░                                               ║
║  ░░░░░██░░░                    Processing Time:           ║
║  ░░░░██░░░░                    0.026 ms (3,250 cycles)    ║
║  ░░░██░░░░░                                               ║
║  ░░██░░░░░░                    Confidence Distribution:   ║
║  ░░██░░░░░░                    0: ████░░░░░░ 12%         ║
║  ░░██░░░░░░                    1: ██░░░░░░░░  5%         ║
║  ░░░░░░░░░░                    2: ███░░░░░░░  8%         ║
║                                3: ██░░░░░░░░  4%         ║
║                                4: ███░░░░░░░  7%         ║
║                                5: ████░░░░░░ 11%         ║
║                                6: ███░░░░░░░  9%         ║
║                                7: ██████████ 95% ← PRED  ║
║                                8: ████░░░░░░ 10%         ║
║                                9: ███░░░░░░░  6%         ║
║                                                            ║
║  Images Processed: 42  |  Accuracy: 97.6%                 ║
╚════════════════════════════════════════════════════════════╝
```
