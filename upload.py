
from src.database import crear_registro, leer_registros, leer_registro
from src.waitElement import waitElement, waitElements
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import tkinter as tk
import os
from tkinter import filedialog
from moviepy.video.io.VideoFileClip import VideoFileClip
import math
import time
import pyperclip
import threading
from datetime import datetime


class Estado:
    def __init__(self):
        self.upload_youtube = True
        self.upload_instagram = True
        self.upload_facebook = True
status = Estado()
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
    options.add_argument("--disable-popup-blocking")
    options.add_argument("--mute-audio")
    driver = webdriver.Chrome(r'C:\scrap\chromedriver.exe', options=options)
    return driver

def uploadVideoYoutube(driver, filePath, idVideo, title, hashtags):
    pyperclip.copy(title)
    #Get information about video
    driver.get("https://studio.youtube.com/")
    time.sleep(5)
    waitElement(driver, '#create-icon', 30, By.CSS_SELECTOR).click()
    waitElement(driver, '#text-item-0', 10, By.CSS_SELECTOR).click()
    time.sleep(2)
    #Upload video
    waitElement(driver, '//input[@type="file"]', 30, By.XPATH).send_keys(filePath)
    #Set title
    titleVideo = waitElement(driver, '#title-textarea #textbox', 180, By.CSS_SELECTOR)
    #Verify limit
    errorShort = waitElement(driver, 'div .error-short', 1, By.CSS_SELECTOR)
    if errorShort and errorShort.text.lower().find("diario de subida alcanzado") != -1:
        print("Se ha alcanzao el limite de videos por dia, esperan 24 horas para volver a intentarlo")
        status.upload_youtube = False
        driver.quit()
        return
    titleVideo.click()
    titleVideo.send_keys(Keys.CONTROL + 'a')
    time.sleep(1)
    titleVideo.send_keys(Keys.BACKSPACE)
    act = ActionChains(driver)
    act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform() 
    time.sleep(3)
    #No kids select
    waitElement(driver, '[name="VIDEO_MADE_FOR_KIDS_NOT_MFK"]', 30, By.CSS_SELECTOR).click()
    time.sleep(1)
    #Show more optiosn
    waitElement(driver, '#toggle-button', 30, By.CSS_SELECTOR).click()
    time.sleep(1)
    #Set hashtags
    etiquetas = waitElement(driver, '#text-input[aria-label="Etiquetas"]', 30, By.CSS_SELECTOR)
    etiquetas.click()
    etiquetas.send_keys(hashtags)
    time.sleep(1)
    #Next button
    waitElement(driver, '#next-button', 30, By.CSS_SELECTOR).click()
    time.sleep(1)
    #Next button
    waitElement(driver, '#next-button[role="button"]', 30, By.CSS_SELECTOR).click()
    time.sleep(1)
    #Next button
    waitElement(driver, '#next-button[role="button"]', 30, By.CSS_SELECTOR).click()
    time.sleep(1)
    #Schedule video
    waitElement(driver, '#schedule-radio-button', 30, By.CSS_SELECTOR).click()
    time.sleep(1)
    #Done Button
    publicado = waitElement(driver, '#done-button', 30, By.CSS_SELECTOR)
    publicado.click()
    if publicado:
        print("Video correctamente subido")
        waitElement(driver, '#dialog-title', 180, By.CSS_SELECTOR)
        crear_registro(f"INSERT INTO UPLOADED VALUES (2, '{idVideo}', '{datetime.today().strftime('%Y-%m-%d')}')")
    else:
        print("Hubo un problema al subir el video")
    driver.quit()

# def uploadVideoFacebook(driver, filePath, idVideo, description):
#     # Navigate to the Facebook page
#     driver.get("https://business.facebook.com/latest/reels_composer")
#     time.sleep(5)  # Wait for the page to load
#     input = waitElement(driver, 'div[data-pagelet="MainView"] [role="button"][tabindex="0"][aria-busy="false"]', 30, By.CSS_SELECTOR)
#     # input.click()
#     input.send_keys(filePath)
#     textarea = waitElement(driver, '/html/body/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div/div/div[2]/div/div/div/div/div[1]/div[1]/div/div[3]/div/div[2]/div[1]/div[2]/div/div[2]', 30, By.XPATH)
#     textarea.click()
#     pyperclip.copy(description)
#     act = ActionChains(driver)
#     act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform() 
#     act.send_keys(Keys.SPACE).perform()
#     waitElement(driver, 'div[role=button][aria-label*=Publicar][tabindex="0"]', 30, By.CSS_SELECTOR).click()
#     publicado = waitElement(driver, '//*[@id="facebook"]/body/div[4]/ul/li/div[1]/div/div', 200, By.XPATH)
#     if publicado:
#         print("Video correctamente subido a Facebook reel")
#         crear_registro(f"INSERT INTO UPLOADED VALUES (1, '{idVideo}')")
#         # crear_registro("UPDATE VIDEO SET FACEBOOK = 1 WHERE idVideo = '"+idVideo+"'")
#     else:
#         print("Hubo un problema al subir el video")

