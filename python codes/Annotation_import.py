 from pathlib import Path 
 from antx import transfer
 import re 


def get_namsel():
	namsel_potis = Path(f'./kangyur_namsel/kangyur_namsel_text').read_text(encoding='utf-8')
	namsel_poti_content = get_poti_content(namsel_potis)
	return namsel_poti_content

def get_poti_content(namsel_potis):
	
	for poti_num, poti_path in enumerate (namsel_potis[1:], 1):
		poti_id = poti_path.name
		single_poti_path = poti_path/f'{poti_id}-000.xml'
		erase_unwanted(single_poti_path, poti_num)

def erase_unwanted(content, poti_num):
	
	result = ''
	page = re.split(r'\[[0-9]+[a-z]{1}\]',content)
	for page in pages:
		if re.search(r'\[[0-9]+[a-z]{1}\]', page):
			new_poti_content = re.sub(r'\[[0-9]+[a-z]{1}\]', ' ', page)
		elif re.search(r'\n',page):
			new_poti_content = re.sub(r'\n', ' ', page)

		result += new_poti_content + ' '

	return result



if __name__() == __main__():
	main():