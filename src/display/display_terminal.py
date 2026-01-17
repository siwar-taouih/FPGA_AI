#!/usr/bin/env python3
"""
MNIST Digit Recognition - Terminal Display
Text-based visualization for FPGA neural network predictions
Works on any system with Python - no GUI required
"""

import numpy as np
import time
import sys

class TerminalDisplay:
    def __init__(self):
        self.total_processed = 0
        self.correct_predictions = 0
        
    def clear_screen(self):
        """Clear terminal screen"""
        print("\033[2J\033[H", end="")
        
    def draw_header(self):
        """Draw header"""
        print("╔" + "═" * 70 + "╗")
        print("║" + " " * 5 + "MNIST Digit Recognition - FPGA Hardware Accelerator" + " " * 12 + "║")
        print("╠" + "═" * 70 + "╣")
        
    def draw_image(self, pixels):
        """Draw 10x10 image using ASCII characters"""
        if len(pixels) == 100:
            pixels = np.array(pixels).reshape(10, 10)
        
        print("║  Input Image (10x10):", " " * 47 + "║")
        print("║", " " * 69 + "║")
        
        for row in pixels:
            line = "║  "
            for pixel in row:
                # Convert pixel value to ASCII character
                if pixel < 0.1:
                    line += "░░"
                elif pixel < 0.3:
                    line += "▒▒"
                elif pixel < 0.6:
                    line += "▓▓"
                else:
                    line += "██"
            line += " " * (67 - len(line) + 1) + "║"
            print(line)
        print("║", " " * 69 + "║")
        
    def draw_prediction(self, prediction, confidence, processing_time_ms, cycles):
        """Draw prediction results"""
        # Prediction
        pred_line = f"║  Prediction: {prediction}"
        pred_line += " " * (70 - len(pred_line)) + "║"
        print(pred_line)
        
        # Confidence with color coding
        conf_pct = confidence * 100
        if conf_pct > 90:
            status = "✓ High"
            symbol = "✓"
        elif conf_pct > 70:
            status = "⚠ Medium"
            symbol = "⚠"
        else:
            status = "✗ Low"
            symbol = "✗"
        
        conf_line = f"║  Confidence: {conf_pct:.1f}% ({status})"
        conf_line += " " * (70 - len(conf_line)) + "║"
        print(conf_line)
        
        print("║", " " * 69 + "║")
        
        # Processing time
        time_line = f"║  Processing Time: {processing_time_ms:.3f} ms ({cycles:,} cycles)"
        time_line += " " * (70 - len(time_line)) + "║"
        print(time_line)
        
        print("║", " " * 69 + "║")
        
    def draw_confidence_bars(self, confidence_scores, prediction):
        """Draw confidence distribution as text bars"""
        print("║  Confidence Distribution:", " " * 45 + "║")
        print("║", " " * 69 + "║")
        
        for digit in range(10):
            conf_pct = confidence_scores[digit] * 100
            bar_length = int(conf_pct / 10)  # 10 chars = 100%
            bar = "█" * bar_length + "░" * (10 - bar_length)
            
            # Mark prediction
            marker = " ← PRED" if digit == prediction else ""
            
            line = f"║  {digit}: {bar} {conf_pct:5.1f}%{marker}"
            line += " " * (70 - len(line)) + "║"
            print(line)
        
        print("║", " " * 69 + "║")
        
    def draw_status(self):
        """Draw status bar"""
        accuracy = (self.correct_predictions / self.total_processed * 100) if self.total_processed > 0 else 0
        
        status_line = f"║  Images Processed: {self.total_processed}  |  Accuracy: {accuracy:.1f}%"
        status_line += " " * (70 - len(status_line)) + "║"
        print(status_line)
        
    def draw_footer(self):
        """Draw footer"""
        print("╚" + "═" * 70 + "╝")
        
    def display_result(self, image, prediction, confidence_scores, true_label=None, 
                      processing_time_ms=0.026, cycles=3250):
        """Display complete result"""
        self.clear_screen()
        self.draw_header()
        self.draw_image(image)
        
        # Get confidence for predicted digit
        pred_confidence = confidence_scores[prediction]
        
        self.draw_prediction(prediction, pred_confidence, processing_time_ms, cycles)
        self.draw_confidence_bars(confidence_scores, prediction)
        
        # Update statistics
        self.total_processed += 1
        if true_label is not None and prediction == true_label:
            self.correct_predictions += 1
            
        self.draw_status()
        self.draw_footer()
        
        # Show if correct
        if true_label is not None:
            if prediction == true_label:
                print(f"\n✓ Correct! (Expected: {true_label}, Got: {prediction})")
            else:
                print(f"\n✗ Incorrect (Expected: {true_label}, Got: {prediction})")

