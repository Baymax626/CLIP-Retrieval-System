import os

import clip
import numpy as np
import torch
from PIL import Image

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
print(f"正在使用{device}")

model , preprocess = clip.load("ViT-B/32", device=device)

image_dir = "../data/images"
output_dir = "../features"
os.makedirs(output_dir, exist_ok=True)

image_paths = []
valid_extensions = (".jpg", ".jpeg", ".png" , "bmp")
for file in os.listdir(image_dir):
    if file.lower().endswith(valid_extensions):
        image_paths.append(os.path.join(image_dir, file))

print(f"找到 {len(image_paths)} 张图片，开始提取特征...")

features = []       # 存储所有图片的特征
valid_paths = []    # 存储成功提取特征的图片路径

for img_path in image_paths:
    try:
        image = preprocess(Image.open(img_path).convert("RGB")).unsqueeze(0).to(device)

        with torch.no_grad():
            feature = model.encode_image(image)
            # 归一化（使特征长度为1，便于计算余弦相似度）
            feature /= feature.norm(dim=-1, keepdim=True)

        features.append(feature.cpu().numpy().squeeze())
        valid_paths.append(img_path)
    except Exception as e:
        print(f"跳过损坏图片 {img_path}: {e}")

features = np.stack(features)

np.save(os.path.join(output_dir, "image_features.npy"), features)

with open(os.path.join(output_dir, "image_paths.txt"), "w") as f:
    for path in valid_paths:
        f.write(path + "\n")

print(f"特征提取完成，共 {len(features)} 张有效图片，已保存至 {output_dir}")