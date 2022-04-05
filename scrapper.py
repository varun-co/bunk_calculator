from selenium.webdriver.common import by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
import tkinter as tk
#from os import wait
import time
import ocr
from selenium import webdriver
from PIL import ImageTk, Image
import threading
import queue
from bunk_calculator import *


#from Screenshot import Screenshot_clipping
def capt():

    window = tk.Tk()
    window.geometry("500x300")
    frame = tk.Frame(window)
    frame.pack()
    img = ImageTk.PhotoImage(Image.open("cap.png"))
    label = tk.Label(frame, image=img)
    label.pack(ipadx=10, ipady=20)
    window.mainloop()


def get_time_table(reg_no, password):
    url = 'https://webstream.sastra.edu/sastraparentweb/'
    driver = webdriver.Chrome()
    page = driver.get(url)
    driver.find_element_by_xpath('//*[@id="txtRegNumber"]').send_keys(reg_no)
    driver.find_element_by_xpath('//*[@id="txtPwd"]').send_keys(password)
    img = driver.find_element_by_xpath('//*[@id="imgCaptcha"]')
    img.click()
    time.sleep(1)
    img.screenshot('cap.png')
    #cap = ocr.get_captahca('cap.png')
    que = queue.Queue()

    t1 = threading.Thread(target=capt)
    t1.start()
    cap = input('Enter the captcha')
    #print(cap)
    captcha = driver.find_element_by_xpath('//*[@id="answer"]').send_keys(cap)
    driver.find_element_by_xpath(
        '//*[@id="frmLogin"]/div[3]/table/tbody/tr[6]/td/input').click()
    time.sleep(5)
    try:
        driver.find_element_by_xpath(
            '//*[@id="masterdiv"]/div[6]/a/font').click()
    except:
        driver.close()
        get_time_table(reg_no, password)
    time.sleep(2)
    timetable = driver.find_elements_by_xpath(
        '//*[@id="courseDetails"]/tbody/tr')
    print(len(timetable))
    rows = len(timetable)

    cols = driver.find_elements_by_xpath(
        '//*[@id="courseDetails"]/tbody/tr[3]/td')
    timetable = []
    for i in range(2, 9):
        timetable.append([])
        for j in range(1, 12):
            s = driver.find_element_by_xpath(
                '//*[@id="courseDetails"]/tbody/tr[' + str(i) + ']/td[' +
                str(j) + ']').text
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
    os.remove('MC-Calandar_2021-22.csv')
    convert_pdf_to_csv('cal', 'MC-Calandar_2021-22')
    lt = preprocess_csv('MC-Calandar_2021-22.csv')
    days = get_days_dict(lt)
    print(days)
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
    driver.find_element_by_xpath('//*[@id="masterdiv"]/div[11]/a/font').click()
    time.sleep(3)
    r = len(
        driver.find_elements_by_xpath('//*[@id="form01"]/table[1]/tbody/tr'))
    c = len(
        driver.find_elements_by_xpath(
            '//*[@id="form01"]/table[1]/tbody/tr[5]/td'))
    section = list(final.keys())[0][-1:]
    print(section)
    print(r, c)
    attendance_marked = []
    for i in range(2, r):
        attendance_marked.append([])
        for k in range(1, c):
            ele = driver.find_element_by_xpath(
                '//*[@id="form01"]/table[1]/tbody/tr[' + str(i) + ']/td[' +
                str(k) + ']').text
            attendance_marked[i - 2].append(ele)
    for a in attendance_marked:
        print(*a)
    print('Subject', 'total', 'Marked', 'Absent', 'bunks_left', sep='\t')
    for i in range(1, len(attendance_marked)):
        print(attendance_marked[i][0],
              final[attendance_marked[i][0] + '-' + section],
              attendance_marked[i][2],
              attendance_marked[i][4],
              (final[attendance_marked[i][0] + '-' + section] / 5) -
              int(attendance_marked[i][4]),
              sep='\t')

    time.sleep(5)
    driver.close()
    return dt


# giver register no and password

get_time_table('123004270', '13122001')