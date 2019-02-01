import pandas as pd
import glob
import os.path
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


strKruFileDir='Krukov'
strShoFileDir='Sholokhov'
strTDFileDir='TD'

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


def read_txt(strDir='', file_mask='*', inter=None):

    lst_files=glob.glob(os.path.join(strDir, file_mask))
    lst_params=[]

    for fl in lst_files:
        try:
            with open(fl, 'r') as f:
                dct={'text': f.read(), 'flag':inter.check_author(strDir), 'name':os.path.split(fl.replace('.txt', ''))[1], 'auth':strDir}

                lst_params.append(dct)
        except IsADirectoryError:
            continue
    pdf=pd.DataFrame(lst_params)
    return  pdf

def make_result_frame(pdfSourse, pdfX_target, y_taget, prob):
    pdf_res = pdfSourse.merge(pd.Series(y_taget, index=pdfX_target.index).to_frame(name='result'), left_index=True, right_index=True)
    res_prob_pdf = pd.DataFrame(prob, index=pdfX_target.index, columns=['Prob_1', 'Prob_2'])
    return pdf_res.merge(res_prob_pdf, left_index=True, right_index=True)


def read_td(strDir=strTDFileDir, flag=-1, auth='?'):
    print(strDir)
    lst_files = [f for f in glob.glob(strDir) if not re.search('txt', f)]


def train_model(pdf, print_test_frame=False):
    print('Train model...')
    X_train, X_test, y_train, y_test=train_test_split(pdf['text'], pdf['flag'])

    #print(X_train)
    clf_pp=Pipeline([('tfidf', TfidfVectorizer()), ('clf_n', MLPClassifier())])

    clf_pp.fit(X_train, y_train)
    res=clf_pp.predict(X_test)
    res_prob=clf_pp.predict_proba(X_test)

    print('Training done. Accurancy score = ', clf_pp.score(X_test, y_test))
    print('+'*40)

    if print_test_frame:
        pdf_res=make_result_frame(pdf, X_test, res, res_prob)

        with pd.option_context('display.max_rows', 30, 'display.max_columns', 7):
            print(pdf_res.loc[pdf_res['result'].notnull(), ('name', 'auth', 'flag', 'result', 'Prob_1', 'Prob_2')])

    print('?' * 40)
    print('\nВОПРОС : автор "Тихого Дона"  -- {0}?\n'.format(pdf.loc[pdf['flag']==1, 'auth'].values[0]))
    print('?' * 40)

    return clf_pp

def show_result(pdf, inter, save_csv=''):
    lstID = ['book', 'part', 'head']

    pdf[lstID] = pdf['name'].str.extract(r'b(?P<book>\d+)_p(?P<part>\d+)_h(?P<head>\d+)')
    pdf[lstID]=pdf[lstID].astype(int)
    pdf.sort_values(lstID, inplace=True)
    pdf['auth']=pdf['result'].apply(inter.check_code)

    print(pdf[lstID + ['auth', 'Prob_1',  'Prob_2', 'result']])
    if save_csv != '':
        pdf['text']=pdf['text'].str.slice(stop=50)
        pdf[lstID + ['auth', 'Prob_1',  'Prob_2', 'text']].to_csv(save_csv, index=False, sep=';')

def main():
    inter = xResultInter(strKruFileDir)
    #inter = xResultInter(strShoFileDir)

    pdf_kru=read_txt(strKruFileDir, inter=inter)
    pdf_sho=read_txt(strShoFileDir, file_mask='*.txt', inter=inter)
    pdf_td= read_txt(strTDFileDir, inter=inter)

    print('read sourses:')
    print('\tСписок Крюкова - ', pdf_kru.shape)
    print('\tСписок Шолохова - ', pdf_sho.shape)
    print('\tТихий Дон - ', pdf_td.shape)
    print('read done')
    print('='*40)

    pdfX=pd.concat([pdf_kru, pdf_sho]).reset_index(drop=True).sort_values('name')
    pdfX['flag']=pdfX['flag'].astype(int) # перестраховка

    model=train_model(pdfX, print_test_frame=False)
    res=model.predict(pdf_td['text'])
    res_prob=model.predict_proba(pdf_td['text'])

    pdf_res = make_result_frame(pdf_td, pdf_td, res, res_prob)
    print('!'*40)
    print()
    show_result(pdf_res, inter, save_csv='result_{}.csv'.format(inter.check_code(1)))

    print('All done.')


if __name__ == "__main__":
    main()