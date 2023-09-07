# -*- coding: utf-8 -*-

# Web kazıma işlemleri ve raporlamalar / main dosyası

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import Select # WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# import chromedriver_autoinstaller

# from tqdm import tqdm
from time import sleep, strftime
from locale import setlocale, LC_ALL
from pandas import DataFrame
from pathlib import Path
from bs4 import BeautifulSoup
from sys import argv, exit
from os import path

import re

setlocale(LC_ALL, 'turkish')


class Scrap():
    def __init__(self):

        #self.home = str(Path.home())+'\\_wyscout'

        self.Site = 'https://platform.wyscout.com/app/'
        self.userName = 'b_avicenna_t@hotmail.com'
        self.password = 'FqeSs8N@kgVjS!7'

        self.TimeRefresh = 2.5
        self.TimeClick   = 2.5

        self.TAKIMLAR = []
        self.TAKIMLAR_ORJ = []

        self.ignored_exceptions=(NoSuchElementException, StaleElementReferenceException,)

############################################################# ÜLKELERİ VE LİGLERİ HARİTALANDIRMA ##################################################################################################################        
        
        self.Ligler = {'Afghanistan':['Premier League'],
                       'Almanya'    :['Bundesliga', '2. Bundesliga'],
                       'Amerika'    :[['MLS', 'USL Championship', 'MLS Next Pro', 'USL League 1', 'USL League 2', #east & west ---> MLS', 'USL Championship', 'MLS Next Pro'
                                       'NISA', 'US Open Cup', 'Diamond Cup',"NCAA Men's Soccer - College Cup", 'ASUN', # kupa maçları ---> 'US Open Cup', 'Diamond Cup',"NCAA Men's Soccer - College Cup"
                                       'America East', 'American Athletic', 'Atlantic 10', 'Atlantic Coast', 'Big East', 
                                       'Big South', 'Big Ten', 'Big West', 'Colonial Athletic Association', 'Conference USA', 
                                       'Horizon League', 'Independent', 'Ivy League', 'Metro Atlantic Athletic Conference', 'Mid-American', # boş ----> 'Independent'
                                       'Missouri Valley', 'Northeast', 'Pacific 12', 'Patriot League', 'Southern', 
                                       'Summit League', 'Sun Belt', 'West Coast', 'Western Athletic', 'NCAA Non-conference Men matches', 
                                       'Suncoast Invitational', 'Timbers Preseason Tournament'], 
                                      ['Eastern Conference', 'Western Conference']],
                       'Andorra'    :['1a Divisió', 'Copa Constitució'],
                       'Arjantin'   :[['Liga Profesional de Fútbol', 'Primera Nacional', 'Prim B Metro'],['Group A', 'Group B']], # Primera Nacional 2 grup
                       'Arnavutluk' :['Abissnet Superiore'],
                       'Avustralya' :['A-League', 'Australia Cup', 'Capital Territory NPL','New South Wales NPL','Queensland NPL', 'South Australia NPL', 'Northern NSW NPL', 'Tasmania NPL', 'Victoria NPL','Western Australia NPL'],
                       'Avusturya'  :['Bundesliga', '2. Liga'],
                       'Azerbaycan' :['Premyer Liqa'],
                       'Bahrain'    :['Premier League'],
                       'Bangladesh' :['Premier League'],
                       'Belçika'    :['First Division A', 'First Division B'],
                       'Birleşik Arap Emirlikleri' : ['Arabian Gulf League', 'Division 1'],
                       'Bolivia'    :['LFPB'],
                       'Bosnia and Herzegovina': ['Premijer Liga', '1st League'],
                       'Brezilya'   :['Serie A', 'Serie B', 'Serie C'],
                       'Bulgaristan':['First League', 'Second League'],
                       'Cambodia'   :['Cambodian Premier League'],
                       'Cameroon'   :['Elite ONE'], ### BOŞ GEÇİYOR
                       'Canada'     :['Canadian Premier League', 'Canadian Championship'],
                       'Cezayir'    :['Ligue 1'],
                       'Danimarka'  :['Superliga', '1st Division', '2nd Division', '3. Division', 'DBU Pokalen'],
                       'Ekvador'    :['Liga Pro', 'Liga Pro Serie B'],
                       'El Salvador':['Primera Division'],
                       'Ermenistan' :['Premier League', 'First League'],
                       'Estonya'    :['A.LeCoq Premium Liiga', 'Esiliiga A'],
                       'Fas'        :['Botola Pro'],
                       'Finlandiya' :['Veikkausliiga', 'Ykkönen'],
                       'Fransa'     :['Ligue 1', 'Ligue 2', 'National 1'],
                       'Galler'     :['Premier League'],
                       'Ghana'      :['Premier League'],
                       'Gibraltar'  :['Gibraltar Football League'],
                       'Guatemala'  :['Liga Nacional'],
                       'Güney Afrika':['PSL'],
                       'Güney Kore' :['K League 1', 'K League 2', 'K3 League', 'K4 League'],
                       'Gürcistan'  :['Erovnuli Liga', 'Erovnuli Liga 2'],
                       'Hindistan'  :['Indian Super League', 'I-League', 'I-League 2nd Division'],
                       'Hollanda'   :['Eredivisie', 'Eerste Divisie', 'Tweede Divisie'],
                       'Honduras'   :['Liga Nacional'],
                       'Hong Kong'  :['Premier League'],
                       'Hırvatistan':['1. HNL', '2. HNL'],
                       'Indonesia'  :['Liga 1', 'Piala Indonesia'],
                       'Japonya'    :['J1 League', 'J2 League', 'J3 League'],
                       'Jordan'     :['League'],   ###BOŞ GEÇİYOR,,
                       'Karadağ'    :['First League', 'Second League'],
                       'Katar'      :['Qatar Stars League', 'Second Division'],
                       'Kazakistan' :['Premier League', '1. Division'],
                       'Kolombiya'  :['Liga BetPlay', 'Torneo BetPlay'],
                       'Kosovo'     :['Superliga'],
                       'Kosta Rika' :['Primera División'],
                       'Kuwait'     :['Premier League'],
                       'Kyrgyzstan' :['Shoro Premier League'],
                       'Kıbrıs'     :['1. Division', '2. Division'],
                       'Letonya'    :['Virsliga', '1. Liga'],
                       'Litvanya'   :['A Lyga', '1 Lyga'],
                       'Luxembourg' :['National Division'],
                       'Macaristan' :['NB I', 'NB II'],
                       'Malaysia'   :['Super League'],
                       'Malta'      :['Premier League'],
                       'Meksika'    :['Liga MX', 'Liga de Expansión MX', 'Liga Premier Serie A', 'Liga Premier Serie B'],
                       'Moldova'    :['Super Liga'],
                       'Mısır'      :['Premier League'],
                       'New Zealand':['National League', 'South Central Series'],
                       'Nicaragua'  :['Primera Division'],
                       'North Macedonia': ['First League'],
                       'Northern Ireland':['Premiership'],
                       'Norveç'     :['Eliteserien', 'Obos Ligaen'],
                       'Panama'     :[['LPF', 'Diğer'], ['East', 'West']],
                       'Paraguay'   :['Division Profesional'],
                       'Peru'       :['Primera División'],
                       'Polonya'    :['Ekstraklasa', 'I Liga', 'II Liga'],
                       'Portekiz'   :['Primeira Liga', 'Segunda Liga', 'Liga 3', 'Campeonato de Portugal', 'Taça de Portugal'],
                       'Republic of Ireland' :['Premier Division', 'First Division'],
                       'Romanya'    :['Superliga','Liga II'],
                       'Rusya'      :['Premier League', 'FNL', 'FNL 2'],
                       'Singapore'  :['Premier League', 'League Cup'],
                       'Slovakya'   :['Super Liga', '2. liga'],
                       'Slovenya'   :['1. SNL', '2. SNL'],
                       'Suudi Arabistan' :['Pro League', 'Division 1'],
                       'Sırbistan'  :['Super Liga', 'Prva Liga'],
                       'Thailand'   :['Thai League', 'Thai League 2'],
                       'Tunus'      :['Ligue 1'],
                       'Türkiye'    :['Süper Lig', '1. Lig'],
                       'Uganda'     :['Premier League'],
                       'Ukrayna'    :['VBET League', 'Persha Liga', 'Druha Liga'],
                       'Uruguay'    :['Primera División', 'Segunda División'],
                       'Vietnam'    :['V.League 1'],
                       'Yunanistan' :['Super League'], #BURADA ALMADIKLARIM VAR (ALT LİG)
                       'Çek Cumhuriyeti' :['Fortuna Liga', 'FNL'],
                       'Çin'        :['CSL', 'China League One'],
                       'Özbekistan' :['Super League', 'Pro League A'],
                       'İngiltere'  :['Premier League', 'Championship', 'League One', 'League Two', 'National League'],
                       'İskoçya'    :['Premiership' , 'Championship', 'League One', 'League Two'],
                       'İspanya'    :['LaLiga', 'Segunda División'],
                       'İsrail'     :["Ligat ha'Al", "Liga Leumit"],
                       'İsveç'      :['Allsvenskan', 'Superettan'],
                       'İsviçre'    :['Super League', 'Challenge League', '1. Liga Promotion'],
                       'İtalya'     :['Serie A', 'Serie B', 'Serie C', 'Serie D'],
                       'İzlanda'    :['Besta-deild karla', '1. Deild'],
                       'Şili'       :['Primera División', 'Primera B']
                       }

