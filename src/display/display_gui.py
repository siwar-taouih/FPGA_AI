#!/usr/bin/env python3
"""
MNIST Digit Recognition - FPGA Display GUI
Displays neural network predictions with visual feedback on monitor
Can run on Zynq ARM processor or development PC
"""

import tkinter as tk
from tkinter import ttk
import numpy as np
import time

class DigitRecognitionDisplay:
    def __init__(self, root):
        self.root = root
        self.root.title("MNIST Digit Recognition - FPGA Accelerator")
        self.root.geometry("800x600")
        self.root.configure(bg='#1E3A8A')
        
        # Create main container
        self.create_header()
        self.create_main_display()
        self.create_confidence_bars()
        self.create_status_bar()
        
        # Statistics
        self.total_processed = 0
        self.correct_predictions = 0
        
    def create_header(self):
        """Create header bar"""
        header = tk.Frame(self.root, bg='#1E3A8A', height=60)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        title = tk.Label(
            header,
            text="MNIST Digit Recognition - FPGA Hardware Accelerator",
            font=('Arial', 20, 'bold'),
            bg='#1E3A8A',
            fg='white'
        )
        title.pack(pady=15)
        
    def create_main_display(self):
        """Create main display area with image and prediction"""
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left side - Input image
        left_frame = tk.Frame(main_frame, bg='white')
        left_frame.pack(side=tk.LEFT, padx=20, pady=20)
        
        tk.Label(
            left_frame,
            text="Input Image",
            font=('Arial', 14, 'bold'),
            bg='white'
        ).pack()
        
        # Canvas for displaying the 10x10 image (scaled up)
        self.image_canvas = tk.Canvas(
            left_frame,
            width=200,
            height=200,
            bg='black',
            highlightthickness=2,
            highlightbackground='#D1D5DB'
        )
        self.image_canvas.pack(pady=10)
        
        # Right side - Prediction results
        right_frame = tk.Frame(main_frame, bg='#F3F4F6', relief=tk.RIDGE, borderwidth=2)
        right_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        tk.Label(
            right_frame,
            text="Prediction Result",
            font=('Arial', 14, 'bold'),
            bg='#F3F4F6'
        ).pack(pady=10)
        
        # Predicted digit (large display)
        self.pred_label = tk.Label(
            right_frame,
            text="?",
            font=('Arial', 72, 'bold'),
            bg='#F3F4F6',
            fg='#111827'
        )
        self.pred_label.pack(pady=20)
        
        # Confidence
        self.conf_label = tk.Label(
            right_frame,
            text="Confidence: ---%",
            font=('Arial', 16),
            bg='#F3F4F6',
            fg='#6B7280'
        )
        self.conf_label.pack(pady=5)
        
        # Processing time
        self.time_label = tk.Label(
            right_frame,
            text="Processing Time:\n--- ms (--- cycles)",
            font=('Arial', 12),
            bg='#F3F4F6',
            fg='#6B7280',
            justify=tk.CENTER
        )
        self.time_label.pack(pady=10)
        
    def create_confidence_bars(self):
        """Create confidence distribution bar chart"""
        bars_frame = tk.Frame(self.root, bg='white', relief=tk.RIDGE, borderwidth=2)
        bars_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(
            bars_frame,
            text="Confidence Distribution",
            font=('Arial', 12, 'bold'),
            bg='white'
        ).pack(pady=5)
        
        # Create bars for each digit 0-9
        self.confidence_bars = []
        self.confidence_labels = []
        
        for digit in range(10):
            bar_container = tk.Frame(bars_frame, bg='white')
            bar_container.pack(fill=tk.X, padx=20, pady=2)
            
            # Digit label
            tk.Label(
                bar_container,
                text=f"{digit}:",
                font=('Arial', 10),
                bg='white',
                width=2
            ).pack(side=tk.LEFT)
            
            # Progress bar
            bar = ttk.Progressbar(
                bar_container,
                length=400,
                mode='determinate',
                maximum=100
            )
            bar.pack(side=tk.LEFT, padx=5)
            self.confidence_bars.append(bar)
            
            # Percentage label
            label = tk.Label(
                bar_container,
                text="0%",
                font=('Arial', 10),
                bg='white',
                width=6
            )
            label.pack(side=tk.LEFT)
            self.confidence_labels.append(label)
            
    def create_status_bar(self):
        """Create bottom status bar"""
        status_frame = tk.Frame(self.root, bg='#374151', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(
            status_frame,
            text="Status: Ready  |  Images Processed: 0  |  Accuracy: ---%",
            font=('Arial', 10),
            bg='#374151',
            fg='white'
        )
        self.status_label.pack(pady=5)
        
    def draw_image(self, pixels):
        """Draw 10x10 pixel array on canvas (scaled 20x)"""
        self.image_canvas.delete("all")
        
        # Reshape to 10x10 if needed
        if len(pixels) == 100:
            pixels = np.array(pixels).reshape(10, 10)
        
        # Draw each pixel as a 20x20 square
        for i in range(10):
            for j in range(10):
                # Convert pixel value (0-1) to grayscale
                gray_value = int(pixels[i][j] * 255)
                color = f'#{gray_value:02x}{gray_value:02x}{gray_value:02x}'
                
                x1 = j * 20
                y1 = i * 20
                x2 = x1 + 20
                y2 = y1 + 20
                
                self.image_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=''
                )
    
    def update_prediction(self, prediction, confidence_scores, processing_time_ms, cycles):
        """Update display with new prediction results"""
        # Update predicted digit
        self.pred_label.config(text=str(prediction))
        
        # Get confidence for predicted digit
        max_confidence = confidence_scores[prediction] * 100
        
        # Color code based on confidence
        if max_confidence > 90:
            color = '#10B981'  # Green
        elif max_confidence > 70:
            color = '#F59E0B'  # Yellow
        else:
            color = '#EF4444'  # Red
        
        self.pred_label.config(fg=color)
        self.conf_label.config(text=f"Confidence: {max_confidence:.1f}%")
        
        # Update processing time
        self.time_label.config(
            text=f"Processing Time:\n{processing_time_ms:.3f} ms ({cycles:,} cycles)"
        )
        
        # Update confidence bars
        for digit in range(10):
            conf_pct = confidence_scores[digit] * 100
            self.confidence_bars[digit]['value'] = conf_pct
            self.confidence_labels[digit].config(text=f"{conf_pct:.1f}%")
            
            # Highlight predicted digit bar
            if digit == prediction:
                self.confidence_labels[digit].config(fg='#10B981', font=('Arial', 10, 'bold'))
            else:
                self.confidence_labels[digit].config(fg='#6B7280', font=('Arial', 10))
        
        # Update statistics
        self.total_processed += 1
        
    def update_status(self, status_text, correct=None):
        """Update status bar"""
        if correct is not None:
            if correct:
                self.correct_predictions += 1
        
        accuracy = (self.correct_predictions / self.total_processed * 100) if self.total_processed > 0 else 0
        
        self.status_label.config(
            text=f"Status: {status_text}  |  Images Processed: {self.total_processed}  |  Accuracy: {accuracy:.1f}%"
        )

