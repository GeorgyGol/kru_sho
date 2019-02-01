import re
import os

strBaseURL=r'https://litlife.club/bd/?b=26946'

strFileDir='TD'
strSourceFileName='Source/Tihii_Don_source.txt'

def read_td(strFile=os.path.join(strFileDir, strSourceFileName)):
    def split(strKey, strText):
        return list([l.strip() for l in re.split(strKey, strText) if l])

    def filter_empty(lst):
        return list(filter(None, lst))

    text=''
    with open(strFile, 'r') as f:
        text=f.read().replace('*', '')

    #books=[ [p.strip() for p in re.split(r'(?m)ЧАСТЬ [А-Я]+', t.strip())]
    # for t in re.split(r'(?m)КНИГА [А-Я]+', text)]

    books = [[[i for i in split(r'(?m)\s?\b[IVX]+\b', p)] for p in split(r'(?m)ЧАСТЬ [А-Я]+', b)] for b in split(r'(?m)КНИГА [А-Я]+', text)]
    print('all books = ', len(books))
    dic_td=dict()

    for n, b in enumerate(books[1:]):
        for k, p in enumerate(b):
            for j, i in enumerate(p):
                num_part=0
                if n==0 :
                    if k==0 and j==0:
                        break
                    else:
                        num_part=k
                else:
                    num_part=j+1

                strT=re.sub(r'(?m)  ', ' ', i)
                strT=re.sub(r'(?m)\n ', '\n', strT)
                dic_td.setdefault('b{0}_p{1}_h{2}'.format(n+1, num_part, j+1), strT)

    #print(len(dic_td))
    #print(list(dic_td.keys()))
    #print(dic_td['b_1_p1_h1'])
    for k, i in dic_td.items():
        with open(os.path.join(strFileDir, k), 'w') as wf:
            wf.write(i)


def main():
    try:
        os.mkdir(strFileDir)
    except:
        pass

    read_td()



if __name__ == "__main__":
    main()
    print('TD - Done.')