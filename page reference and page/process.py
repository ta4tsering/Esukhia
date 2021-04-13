import re 
import yaml
from pathlib import Path



def parse_page_ann(page_ann):
    page_ann_parts = page_ann.split('-')
    vol = page_ann_parts[0]
    page_num = page_ann_parts[1]
    return (vol, page_num)


def get_num(line):
    tib_num = re.sub(r"\W", "", line)
    tib_num = re.sub(r"(\d+?)r", "", tib_num)
    table = tib_num.maketrans("༡༢༣༤༥༦༧༨༩༠", "1234567890", "<r>")
    eng_num = int(tib_num.translate(table))
    return eng_num


def get_pages(text_content):
    pages = re.split(r"(<p\d+\W\d+\>)", text_content)
    pg_text = ""
    pages_dict = {}
    for i, line in enumerate(pages):
        if i % 2 == 0:
            pg_text += line
        elif i % 2 != 0:
            num = re.sub("\<", "", line)
            num = re.sub("\>", "", num)
            num = re.sub("p", "", num)
            pages_dict[num] = pg_text
            pg_text = ""
    return pages_dict


def get_page_refs(page_content):
    refs = re.findall(r"<r.+?>", page_content)
    if refs:
        if len(refs) > 2:
            refs[0] = get_num(refs[0])
            refs[-1] = get_num(refs[-1])
            return (refs[0], refs[-1])
        else:
            refs[0] = get_num(refs[0])
            return (refs[0], '')
    else:
        return ('', '')
    

if __name__ == "__main__":
    text_content = Path(f"./output/D1118.txt").read_text(encoding="utf-8")
    page_dict = get_pages(text_content)
    result = []
    cur_info = {}
    for page_ann, page_content in page_dict.items():
        cur_page_info = {}
        vol, page_num = parse_page_ann(page_ann)
        start, end = get_page_refs(page_content)
        cur_info= {
                    'start': start,
                    'end': end,
                    'page': page_num,
                    'vol': vol
                }
        result.append(cur_info)
        cur_info = {}
    final = yaml.safe_dump(result, sort_keys = False)
    Path(f"./final/output.yaml").write_text(final, encoding="utf-8")