def uploadVideoFacebook(driver, filePath, idVideo, description):
    # Navigate to the Facebook page
    driver.get("https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS")
    time.sleep(5)  # Wait for the page to load
    input = waitElement(driver, 'input[accept*=video]', 30, By.CSS_SELECTOR)
    # input.click()
    input.send_keys(filePath)
    waitElement(driver, 'div[role=button][aria-label*=Sigu][tabindex="0"]', 30, By.CSS_SELECTOR).click()
    waitElement(driver, 'div[role=button][aria-label*=Sigu][tabindex="0"]', 30, By.CSS_SELECTOR).click()
    textarea = waitElement(driver, 'div[role=textbox]', 50, By.CSS_SELECTOR)
    textarea.click()
    pyperclip.copy(description)
    act = ActionChains(driver)
    act.key_down(Keys.CONTROL).send_keys("v").key_up(Keys.CONTROL).perform() 
    act.send_keys(Keys.SPACE).perform()
    errorShort = waitElement(driver, '//html/body/div[1]/div/div[1]/div/div[7]/div/div/div[3]/form/div/div/div[1]/div/div[4]/div[1]/div[1]/div/div/div/div[2]/div/div/div/div/span/span/div/div', 2, By.XPATH)
    if not errorShort:
        errorShort = waitElement(driver, '//body/div/div/div/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[1]/div[1]/div/div/div/div[2]/div/div/div/div/span/span/div/div', 1, By.XPATH)
    if errorShort and errorShort.text.lower().find("no se puede subir") != -1:
        print("Se ha alcanzao el limite de videos por dia en Facebook")
        status.upload_facebook = False
        return
    waitElement(driver, 'div[role=button][aria-label*=Publicar][tabindex="0"]', 200, By.CSS_SELECTOR).click()
    publicado = waitElement(driver, '//*[@id="facebook"]/body/div[4]/ul/li/div[1]/div/div', 100, By.XPATH)
    if publicado:
        print("Video correctamente subido a Facebook reel")
        crear_registro(f"INSERT INTO UPLOADED VALUES (1, '{idVideo}', '{datetime.today().strftime('%Y-%m-%d')}')")
        # crear_registro("UPDATE VIDEO SET FACEBOOK = 1 WHERE idVideo = '"+idVideo+"'")
    else:
        print("Hubo un problema al subir el video")

def selectFolder():
    root = tk.Tk()
    root.withdraw() 
    return filedialog.askdirectory().replace('/', '\\')

def forReel(folder):
    list_files = os.listdir(f'{folder}')
    lista_videos = []
    print("Analizando archivos...")
    for archivo in list_files:
        if archivo.endswith(".mp4"):
            clip = VideoFileClip(f'{folder}\\{archivo}')
            if math.ceil(clip.duration) <= 60:
                lista_videos.append(f'{folder}\\{archivo}')
            clip.close()
    return lista_videos

def analyze(folder):
    lista_videos = forReel(folder)
    def searchVideo(resultado, search):
        for v in resultado:
            if search in v:
                return True
        return False
    
    if not lista_videos: 
        print("Sin videos para subir") 
        return
    for i, filePath in enumerate(lista_videos):
        idVideo = os.path.splitext(os.path.basename(filePath))[0]

        resultado = leer_registro("SELECT DESCRIPTION, HASHTAGS FROM VIDEO WHERE IDVIDEO = '" + idVideo +"'")
        subido = leer_registros("SELECT N.network FROM uploaded AS U JOIN network AS N ON U.IDNETWORK = N.idNetwork WHERE U.IDVIDEO = '" + idVideo + "'")

        description, hashtags = resultado[0], resultado[1]
        
        concat_description_hashtags = description
        if len(hashtags) > 1:
            temp = " #" + hashtags.replace(",", " #")
            concat_description_hashtags += temp
        driver = None

        if (not searchVideo(subido, "Facebook") and status.upload_facebook) or (not searchVideo(subido, "Youtube") and status.upload_youtube):
            print("Iniciando DRIVER")
            driver = set_driver()
        else:
            print("Omitiendo", idVideo)
        if not searchVideo(subido, "Facebook") and status.upload_facebook:
            print(f"Subiendo {idVideo} a Facebook Reel")
            hilo = threading.Thread(target=uploadVideoFacebook, args=(driver, filePath, idVideo, concat_description_hashtags,))
            hilo.start()
            hilo.join()

        if not searchVideo(subido, "Youtube") and status.upload_youtube:
            print(f"Subiendo {idVideo} a YouTube Reel")
            hilo = threading.Thread(target=uploadVideoYoutube, args=(driver, filePath, idVideo, description, hashtags,))
            hilo.start()
            hilo.join()
        if not status.upload_facebook and not status.upload_youtube:
            print("Limite alcanzo en ambas redes sociales, esperar algunas horas y volver a intentarlo")
            return

if __name__ == "__main__":
    folder = selectFolder()
    if folder:
        analyze(folder)