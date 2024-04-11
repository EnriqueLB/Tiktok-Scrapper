from TikTokApi import TikTokApi
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
import time
import json
import threading
import re
from src.database import crear_registro, leer_registros
from src.waitElement import waitElement, waitElements
from datetime import datetime
from anticopyright import *


# Set the browser driver
def set_driver(headless=False):
    driver = None
    # get current user
    user = os.getlogin()
    user_profile = r'C://Users//' + user + r'//AppData//Local//Google//Chrome//User Data'
    print(user_profile)
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument('headless')
    options.add_argument("--user-data-dir=" + user_profile)
    driver = webdriver.Chrome(r'C:\scrap\chromedriver.exe', options=options)
    return driver

def inputText(driver, listURL):
    def createDirectory():
        # Crear una cadena de texto con el formato de la fecha
        fecha_str = datetime.now().strftime("%Y-%m-%d")
        # Crear el directorio
        if not os.path.exists("tiktoks/" + fecha_str):
            os.mkdir("tiktoks/" + fecha_str)
        return fecha_str
        

    folderName = createDirectory() # create directory

    def downloadFile(tiktokURL, filename):
        r = requests.get(tiktokURL, allow_redirects=True)
        open(f'tiktoks/{folderName}/{filename}.mp4', 'wb').write(r.content)

    # Navigate to the OpenAI chat page
    driver.get("https://douyin.wtf/")
    time.sleep(5)  # Wait for the page to load
    textarea = waitElement(driver, '.input-container > .form-group textarea', 30, By.CSS_SELECTOR)
    textarea.click()
    for lista in listURL:
        textarea.send_keys(lista["url"]+"\n")     

    waitElement(driver, 'button[type=submit]', 20, By.CSS_SELECTOR).click()
        
    #Esperar todos los videos
    time.sleep(6)
    checked = []
    while True:
        elementos = None
        try:
            # elementos = driver.find_elements(By.XPATH, "//*/div[2]/table/tbody/tr[6]/td[2]/a")
            elementos = driver.find_elements(By.CSS_SELECTOR, "[id*=pywebio-scope] table")
            if len(checked) == len(listURL):
                print("Descargas terminadas, procesando videos")
                driver.quit()
                ruta = f'{os.getcwd()}\\tiktoks\{folderName}'
                procesarVideos(ruta) # COPYRIGHT
                return

            for children in elementos:
                titkokID = waitElement(children, "tr:nth-child(4) td:nth-child(2) > span", 20, By.CSS_SELECTOR).text
                
                if not titkokID in checked:
                    checked.append(titkokID)
                    titkokURL = waitElement(children, "tr:nth-child(6) > td:nth-child(2) > a", 10, By.CSS_SELECTOR).get_attribute("href")
                    print("Descargando tiktok ID:", titkokID)
                    titkokURL = waitElement(children, "tr:nth-child(6) > td:nth-child(2) > a", 10, By.CSS_SELECTOR).get_attribute("href")
                    hilo = threading.Thread(target=downloadFile, args=(titkokURL, titkokID))
                    hilo.start()
                    hilo.join()
                    for tiktok in listURL:
                        if tiktok["id"] == titkokID:
                            crear_registro(f"INSERT INTO video(idVideo, idUser, URL, description, hashtags, plays, likes, comments, shares, duration, date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s)", *tiktok["args"])
                            break



        except:
            time.sleep(1)
            # if int(waitElements(driver, '//*[@id="pywebio-scope-result"]/pre[2]/code', 30, By.XPATH)) + len(checked) == len(listURL):
            #     print("Descargas terminadas con algunos tiktoks fallidos")
            #     break
            print("elemento no encontrado")

def timeFormat(segundos):
    # Calcular horas, minutos y segundos
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = (segundos % 3600) % 60
    tiempo_formateado = "{:02d}:{:02d}:{:02d}".format(horas, minutos, segundos)
    return tiempo_formateado

def getTrendingVideos():
    verifyFp="verify_lgefovzj_tvbhLAjm_2jOd_4hhc_Byrh_CvMfARcSeccU"
    listURLS = []
    with TikTokApi(custom_verify_fp=verifyFp) as api:
        for trending_video in api.trending.videos(count=90):
            if len(listURLS) >= 23: break # demasiados videos, dejar de registrar a partir de los 23
            if trending_video.stats["diggCount"] < 150000 or trending_video.as_dict["video"]["duration"] > 60: # IGNORAR VIDEOS CON MENOS DE 20K DE LIKES Y QUE DUREN MAS DE 200 SEGUNDSO
                continue
            user_id = trending_video.author.user_id
            username = trending_video.author.username
            tiktok_id = trending_video.id 
            comments_count = trending_video.stats["commentCount"]
            likes_count = trending_video.stats["diggCount"]
            play_count = trending_video.stats["playCount"]
            share_count = trending_video.stats["shareCount"]
            hashtags = [hashtag.name for hashtag in trending_video.hashtags]
            joinHashtags = ",".join(hashtags)
            description = trending_video.as_dict["desc"] or ""
            description = re.sub(r'[@#]\w+', '', description)
            description = f"{description}@ {username}".strip()
            url = f"https://www.tiktok.com/@{username}/video/{tiktok_id}"
            duration = timeFormat(trending_video.as_dict["video"]["duration"]) 
            

            if not leer_registros(f"SELECT idVideo FROM video WHERE idVideo ='{tiktok_id}'"):
                if not leer_registros(f"SELECT * FROM user WHERE idUser = '{user_id}'"):
                    crear_registro(f"INSERT INTO user (idUser, username) VALUES ('{user_id}','{username}')")
                args = [tiktok_id, user_id, url, description, joinHashtags, play_count, likes_count, comments_count, share_count, duration, datetime.today().strftime('%Y-%m-%d %H:%M:%S')]
                listURLS.append({"url": url, "hashtags": hashtags, "id": tiktok_id, "args": args})

    print("Lista de tiktoks generada...")
    return listURLS


if __name__ == "__main__":
    listURLS = getTrendingVideos()
    driver = set_driver()
    inputText(driver, listURLS)
 
