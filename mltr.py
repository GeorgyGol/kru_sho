import pandas as pd
import glob
import os.path
import re
import datetime as dt
import warnings

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
    #print(strDir)
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
    clf_pp = Pipeline([('tfidf', TfidfVectorizer()), ('clf_n', MLPClassifier(hidden_layer_sizes=(470,50,),
                                                                             activation='tanh', tol=1e-5,
                                                                             n_iter_no_change=5,
                                                                             max_iter=250, alpha=1e-5, verbose=False,
                                                                             warm_start=True))])

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


def modeling(strIndex, lstPredict):
    def get_make_dir(strName):
        strResultDir = re.sub('predict', 'result', strName)

        try:
            os.mkdir(strResultDir)
        except:
            pass
        return strResultDir

    def get_res_data_frame(strSourceDir, pdf_src):
        if strSourceDir == str_TD_FileDir:
            pdf_result = sort_result(make_result_pdf(pdf_src))
        else:
            pdf_result = make_result_pdf(pdf_src)
        return pdf_result

    authors.main_author = strIndex

    pdfX = pd.concat([pdf for pdf in authors.index.map(read_source_txt)])

    print('loading sourses (files):')
    print(pdfX.groupby(by='auth').size())
    print('=' * 40)

    print('Loaded study files: ', pdfX.shape[0])
    print('Train model for ', strIndex)
    #os._exit(0)
    model = train_model(pdfX)
    print('o.k.', end='\n')
    #res = model.predict(pdf_td['text'])
    for l in lstPredict:
        print('?' * 20, '\t', l, '\t', '?' * 20)
        print('\n{1} ВОПРОС : автор "кучи непонятных текстов" -- {0}?'.format(
                authors.main_author['strRuName'].values[0],
                dt.datetime.now().strftime('%d.%m.%Y %H:%M:%S')))
        print(authors.index.tolist())

        pdf_td = read_TD(strDir=l)  # read ASK samle
        pdf_result=get_res_data_frame(l, pdf_td)
        res_prob = model.predict_proba(pdf_td['text'])

        pdf = pd.DataFrame({'prob2_0': [j for _, j in res_prob]}, index=pdf_td.index.tolist())
        pdf_result = pdf_result.join(pdf)
        prob2_mean = pdf_result['prob2_0'].mean()
        print('DONE. Probability for YES - {0:.3f}'.format(prob2_mean))
        strResFile = os.path.join(get_make_dir(l),
                                  'result_prob_{}.csv'.format(authors.main_author['strFileDir'].values[0]))
        pdf_result.to_csv(strResFile, sep=';', index=False)
        print('writing result to file ', strResFile)
        print('\nDone for ', l)
        print('?' * 80)

    print('All done for', strIndex)

def main():
    lst_predict=['predict/f1', 'predict/ka1', 'predict/pl1', 'predict/at1',
                 'predict/ga1', 'predict/pa1', 'predict/o1', 'predict/ilf1',
                 'predict/lt1', 'predict/mm', str_TD_FileDir]
    #lst_predict = ['predict/f1']

    # TD
    #'predict/f1'  # Fadeev's texts
    #'predict/ka1'  # Kataev's texts
    #'predict/pl1'  # Platonov's texts
    #'predict/lt1'  # L. Tolstoj's texts
    # 'predict/at1'  # A. Tolstoj's texts
    #'predict/mm'  # Bulgakov's texts

    authors.use(val=False)
    authors.use(index=['kru', 'sho', 'sera', 'fad', 'ltol', 'pla', 'kat', 'bab', 'blg', 'atol'], val=True)
    #print(authors)
    
    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        for n, auth in authors.iterrows():
            if auth['in_use']:
                modeling(n, lst_predict)


if __name__ == "__main__":
    main()
    #modeling('fad', 'predict/f1')