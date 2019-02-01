import requests
from bs4 import BeautifulSoup, Comment
import re
import os

strBaseURL=r'http://www.lib.ru/PROZA/SHOLOHOW/'
strFileDir='Sholokhov'

strCelina=r'http://www.lib.ru/PROZA/SHOLOHOW/celina.txt'
strDestiny=r'http://www.lib.ru/PROZA/SHOLOHOW/sudbache.txt'

def format_para(text):
    strs = re.split(r'(?m)\n\s{3}', text)
    lst = [re.sub(' {2,}', ' ', s.replace('\n', ' ')).strip() for s in strs]
    lst = [re.sub('\[.*\]', '', s).replace(' .', '.') for s in lst]
    return '\n'.join(lst)

def celina(strURL=strCelina):
    r = requests.get(strURL)

    r_split=re.compile(r'<ul><a name=\d+></a><h2>\d+</h2></ul>')
    text = list(map(str.strip, r_split.split(r.text)))
    strFN_pre=''
    for i, t in enumerate(text):
        sp=BeautifulSoup(t, 'html.parser')
        nb=sp.find('h2', text=lambda x: re.search('[А-Я]{3,}', x))
        if nb:
            strFN_pre=nb.text.replace(' ', '_')
        else:
            strFileName='Поднятая_целина_{pre}-{num}.txt'.format(pre=strFN_pre, num=i)
            with open(os.path.join(strFileDir, strFileName), 'w') as fl:
                fl.write(format_para(t))

            print('Done for file ', strFileName)

def destiny(strURL=strDestiny):
    r = requests.get(strURL)
    strFileName='Судьба_человека.txt'
    strT=format_para(r.text)
    strT=strT[strT.find('Первая послевоенная весна была на Верхнем Дону'):strT.find('<ul><a name=1></a><h2>1956-1957</h2></ul>')+1]

    with open(os.path.join(strFileDir, strFileName), 'w') as fl:
        fl.write(strT)

    print('Done for file ', strFileName)

def main():
    try:
        os.mkdir(strFileDir)
    except:
        pass

    #destiny()


if __name__ == "__main__":
    main()