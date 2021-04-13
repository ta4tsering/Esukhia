from pathlib import Path
from collections import defaultdict
import re
import yaml

result = {}
text_id = 1

def get_durchen_span(pages, poti_num, text_id):
    span = []
    cur_text = {}
    result = {}
    for page_num, page in enumerate(pages, 1):
        if re.search(r'\nབསྡུར་མཆན(་|།)(\s|\n)', page):
            span.append(page_num)
        if re.search(r'\nབསྡུར་འབྲས་རེའུ་མིག\n', page):
            span.append(page_num)
            cur_text[f'T{text_id}'] = {
                'start': span[0],
                'end': span[1],
                'vol': poti_num
            }
            result.update(cur_text)
            text_id += 1
            cur_text = {}
            span = []
    write_durchen_span(result,poti_num)
    
    return result


def write_durchen_span(durchen_span,poti_num):
    durchen_span_yml = yaml.safe_dump(durchen_span, sort_keys = False)
    Path(f'./test/google_80_yaml/tengyur_durchen_spans_v{poti_num:03}.yml').write_text(durchen_span_yml, encoding = 'utf-8')
    print(f'Tengyur durchen completed ..')


def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(f"(\[\d+\w+\])", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
            
    return result


def read_poti_content(poti_path):
    content = poti_path.read_text(encoding = 'utf-8')
    return content


def get_pecha_durchen():
    google_ocr = list(Path(f'./test/best_google').iterdir())
    google_ocr.sort()
    
    for poti_num, poti_path in enumerate(google_ocr[1:],88):
        print(f'v{poti_num} processing ....')
        vol_text = read_poti_content(poti_path)
        pages = get_pages(vol_text)
        result = get_durchen_span(pages, poti_num, text_id)


if __name__ == "__main__":
    get_pecha_durchen()

