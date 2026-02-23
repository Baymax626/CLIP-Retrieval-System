import os
import requests
from tqdm import tqdm

# 图片 URL 列表（Unsplash 精选，可自行增删）
image_urls = [
    "https://images.unsplash.com/photo-1504208434309-cb69f4fe52b0?w=400",  # 山脉
    "https://images.unsplash.com/photo-1519046904884-53103b34b206?w=400",  # 海滩
    "https://images.unsplash.com/photo-1517519014922-8fc06b814a0e?w=400",  # 森林
    "https://images.unsplash.com/photo-1500462918059-b1a0cb512f1d?w=400",  # 城市
    "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400",  # 猫
    "https://images.unsplash.com/photo-1543852786-1cf6624b9987?w=400",  # 狗
    "https://images.unsplash.com/photo-1568605117036-5fe5e7b0b8a4?w=400",  # 汽车
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=400",  # 科技
    "https://images.unsplash.com/photo-1469474968028-56623f02e42e?w=400",  # 自然
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400",  # 日出
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400",  # 森林
    "https://images.unsplash.com/photo-1472214103451-9374bd1c798e?w=400",  # 湖泊
    "https://images.unsplash.com/photo-1501854140801-50d01698950b?w=400",  # 海岸
    "https://images.unsplash.com/photo-1426604966848-d7adac402b0c?w=400",  # 山景
    "https://images.unsplash.com/photo-1471922694850-2b4639be7ebc?w=400",  # 海滩
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400",  # 晨光
    "https://images.unsplash.com/photo-1444464666168-49d633b86797?w=400",  # 鸟
    "https://images.unsplash.com/photo-1504006833117-8886a355efbf?w=400",  # 蝴蝶
    "https://images.unsplash.com/photo-1535083783855-76ae62b2914e?w=400",  # 花
    "https://images.unsplash.com/photo-1558980664-10dbd0f9b6b3?w=400",   # 美食
    "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",  # 披萨
    "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?w=400",  # 饼干
    "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400",  # 沙拉
    "https://images.unsplash.com/photo-1560807707-8cc77767d783?w=400",  # 咖啡
    "https://images.unsplash.com/photo-1517436073-3b1b1b1b1b1b?w=400",  # 建筑
]

# 创建保存目录
save_dir = "../data/images"
os.makedirs(save_dir, exist_ok=True)

# 下载图片
for i, url in enumerate(tqdm(image_urls, desc="下载图片")):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            # 从 URL 提取扩展名，若没有则用 .jpg
            ext = url.split('.')[-1].split('?')[0]
            if ext not in ['jpg', 'jpeg', 'png', 'bmp']:
                ext = 'jpg'
            filename = f"img_{i:03d}.{ext}"
            filepath = os.path.join(save_dir, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
        else:
            print(f"下载失败 {url}")
    except Exception as e:
        print(f"出错 {url}: {e}")

print(f"下载完成，图片保存在 {save_dir}")