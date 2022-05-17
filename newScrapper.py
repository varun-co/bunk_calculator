from base64 import urlsafe_b64decode
from selenium import webdriver
from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import tkinter as tk
import os
import shutil
from selenium.webdriver.chrome.options import Options
import math

#from os import wait
import time
from PIL import ImageTk, Image
import threading
import queue
from bunk_calculator import *
import re
import numpy as np

class scrapper :
    def __init__(self,url):
        self.url = url
        chrome_options = Options()
        chrome_options.add_argument("--silent")
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option('excludeSwitches',
                                            ['enable-logging'])
        if os.name =='nt':
            self.driver = webdriver.Chrome(options=chrome_options)
        elif os.name == 'posix':
            dir_path = os.path.dirname(os.path.realpath(__file__))
            execpath= dir_path+'/chromedriver'
            self.driver = webdriver.Chrome(executable_path=execpath,options=chrome_options)
        self.page = self.driver.get(url)
        self.captchaPath = 'static/image/cap.png'
        img = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="imgCaptcha"]')))
        img.click()
        time.sleep(1)
        img.screenshot('static/images/cap.png')
        print('done')
    def getTimeTable(self,reg_no,password,cap):
        
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="txtRegNumber"]'))).send_keys(reg_no)
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="txtPwd"]'))).send_keys(password)
        '''img = driver.find_element_by_xpath('//*[@id="imgCaptcha"]')
        img.click()
        time.sleep(1)
        img.screenshot('cap.png')
        #cap = ocr.get_captahca('cap.png') 
        # que = queue.Queue()

        t1 = threading.Thread(target=capt)
        t1.start()
        cap = input('Enter the captcha: ')
        #print(cap) '''
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="answer"]'))).send_keys(cap)
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="frmLogin"]/div[3]/table/tbody/tr[6]/td/input'))).click()
        try:
            #time.sleep(0.5)
            WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="masterdiv"]/div[6]/a/font'))).click()
        except:
            self.driver.close()
            return (False,False)
        #timetable = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="courseDetails"]/tbody/tr')))

        cols = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="courseDetails"]/tbody/tr[3]/td')))
        timetable = []
        for i in range(2, 9):
            timetable.append([])
            for j in range(1, 12):
                s = WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="courseDetails"]/tbody/tr[' + str(i) + ']/td[' +
                    str(j) + ']'))).text
                timetable[i - 2].append(s)
        #print(tt)
        for i, t in enumerate(timetable):
            for j, t2 in enumerate(t):
                if ',' in timetable[i][j]:
                    if j != 0:
                        if ',' in timetable[i][j - 1]:
                            print(timetable[i][j])
                            timetable[i][j] = timetable[i][j - 1]
        dt = {}
        for i in range(1, len(timetable)):
            for j in range(1, len(timetable[i])):
                if timetable[i][j] != '':
                    dt[timetable[i][j]] = dt.get(timetable[i][j], {})
                    dt[timetable[i][j]][timetable[i][0]] = dt[timetable[i][j]].get(
                        timetable[i][0], 0) + 1
        for t in timetable:
            print(*t, sep='\t')
        try:
            os.remove('MC-Calandar_2021-22.csv')
        except:
            pass
        convert_pdf_to_csv('cal', 'MC-Calandar_2021-22')
        lt = preprocess_csv('MC-Calandar_2021-22.csv')
       
        days = get_days_dict(lt)
        print(days)
        days['Wed'] = days['Wed'] - 1
        final = {}
        for key in dt.keys():
            for key2 in dt[key].keys():
                final[key] = final.get(key, {})
                final[key][key2] = dt[key][key2] * days[key2]

        final = {k: sum(v.values()) for k, v in final.items()}
        print(final)
        '''crscode = {}
        for i in range(2, 8):
            cc = driver.find_element_by_xpath(
                '//*[@id="frmStudentTimetable"]/table/tbody/tr[4]/td/table/tbody/tr['
                + str(i) + ']').text
            crscode[cc[0:6]] = cc[7:].split(' ')
        print(crscode)
        list1 = list(set(crscode.keys()))
        day = {}
        section = 'C'
        for i in tt.keys():
            day[i] = []

            for j in list1:
                if str(j) + "-" + str(section) in tt[i]:
                    day[i].append((j, 1))
        print(list1)
        print(day)


        time.sleep(5)
        #print(timetable)
        t1.join()
        time.sleep(30) '''
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="masterdiv"]/div[11]/a/font'))).click()
        r = len(WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="form01"]/table[1]/tbody/tr'))))
        c = len(WebDriverWait(self.driver,10).until(EC.presence_of_all_elements_located((By.XPATH,'//*[@id="form01"]/table[1]/tbody/tr[5]/td'))))
        section = list(final.keys())[0][-1:]
        print(section)
        print(r, c)
        attendance_marked = []
        for i in range(2, r):
            attendance_marked.append([])
            for k in range(1, c):
                ele = self.driver.find_element_by_xpath(
                    '//*[@id="form01"]/table[1]/tbody/tr[' + str(i) + ']/td[' +
                    str(k) + ']').text
                attendance_marked[i - 2].append(ele)
        for a in attendance_marked:
            print(*a)
        print('Subject', 'total', 'Marked', 'Absent', 'bunks_left', sep='\t')
        sum_bunk = 0
        result = []
        for i in range(1, len(attendance_marked)):
            temp = attendance_marked[i][0]
            res = None
            for key in final.keys():
                pattern = f'^{temp}'
                if re.search(pattern, key) != None:
                    res = key
                    break
            print(attendance_marked[i][0][:6],
                final[key],
                attendance_marked[i][2],
                attendance_marked[i][4],
                math.floor((final[key] / 5) - int(attendance_marked[i][4])),
                sep='\t')
            result.append([attendance_marked[i][0],attendance_marked[i][1],final[key],attendance_marked[i][2],attendance_marked[i][3],round(int(attendance_marked[i][3])*100/int(attendance_marked[i][2]),2),attendance_marked[i][4],math.floor((final[key]/5) - int(attendance_marked[i][4]))])
            sum_bunk += math.floor(final[key] / 5) - int(attendance_marked[i][4])
        
        totalClasses , totalMarked ,totalPresent, totalBunk ,totalBunkleft,totalpercent = 0,0,0,0,0,0
        for i in range(0,len(result)):
            totalClasses += int(result[i][2])
            totalMarked += int(result[i][3])
            totalPresent += int(result[i][4])
            totalpercent += int(result[i][5])
            totalBunk += int(result[i][6])
            totalBunkleft += int(result[i][7])
        totalpercent = totalpercent/len(result)
        print('total bunks left:', sum_bunk)
        # convert into a two 2d list 
        shutil.copy('static/images/cap.png',os.path.join('captcha',cap +'.png'))
        return result,(totalClasses,totalMarked,totalPresent,round(totalpercent,2),totalBunk,totalBunkleft)
        time.sleep(5)
        self.driver.close()

