from pathlib import Path
import re

def normalise_dash(text):
    dashs = [
        "-",
        "֊",
        "־",
        "᐀",
        "᠆",
        "﹘",
        "゠",
        "〰",
        "〜",
        "⹀",
        "⸻",
        "⸺",
        "⸚",
        "⸗",
        "―",
        "—",
        "–",
        "‒",
        "‐",
        "‑",
        "－",
        "﹣",
        "=",
        "_",
    ]
    for dash in dashs:
        text = text.replace(dash, "-")
    text = re.sub("-+", "-", text)
    return text

def fix_abnormal_pagination(text, vol_num):
    if str(vol_num)[0] == "1":
        text = re.sub("\n7", "\n1", text)
    text = re.sub(f"{vol_num}ཝ་", f"{vol_num}-", text)
    text = re.sub(f"{vol_num}-.*?\n*([0-9]+)", rf"{vol_num}-\1", text)
    ab_pg_without_vol_nums = re.finditer(r"\n-([0-9]+)", text)
    for ab_pg_without_vol_num in ab_pg_without_vol_nums:
        pg_no = ab_pg_without_vol_num.group(1)
        text = re.sub(ab_pg_without_vol_num[0], f"\n{vol_num}-{pg_no}", text)
    ab_pgs = re.finditer(f"{vol_num}\n([0-9]+)\n\n", text)
    for ab_pg in ab_pgs:
        pg_no = ab_pg.group(1)
        text = re.sub(ab_pg[0], f"{vol_num}-{pg_no}\n\n", text)
    return text

def bind_pages(pages):
    return "".join(pages)

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(f"(\[\d+[a-b]\])", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result

def namsel_ab_page_fix(text, vol_num):
    ab_pgs = re.finditer(f"\n+({vol_num}\u0020*-*—*_*–*=*[0-9]+)", text)
    for ab_pg in ab_pgs:
        pg_ann = ab_pg.group(1)
        text = re.sub(ab_pg[0], f"\n{pg_ann}", text)
    return text

def normalise_pagination(page, vol_num):
    pg_ann = re.search(f"{vol_num}[\s\n]?(-|ཝ་|་|།|།དེ|\n)?[\s\n]?(([0-9][\s\n]?)+)", page)
    print(pg_ann[0])
    pg_no_part = pg_ann.group(2)
    pg_no = re.sub("\s|\n", "", pg_no_part)
    page = re.sub(pg_ann[0], f"{vol_num}-{pg_no}\n\n", page)
    return page

def find_next(prev_pg, cur_pg):
    prev_lines = prev_pg.splitlines()
    cur_pg_lines = cur_pg.splitlines()
    prev_pg_pat = re.search("\[(\d+)([a-z]{1})\]", prev_lines[0])
    prev_pg_num = int(prev_pg_pat.group(1))
    prev_pg_face = prev_pg_pat.group(2)
    cur_pg_pat = re.search("\[(\d+)([a-z]{1})\]", cur_pg_lines[0])
    cur_pg_num = int(cur_pg_pat.group(1))
    cur_pg_face = cur_pg_pat.group(2)
    if prev_pg_num == cur_pg_num - 1:
        if prev_pg_face == "b" and cur_pg_face == "a":
            return []
        elif prev_pg_face == "a" and cur_pg_face == "a":
            return [f"[{prev_pg_num}b]\n\n\n\n"]
        elif prev_pg_face == "b" and cur_pg_face == "b":
            return [f"[{cur_pg_num}a]\n\n\n\n"]
        elif prev_pg_face == "a" and cur_pg_face == "b":
            return [f"[{prev_pg_num}b]\n\n\n\n", f"[{cur_pg_num}a]\n\n\n\n"]
    elif prev_pg_num < cur_pg_num:
        next_pages = []
        for pg_num in range(prev_pg_num, cur_pg_num + 1):
            next_pages.append(f"[{pg_num}a]\n\n\n\n")
            next_pages.append(f"[{pg_num}b]\n\n\n\n")
        if prev_pg_face == "a" and cur_pg_face == "a":
            return next_pages[1:-2]
        elif prev_pg_face == "a" and cur_pg_face == "b":
            return next_pages[1:-1]
        elif prev_pg_face == "b" and cur_pg_face == "a":
            return next_pages[2:-2]
        elif prev_pg_face == "b" and cur_pg_face == "b":
            return next_pages[2:-1]
    else:
        return []

def reconstruct_pages(pages, vol_num):
    result = []
    for pg_walker, pg in enumerate(pages):
        pg = pg.replace("O", "0")
        cur_pg_lines = pg.splitlines()
        cur_pg_body = "\n".join(cur_pg_lines[1:])
        if re.search(f"{vol_num}[\s\n]?(-|ཝ་|་|།|།དེ|\n)?[\s\n]?([0-9][\s\n]?)+", cur_pg_body):
            normalised_pg_body = normalise_pagination(cur_pg_body, vol_num)
            normalised_pg_body = normalised_pg_body.replace('\n','')
            pg = cur_pg_lines[0] + "\n" + normalised_pg_body + "\n\n"
        if pg_walker == 0:
            if re.search("1a", cur_pg_lines[0]):
                result.append(pg)
            else:
                result.append("[1a]\n\n\n\n")
                next_pgs = find_next(result[-1], pg)
                if next_pgs:
                    for next_pg in next_pgs:
                        result.append(next_pg)
                result.append(pg)

        else:
            prev_pg = result[-1]
            next_pgs = find_next(prev_pg, pg)
            if re.search(r'\[\d+[a-b]\]\s?\n\n\n', pg):
                pg = pg.replace('\n\n\n\n', '\n\n\n')
            else:
                pg = pg.replace('\n\n\n\n', '\n\n')
            if next_pgs:
                for next_pg in next_pgs:
                    result.append(next_pg)
                result.append(pg)
            else:
                result.append(pg)
    return result

if __name__ == "__main__":
    poti = Path(f"../../v112.txt")
    # potis.sort()
    # print(len(potis))
    # for vol_num, poti in enumerate(potis, 1):
    vol_num = 112
    vol_text = poti.read_text(encoding="utf-8")
    vol_text = vol_text.replace("O", "0")
    vol_text = normalise_dash(vol_text)
    vol_text = fix_abnormal_pagination(vol_text, vol_num)
    vol_text = namsel_ab_page_fix(vol_text, vol_num)
    pages = get_pages(vol_text)
    new_pages = reconstruct_pages(pages, vol_num)
    new_vol_text = bind_pages(new_pages)
    Path(f"../../reconstructed").write_text(new_vol_text, encoding="utf-8")
    print(f"reconstruction completed...")
    


