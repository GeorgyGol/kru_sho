import pandas as pd
import glob
import os.path
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

from main_serv import authors, str_TD_FileDir

def read_source_txt(strAuthIndex):
    if not authors.check_inUse(strAuthIndex):
        return None

    asr=authors.loc[strAuthIndex]

    lst_files=glob.glob(os.path.join(asr['strFileDir'], asr['file_mask']))
    lst_params=[]

    for fl in lst_files:
        try:
            with open(fl, 'r') as f:
                dct={'text': f.read().strip(),
                     'flag':asr['fire'],
                     'name':os.path.split(fl.replace('.txt', ''))[1],
                     'auth':asr['strRuName'] }

                lst_params.append(dct)

        except IsADirectoryError:
            continue

    pdf=pd.DataFrame(lst_params)
    #print(pdf['name'].tolist())
    return  pdf


def read_TD(strDir=str_TD_FileDir, file_mask='*'):

    lst_files=glob.glob(os.path.join(strDir, file_mask))
    lst_params=[]

    for fl in lst_files:
        try:
            with open(fl, 'r') as f:
                dct={'text': f.read().strip(),
                     'flag':'?',
                     'name':os.path.split(fl.replace('.txt', ''))[1],
                     'auth':strDir}

                lst_params.append(dct)

        except IsADirectoryError:
            continue
    pdf=pd.DataFrame(lst_params)
    #print(pdf['name'].tolist())
    return  pdf

def train_model(pdf, train_with_test=True):
    print('Train model...', end='')
    X_train, X_test, y_train, y_test=train_test_split(pdf['text'], pdf['flag'])

    #print(X_train)
    #clf_pp=Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 2))), ('clf_n', MLPClassifier())]) # настройка с параметрами
    clf_pp = Pipeline([('tfidf', TfidfVectorizer()), ('clf_n', MLPClassifier())])

    if train_with_test:
        clf_pp.fit(X_train, y_train)
        res=clf_pp.predict(X_test)
        res_prob=clf_pp.predict_proba(X_test)

        print('Training done. Accurancy score = ', clf_pp.score(X_test, y_test), end='\n')
    else:
        clf_pp.fit(pdf['text'], pdf['flag'])
        print('Train comlete - without test', end='\n')
    #print('+'*40)

    #print('?' * 40)
    #print('\nВОПРОС : автор "Тихого Дона"  -- {0}?\n'.format(pdf.loc[pdf['flag']==1, 'auth'].values[0]))
    #print('?' * 40)

    return clf_pp


def make_result_pdf(pdf):
    pdf_res=pdf[['name', 'text']]
    pdf_res['short_text']=pdf_res['text'].str[:150]
    return pdf_res[['name', 'short_text']]

def sort_result(pdf):
    lstID = ['book', 'part', 'head']
    #pdf_res=pdf
    pdf[lstID] = pdf['name'].str.extract(r'b(?P<book>\d+)_p(?P<part>\d+)_h(?P<head>\d+)')
    pdf[lstID] = pdf[lstID].astype(int)
    pdf.sort_values(lstID, inplace=True)
    return pdf.drop(lstID, axis=1)


def modeling(strIndex):

    authors.main_author = strIndex

    pdfX = pd.concat([pdf for pdf in authors.index.map(read_source_txt)])

    print('loading sourses (files):')
    print(pdfX.groupby(by='auth').size())
    print('=' * 40)
    print('All files: ', pdfX.shape[0])

    pdf_td = read_TD()  # read Тихий Дон
    pdf_result = sort_result(make_result_pdf(pdf_td))

    print('?' * 80)
    print('\nВОПРОС : автор "Тихого Дона" -- {0}?\n'.format(authors.main_author['strRuName'].values[0]))

    for i in range(13):
        print('STEP :', i)
        model = train_model(pdfX)
        res = model.predict(pdf_td['text'])
        res_prob = model.predict_proba(pdf_td['text'])

        pdf = pd.DataFrame({'prob2_{0}'.format(i): [j for _, j in res_prob]}, index=pdf_td.index.tolist())
        pdf_result = pdf_result.join(pdf)
        prob2_mean = pdf_result['prob2_{0}'.format(i)].mean()
        print('STEP {0} DONE. Probability for YES - {1:.3f}'.format(i, prob2_mean))

    pdf_result.to_csv('result_prob_{}.csv'.format(authors.main_author['strFileDir'].values[0]), sep=';', index=False)
    print('writing result to file ', 'result_prob_{}.csv'.format(authors.main_author['strFileDir'].values[0]))
    print('?' * 80)
    print('All done.')

def main():
    authors.use(val=False)
    authors.use(index=['kru', 'sho', 'sera', 'fad'], val=True)
    authors.main_author='kru'

    for n, auth in authors.iterrows():
        if auth['in_use']:
            modeling(n)


if __name__ == "__main__":
    main()