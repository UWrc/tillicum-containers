import sys
import os
from PIL import Image
import torch
from pynvml import *
import timm
from torchvision import transforms

# Initialize NVML to monitor GPU memory usage
nvmlInit()
handle = nvmlDeviceGetHandleByIndex(0)   # GPU 0 (assumed single GPU per job)

image_dir = sys.argv[1]
output_file = sys.argv[2]

# Load pretrained model
model = timm.create_model("resnet50", pretrained=True)
model = model.eval().cuda()

# Report GPUs in use
num_gpus = torch.cuda.device_count()
print(f"GPUs visible to PyTorch: {num_gpus}")
for i in range(num_gpus):
    print(f"  GPU {i}: {torch.cuda.get_device_name(i)}")

print(f"Model is using GPU: {torch.cuda.current_device()} ({torch.cuda.get_device_name(torch.cuda.current_device())})")

# Load ImageNet class labels
# Ensure imagenet_classes.txt is in the working directory
with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f]

# Image preprocessing transform
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
])

with open(output_file, "w") as f:
    for img_name in os.listdir(image_dir):
        path = os.path.join(image_dir, img_name)

        try:
            img = Image.open(path).convert("RGB")
        except:
            continue

        x = transform(img).unsqueeze(0).cuda()

        with torch.no_grad():
            pred_idx = model(x).argmax(dim=1).item()

        pred_label = labels[pred_idx]
        f.write(f"{img_name}, {pred_label}\n")

        # GPU usage reporting
        torch.cuda.synchronize()  # ensure inference has completed
        mem_info = nvmlDeviceGetMemoryInfo(handle)
        used_mb = mem_info.used / 1024**2
        total_mb = mem_info.total / 1024**2
        print(f"{img_name}: GPU Memory Used {used_mb:.1f} MB / {total_mb:.1f} MB")

# Clean up NVML
nvmlShutdown()