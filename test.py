import pandas as pd
import re

strKruFileDir='Krukov'
strShoFileDir='Sholokhov'

dct_flag={strKruFileDir:1, strShoFileDir:0}

class xResultInter:
    _strName=''
    def __init__(self, strName):
        self._strName=strName

    @property
    def author(self):
        return self._strName

    @author.setter
    def author(self, strName):
        self._strName=strName

    def check_author(self, strAuth):
        return 1 if strAuth == self._strName else 0

    def check_code(self, flag):
        return self._strName if flag ==1 else 'NOT {}'.format(self._strName)



def show_result(pdf, inter, save_csv=''):
    lstID = ['book', 'part', 'head']

    pdf[lstID] = pdf['name'].str.extract(r'b(?P<book>\d+)_p(?P<part>\d+)_h(?P<head>\d+)')
    pdf[lstID]=pdf[lstID].astype(int)
    pdf.sort_values(lstID, inplace=True)
    pdf['auth']=pdf['result'].apply(inter.check_code)

    print(pdf[lstID + ['auth', 'Prob_1',  'Prob_2', 'result']])
    if save_csv != '':
        pdf.to_csv(save_csv, index=False)


def main():

    inter=xResultInter(strKruFileDir)
    #inter.author=strKruFileDir

    show_result(pd.read_csv('result.csv', index_col=0), inter)


    #print(pdf.merge(pdf_n, left_index=True, right_index=True))
    print('All done.')


if __name__ == "__main__":
    main()