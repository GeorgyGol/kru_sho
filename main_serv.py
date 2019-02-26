import pandas as pd


Krukov={'strFileDir':'Krukov',
        'strUrl':r'http://az.lib.ru/k/krjukow_f_d/',
        'strRuName':'Ф. Крюков',
        'index':'kru',
        'file_mask':'*',
        'in_use':True,
        'fire':0}

Sholokhov={'strFileDir':'Sholokhov',
           'strUrl':r'http://www.lib.ru/PROZA/SHOLOHOW/',
           'strRuName':'М. Шолохов',
           'index':'sho',
            'file_mask':'*.txt',
           'in_use':True,
           'fire':0}

Tolstoy={'strFileDir':'Tolstoy',
           'strUrl':r'',
           'strRuName':'Л. Толстой',
           'index':'ltol',
           'file_mask':'*',
           'in_use':True,
           'fire':0}

Serafimovich={'strFileDir':'Serafimovich',
           'strUrl':r'http://lib.ru/RUSSLIT/SERAFIMOWICH/',
           'strRuName':'А. Серафимович',
           'index':'sera',
           'file_mask':'*',
           'in_use':True,
           'fire':0}


Babel={'strFileDir':'Babel',
           'strUrl':r'http://www.lib.ru/PROZA/BABEL/',
           'strRuName':'И. Бабель',
           'index':'bab',
           'file_mask':'*',
           'in_use':True,
           'fire':0}

Fadeyev={'strFileDir':'Fadeyev',
           'strUrl':r'http://www.lib.ru/RUSSLIT/FADEEW/',
           'strRuName':'А. Фадеев',
           'index':'fad',
           'file_mask':'*',
           'in_use':True,
           'fire':0}

Kataev={'strFileDir':'Kataev',
           'strUrl':r'http://www.lib.ru/PROZA/KATAEW/',
           'strRuName':'В. Катаев',
           'index':'kat',
           'file_mask':'*',
           'in_use':True,
           'fire':0}


Platonov={'strFileDir':'Platonov',
           'strUrl':r'http://platonov-ap.ru/novels/',
           'strRuName':'А. Платонов',
           'index':'pla',
           'file_mask':'*',
           'in_use':True,
           'fire':0}

lst_authors=[Krukov, Sholokhov, Tolstoy, Serafimovich, Fadeyev, Babel, Kataev, Platonov]

strCelina=r'http://www.lib.ru/PROZA/SHOLOHOW/celina.txt'
strDestiny=r'http://www.lib.ru/PROZA/SHOLOHOW/sudbache.txt'

str_TD_FileDir='predict/TD'


class xAuthors (pd.DataFrame):

    @property
    def _constructor(self):
        return xAuthors

    def __init__(self, *args, **kwargs):
        super(xAuthors, self).__init__(*args, **kwargs)


    def get_fire(self):
        return self[self['fire']==1]

    def set_fire(self, strIndex):
        if self.loc[strIndex, 'in_use']:
            self.fire = 0
            self.loc[strIndex, 'fire'] = 1
        else:
            raise ValueError('notfire not in use')

    main_author=property(get_fire, set_fire)

    def check_inUse(self, strIndex):
        return self.loc[strIndex, 'in_use']

    def use(self, **kwargs):
        #params - index=<list of str, str> if empty set to all;
        #       - val=<True|False>
        val=True
        inx=None
        try:
            val=kwargs['val']
        except KeyError:
            pass # default val = True

        try:
            inx=kwargs['index']
        except KeyError:
            print('not found param key_word "index" so set value to ALL authors')
            self['in_use']=val
            return

        self.loc[inx, 'in_use'] = val
    def working_authors(self):
        self.index.lolist()

authors = xAuthors(lst_authors).set_index('index')

def main():

    #print('Service for all moduls')
    #authors.loc['ltol', 'in_use']=False

    #print(authors.check_inUse('kru'))
    #authors.use(index=['ltol', 'sho'], val=False)

    #print(authors[['fire', 'in_use']])

    lsts=[[0.60655318, 0.39344682], [0.30902467, 0.69097533], [0.35681706, 0.64318294], [0.15124402, 0.84875598],
        [0.44869346, 0.55130654], [0.37768295, 0.62231705],  [0.5384363,  0.4615637 ],  [0.43850079, 0.56149921]]

    lst1=[j for _, j in lsts]
    print(lst1)




if __name__ == "__main__":
    pass
    #main()
