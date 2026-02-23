import clip
import numpy as np
import torch
from PIL import Image


class CLIPRetriever:
    def __init__(self , features_dir = "features" , model_name = "VIT-B/32"):
        """
        初始化检索器
        :param feature_dir: 存放特征的文件夹
        :param model_name: CLIP 模型名称
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model , self.preprocess = clip.load(model_name , device=self.device)

        self.image_features = np.load(f"{features_dir}/image_features.npy")
        with open(f"{features_dir}/image_paths.txt", "r") as f:
            self.image_paths = [line.strip() for line in f.readlines()]
        print(f"已加载 {len(self.image_paths)} 张图像的特征。")

    def encode_text(self , texts):
        """
        将文本列表编码为归一化的特征向量
        """
        text_tokens = clip.tokenize(texts).to(self.device)
        with torch.no_grad():
            text_features = self.model.encode_text(text_tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)
        return text_features.cpu().numpy()

    def encode_image(self, image_path):
        """
       将单张图片编码为归一化的特征向量
       """
        image = self.preprocess(Image.open(image_path)).unsqueeze(0).to(self.device)
        with torch.no_grad():
            image_features = self.model.encode_image(image)
            image_features /= image_features.norm(dim=-1, keepdim=True)
        return image_features.cpu().numpy()


    def text_to_image(self , query_text , top_k = 5):
        """
       以文搜图：返回最相似的 top_k 张图片路径和相似度
       """
        text_feat = self.encode_text([query_text])
        similarities = (self.image_features @ text_feat.T).squeeze()  # (N,)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(self.image_paths[i], float(similarities[i])) for i in top_indices]
        return results

    def image_to_text(self, query_image_path, candidate_texts, top_k=5):
        """
        以图搜文：输入图片路径和候选文本列表，返回最匹配的文本
        """
        image_feat = self.encode_image(query_image_path)  # (1, D)
        text_feats = self.encode_text(candidate_texts)    # (N, D)
        similarities = (image_feat @ text_feats.T).squeeze()  # (N,)
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [(candidate_texts[i], float(similarities[i])) for i in top_indices]
        return results