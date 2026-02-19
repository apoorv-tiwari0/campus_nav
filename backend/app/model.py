import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image


# Load pretrained MobileNetV3
model = models.mobilenet_v3_small(weights="DEFAULT")

# Remove classification head → keep feature extractor
model.classifier = torch.nn.Identity()

model.eval()


# Image preprocessing pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


def get_embedding(image: Image.Image):
    img = transform(image).unsqueeze(0)

    with torch.no_grad():
        embedding = model(img)

    return embedding.squeeze().numpy()
