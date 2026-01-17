import numpy as np
import cv2
import os

# Script to generate C++ test image arrays from MNIST dataset
# Output can be copied into matmul_tb.cpp for hardware testing

def generate_test_images(num_images=10):
    """Generate test images in C++ array format"""
    
    dims = (10, 10)  # 10x10 images
    dataset_dir = '/Users/siwartaouih/FPGA_AI/MNIST_Dataset_JPG'
    
    print("Generating C++ test image arrays from MNIST dataset...\n")
    print("=" * 70)
    
    # Load test images for each digit (0-9)
    for digit in range(10):
        read_folder = dataset_dir + '/MNIST_JPG_testing/' + str(digit) + '/'
        
        # Get first image of this digit
        image_files = os.listdir(read_folder)
        if not image_files:
            print(f"No images found for digit {digit}")
            continue
            
        # Read and process the first image
        img_path = os.path.join(read_folder, image_files[0])
        img = cv2.imread(img_path, 0)  # grayscale
        img = cv2.resize(img, dims, interpolation=cv2.INTER_AREA)
        img = img / 255.0  # normalize to 0-1
        
        # Flatten to 1D array (100 pixels)
        img_flat = img.flatten()
        
        # Generate C++ array format
        print(f"\n// Test image for digit: {digit}")
        print(f"// Source: {image_files[0]}")
        print(f"float input_img_{digit}[n_inputs] = {{", end="")
        
        # Print 10 values per line for readability
        for i in range(len(img_flat)):
            if i % 10 == 0:
                print("\n\t\t", end="")
            print(f"{img_flat[i]}", end="")
            if i < len(img_flat) - 1:
                print(", ", end="")
        
        print("}}; // {}\n".format(digit))
        
        # Generate the inference call
        print(f"int pred_{digit} = nn_inference(input_img_{digit});")
        print(f'std::cout << "NN Prediction for digit {digit}: " << pred_{digit} << std::endl;')
        print("=" * 70)

    print("\n\nCopy the arrays above into matmul_tb.cpp to test more digits!")
    print("Each array represents a real MNIST handwritten digit image.")

if __name__ == "__main__":
    generate_test_images()
