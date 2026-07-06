import pickle

# Load model
with open("detection_model.pkl", "rb") as f:
    model = pickle.load(f)

# Check model type
print("Model type:", type(model))

# Try a sample prediction (you may need to adjust input)
try:
    result = model.predict([[1, 2, 3, 4]])
    print("Prediction:", result)
except Exception as e:
    print("Error during prediction:", e)