def demo_mode(display):
    """Demo mode - simulate predictions for testing"""
    # Example test data (from your testbench)
    test_images = [
        # Test image 1 (digit 1)
        [0.0, 0.0, 0.0, 0.0, 0.003921569, 0.003921569, 0.015686275, 0.019607844, 0.003921569, 0.0,
         0.0, 0.0, 0.0, 0.003921569, 0.0, 0.02745098, 0.13725491, 0.015686275, 0.007843138, 0.0,
         0.0, 0.0, 0.0, 0.003921569, 0.003921569, 0.34117648, 0.6, 0.015686275, 0.015686275, 0.0,
         0.0, 0.0, 0.0, 0.011764706, 0.007843138, 0.60784316, 0.54509807, 0.015686275, 0.007843138, 0.0,
         0.0, 0.0, 0.0, 0.007843138, 0.13725491, 0.9490196, 0.19607843, 0.019607844, 0.003921569, 0.0,
         0.0, 0.0, 0.0, 0.007843138, 0.4627451, 0.627451, 0.019607844, 0.007843138, 0.007843138, 0.0,
         0.0, 0.0, 0.0, 0.011764706, 0.68235296, 0.2901961, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.02745098, 0.7529412, 0.0627451, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.02745098, 0.6901961, 0.11372549, 0.0, 0.0, 0.0, 0.0,
         0.0, 0.0, 0.0, 0.007843138, 0.015686275, 0.007843138, 0.0, 0.0, 0.0, 0.0],
    ]
    
    test_labels = [1]
    
    # Simulate predictions
    for idx, (image, true_label) in enumerate(zip(test_images, test_labels)):
        display.update_status("Processing...")
        display.draw_image(image)
        display.root.update()
        
        time.sleep(0.5)  # Simulate processing time
        
        # Simulate confidence scores (softmax output)
        confidence = np.random.rand(10)
        confidence[true_label] = 0.95  # High confidence for correct digit
        confidence = confidence / confidence.sum()  # Normalize
        
        # Simulate processing metrics
        processing_time = 0.026  # ms
        cycles = 3250
        
        display.update_prediction(true_label, confidence, processing_time, cycles)
        display.update_status("Ready", correct=True)
        display.root.update()
        
        time.sleep(2)  # Display result for 2 seconds

def main():
    """Main entry point"""
    root = tk.Tk()
    display = DigitRecognitionDisplay(root)
    
    # Run demo mode after a short delay
    root.after(1000, lambda: demo_mode(display))
    
    root.mainloop()

if __name__ == "__main__":
    main()
