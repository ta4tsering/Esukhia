import re


def get_line(final_content):
    with_sn = final_content.read_text(encoding="utf-8")
    pg_text = ""
    result = []
    lines = re.split(f"(\n)", with_sn)
    for i, line in enumerate(lines[1:]):
        if i % 2 == 0:
            pg_text += line
        elif i % 2 != 0:
            pg_text += line
            result.append(pg_text)
            pg_text = ""
    return get_page_and_border_durchen(result)

def get_page_and_border_durchen(final_content):
    line_text = ""
    page = 0
    final_output = []

    for n, line in enumerate(final_content):
        if re.match(r"\n\d+\W<r?([༠-༩]+?)>", line):
            tib_num = re.search(r"\n\d+\W<r?([༠-༩]+?)>", line)
            line_text += (tib_num.group(0))
            final_output.append(line_text)
            line_text = ""
        if re.search(r"\<p\d+\W\d+\>", line):
                tib_num = re.search(r"\<p\d+\W\d+\>", line)
                line_text += (tib_num.group(0))
                final_output.append(line_text)
                line_text = ""
                page += 1
        return get_essential(final_output, page)


def get_essential(final, page):
    line_text = ""
    final_output = []
    durchen = 0
    pages = re.split(r"(<p\d+\W\d+\>)", final)
    for 
    # if re.search(r"\n?(\d+)?(\W)\<r?([༠-༩]+?)\>", con):
    #     num = re.search(r"\n?(\d+)?(\W)\<r?([༠-༩]+?)\>", con)
    #     line_text += con
    #     line_text = get_num(line_text)
    #     final_output.append(line_text)
    #     line_text = "" 
    # if re.search(r"<p\d+\W\d+\>", con):
    #     num = re.sub("\<", "", con)
    #     num = re.sub("\>", "", num)
    #     num = re.sub("p", "", num)
    #     final_output.append(num)
        
    return final_output     

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
        file_ = Path("./output/output67.txt")
        final_file = Path("./final/output67.txt")
        final = str(get_line(file_))
        final_file.write_text(final, encoding="utf-8")