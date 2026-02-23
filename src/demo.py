from retriever import CLIPRetriever


def main():
    # 创建检索器实例（会自动加载特征）
    retriever = CLIPRetriever()

    while True:
        print("\n" + "=" * 40)
        print("图文检索系统 (CLIP)")
        print("1. 以文搜图")
        print("2. 以图搜文")
        print("3. 退出")
        choice = input("请选择 (1/2/3): ").strip()

        if choice == "1":
            query = input("请输入查询文本: ")
            results = retriever.text_to_image(query, top_k=5)
            print("\n最匹配的图片：")
            for path, score in results:
                print(f"  {path} (相似度: {score:.4f})")
        elif choice == "2":
            img_path = input("请输入图片路径: ")
            # 候选文本列表（你可以根据自己的图片内容调整）
            candidates = [
                "a cat",
                "a dog",
                "a car",
                "a beautiful landscape",
                "a city view",
                "food",
                "a flower",
                "a mountain",
                "a beach",
                "a forest"
            ]
            results = retriever.image_to_text(img_path, candidates, top_k=3)
            print("\n最匹配的文本：")
            for text, score in results:
                print(f"  {text} (相似度: {score:.4f})")
        elif choice == "3":
            print("再见！")
            break
        else:
            print("无效输入，请重新选择。")


if __name__ == "__main__":
    main()