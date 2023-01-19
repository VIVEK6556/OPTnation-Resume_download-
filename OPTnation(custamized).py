import codecs
import os
from datetime import date
from datetime import date as dt
import time
import json
from bs4 import BeautifulSoup
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from driver import get_options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
class Optnation:
    def login(self):
        self.options=int(input("Details_scraping-1\nDownload_pages-2\nLink_Scraping-3\nSelect your above options:"))
        self.path=input('Result destination folder:')
        options = get_options("testing1")
        cs = service.Service(executable_path="driver/chromedriver.exe")
        self.driver = webdriver.ChromiumDriver(service=cs, browser_name="chrome", vendor_prefix="GC", options=options, )
        self.driver.get('https://www.optnation.com/employers-login')
        time.sleep(2)
        WebDriverWait(self.driver,30).until(Ec.presence_of_element_located((By.ID,'username'))).send_keys('akshay@advaana.com',Keys.TAB)
        WebDriverWait(self.driver,30).until(Ec.presence_of_element_located((By.ID,'password'))).send_keys('Adva2022Bug@',Keys.ENTER)
        WebDriverWait(self.driver,30).until(Ec.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[2]/div[2]/nav/div/div[2]/ul/li[1]'))).click()
        WebDriverWait(self.driver, 30).until(Ec.presence_of_element_located((By.XPATH, '/html/body/div/div[1]/div[3]/div/form/input[3]'))).click()
        if self.options==1:
            self.Link_Scraping()
        elif self.options==2:
            self.Download_Links()
        elif self.options==3:
            self.url_Scraping()
        else:
            print("*****Selected_wrong_option*****")
            self.driver.close()
            self.login()
    def Link_Scraping(self):
        number_of_links=int(input("Number_of_details:"))/10
        if os.path.isfile('' + self.path + '' + str(dt.today()) + '.xlsx') == False:
            last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
                new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                if new_Hieght == last_Hieght:
                    break
                last_Hieght = new_Hieght
            read = open('Counter.json', 'r')
            data = read.read()
            load = json.loads(data)
            self.details_cnt = load['cnt']
            if self.details_cnt != 0:
                last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                while True:
                    self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                    time.sleep(2)
                    new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                    if new_Hieght == last_Hieght:
                        break
                    last_Hieght = new_Hieght
                j = 0
                while j != self.details_cnt:
                    button = WebDriverWait(self.driver, 30).until(Ec.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
                    last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                    while True:
                        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                        time.sleep(2)
                        new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                        if new_Hieght == last_Hieght:
                            break
                        last_Hieght = new_Hieght
                    j += 1
            else:
                pass
            self.url_lst = []
            self.date = []
            cnt=0
            while cnt<number_of_links:
                soup=BeautifulSoup(self.driver.page_source,'lxml')
                link=soup.find_all('div',{'class':'job_cent_boxft resume_cent_boxft'})
                for i in link:
                    url=i.findNext('a').get('href')
                    date=i.findNext('p').text
                    self.date.append(date)
                    self.url_lst.append(url)
                self.details_cnt+=1
                cnt+=1
                button=WebDriverWait(self.driver,30).until(Ec.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(10)
            with open('Counter.json') as f:
                data = json.load(f)
                data["cnt"] =self.details_cnt
                with open('Counter.json', 'w') as f:
                    json.dump(data, f)
        else:
            print('ok')
            last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
                new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                if new_Hieght == last_Hieght:
                    break
                last_Hieght = new_Hieght
            self.url_lst = []
            self.date = []
            cnt = 0
            while cnt < number_of_links:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                link = soup.find_all('div', {'class': 'job_cent_boxft resume_cent_boxft'})
                for i in link:
                    url = i.findNext('a').get('href')
                    date = i.findNext('p').text
                    self.date.append(date)
                    self.url_lst.append(url)
                cnt += 1
                button = WebDriverWait(self.driver, 30).until(Ec.presence_of_element_located(
                    (By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(10)
        self.Details_Scraping()
    def Details_Scraping(self):
        df = pd.DataFrame({"URL":[''],"Name":[''],"Address":[''],"Email":[''],"Phone":[''],"Work Authorization":[''],
                           "Expected Salary":[''],"Designation":[''],"Key Skills":[''],"Degree":[''],"College/University":[''],
                           "City":[''],"Started":[''],"Ending":[''],'Applied_Date':['']})
        for i,j in zip(self.url_lst,self.date):
            self.driver.get('https://www.optnation.com/'+i+'')
            soup=BeautifulSoup(self.driver.page_source,'lxml')
            link='https://www.optnation.com/'+i+''
            basic_details=soup.find('div',{'class':'view_resumepage_header'})
            name=basic_details.find('h1').text
            address=basic_details.find_all('p')[0].text
            mail_id=basic_details.find_all('p')[1].text
            contact_no=basic_details.find_all('p')[2].text
            work_details=soup.find('div',{'class':'view_resume_work'})
            work_authorization_=work_details.find('h4')
            work_authorization=work_authorization_.find('span').text
            expected_Salary_=work_details.find('h3')
            expected_salary=expected_Salary_.find('span').text
            designation_=work_details.find_all('p')[0]
            designation=designation_.findNext('span').text
            key_skills_= work_details.find_all('p')[1]
            key_skills=key_skills_.findNext('span').text
            education_details_=soup.find('div',{'class':'view_resume_edu'})
            education_details=education_details_.find_all('tr')[1]
            degree=education_details.find_all('td')[0].text
            college_university=education_details.find_all('td')[1].text
            city=education_details.find_all('td')[2].text
            started=education_details.find_all('td')[3].text
            ending=education_details.find_all('td')[4].text
            df = df.append(
                {"URL":link, "Name":name, "Address": address, "Email": mail_id, "Phone": contact_no, "Work Authorization": work_authorization,
                 "Expected Salary": expected_salary, "Designation": designation, "Key Skills": key_skills, "Degree": degree,"College/University":college_university,
                 "City": city, "Started": started, "Ending": ending, 'Applied_Date': j},ignore_index=True)
        df.to_excel(''+self.path+''+str(date.today())+'.xlsx')
    def url_Scraping(self):
        number_of_links = int(input("Number_of_links:")) / 10
        if os.path.isfile(''+self.path+''+str(date.today())+'_url.xlsx')== False:
            last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
                new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                if new_Hieght == last_Hieght:
                    break
                last_Hieght = new_Hieght
            read = open('Counter.json', 'r')
            data = read.read()
            load = json.loads(data)
            self.url_cnt = load['cnt_1']
            if self.url_cnt != 0:
                last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                while True:
                    self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                    time.sleep(2)
                    new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                    if new_Hieght == last_Hieght:
                        break
                    last_Hieght = new_Hieght
                j = 0
                while j != self.url_cnt:
                    button = WebDriverWait(self.driver, 30).until(Ec.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
                    last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                    while True:
                        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                        time.sleep(2)
                        new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                        if new_Hieght == last_Hieght:
                            break
                        last_Hieght = new_Hieght
                    j += 1
            else:
                pass
            self.url_lst = []
            cnt = 0
            fd = pd.DataFrame({"URL": [''], "Page": ['']})
            while cnt<number_of_links:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                link = soup.find_all('div', {'class': 'job_cent_boxft resume_cent_boxft'})
                for i in link:
                    url = i.findNext('a').get('href')
                    link = 'https://www.optnation.com/' +url+ ''
                    fd = fd.append({"URL": link, "Page": cnt+1}, ignore_index=True)
                self.url_cnt+=1
                cnt += 1
                button = WebDriverWait(self.driver, 30).until(
                    Ec.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(10)
            with open('Counter.json') as f:
                data = json.load(f)
                data["cnt_1"] = self.url_cnt
                with open('Counter.json', 'w') as f:
                    json.dump(data, f)
        else:
            last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
                new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                if new_Hieght == last_Hieght:
                    break
                last_Hieght = new_Hieght
            self.url_lst = []
            cnt = 0
            fd = pd.DataFrame({"URL": [''], "Page": ['']})
            while cnt < number_of_links:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                link = soup.find_all('div', {'class': 'job_cent_boxft resume_cent_boxft'})
                for i in link:
                    url = i.findNext('a').get('href')
                    link = 'https://www.optnation.com/' + url + ''
                    fd = fd.append({"URL": link, "Page": cnt + 1}, ignore_index=True)
                cnt += 1
                button = WebDriverWait(self.driver, 30).until(
                    Ec.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(10)
            fd.to_excel('' + self.path + '' + str(date.today()) + '_url.xlsx')
    def Download_Links(self):
        download_link=int(input("Enter the no of resumes:"))/10
        if not os.path.exists('' + self.path + '' + 'Download_pages/' + '' + str(dt.today())):
            try:
                if not os.path.exists('' + self.path + '' + 'Download_pages/' + '' + str(dt.today())):
                    os.makedirs('' + self.path + '' + 'Download_pages/' + '' + str(dt.today()))
            except OSError:
                print('Error:Creating directory.' + ('' + self.path + '' + str(dt.today())))
            read = open('Counter.json', 'r')
            data = read.read()
            load = json.loads(data)
            self.cnt= load['cnt_2']
            if self.cnt != 0:
                last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                while True:
                    self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                    time.sleep(2)
                    new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                    if new_Hieght == last_Hieght:
                        break
                    last_Hieght = new_Hieght
                j = 0
                while j != self.cnt:
                    button = WebDriverWait(self.driver, 30).until(Ec.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                    self.driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
                    last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                    while True:
                        self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                        time.sleep(2)
                        new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                        if new_Hieght == last_Hieght:
                            break
                        last_Hieght = new_Hieght
                    j += 1
            else:
                pass
            last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
                new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                if new_Hieght == last_Hieght:
                    break
                last_Hieght = new_Hieght
            self.url_lst = []
            cnt=0
            while cnt < download_link:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                link = soup.find_all('div', {'class': 'job_cent_boxft resume_cent_boxft'})
                for i in link:
                    url = i.findNext('a').get('href')
                    self.url_lst.append(url)
                self.cnt += 1
                cnt+=1
                button = WebDriverWait(self.driver, 30).until(
                    Ec.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(10)
            with open('Counter.json') as f:
                data = json.load(f)
                data["cnt_2"] = self.cnt
                with open('Counter.json', 'w') as f:
                    json.dump(data, f)
        else:
            last_Hieght = self.driver.execute_script('return document.body.scrollHeight')
            while True:
                self.driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                time.sleep(2)
                new_Hieght = self.driver.execute_script('return document.body.scrollHeight')
                if new_Hieght == last_Hieght:
                    break
                last_Hieght = new_Hieght
            self.url_lst = []
            cnt = 0
            while cnt < download_link:
                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                link = soup.find_all('div', {'class': 'job_cent_boxft resume_cent_boxft'})
                for i in link:
                    url = i.findNext('a').get('href')
                    self.url_lst.append(url)
                cnt += 1
                button = WebDriverWait(self.driver, 30).until(
                    Ec.presence_of_element_located(
                        (By.XPATH, '/html/body/div[3]/div[4]/div/div/div[1]/div[15]/ul/li[3]')))
                self.driver.execute_script("arguments[0].click();", button)
                time.sleep(10)
        self.Download_pages()
    def Download_pages(self):
        for i in self.url_lst:
            self.driver.get('https://www.optnation.com/' + i + '')
            file_name = i.split("-", )[-1]
            download_path = os.path.join('' + self.path +''+'Download_pages/'+'' + str(dt.today()), '' + file_name + '.html')
            file_open = codecs.open(download_path, "w", "utf−8")
            page_source = self.driver.page_source
            file_open.write(page_source)
object=Optnation()
object.login()

