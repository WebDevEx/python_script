import shutil
import tk
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from tkinter import Canvas
from tkinter import *
from tkinter.ttk import *
from bs4 import BeautifulSoup as bs
import requests
import os
from multiprocessing.pool import ThreadPool
import _thread
import pandas as pd
from datetime import date
import datetime
from PIL import Image
import math


def driver1():
    options = Options()
    # options.add_argument("--start-fullscreen")
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--enable-javascript")
    return webdriver.Chrome(chrome_options=options)
driver = driver1()
years_for_search = []
listofauctions=[]
listofmakes=[]
listofmodels=[]
selflotn=[]
class Scrapper:
    def __init__(self,pas,year=None):
        self.pas=pas
        self.year=year
        #self.lot_name=lot_name


    def mkdir(self):
        global path
        path = str(self.year).replace(',','_')+'('+str(date.today())+')'
        global pathresized
        pathresized = path + 'resized'
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)
    def scrap(self):
        self.mkdir()
        global cards
        cards = []
        first_row = driver.find_element_by_xpath('//*[@id="carlist"]').find_element_by_xpath('//*[@id="row1"]').find_element_by_xpath('//*[@id="row1"]/td[2]')
        driver.execute_script("arguments[0].click();", first_row)
        print('CALCULATING RESULTS')
        pagenum = '1'
        try:
            pagenum = str(driver.find_element_by_xpath('//*[@id="detail-pager"]/div/div[2]/div[3]').text).strip('')
        except:
            pass
        counter = []
        count = 0
        while count < int(pagenum[2:]):
            count = count + 1
            counter.append(count)
        ########################################################################################
        #######################################################################################
        print('PAGES TO SCRAP ' + str(count))
        ######################################################
        for number in counter:
            btn_state = driver.find_element_by_xpath('//*[@id="detail-pager"]/div/div[2]/div[3]').text
            try:
                AUCTION_NUM = driver.find_element_by_xpath('//h4[contains(text(),"Number of Times Held")]//following::p').text
            except:
                AUCTION_NUM = ''
            try:
                LOT_NUM = driver.find_element_by_xpath('//h4[contains(text(),"Lot No.")]//following::p').text
            except:
                LOT_NUM = ''
            try:
                YEAR_year = str(driver.find_element_by_xpath('//h4[contains(text(),"Year")]//following::p').text)
                if len(YEAR_year)>4:
                    YEAR=datetime.datetime.strptime(YEAR_year,"%b.%Y").strftime("%m/%y")
                else:
                    YEAR=YEAR_year
                #YEAR=driver.find_element_by_xpath('//h4[contains(text(),"Year")]//following::p').text
            except:
                YEAR = ''
            try:
                MODEL_NAME = str(driver.find_element_by_xpath('//div[@id="detail-name"]/p[2]').get_attribute('innerHTML').strip('<p>&nbsp;').split(' ')[:-1]).strip('[]').replace(',',' ').replace("'","")
            except:
                MODEL_NAME =''
            try:
                GRADE = driver.find_element_by_xpath('//h4[contains(text(),"Grade")]//following::p').text
            except:
                GRADE = ''
            try:
                MODEL = str(driver.find_element_by_xpath('//*[@id="detail-name"]/p[2]').get_attribute('innerHTML').strip('<p>&nbsp;').split(' ')[-1]).split('-')[0]
            except:
                MODEL = ''
            try:
                CC = driver.find_element_by_xpath('//p[contains(text(),"cc")]').text
            except:
                CC = ''
            try:
                REGISTRATION_TIME_date = driver.find_element_by_xpath('//h4[contains(text(),"Holding Date")]//following::p').text
                REGISTRATION_TIME_date_string=str(REGISTRATION_TIME_date).split('.')[0]
                REGISTRATION_TIME=datetime.datetime.strptime(REGISTRATION_TIME_date_string, "%b %d").strftime("%d/%m")
            except:
                REGISTRATION_TIME = ''
            try:
                KM = driver.find_element_by_xpath('//p[contains(text(),"km")]').text
            except:
                KM = ''
            try:
                COLOR = driver.find_element_by_xpath('//h4[contains(text(),"Color")]//following::p').text
            except:
                COLOR = ''
            try:
                TRANSMISSION = driver.find_element_by_xpath('//h4[contains(text(),"Transmission")]//following::p').text
            except:
                TRANSMISSION = ''
            try:
                CONDITIONER = driver.find_element_by_xpath('//h4[contains(text(),"A/C")]//following::p').text
            except:
                CONDITIONER = ''
            try:
                AUDION_GRADE = driver.find_element_by_xpath('//h4[contains(text(),"Score")]//following::p').text
            except:
                AUDION_GRADE = ''
            try:
                EXTERIOR_GRADE = driver.find_element_by_xpath('//h4[contains(text(),"Exterior")]//following::p').text
            except:
                EXTERIOR_GRADE = ''
            try:
                INTERIOR_GRADE = driver.find_element_by_xpath('//h4[contains(text(),"Interior")]//following::p').text
            except:
                INTERIOR_GRADE = ''
            try:
                START_PRICE = driver.find_element_by_xpath('//h4[contains(text(),"Start Price")]//following::p').text
            except:
                START_PRICE = ''
            try:
                AUCTION_DATE_date = driver.find_element_by_xpath('//h4[contains(text(),"Bidding Deadline")]//following::p').text
                AUCTION_DATE_date_string=str(AUCTION_DATE_date).split('.')[0]
                AUCTION_DATE=datetime.datetime.strptime(AUCTION_DATE_date_string, "%b %d").strftime("%d/%m")
            except:
                AUCTION_DATE = ''
            try:
                AUCTION_TIME = driver.find_element_by_xpath('//h4[contains(text(),"Schedule Time")]//following::p').text
            except:
                AUCTION_TIME = ''
            try:
                FINAL_PRICE = driver.find_element_by_xpath('//h4[contains(text(),"Result")]//following::p').text
            except:
                FINAL_PRICE = ''
            try:
                EQUIPMENT = driver.find_element_by_xpath('//h4[contains(text(),"Equipment")]//following::p').text
            except:
                EQUIPMENT = ''
            picsource = driver.find_element_by_xpath('//*[@id="detail-imgs"]').get_attribute('innerHTML')

            PIC = ''
            PIC2 = ''
            PIC3 = ''
            PIC4 = ''
            PICLINK = ''
            PIC2LINK = ''
            PIC3LINK = ''
            PIC4LINK = ''

            try:
                PIC = bs(picsource, "html.parser").findAll('img')[0]['src']
                PICNAME=PIC.split('/')[-1].split('.')[0]
                PICLINK='/auctiondata/AsnetImg/'+PICNAME+'.jpg'
                PIC2 = bs(picsource, "html.parser").findAll('img')[1]['src']
                PIC2NAME=PIC2.split('/')[-1].split('.')[0]
                PIC2LINK='/auctiondata/AsnetImg/'+PIC2NAME+'.jpg'
                PIC3 = bs(picsource, "html.parser").findAll('img')[2]['src']
                PIC3NAME=PIC3.split('/')[-1].split('.')[0]
                PIC3LINK='/auctiondata/AsnetImg/'+PIC3NAME+'.jpg'
                PIC4 = bs(picsource, "html.parser").findAll('img')[3]['src']
                PIC4NAME=PIC4.split('/')[-1].split('.')[0]
                PIC4LINK='/auctiondata/AsnetImg/'+PIC4NAME+'.jpg'
                PICS = [PIC, PIC2, PIC3, PIC4]
                for pic in PICS:
                    img = requests.get(pic)
                    with open(path + "/" + pic.split('/')[-1].split('.')[0] + '.jpg', 'wb') as f:
                        f.write(img.content)
                    foo = Image.open(path + "/" + pic.split('/')[-1].split('.')[0] + '.jpg')
                    x, y = foo.size
                    x2, y2 = math.floor(x - 50), math.floor(y - 20)
                    foo = foo.resize((x2, y2), Image.ANTIALIAS)
                    ############################################
                    try:
                        os.mkdir(path=pathresized)
                    except:
                        pass
                    foo.save(pathresized+ '/' + pic.split('/')[-1].split('.')[0] + '.jpg', quality=50)
            except:
                print('NO 4th PIC')
                PIC4=''
                PICS = [PIC, PIC2, PIC3]
                for pic in PICS:
                    img = requests.get(pic)
                    with open(path + "/" + pic.split('/')[-1].split('.')[0] + '.jpg', 'wb') as f:
                        f.write(img.content)
                    foo = Image.open(path + "/" + pic.split('/')[-1].split('.')[0] + '.jpg')
                    x, y = foo.size
                    x2, y2 = math.floor(x - 50), math.floor(y - 20)
                    foo = foo.resize((x2, y2), Image.ANTIALIAS)
                    ############################################
                    try:
                        os.mkdir(path=pathresized)
                    except:
                        pass
                    foo.save(pathresized + '/' + pic.split('/')[-1].split('.')[0] + '.jpg', quality=50)
            LOT_STATUS=''
            VIN=''
            # VIN=
            # LOT_STATUS=
            card = {
                'AUCTION_NUM': AUCTION_NUM,
                'LOT_NUM': LOT_NUM,
                'YEAR': YEAR,
                'MODEL_NAME': MODEL_NAME,
                'GRADE': GRADE,
                'MODEL': MODEL,
                'CC': CC,
                'REGISTRATION_TIME': REGISTRATION_TIME,
                'KM': KM,
                'COLOR': COLOR,
                'TRANSMISSION': TRANSMISSION,
                'CONDITIONER': CONDITIONER,
                'AUDION_GRADE': AUDION_GRADE,
                'EXTERIOR_GRADE': EXTERIOR_GRADE,
                'INTERIOR_GRADE': INTERIOR_GRADE,
                'START_PRICE': START_PRICE,
                'LOT_STATUS': LOT_STATUS,
                'AUCTION_DATE': AUCTION_DATE,
                'AUCTION_TIME': AUCTION_TIME,
                'FINAL_PRICE': FINAL_PRICE,
                'VIN': VIN,
                'EQUIPMENT': EQUIPMENT,
                'PIC1':PICLINK,
                'PIC2':PIC2LINK,
                'PIC3':PIC3LINK,
                'PIC4':PIC4LINK
            }
            print(card)
            cards.append(card)
            try:
                next_btn = driver.find_element_by_xpath('//*[@id="btn-next"]')
                driver.execute_script("arguments[0].click();", next_btn)
            except:
                pass
            btn_state2 = driver.find_element_by_xpath('//*[@id="detail-pager"]/div/div[2]/div[3]').text
            max_tries = 1000
            while max_tries > 0:
                max_tries -= 1
                if btn_state!=btn_state2:
                    break
                else:
                    try:
                        btn_state2 = driver.find_element_by_xpath('//*[@id="detail-pager"]/div/div[2]/div[3]').text
                    except:
                        pass
    def yearfunc(self):
        y_split = str(self.year).split(',')
        year1 = int(y_split[0])
        year2 = int(y_split[1])
        end = year1
        years_for_search.append(end)
        while end < year2:
            end = end + 1
            years_for_search.append(end)
        select_year=driver.find_element_by_xpath('//*[@id="carlist_head"]/tbody/tr[2]/th[2]/a')
        driver.execute_script("arguments[0].click();", select_year)
        time.sleep(10)
        driver.switch_to.frame(driver.find_element_by_xpath('//*[@id="narrow_iframe"]'))
        for year in years_for_search:
            try:
                selected_year = driver.find_element_by_xpath('//*[@id="filter_content"]').find_element_by_xpath("//label/div[contains(text(),'" + str(year) + "')]")
                driver.execute_script("arguments[0].click();", selected_year)
            except:
                print('NO YEAR ' + str(year))
        driver.switch_to.parent_frame()
        driver.find_element_by_xpath('//*[@id="narrow_button"]').click()
        print('SELECTED YEARS ARE'+str(years_for_search))
        time.sleep(5)
    def login(self):
        #driver.execute_script("document.body.style.zoom='60%'")
        page_url = 'https://www.iauc.co.jp/service/login'
        driver.get(page_url)
        print('LOGING IN')
        login_btn = driver.find_element_by_xpath('//a[contains(@class , "login-btn")]')
        driver.execute_script("arguments[0].click();", login_btn)
        driver.find_element_by_xpath('//*[@id="form_login"]/div[1]/div/input').send_keys('W710679')
        driver.find_element_by_xpath('//*[@id="form_login"]/div[2]/div/input').send_keys(self.pas)
        driver.find_element_by_xpath('//*[@id="login_button"]').click()
        driver.find_element_by_xpath('//*[@id="toggle_lang"]').click()
    def logout(self):
        print('LOGOUT')
        logout=driver.find_element_by_xpath('//*[@id="logout"]')
        driver.execute_script("arguments[0].click();", logout)
        shutil.rmtree(path, ignore_errors=False, onerror=None)
        driver.close()
    def getauc(self):
        self.login()
        print('SCRAPING AUCTIONS')
        allaucs=[]
        today=driver.find_elements_by_xpath('//div[@id="vehicle_day"]/div[1]/div[2]/div/*[@class="day-site-box"]/label')
        for item in today:
            title=item.get_attribute('title')
            allaucs.append(title)
        tomorrow=driver.find_elements_by_xpath('//div[@id="vehicle_day"]/div[2]/div[2]/div/*[@class="day-site-box"]/label')
        for item in tomorrow:
            title=item.get_attribute('title')
            allaucs.append(title)
        dafter=driver.find_elements_by_xpath('//div[@id="vehicle_day"]/div[3]/div[2]/div/*[@class="day-site-box"]/label')
        for item in dafter:
            title=item.get_attribute('title')
            allaucs.append(title)
        return allaucs
    def setauc(self):
        driver.find_element_by_xpath('//*[@id="btn_vehicle_day_clear"]').click()
        driver.find_element_by_xpath('//*[@id="btn_vehicle_everyday_clear"]').click()
        for auc in listofauctions:
            print('SELECTING '+auc)
            try:
                driver.find_element_by_xpath('//div[@id="vehicle_day"]/div[1]/div[2]/div/*[@class="day-site-box"]/label[@title="'+auc+'"]').click()
            except:
                pass
            try:
                driver.find_element_by_xpath('//div[@id="vehicle_day"]/div[2]/div[2]/div/*[@class="day-site-box"]/label[@title="'+auc+'"]').click()
            except:
                pass
            try:
                driver.find_element_by_xpath('//div[@id="vehicle_day"]/div[3]/div[2]/div/*[@class="day-site-box"]/label[@title="'+auc+'"]').click()
            except:
                pass
    def getmake(self):
        self.setauc()
        driver.find_element_by_xpath('//button[contains(@class, "page-next-button")]').click()
        print('SCRAPING MAKE')
        allmakes=[]
        japanese=driver.find_elements_by_xpath('//*[@id="domestic-maker"]/ul/li/div[3]')
        for car in japanese:
            title=car.text
            allmakes.append(title)
        imported=driver.find_elements_by_xpath('//*[@id="foreign-maker"]/ul/li/div[3]')
        for car in imported:
            title=car.text
            allmakes.append(title)
        return allmakes
    def setmake(self):
        for make in listofmakes:
            print('SELECTING '+make)
            try:
                driver.find_element_by_xpath('//*[@id="domestic-maker"]/ul/li/div[.="'+make+'"]').click()
            except:
                pass
            try:
                driver.find_element_by_xpath('//*[@id="foreign-maker"]/ul/li/div[.="' + make + '"]').click()
            except:
                pass
        time.sleep(5)
        models=driver.find_elements_by_xpath('//*[@id="box-type"]/ul/li[contains(@class, "show")]/div[2]/span[1]')
        allmodels=[]
        for model in models:
            title=model.text
            allmodels.append(title)
        return allmodels
    def setmodel(self):
        for model in listofmodels:
            print('SELECTING ' + model)
            try:
                driver.find_element_by_xpath('//*[@id="box-type"]/ul/li[contains(@class, "show")]/div[2]/span[.="'+model+'"]').click()
            except:
                pass
        driver.find_element_by_xpath('//*[@id="next-bottom"]').click()
        self.yearfunc()
        self.scrap()
        self.logout()
        return cards


