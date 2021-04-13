from antx import transfer
from pathlib import Path
import re

def get_pages(vol_text):
    result = []
    pg_text = ""
    pages = re.split(f"(\[\d+[a-b]+\])", vol_text)
    for i, page in enumerate(pages[1:]):
        if i % 2 == 0:
            pg_text += page
        else:
            pg_text += page
            result.append(pg_text)
            pg_text = ""
    return result

def annotation_transfer(source, target):
    annotations = [['author_end', r'(\n)']]
    result = transfer(source, annotations, target, output= "txt", optimized=True)
    return result

def remove_annotations(target):
    result = ''
    result = re.sub(r'\n', '', target)
    return result

def get_transfered_text(source, target):
    google_pages = get_pages(source)
    namsel_pages = get_pages(target)
    transfered_text = ''
    for namsel_page, google_page in zip(namsel_pages, google_pages):
        if re.search('\n\n\n\n', namsel_page):
            transfered_text += google_page
        else:
            transfered_text += annotation_transfer(google_page, namsel_page)
    return transfered_text

def get_content(poti_path):
    return poti_path.read_text(encoding = 'utf-8')

sources = list(Path(f'./clean_tengyur_google_text').iterdir())
sources.sort()
targets = list(Path(f'./tengyur_namsel_reconstructed').iterdir())
targets.sort()
for source_vol, target_vol in zip(sources,targets):
    print(f'{source_vol.stem} and {target_vol.stem} processing')
    google_text = get_content(source_vol)
    namsel_text = get_content(target_vol)
    transfered_text = get_transfered_text(google_text, namsel_text)
    Path(f'./tengyur_namsel_transfered/{target_vol.stem}').write_text(transfered_text, encoding='utf-8')
    print(f'{target_vol.stem} completed..')