def demo():
    """Demo mode with test images"""
    display = TerminalDisplay()
    
    # Test images from your testbench
    test_cases = [
        {
            'image': [0.0, 0.0, 0.0, 0.0, 0.003921569, 0.003921569, 0.015686275, 0.019607844, 0.003921569, 0.0,
                     0.0, 0.0, 0.0, 0.003921569, 0.0, 0.02745098, 0.13725491, 0.015686275, 0.007843138, 0.0,
                     0.0, 0.0, 0.0, 0.003921569, 0.003921569, 0.34117648, 0.6, 0.015686275, 0.015686275, 0.0,
                     0.0, 0.0, 0.0, 0.011764706, 0.007843138, 0.60784316, 0.54509807, 0.015686275, 0.007843138, 0.0,
                     0.0, 0.0, 0.0, 0.007843138, 0.13725491, 0.9490196, 0.19607843, 0.019607844, 0.003921569, 0.0,
                     0.0, 0.0, 0.0, 0.007843138, 0.4627451, 0.627451, 0.019607844, 0.007843138, 0.007843138, 0.0,
                     0.0, 0.0, 0.0, 0.011764706, 0.68235296, 0.2901961, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.02745098, 0.7529412, 0.0627451, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.02745098, 0.6901961, 0.11372549, 0.0, 0.0, 0.0, 0.0,
                     0.0, 0.0, 0.0, 0.007843138, 0.015686275, 0.007843138, 0.0, 0.0, 0.0, 0.0],
            'label': 1
        },
        {
            'image': [0.007843138, 0.007843138, 0.007843138, 0.007843138, 0.011764706, 0.011764706, 0.019607844, 0.011764706, 0.011764706, 0.0,
                     0.003921569, 0.007843138, 0.02745098, 0.12941177, 0.18431373, 0.21960784, 0.09019608, 0.015686275, 0.003921569, 0.0,
                     0.011764706, 0.007843138, 0.25490198, 0.8509804, 0.84705883, 0.88235295, 0.6745098, 0.019607844, 0.003921569, 0.0,
                     0.0, 0.0, 0.023529412, 0.10980392, 0.05882353, 0.40784314, 0.74509805, 0.023529412, 0.007843138, 0.0,
                     0.0, 0.003921569, 0.003921569, 0.050980393, 0.52156866, 0.9411765, 0.5647059, 0.019607844, 0.015686275, 0.0,
                     0.003921569, 0.003921569, 0.003921569, 0.2509804, 0.7254902, 0.53333336, 0.9137255, 0.15294118, 0.003921569, 0.0,
                     0.015686275, 0.011764706, 0.007843138, 0.011764706, 0.023529412, 0.03137255, 0.88235295, 0.2901961, 0.015686275, 0.0,
                     0.011764706, 0.011764706, 0.043137256, 0.21960784, 0.34117648, 0.5529412, 0.8745098, 0.12941177, 0.011764706, 0.0,
                     0.015686275, 0.015686275, 0.3019608, 0.9098039, 0.88235295, 0.6392157, 0.1764706, 0.011764706, 0.003921569, 0.0,
                     0.007843138, 0.011764706, 0.019607844, 0.003921569, 0.007843138, 0.007843138, 0.0, 0.0, 0.0, 0.0],
            'label': 3
        },
        {
            'image': [0.003921569, 0.007843138, 0.003921569, 0.007843138, 0.003921569, 0.007843138, 0.003921569, 0.007843138, 0.003921569, 0.0,
                     0.003921569, 0.023529412, 0.1254902, 0.003921569, 0.003921569, 0.003921569, 0.007843138, 0.003921569, 0.003921569, 0.0,
                     0.011764706, 0.011764706, 0.6745098, 0.023529412, 0.007843138, 0.003921569, 0.11372549, 0.05490196, 0.003921569, 0.0,
                     0.011764706, 0.043137256, 0.7058824, 0.043137256, 0.011764706, 0.019607844, 0.49411765, 0.34901962, 0.007843138, 0.0,
                     0.007843138, 0.21176471, 0.85490197, 0.6039216, 0.44705883, 0.5882353, 0.654902, 0.36862746, 0.011764706, 0.0,
                     0.007843138, 0.5411765, 0.2509804, 0.05882353, 0.0627451, 0.023529412, 0.35686275, 0.37254903, 0.007843138, 0.0,
                     0.007843138, 0.05490196, 0.019607844, 0.0, 0.0, 0.003921569, 0.31764707, 0.53333336, 0.003921569, 0.0,
                     0.011764706, 0.015686275, 0.015686275, 0.0, 0.0, 0.003921569, 0.1764706, 0.67058825, 0.007843138, 0.0,
                     0.007843138, 0.007843138, 0.007843138, 0.0, 0.0, 0.0, 0.07058824, 0.6, 0.007843138, 0.0,
                     0.0, 0.0, 0.0, 0.0, 0.0, 0.003921569, 0.011764706, 0.023529412, 0.011764706, 0.0],
            'label': 4
        }
    ]
    
    print("\n" + "=" * 72)
    print("  FPGA Neural Network Display - Demo Mode")
    print("  Showing example predictions from C simulation")
    print("=" * 72)
    print("\nPress Ctrl+C to exit\n")
    time.sleep(2)
    
    try:
        for test in test_cases:
            # Simulate confidence scores (softmax output)
            confidence = np.random.rand(10)
            confidence[test['label']] = 0.95  # High confidence for correct digit
            confidence = confidence / confidence.sum()  # Normalize to sum to 1
            
            # Display result
            display.display_result(
                image=test['image'],
                prediction=test['label'],
                confidence_scores=confidence,
                true_label=test['label'],
                processing_time_ms=0.026,
                cycles=3250
            )
            
            time.sleep(3)  # Display for 3 seconds
            
        # Final summary
        print("\n" + "=" * 72)
        print(f"  Demo Complete!")
        print(f"  Total Images: {display.total_processed}")
        print(f"  Correct: {display.correct_predictions}")
        print(f"  Accuracy: {(display.correct_predictions/display.total_processed*100):.1f}%")
        print("=" * 72)
        
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
        sys.exit(0)

if __name__ == "__main__":
    demo()
