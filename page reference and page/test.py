import re


def get_num(line):
    tib_num = re.sub(r"\W", "", line)
    #tib_num = re.sub(r"\d", "", tib_num)
    tib_num = re.sub(r"(\d+?)r", "", tib_num)
    print(tib_num)
    table = tib_num.maketrans("༡༢༣༤༥༦༧༨༩༠", "1234567890", "<r>")
    eng_num = int(tib_num.translate(table))
    print(eng_num)
    return eng_num


if __name__ == "__main__":
    man = ['\n3-<r༤༩>', '\n-<r༩༨>', '<p67-493>']
    line_text = ""
    final_output = []
    for i, con in enumerate(man):
        if i == 1:
            if re.search(r"\n?(\d+)?(\W)\<r?([༠-༩]+?)\>", con):
                print("yes")
                num = re.search(r"\n?(\d+)?(\W)\<r?([༠-༩]+?)\>", con)
                line_text += (num.group(0))
                print(line_text)
                line_text = get_num(line_text)
                final_output.append(line_text)
                line_text = ""    
        elif i == 2:
            if re.search(r"<p\d+\W\d+\>", con):
                num = re.sub("\<", "", con)
                num = re.sub("\>", "", num)
                num = re.sub("p", "", num)
                print(num)