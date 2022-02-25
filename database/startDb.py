from utils import utils
from objects import SaoMdObjects
import sqlite3
import os
import cv2
import time
import csv

def connectToDb(path):
    con = sqlite3.connect(path)
    return con

def createTables(con):
    cursor = con.cursor()
    cursor
    cursor.execute('''CREATE TABLE IF NOT EXISTS weapon(
        id integer,
        weapon text,
        PRIMARY KEY (id))''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS element(
        id integer,
        weapon text,
        PRIMARY KEY (id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS chara(
        id integer,
        charaName text,
        unitName text,
        rarity integer,
        weapon text,
        element text,
        hp integer,
        mp integer,
        atk integer,
        def integer,
        crit integer,
        swordSkills text,
        battleSkills text,
        specialSkills text,
        upgradedStats text,
        picUrls text,
        PRIMARY KEY (id))''')

def insert_stuff(con, stuffList, tableName):
    cursor = con.cursor()
    for thing in stuffList:
        cursor.execute(
            f'INSERT INTO {tableName} values (?,?)', [thing[0],thing[1]]
        )
    con.commit()


def insert_character(con,chara:SaoMdObjects.Chara):
    cursor = con.cursor()
    data = chara.to_db()
    cursor.execute(
            'insert into chara values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
def manage_exceptions(data):
    out = []
    for chara in data:
        updatedChara = chara
        if chara.unitName == '[Dual Pen Cartoonist]' and int(chara.id) == 0:
            updatedChara.id = 1
        out.append(updatedChara)
    return out

def createCSV(filePath,columns,content):
  with open(filePath,'w',newline='', encoding="utf8") as f:
      write = csv.writer(f)
      write.writerow(columns)
      write.writerows(content)

async def get_chara_pics_url(folderPath,channel,csvPath):
    urls = []
    for filename in os.listdir(folderPath):
        if filename.endswith('.png'):
            msg = await utils.send_img(None,channel=channel,inPath=os.path.join(folderPath,filename))
            urls.append((filename[:-4],msg.attachments[0].url))
            time.sleep(0.5)
    createCSV(csvPath,['file','url'],urls)

def load_pics_from_csv(CSVpath):
    data = utils.loadCSV(CSVpath,delimiter=',')
    out={}
    for chara,url in sorted(data):
        chara = str(chara)
        if chara.count('_')>1:
            out[chara[:-2]].append(url)
        else:
            out[chara]=[url]
    return out



def start_db(con,csvPath = None,picsPath=None):
    if csvPath and picsPath:
        data = []
        pics = load_pics_from_csv(picsPath)
        for line in utils.loadCSV(csvPath,delimiter=';'):
            pic = pics.get(f'character_{int(line[0])}')
            if not pic:
                pic = pics['no_image']
            data.append(SaoMdObjects.Chara.from_csv_line(line,pic))
    else:
        return
    data = manage_exceptions(data)
    createTables(con)
    for chara in data:
        insert_character(con,chara)
    con.commit()


    






