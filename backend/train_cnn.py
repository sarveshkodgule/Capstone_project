import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F

# 1. Define the exact same CNN architecture used in the backend
class FundusCNN(nn.Module):
    def __init__(self, num_classes=5):
        super(FundusCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 28 * 28, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x))) # 224 -> 112
        x = self.pool(F.relu(self.conv2(x))) # 112 -> 56
        x = self.pool(F.relu(self.conv3(x))) # 56 -> 28
        x = x.view(-1, 64 * 28 * 28)
        x = self.dropout(F.relu(self.fc1(x)))
        x = self.fc2(x)
        return x

# 2. Custom Dataset Loader for your Fundus Images
class MyopiaDataset(Dataset):
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        image = Image.open(img_path).convert("RGB")
        label = self.labels[idx]
        
        if self.transform:
            image = self.transform(image)
            
        return image, label

# 3. Model Training Loop
def train_model(train_loader, val_loader, num_epochs=10, learning_rate=0.001):
    # Select Device (NVIDIA GPU if available)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on device: {device}")
    
    # Initialize Model, Loss Function, and Optimizer
    model = FundusCNN(num_classes=5).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
            
        epoch_loss = running_loss / len(train_loader.dataset)
        epoch_acc = (correct / total) * 100
        
        print(f"Epoch [{epoch+1}/{num_epochs}] - Loss: {epoch_loss:.4f} - Accuracy: {epoch_acc:.2f}%")
        
        # (Optional) Validate model performance
        if val_loader:
            model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            with torch.no_grad():
                for images, labels in val_loader:
                    images, labels = images.to(device), labels.to(device)
                    outputs = model(images)
                    loss = criterion(outputs, labels)
                    val_loss += loss.item() * images.size(0)
                    _, predicted = outputs.max(1)
                    val_total += labels.size(0)
                    val_correct += predicted.eq(labels).sum().item()
            val_loss /= len(val_loader.dataset)
            val_acc = (val_correct / val_total) * 100
            print(f"Val Loss: {val_loss:.4f} - Val Accuracy: {val_acc:.2f}%")
            
    # Save the trained model parameters to models/fundus_cnn.pth
    os.makedirs("models", exist_ok=True)
    torch.save(model.state_dict(), "models/fundus_cnn.pth")
    print("Model successfully trained and saved as 'models/fundus_cnn.pth'!")

if __name__ == "__main__":
    print("=== PyTorch CNN Training Script ===")
    print("To train on a real dataset, populate the `image_paths` and `labels` lists with your dataset.")
    print("Running a mock training dry run to test CUDA performance...")
    
    # Preprocessing transforms (Resize, Normalize)
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create random synthetic data representing 100 images
    import numpy as np
    import tempfile
    
    # Setup temporary images to test the actual dataset loader pipeline
    with tempfile.TemporaryDirectory() as temp_dir:
        mock_paths = []
        mock_labels = []
        for i in range(50):
            # Create a random RGB image and save it
            arr = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
            img = Image.fromarray(arr)
            path = os.path.join(temp_dir, f"mock_img_{i}.jpg")
            img.save(path)
            mock_paths.append(path)
            # Random label 0-4
            mock_labels.append(np.random.randint(0, 5))
            
        # Create DataLoaders
        dataset = MyopiaDataset(mock_paths, mock_labels, transform=transform)
        train_loader = DataLoader(dataset, batch_size=8, shuffle=True)
        
        # Run 2 epochs to verify it works on GPU
        train_model(train_loader, val_loader=None, num_epochs=2, learning_rate=0.001)
