import numpy as np

if __name__ == '__main__':
    f = open('chat.txt', "r", encoding="utf-8")
    text = f.read()
    list_text = text.split("\n")
    list_text_ = []
    for el in list_text:
        if el != "" and "\u200b" not in el:
            list_text_.append(el)
    unique, counts = np.unique(list_text_, return_counts=True)
    result = np.column_stack((unique, counts))
    print(result)
