import requests
from bs4 import BeautifulSoup, Comment
import re
import os

strBaseURL=r'http://az.lib.ru/k/krjukow_f_d/'
strFileDir='Krukov'

def get_file(strURL, strName):
    r=requests.get(strURL)
    soup=BeautifulSoup(r.text, 'html.parser')
    commStart = soup.find(
        text=lambda x: isinstance(x, Comment) and re.search('Section Begins', str(x)))
    commEnd = soup.find(
        text=lambda x: isinstance(x, Comment) and re.search('Section End', str(x)))
    wsp=BeautifulSoup(r.text[r.text.find(commStart)+len(commStart)+3:r.text.find(commEnd)-4], 'html.parser')
    text=list(map(lambda x: x.strip(), wsp.text.split('\n')))

    indStart=0
    indEnd=-1

    for i, line in enumerate(text[:50]):

        if re.match(r'(?i){}\.?'.format(strName), line):
            indStart=i+1
        if re.match(r'\(.*\)'.format(strName), line):
            indStart = i + 1

    for i, line in enumerate(text[-10:]):

        if re.match(r'(?i)Подпись:', line):
            indEnd=i-10
            break
        if re.match(r'Оригинал здесь --', line):
            indEnd = i-10

    return '\n'.join(text[indStart:indEnd]).strip()


def get_items_url(strURL=strBaseURL):
    r=requests.get(strURL)
    soup=BeautifulSoup(r.text, 'html.parser')
    commStart=soup.find(text=lambda x: isinstance(x, Comment) and re.search('вместо <body> вставятся ссылки на произведения!', str(x)))
    commEnd = soup.find(
        text=lambda x: isinstance(x, Comment) and re.search('Подножие', str(x)))
    wsoup=BeautifulSoup(r.text[r.text.find(commStart):r.text.find(commEnd)], 'html.parser')
    a_s=wsoup.find_all('a', href=lambda x: re.match(r'text', str(x)))
    for a in a_s:
        with open(os.path.join(strFileDir, a.text), 'w') as fl:
            fl.write(get_file(strBaseURL+a.get('href'), a.text))
        print(a.text, ' -- done')
        #print(a.text, a.get('href'))


def main():
    try:
        os.mkdir(strFileDir)
    except:
        pass

    get_items_url()


if __name__ == "__main__":
    main()