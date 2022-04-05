import pdfplumber
import csv
import numpy as np
from PIL import Image
import os
import img2pdf
import pandas as pd


def convert_pdf_to_csv(mode, filename):
    # convert pdf to mc calandar pdf to csv file
    with pdfplumber.open(filename + '.pdf') as f:
        for page in f.pages:
            tables = page.extract_tables()
            if len(tables) != 1 and mode == 'cal':
                tables.pop()
            for table in tables:
                data = pd.DataFrame(table[1:], columns=table[0])
                data.to_csv(filename + '.csv', mode='a', encoding="ANSI")


def preprocess_csv(filename):
    with open(filename) as fhandle:
        reader = csv.reader(fhandle)
        lt = []
        for row in reader:
            lt.append(row)
    lt.pop(0)
    for i in range(len(lt)):
        for j in range(len(lt[i])):
            lt[i][j] = lt[i][j].replace('\n', '')

    return lt


def get_days_dict(lt):
    cal = {}
    for i in range(3, len(lt[0])):
        prog = lt[0][i].split('/')
        td = [(lt[a][2], lt[a][i]) for a in range(len(lt))]
        td.pop(0)
        for p in prog:
            cal[p] = td
    '''for k,c in cal.items():
        print(k,c)'''
    btech = cal['B. Tech.']
    days = {}
    for it in btech:
        if not (len(it[1]) == 0 or it[1] == '-'):
            try:
                temp = int(it[1])
                days[it[0]] = days.get(it[0], 0) + 1
            except:
                if it[1] == 'CIA I (I Yr)' or it[1] == 'CIA II (I Year)' or it[
                        1] == 'CIA III (I Yr)':
                    days[it[0]] = days.get(it[0], 0) + 1

    print(sum(days.values()))
    #print(days)
    return days


def convert_img_to_pdf(filename):
    img_path = filename + '.png'

    pdf_path = filename + '.pdf'

    image = Image.open(img_path)

    pdf_bytes = img2pdf.convert(image.filename)

    file = open(pdf_path, "wb")

    file.write(pdf_bytes)

    image.close()

    file.close()


def main():
    os.remove('MC-Calandar_2021-22.csv')
    convert_pdf_to_csv('cal', 'MC-Calandar_2021-22')
    lt = preprocess_csv('MC-Calandar_2021-22.csv')
    days = get_days_dict(lt)
    #print(days)
    convert_img_to_pdf('time_table')


if __name__ == '__main__':
    main()
