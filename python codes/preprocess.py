# coding='utf-8'
from pathlib import Path
import re
import linecache

def derge_page_increment(p_num):
    sides = {"a": "b", "b": "a"}
    page, side = int(p_num[1:-2]), p_num[-2:-1]

    # increment
    if side == "b":
        page += 1
    side = sides[side]

    return f"[{page}{side}]"

def preprocess_namsel_notes(text):
    """
    this cleans up all note markers
    :param text: plain text
    :return: cleaned text
    """

    patterns = [
        # normalize single zeros '༥༥་' --> '༥༥༠'
        ["([༠-༩])[་༷]", "\g<1>༠"],
        # normalize double zeros '༧༷་' --> '༧༠༠'
        ["༠[་༷]", "༠༠"],
        ["༠[་༷]", "༠༠"],
        # normalize punct
        ["\r", "\n"],
        ["༑", "།"],
        ["།།", "། །"],
        ["།་", "། "],
        ["\s+", " "],
        ["།\s།\s*\n", "།\n"],
        ["།\s།\s«", "། «"],
        ["༌", "་"],  # normalize NB tsek
        ["ག\s*།", "ག"],
        ["་\s*", "་"],
        ["་\s*", "་"],
        ["་\s*\n", "་"],
        ["་+", "་"],
        # normalize and tag page numbers '73ཝ་768' --> ' <p73-768> '
        ["([0-9]+?)[ཝ—-]་?([0-9]+)", " <p\g<1>-\g<2>> "],
        # tag page references '༡༤༥ ①' --> <p༡༤༥> ①'
        [" ?([༠-༩]+?)(\s\(?[①-⓪༠-༩ ཿ༅]\)?)", " \n<r\g<1>>\g<2>"],  # basic page ref
        # normalize edition marks «<edition>»
        ["〈〈?", "«"],
        ["〉〉?", "»"],
        ["《", "«"],
        ["》", "»"],
        ["([ཀགཤ།]) །«", "\g<1> «"],
        ["([ཀགཤ།])་?«", "\g<1> «"],
        ["»\s+", "»"],
        ["«\s+«", "«"],
        ["»+", "»"],
        ["[=—]", "-"],
        ["\s+-", "-"],
        ["\s+\+", "+"],
        ["»\s+«", "»«"],
        
        
        
       
    ]

    for p in patterns:
        text = re.sub(p[0], p[1], text)
    
    # text = translate_ref(text)

    return text


def save(content, filename, tag):
    # saves file
    new_file = filename.parent / (filename.stem + tag + filename.suffix)
    new_file.write_text(content, encoding="utf-8")


def add_sn(content):
    marker = "<r"
    list = re.split(marker, content)
    new = ""

    for i, e in enumerate(list, 2):
        new += f"{i}-{marker}{e}"

    return new

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
    count = 0
    final_output = []

    for n, line in enumerate(final_content):
        if count == 0 :
            if re.match(r"\n\d+\W<r?([༠-༩]+?)>", line):
                tib_num = re.search(r"\n\d+\W<r?([༠-༩]+?)>", line)
                line_text += (tib_num.group(0))
                final_output.append(line_text)
                line_text = ""
                count +=1
        elif n == (len(final_content)-1):
            if re.search(r"\n\d+\W<r?([༠-༩]+?)>", line):
                tib_num = re.search(r"\n\d+\W<r?([༠-༩]+?)>", line)
                line_text += (tib_num.group(0))
                final_output.append(line_text)
                line_text = ""
                count += 1
            if re.search(r"\<p\d+\W\d+\>", line):
                tib_num = re.search(r"\<p\d+\W\d+\>", line)
                line_text += (tib_num.group(0))
                final_output.append(line_text)
                line_text = ""
    return final_output




if __name__ == "__main__":
    namsel_path = Path("./input/67N-footnotes.txt")
    namsel_content = namsel_path.read_text(encoding="utf-8") 
    namselPrep = preprocess_namsel_notes(namsel_content)
    with_sn = add_sn(namselPrep)
    new_file = Path("./output/output67.txt")
    new_file.write_text(with_sn, encoding="utf-8") 
    final = str(get_line(new_file))
    final_file = Path("./final/output67.txt")
    final_file.write_text(final, encoding="utf-8")