class GUI:
    def __init__(self):
        pass
    @staticmethod
    def StartGUI():
        def BUTTON1(name):
            if name not in listofauctions:
                listofauctions.append(name)
            v.set(str(listofauctions).strip("[]").replace(",", '\n'))
            print(listofauctions)
        def BUTTON2(name):
            if name not in listofmakes:
                listofmakes.append(name)
            v.set(str(listofmakes).strip("[]").replace(",", '\n'))
            print(listofmakes)
        def BUTTON3(name):
            if name not in listofmodels:
                listofmodels.append(name)
            v.set(str(listofmodels).strip("[]").replace(",", '\n'))
            print(listofmodels)
        def processauc():
            threadp = ThreadPool(processes=1)
            progres.start()
            entery=Scrapper(ent.get(),)
            res = threadp.apply_async(Scrapper.getauc, (entery,))
            return_val = res.get()
            def addcheck():
                global canvas
                canvas = Canvas(window)
                global scroll_y
                scroll_y = Scrollbar(window, orient="vertical", command=canvas.yview)
                frame = Frame(canvas)
                for item in return_val:
                    Button(frame, text=item,command=(lambda x=item:BUTTON1(x))).pack(side=TOP, fill=BOTH)
                canvas.create_window(0, 0, anchor='nw', window=frame)
                canvas.update_idletasks()
                canvas.configure(scrollregion=canvas.bbox('all'),yscrollcommand=scroll_y.set)
                canvas.pack(fill='both', expand=True, side='left')
                scroll_y.pack(fill='y', side='right')
                btngetauc.destroy()
                lable.pack(side=TOP, fill=BOTH)
                btnsetauc.pack(side=TOP, fill=BOTH)
            addcheck()
            progres.stop()
        def processmake():
            threadp = ThreadPool(processes=1)
            progres.start()
            entery = Scrapper(ent.get(), )
            res1 = threadp.apply_async(Scrapper.getmake, (entery,))
            return_val = res1.get()
            frame = Frame(canvas)
            def addcheck():
                for item in return_val:
                    Button(frame, text=item,command=(lambda x=item:BUTTON2(x))).pack(side=TOP, fill=BOTH)
            canvas.create_window(0, 0, anchor='nw', window=frame)
            canvas.update_idletasks()
            addcheck()
            progres.stop()
            btnsetauc.destroy()
            btngetmodel.pack(side=TOP, fill=BOTH)
        def processModel():
            threadp = ThreadPool(processes=1)
            progres.start()
            entery = Scrapper(ent.get(), )
            res1 = threadp.apply_async(Scrapper.setmake, (entery,))
            return_val = res1.get()
            frame = Frame(canvas)

            def addcheck():
                for item in return_val:
                    Button(frame, text=item, command=(lambda x=item: BUTTON3(x))).pack(side=TOP, fill=BOTH)

            canvas.create_window(0, 0, anchor='nw', window=frame)
            canvas.update_idletasks()
            addcheck()
            progres.stop()
            btngetmodel.destroy()
            ent2.pack(side=TOP, fill=BOTH)
            ent2.insert(0, "Year")
            btn.pack(side=TOP, fill=BOTH)
        def processScrap():
            threadp = ThreadPool(processes=1)
            progres.start()
            entery = Scrapper(ent.get(), year=ent2.get())
            res4 = threadp.apply_async(Scrapper.setmodel, (entery,))
            canvas.destroy()
            lable.destroy()
            btn.destroy()
            return_val = res4.get()
            df = pd.DataFrame(return_val)
            global df_forexpor
            df_forexpor = df
            export()
            progres.stop()
        def Launchauc():
            _thread.start_new_thread(processauc, ())
        def LaunchMake():
            _thread.start_new_thread(processmake, ())
            canvas.delete("all")
        def LaunchModel():
            _thread.start_new_thread(processModel, ())
            canvas.delete("all")
        def LaunchScrap():
            _thread.start_new_thread(processScrap, ())
            canvas.delete("all")
        def export():
            df_forexpor.to_csv(str(ent2.get()).replace(',','_')+'('+str(date.today())+')' + '.csv',index=False,encoding="utf_8_sig")

        window = Tk()
        window.title('Scrap')
        window.resizable(height=None, width=None)
        v = StringVar()
        """Start Window"""
        ent = Entry(window, width=10)
        ent.pack(side=TOP, fill=BOTH)
        ent.insert(0, "Password")
        btngetauc = Button(window, text="Get Auctions", command=Launchauc)
        btngetauc.pack(side=TOP, fill=BOTH)
        progres = Progressbar(window, orient='horizontal', length=10)
        progres.pack(side=TOP, fill=BOTH)
        """Second Window"""
        btnsetauc= Button(window, text="Next", command=LaunchMake)
        lable = Message(window, textvariable=v)
        """Third Screen"""
        btngetmodel=Button(window, text="Next", command=LaunchModel)
        """Forth Screen"""
        ent2 = Entry(window, width=10)
        btn = Button(window, text="Start", command=LaunchScrap)
        window.mainloop()
GUI.StartGUI()


