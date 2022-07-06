import spacy


def main():
    # 入力のtxtファイル
    file_path = "output/txt/MIT 6.S191: Uncertainty in Deep Learning_sub.txt"
    class_name = file_path.split("/")[-1]

    with open(file_path) as f:
        text = f.read()

    text.strip(' ')

    print("Loading LANG Model...", end="")
    nlp = spacy.load('ja_ginza')

    print("\rAnalyzing text...", end="")
    doc = nlp(text)

    with open(f"output/caption/{class_name}", "a") as f:
        for sent in doc.sents:
            f.write(f"{str(sent)}\n")

    print("\rFinished!")


if __name__ == '__main__':
    main()
