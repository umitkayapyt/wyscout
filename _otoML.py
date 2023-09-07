import pandas as pd
import numpy as np
import itertools
from time import sleep
import re
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale
from sklearn.preprocessing import StandardScaler
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import neighbors
from sklearn.svm import SVR
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from lightgbm import LGBMRegressor
# from catboost import CatBoostRegressor
from xgboost import XGBRegressor
import os
import openpyxl


class Wyscout(): # QMainWindow
        
    def __init__(self):
        
        self.dizin = "C:/Users/umit/data science/KENDİ ÇALIŞMALARIM/- PREMIER LEAGUE/- TAKIMLAR"

        self.ToplamGiris   = 0
        self.SaglamaCum    = 0
        self.ToplamCikis   = 0

        self.DF = pd.DataFrame()
        self.X  = pd.DataFrame()
        self.y  = pd.DataFrame()

        self.dog_olmayan_reg_models=[LGBMRegressor,
                                     XGBRegressor,
                                     GradientBoostingRegressor,
                                     RandomForestRegressor,
                                     DecisionTreeRegressor,
                                     MLPRegressor,
                                     KNeighborsRegressor,
                                     SVR]

        self.lig   = []
        self.ligs  = []

        self.coll = ['Grubun_veritabani', 'Tarih', 'Yarisma', 'Saha', 'Şema', 'Rakip', 'xG',
                    'Sutlar', 'Sutlar_hedef', 'Sut_yuzdesi', 'Paslar', 'Paslar_dogru',
                    'Pas_yuzdesi', 'Top_hakimiyeti_yuzdesi', 'Kayiplar', 'Kayiplar_Dusuk',
                    'Kayiplar_Orta', 'Kayiplar_Yuksek', 'Kurtarislar', 'Kurtarislar_Dusuk',
                    'Kurtarislar_Orta', 'Kurtarislar_Yuksek', 'Cekismeler',
                    'Cekismeler_kazanilan', 'Cekismeler_yuzdesi', 'Yenilen_Gol',
                    'Atilan_Gol']


        self.FileNameAndPath(self.dizin)
        sleep(2)
        self.FileProcessing(self.lig)
        sleep(5)
        self.FileConvertExcel()
        sleep(5)
        self.Encode_1_()
        sleep(5)
        self.y_target()
        self.Modellemeler()
        


    def FileNameAndPath(self, dizin):
        # Download edilen takım stats excelleri tek bir klasörde toplanmış olmalı
        # dizin kontrol edilmeli
        # for döngüsüne girecek liste belirlenmeli
        
        premier=os.listdir(dizin)
        for b in premier:
            self.ligs.append(b)
            a=b[11:-5]
            self.lig.append(a)

    def FileProcessing(self, lig):
        try:
            os.remove("DF.csv")
            pass
        except:
            pass

        for l in lig:
            # veri setinin import edilmesi, 
            # eksik verilerin atılması (ilk 2 satır değilse kontrol edilmeli)
            # yeniden indexleme
            df = pd.read_excel("C:/Users/umit/data science/KENDİ ÇALIŞMALARIM/- PREMIER LEAGUE/- TAKIMLAR/"+"Team Stats "+str(l)+".xlsx")
            df = df.dropna()
            df=df.rename(index={j: i for i, j in enumerate(df.index)})

            # Sağlama Giriş
            # sağlama yapılacak kolon değeri değiştirilirken giriş kolon ismine ve çıkış kolon isimlerine dikkat edilmeli 'df=df.rename(columns={' satırlarından bakılabilir
            self.ToplamGiris = df.loc[df['Grubun veritabanı']==l, "Unnamed: 18"].sum() # sağlama yapılacak kolon


            # Karşılaşma takımlarının ayrımı, atılan goller ve yenilen gollerin belirlenmesi -- regepx-- uzunluklar kontrol edildi.
            EvSahibi      = []
            Deplasman     = []
            EvSahibiSkor  = []
            DeplasmanSkor = []
            Sema          = []
            db = [i for i in df['Grubun veritabanı']]
            db = set(db)

            for index in df['Mac']:
                nesne1 = re.match(".+-",index)    # - öncesi bütün karakterler
                nesne1 = nesne1.group()
                nesne1 = nesne1[:-2]

                if nesne1 == 'Brighton & Hove Albion':
                        nesne1 = 'Brighton'
                        EvSahibi.append(nesne1)

                elif nesne1 == 'Olympiakos Piraeus':
                    nesne1 = 'Olympiacos Piraeus'
                    EvSahibi.append(nesne1)
                
                else:
                    EvSahibi.append(nesne1)
                    #print('Dikkat: {} Evsahibi takımı isim olarak yanlış yazılışmış olabilir'.format(nesne1))

                nesne2 = re.search('-.+([A-Z]|\')\w+',index) # - sonrası bütün karakterler boşluğa kadar
                nesne2 = nesne2.group()
                nesne2 = nesne2[2:]
                r = re.compile(".*{}".format(nesne2))
                newlist = list(filter(r.match, db))
                search = ''.join(newlist)

                if search:
                    Deplasman.append(search)

                else:
                    if nesne2 == 'Brighton & Hove Albion':
                        nesne2 = 'Brighton'
                        Deplasman.append(nesne2)

                    elif nesne2 == 'Olympiakos Piraeus':
                        nesne2 = 'Olympiacos Piraeus'
                        Deplasman.append(nesne2)
                    
                    else:
                        Deplasman.append(nesne2)
                        print('Dikkat: {} Deplasman takımı isim olarak yanlış yazılışmış olabilir'.format(nesne2))

                nesne3 = re.search(".+:",index)   # : öncesi bütün karakterler
                nesne3 = nesne3.group()
                nesne3 = nesne3[len(nesne3)-2:-1]
                EvSahibiSkor.append(int(nesne3))

                nesne4 = re.search(":[0-9]+",index)   # : sonrası bütün karakterler
                nesne4 = nesne4.group()
                nesne4 = nesne4[1:]
                DeplasmanSkor.append(int(nesne4))

            for i in df['Şema']:
                nesne = re.search("(?<=\\().*?(?=\\))", i)
                nesne = nesne.group()
                nesne  = i.replace(nesne, '').replace('()','').replace(' ','')
                Sema.append(nesne)

            # yeni eklenen kolonlar ve Tarih sütunu
            EvSahibi=pd.DataFrame(data=EvSahibi,index=range(len(EvSahibi)),columns=["EvSahibi"])
            EvSahibiSkor=pd.DataFrame(data=EvSahibiSkor,index=range(len(EvSahibiSkor)),columns=["EvSahibiSkor"])
            Deplasman=pd.DataFrame(data=Deplasman,index=range(len(Deplasman)),columns=["Deplasman"])
            DeplasmanSkor=pd.DataFrame(data=DeplasmanSkor,index=range(len(DeplasmanSkor)),columns=["DeplasmanSkor"])
            Sema=pd.DataFrame(data=Sema,index=range(len(Sema)),columns=["Sema"])
            df['Şema'] = Sema['Sema']
            df=df.drop(["Süre","Mac"],axis=1)
            df=pd.concat([EvSahibi, EvSahibiSkor, Deplasman, DeplasmanSkor, df],axis=1)
            df['Tarih'] = df['Tarih'].apply(lambda x: pd.to_datetime(x))

            # kolonlar yeniden adlandırıldı
            df=df.rename(columns={
                'EvSahibi':'EvSahibi',
                'EvSahibiSkor':'EvSahibiSkor',
                'Deplasman':'Deplasman',
                'DeplasmanSkor':'DeplasmanSkor',
                'Tarih':'Tarih',
                'Yarışma':'Yarisma',
                'Grubun veritabanı':'Grubun_veritabani',
                'Şema':'Şema',
                'Goller':'Atilan_Gol',
                'xG':'xG',
                'Şutlar / Hedefe':'Sutlar',
                'Unnamed: 9':'Sutlar_hedef',
                'Unnamed: 10':'Sut_yuzdesi',
                'Paslar / doğru':'Paslar',
                'Unnamed: 12':'Paslar_dogru',
                'Unnamed: 13':'Pas_yuzdesi',
                'Top hakimiyeti, %':'Top_hakimiyeti_yuzdesi',
                'Kayıplar / Düşük / Orta / Yüksek':'Kayiplar',
                'Unnamed: 16':'Kayiplar_Dusuk',
                'Unnamed: 17':'Kayiplar_Orta',
                'Unnamed: 18':'Kayiplar_Yuksek',
                'Kurtarışlar / Düşük / Orta / Yüksek':'Kurtarislar',
                'Unnamed: 20':'Kurtarislar_Dusuk',
                'Unnamed: 21':'Kurtarislar_Orta',
                'Unnamed: 22':'Kurtarislar_Yuksek',
                'Çekişmeler / kazanilan':'Cekismeler',
                'Unnamed: 24':'Cekismeler_kazanilan',
                'Unnamed: 25':'Cekismeler_yuzdesi'
            })

            # Saha, Rakip ve Yenilen Gollerin kolon haline getirilerek daha belirginleştirilmesi
            evsahibi=df["EvSahibi"]
            DBKlup=df["Grubun_veritabani"]
            deplasman=df["Deplasman"]
            EvSahibiSkor=df['EvSahibiSkor']
            DeplasmanSkor=df['DeplasmanSkor']
            Saha  = []
            Rakip = []
            Yenilen_Gol = []
            for ev, kl, dep, evskr, depskr in zip(evsahibi, DBKlup, deplasman, EvSahibiSkor, DeplasmanSkor):
                if ev==kl:
                    Saha.append("Evsahibi")
                    Rakip.append(dep)
                    Yenilen_Gol.append(depskr)
                else:
                    Saha.append("Deplasman")
                    Rakip.append(ev)
                    Yenilen_Gol.append(evskr)
            Saha=pd.DataFrame(data=Saha,index=range(len(Saha)),columns=["Saha"])
            Rakip=pd.DataFrame(data=Rakip,index=range(len(Rakip)),columns=["Rakip"])
            Yenilen_Gol=pd.DataFrame(data=Yenilen_Gol,index=range(len(Yenilen_Gol)),columns=["Yenilen_Gol"])
            df=pd.concat([Saha,Rakip, Yenilen_Gol, df],axis=1)
            #roden=roden.dropna()

            # tablonun daha anlamlı hale gelmesi için kolonların yeniden sıralanması
            bir_kisim   = df['Grubun_veritabani']
            iki_kisim   = df['Tarih']
            uc_kisim    = df['Yarisma']
            dort_kisim  = df['Saha']
            bes_kisim   = df['Şema']
            alti_kisim  = df['Rakip']
            Son_kisim   = df.loc[:,"xG":]
            yedi_kisim  = df['Atilan_Gol']
            sekiz_kisim = df['Yenilen_Gol']
            df=pd.concat([bir_kisim, iki_kisim, uc_kisim, dort_kisim, bes_kisim, alti_kisim, Son_kisim, sekiz_kisim, yedi_kisim],axis=1)

            # kolon tiplerinin düzenlemesi
            df['Atilan_Gol'] = df['Atilan_Gol'].astype('int')
            df['Yenilen_Gol'] = df['Yenilen_Gol'].astype('int')
            df['Sutlar'] = df['Sutlar'].astype('int')
            df['Sutlar_hedef'] = df['Sutlar_hedef'].astype('int')
            df['Paslar'] = df['Paslar'].astype('int')
            df['Paslar_dogru'] = df['Paslar_dogru'].astype('int')
            df['Kayiplar'] = df['Kayiplar'].astype('int')
            df['Kayiplar_Dusuk'] = df['Kayiplar_Dusuk'].astype('int')
            df['Kayiplar_Orta'] = df['Kayiplar_Orta'].astype('int')
            df['Kayiplar_Yuksek'] = df['Kayiplar_Yuksek'].astype('int')
            df['Kurtarislar'] = df['Kurtarislar'].astype('int')
            df['Kurtarislar_Dusuk'] = df['Kurtarislar_Dusuk'].astype('int')
            df['Kurtarislar_Orta'] = df['Kurtarislar_Orta'].astype('int')
            df['Kurtarislar_Yuksek'] = df['Kurtarislar_Yuksek'].astype('int')
            df['Cekismeler'] = df['Cekismeler'].astype('int')
            df['Cekismeler_kazanilan'] = df['Cekismeler_kazanilan'].astype('int')

            #Sağlama Giriş
            self.ToplamCikis = df.loc[df.Grubun_veritabani==l, "Kayiplar_Yuksek"].sum() #sağlama yapılacak kolon değişişmi
            
            # verilerin tabloya açık bir şekilde işlenmesi
            df.to_csv("DF.csv", index=False, mode = 'a', header=False)

            #Sağlama Toplamları
            self.SaglamaCum   = self.ToplamGiris - self.ToplamCikis
            print(l, 'xG Sağlama:', self.SaglamaCum)
    
    def FileConvertExcel(self):
        df=pd.read_csv("DF.csv", names=self.coll)
        df=df.rename(index={j: i for i, j in enumerate(df.index)})
        df['Tarih'] = df['Tarih'].apply(lambda x: pd.to_datetime(x))
        df=df.drop_duplicates(keep='last')
        df=df.rename(index={j: i for i, j in enumerate(df.index)})
        df.to_excel("df.xlsx",index=False)
        self.DF = df

    def Encode_1_(self):
        setTakimlar=list(set(self.DF['Grubun_veritabani']))
        Setdf = pd.DataFrame(columns=setTakimlar)
        zeros = list(np.zeros(len(self.DF['Grubun_veritabani']), dtype=int))
        sözlükTakimlar = {i: zeros for i in setTakimlar}
        dfTakimlar = pd.DataFrame(sözlükTakimlar)
        for i, tk, rkp in zip(range(len(self.DF['Grubun_veritabani'])), self.DF['Grubun_veritabani'], self.DF['Rakip']):
            dfTakimlar.loc[i,tk] = 1
            dfTakimlar.loc[i,rkp] = 1
        self.DF = pd.concat([dfTakimlar, self.DF],axis=1)
        self.DF.to_excel("df.xlsx",index=False)
        self.DF=self.DF.drop(["Grubun_veritabani", "Rakip", "Tarih"],axis=1)


        lb=LabelEncoder()

        lb.fit_transform(self.DF["Yarisma"]) #2
        Yarisma=pd.get_dummies(self.DF.iloc[:,122:123],columns=["Yarisma"], dtype=int)

        lb.fit_transform(self.DF["Saha"]) #3
        Saha=pd.get_dummies(self.DF.iloc[:,123:124],columns=["Saha"], dtype=int)
        Saha.drop(['Saha_Deplasman'],axis=1,inplace=True)
        Saha=Saha.rename(columns={'Saha_Evsahibi':'Saha'})

        lb.fit_transform(self.DF["Şema"]) #4
        Sema=pd.get_dummies(self.DF.iloc[:,124:125],columns=["Şema"], dtype=int)

        birinci_kisim=self.DF.iloc[:,:122]
        ikinci_kisim=self.DF.iloc[:,125:-2]

        self.X=pd.concat([birinci_kisim, Yarisma,Saha,Sema, ikinci_kisim],axis=1)

    def y_target(self):
        #self.DF['Atilan_Gol'] = self.DF.apply(lambda x: self.y_metot(x['Atilan_Gol']), axis=1)
        self.y = self.DF['Atilan_Gol']

    def y_metot(self, x):
           
        if x > 0:
            return 1
        else:
            return 0
        
    
    def compML(self, X, y, alg):
        #train-test ayrımı
        
        X_train, X_test, y_train, y_test=train_test_split(X, y , test_size=0.20, random_state=42)
        
        #modelleme
        model=alg().fit(X_train,y_train)
        y_pred=model.predict(X_test)
        RMSE=np.sqrt(mean_squared_error(y_test,y_pred))
        model_ismi=alg.__name__ 
        #print(model_ismi,"Modelin İlkel Test Hatası:",RMSE)
        print(model_ismi,"Modelin score yüzdesi:",model.score(X_test,y_test))
    
    def Modellemeler(self):
        for i in self.dog_olmayan_reg_models:
            self.compML(self.X, self.y, i)

Wyscout()