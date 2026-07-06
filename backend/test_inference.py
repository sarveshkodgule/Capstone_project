import os
import sys

# Add the current directory to python path so it can import services
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import predict_image

def test_single_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File not found at '{image_path}'")
        return
        
    print(f"Reading image: {image_path}...")
    with open(image_path, "rb") as f:
        image_bytes = f.read()
        
    print("Running GPU-accelerated CNN inference...")
    result = predict_image(image_bytes)
    
    print("\n" + "="*40)
    print("           CNN INFERENCE RESULT         ")
    print("="*40)
    print(f"Target Image: {os.path.basename(image_path)}")
    print(f"Prediction:   {result['prediction']}")
    print(f"Confidence:   {result['confidence'] * 100:.2f}%")
    print(f"Findings:     {', '.join(result['morphology_findings'])}")
    print("="*40)

if __name__ == "__main__":
    # You can change this path to test any other image!
    default_test_image = r"c:\Users\Sarvesh Kodgule\Desktop\Studdyyy\capstone\PALM\PALM\Training\Images\H0001.jpg"
    
    print("=== CNN Fundus Image Testing Tool ===")
    print("You can run: python test_inference.py <path_to_image> to test a specific image.")
    
    # If a path was passed via command line, use it
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
    else:
        test_path = default_test_image
        print(f"No image path specified. Using default: {default_test_image}")
        
    test_single_image(test_path)
