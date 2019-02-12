import re
import os

strFileDir='Tolstoy'
strSourceFileName='Source/Karenina1.txt'


def read_t(strFile=os.path.join(strFileDir, strSourceFileName)):
    def split(strKey, strText):
        return list([l.strip() for l in re.split(strKey, strText) if l])

    def filter_empty(lst):
        return list(filter(None, lst))

    text=''
    with open(strFile, 'r') as f:
        text=f.read().replace('*', '')

    #books=[ [p.strip() for p in re.split(r'(?m)ЧАСТЬ [А-Я]+', t.strip())]
    # for t in re.split(r'(?m)КНИГА [А-Я]+', text)]

    heads=[h.strip() for h in re.split(r'(?m)^\s*\b[IVX]+\b', text)]
    print('all heads = ', len(heads))
    dic_td=dict()

    for n, b in enumerate(heads):
        with open(os.path.join(strFileDir, str(n)), 'w') as wf:
            wf.write(b)


def main():
    try:
        os.mkdir(strFileDir)
    except:
        pass

    read_t()



if __name__ == "__main__":
    main()
    print('Tolstoy - Done.')