#################################################################### METOTLAR AKTİF ##################################################################################################################        
        
        self.Login()
        self.Upload()

#################################################################### METOTLAR MİMARİ ##################################################################################################################        

    def Login(self):
        opt = webdriver.ChromeOptions()
        opt.add_experimental_option('excludeSwitches', ['enable-logging'])
        opt.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=opt)
        self.driver.get(self.Site)
        #self.scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
        sleep(self.TimeClick)

        kullaniciADIxpath   = '/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/input'
        kullaniciSIFRExpath = '/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/div[2]/div[2]/input'
        Signinxpath         = '/html/body/div[1]/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div[2]/div[3]/div/button'
        buttonLANGUExpath   = '/html/body/div[1]/div/div[1]/div[5]/div[1]/div[2]/a'
        buttonTURKCExpath   = '/html/body/div[13]/div[1]/div/div/div/div[8]/div'

        kullaniciADIinput   = self.driver.find_element(By.XPATH, kullaniciADIxpath)
        kullaniciSIFREinput = self.driver.find_element(By.XPATH, kullaniciSIFRExpath)

        kullaniciADIinput.send_keys(self.userName)
        sleep(0.1)
        kullaniciSIFREinput.send_keys(self.password)
        sleep(0.1)
        Signin = self.driver.find_element(By.XPATH, Signinxpath)
        Signin.click()
        sleep(6.1)
        btnlngue = self.driver.find_element(By.XPATH, buttonLANGUExpath)
        btnlngue.click()
        sleep(self.TimeClick)
        btntrkce = self.driver.find_element(By.XPATH, buttonTURKCExpath)
        btntrkce.click()
        sleep(self.TimeClick)
        self.driver.refresh()
        sleep(4.5)

    def Soup__Tkm_Parser(self, index):
        scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
        tk = [element.text.strip() for element in scout_soup.find_all("div", "item-element item-text title")]
        indx = tk.index(index)+1
        takimlar = tk[indx:]
        for t in takimlar:
            self.TAKIMLAR.append(t)
        print(takimlar)
        takimSayisi = len(takimlar)
        return takimSayisi

    def Soup_TkmUSA_Parser(self, indexbas, indexbit):
        scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
        tk = [element.text.strip() for element in scout_soup.find_all("div", "item-element item-text title")]
        indx_bas = tk.index(indexbas)+1
        indx_bit = tk.index(indexbit)
        takimlar = tk[indx_bas:indx_bit]
        print(takimlar)
        for t in takimlar:
            self.TAKIMLAR.append(t)
        TkSayisi = len(takimlar)
        for tkm in range(TkSayisi):
            TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+2))
            TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
            TakimGir.click()
            sleep(self.TimeClick)

            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
            TkmNameOrjnal = tkmm[0]
            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
            print(TkmNameOrjnal)

            self.DownLoad()

            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
            before = self.driver.find_element(By.XPATH, beforeXpath)
            before.click()
            sleep(self.TimeClick)
    
    def DownLoad(self):
        statsXPATH = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[4]/div[3]/div/div[5]/a/span/span'
        statsGir   = self.driver.find_element(By.XPATH, statsXPATH)
        statsGir.click()
        sleep(self.TimeClick)

        excelPATH = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div[5]/div/div/div/main/div[3]/div[1]/div[2]/a'
        excelGir   = self.driver.find_element(By.XPATH, excelPATH)
        excelGir.click()
        sleep(self.TimeClick)

    def Upload(self): # TAKIMLARA GİR

        for i, (key, val) in zip(range(len(self.Ligler)), self.Ligler.items()):
            ulkeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[1]/div[1]/div[1]/div/div/div[1]/div/div[{}]/div/div[2]'.format(str(i+1))
            ulkegir  = self.driver.find_element(By.XPATH, ulkeXpath)
            ulkegir.click()
            sleep(self.TimeClick)

            scout_soup_ilk=BeautifulSoup(self.driver.page_source,"html.parser")
            self.ulusal = [element.text.strip() for element in scout_soup_ilk.find_all( "div", attrs={"class":"gears-list-item aengine-model team", "itemkey": True})]
            
            valstr = ", ".join(str(x) for x in val)

            if key in {'Afghanistan', 'Cameroon', 'Jordan'}: #BOŞ {'Afghanistan', 'Cameroon', 'Jordan'}
                pass

            elif key == 'Amerika': # KITA YENİDEN KEŞFEDİLİYOR
                
                for idx, usa in enumerate(val[0]):
                    if usa in {'USL League 2', 'US Open Cup', 'Diamond Cup', 'Independent', "NCAA Men's Soccer - College Cup"}: #BOŞ 'USL League 2', 'US Open Cup', 'Diamond Cup', 'Independent', "NCAA Men's Soccer - College Cup"
                        pass

                    elif usa == 'MLS':
                        MLSxpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(idx+1))
                        MLSGir   = self.driver.find_element(By.XPATH, MLSxpath)
                        MLSGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'EAST '+usa)
                        EastXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div/div/div[1]/div/div[2]'
                        EastGir   = self.driver.find_element(By.XPATH, EastXpath)
                        EastGir.click()
                        sleep(self.TimeClick)

                        TkSayisi = self.Soup__Tkm_Parser(index='Geri')
                        for tkm in range(TkSayisi):
                            TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+2))
                            TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                            TakimGir.click()
                            sleep(self.TimeClick)

                            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                            TkmNameOrjnal = tkmm[0]
                            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                            print(TkmNameOrjnal)
                            
                            self.DownLoad()

                            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                            before = self.driver.find_element(By.XPATH, beforeXpath)
                            before.click()
                            sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'WEST '+usa)
                        WestXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/div[2]'
                        WesttGir   = self.driver.find_element(By.XPATH, WestXpath)
                        WesttGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                    
                    elif usa == 'USL Championship':
                        USLxpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(idx+1))
                        USLGir   = self.driver.find_element(By.XPATH, USLxpath)
                        USLGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'EAST '+usa)
                        EastXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div/div/div[1]/div/div[2]'
                        EastGir   = self.driver.find_element(By.XPATH, EastXpath)
                        EastGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                        
                        print(key+' Hedef   Lig   : '+'WEST '+usa)
                        WestXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/div[2]'
                        WesttGir   = self.driver.find_element(By.XPATH, WestXpath)
                        WesttGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                    
                    elif usa == 'MLS Next Pro':
                        MLSPROxpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(idx+1))
                        MLSPROGir   = self.driver.find_element(By.XPATH, MLSPROxpath)
                        MLSPROGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'EAST '+usa)
                        EastXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div/div/div[1]/div/div[2]'
                        EastGir   = self.driver.find_element(By.XPATH, EastXpath)
                        EastGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'WEST '+usa)
                        WestXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div/div/div[2]/div/div[2]'
                        WesttGir   = self.driver.find_element(By.XPATH, WestXpath)
                        WesttGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                    
                    else:
                        print(key+' Hedef   Lig   : '+usa)
                        USALigXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(idx+1))
                        USALigGir   = self.driver.find_element(By.XPATH, USALigXpath)
                        USALigGir.click()
                        sleep(self.TimeClick)

                        scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
                        tk = [element.text.strip() for element in scout_soup.find_all("div", "item-element item-text title")]
                        # indx_bas = tk.index('Diğer')+1
                        # indx_bit = tk.index('Geri')
                        # takimlar = tk[indx_bas:indx_bit]
                        takimlar = tk[-4:]
                        print(takimlar) 
                        for t in takimlar:
                            self.TAKIMLAR.append(t)
                        TkSayisi = len(takimlar)
                        for tkm in range(TkSayisi):
                                          
                            TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+1))
                            TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                            TakimGir.click()
                            sleep(self.TimeClick)

                            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                            TkmNameOrjnal = tkmm[0]
                            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                            print(TkmNameOrjnal)

                            self.DownLoad()

                            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                            before = self.driver.find_element(By.XPATH, beforeXpath)
                            before.click()
                            sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

            elif key == 'Arjantin':   #:[[, , ],['Group A', 'Group B']] 
                
                for idj, arj in enumerate(val[0]):
                    if arj == 'Liga Profesional de Fútbol':
                        ProfesionalXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div/div[2]'
                        ProfesionalGir   = self.driver.find_element(By.XPATH, ProfesionalXpath)
                        ProfesionalGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+arj)
                        scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
                        tk = [element.text.strip() for element in scout_soup.find_all("div", "item-element item-text title")]
                        indx_bas = tk.index('Diğer')+1
                        takimlar = tk[indx_bas:]
                        print(takimlar)
                        for t in takimlar:
                            self.TAKIMLAR.append(t)
                        TkSayisi = len(takimlar)
                        for tkm in range(TkSayisi):
                            TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+1))
                            TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                            TakimGir.click()
                            sleep(self.TimeClick)

                            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                            TkmNameOrjnal = tkmm[0]
                            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                            print(TkmNameOrjnal)

                            self.DownLoad()

                            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                            before = self.driver.find_element(By.XPATH, beforeXpath)
                            before.click()
                            sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                    
                    elif arj == 'Primera Nacional':
                        Nacionalxpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(idj+1))
                        NacionalOGir   = self.driver.find_element(By.XPATH, Nacionalxpath)
                        NacionalOGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'GroupA '+arj)
                        GroupAXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'
                        GroupAGir   = self.driver.find_element(By.XPATH, GroupAXpath)
                        GroupAGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'GroupB '+arj)
                        GroupBXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div[2]'
                        GroupBGir   = self.driver.find_element(By.XPATH, GroupBXpath)
                        GroupBGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')
                                    
                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                    
                    elif arj == 'Prim B Metro':
                        MetroXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[3]/div/div[2]'
                        MetroGir   = self.driver.find_element(By.XPATH, MetroXpath)
                        MetroGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+arj)
                        scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
                        tk = [element.text.strip() for element in scout_soup.find_all("div", "item-element item-text title")]
                        indx_bas = tk.index('Diğer')+1
                        indx_bit = tk.index('Geri')
                        takimlar = tk[indx_bas:indx_bit]
                        print(takimlar)
                        for t in takimlar:
                            self.TAKIMLAR.append(t)
                        TkSayisi = len(takimlar)
                        for tkm in range(TkSayisi):
                                          
                            TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+1))
                            TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                            TakimGir.click()
                            sleep(self.TimeClick)

                            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                            TkmNameOrjnal = tkmm[0]
                            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                            print(TkmNameOrjnal)

                            self.DownLoad()

                            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                            before = self.driver.find_element(By.XPATH, beforeXpath)
                            before.click()
                            sleep(self.TimeClick)


                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

            elif key == 'Panama': # [[,], ['East', 'West']]
                
                for idp, pan in enumerate(val[0]):
                    if pan == 'LPF':
                        LPFxpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(idp+1))
                        LPFGir   = self.driver.find_element(By.XPATH, LPFxpath)
                        LPFGir.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'EAST '+pan)
                        EAST_Xpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[1]/div/div[2]'
                        EAST_AGir   = self.driver.find_element(By.XPATH, EAST_Xpath)
                        EAST_AGir.click()
                        sleep(self.TimeClick)

                        TkSayisi = self.Soup__Tkm_Parser(index='Geri')
                        for tkm in range(TkSayisi):
                            TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+2))
                            TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                            TakimGir.click()
                            sleep(self.TimeClick)

                            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                            TkmNameOrjnal = tkmm[0]
                            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                            print(TkmNameOrjnal)

                            scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                            tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                            TkmNameOrjnal = tkmm[0]
                            self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                            print(TkmNameOrjnal)

                            self.DownLoad()

                            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                            before = self.driver.find_element(By.XPATH, beforeXpath)
                            before.click()
                            sleep(self.TimeClick)

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        print(key+' Hedef   Lig   : '+'WEST '+pan)
                        WEST_BXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[1]/div[1]/div/div[2]/div/div[2]'
                        WEST_BGir   = self.driver.find_element(By.XPATH, WEST_BXpath)
                        WEST_BGir.click()
                        sleep(self.TimeClick)

                        self.Soup_TkmUSA_Parser(indexbas='Geri', indexbit='Gol')
                                    
                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/span'
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)

                        before_Xpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        before__ = self.driver.find_element(By.XPATH, before_Xpath)
                        before__.click()
                        sleep(self.TimeClick)

                    else:
                        pass
                        # DigerXPath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]'   
                        # DigerGir   = self.driver.find_element(By.XPATH, DigerXPath)
                        # DigerGir.click()
                        # sleep(self.TimeClick)

                        # print(key+' Hedef   Lig   : '+'Liga Nacional de Ascenso')
                        # AscensoXPath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[2]/div/div[2]'   
                        # AscensoGir   = self.driver.find_element(By.XPATH, AscensoXPath)
                        # AscensoGir.click()
                        # sleep(self.TimeClick)

                        # scout_soup=BeautifulSoup(self.driver.page_source,"html.parser")
                        # tk = [element.text.strip() for element in scout_soup.find_all("div", "item-element item-text title")]
                        # indx = tk.index('Geri')+3
                        # takimlar = tk[indx:-40]
                        # print(takimlar)
                        # for t in takimlar:
                        #     self.TAKIMLAR.append(t)
                        # TkSayisi = len(takimlar)
                        # for tkm in range(TkSayisi):
                                          
                        #     TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+1))
                        #     TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                        #     TakimGir.click()

                        #     scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                        #     tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                        #     TkmNameOrjnal = tkmm[0]
                        #     self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                        #     print(TkmNameOrjnal)
                        #     sleep(self.TimeClick)

                        #     beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                        #     before = self.driver.find_element(By.XPATH, beforeXpath)
                        #     before.click()
                        #     sleep(self.TimeClick)

                        # beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                        # before = self.driver.find_element(By.XPATH, beforeXpath)
                        # before.click()
                        # sleep(self.TimeClick)

                        # before_Xpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div/div[1]/span'
                        # before_ = self.driver.find_element(By.XPATH, before_Xpath)
                        # before_.click()
                        # sleep(self.TimeClick)

            else:
                for ind, v in enumerate(val):
                    print(key+' Hedef   Lig   : '+v)
                    ligXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[2]/div[1]/div[1]/div/div[2]/div[1]/div/div/div/div[{}]/div/div[2]'.format(str(ind+1))
                    ligGir   = self.driver.find_element(By.XPATH, ligXpath)
                    ligGir.click()
                    sleep(self.TimeClick)

                    scout_soup_tk=BeautifulSoup(self.driver.page_source,"html.parser")
                    tk = [element.text.strip() for element in scout_soup_tk.find_all( "div", attrs={"class":"gears-list-item aengine-model team","itemkey": True})]
                    frk = [item for item in tk if item not in self.ulusal]
                    print(frk)
                    print(len(frk))
                    for t in frk:
                            self.TAKIMLAR.append(t)
                    TkSayisi = len(frk)
                    for tkm in range(TkSayisi):
                        TakimXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div[{}]/div/div[2]'.format(str(tkm+1))
                        TakimGir   = self.driver.find_element(By.XPATH, TakimXpath)
                        TakimGir.click()
                        sleep(self.TimeClick)
                        
                        scout_soup_tkm=BeautifulSoup(self.driver.page_source,"html.parser")
                        tkmm = [element.text.strip() for element in scout_soup_tkm.find_all( "div", attrs={"id":"detail_0_team_name"})]
                        TkmNameOrjnal = tkmm[0]
                        self.TAKIMLAR_ORJ.append(TkmNameOrjnal)
                        print(TkmNameOrjnal)

                        self.DownLoad()

                        beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(4))
                        before = self.driver.find_element(By.XPATH, beforeXpath)
                        before.click()
                        sleep(self.TimeClick)
                
                    beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(3))
                    before = self.driver.find_element(By.XPATH, beforeXpath)
                    before.click()
                    sleep(self.TimeClick)

            beforeXpath = '/html/body/div[1]/div/div[2]/div[1]/div/div/div/div[1]/div[1]/div/div/div[{}]/div[2]/div[2]/div[1]/a/span[1]'.format(str(2))
            before = self.driver.find_element(By.XPATH, beforeXpath)
            before.click()
            sleep(self.TimeClick)
            self.driver.refresh()
            sleep(self.TimeRefresh)

        cikispath = '/html/body/div[1]/div/div[1]/div[5]/div[2]/div/a/div[2]/h1'
        cikis = self.driver.find_element(By.XPATH, cikispath)
        cikis.click()
        sleep(self.TimeClick)

        KAPATpath = '/html/body/div[13]/div[1]/div/div/div/div[3]/div[2]/a/span[2]'
        kapat = self.driver.find_element(By.XPATH, KAPATpath)
        kapat.click()

        sett = set(self.TAKIMLAR)
        print(sett)
        print('Toplam Takım Sayısı :'+str(len(sett)))


Scrap()