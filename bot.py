from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as expect
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
import time


#Va el nombre del archivo donde están todas las cuentas de Youtube
archivoUsuarios = "usuarios.txt"
#Va el nombre del archivo donde están todos los comentarios
archivoComentarios = "comentarios.txt"

#Va el nombre del archivo donde están los nombres de las canciones a buscar
archivoNombresVideos = "videos.txt"

#Usuario y contraseña del mail que se usa para verificar los logins
mailVerificacion = ""
contraseñaVerificacion = ""
busquedaEnYoutube = ""

browser = ""

#Path donde esta ubicada la extension Free-VPN-ZenMate-Best-VPN-for-Chrome
ext_path = ""

def modificarIndice(indice,listaComentarios):
    cantidadComentarios = len(listaComentarios)
    archivoIndice = open("indice.txt","w")
    archivoIndice.write(str((indice+1) %cantidadComentarios))
    archivoIndice.close()

def login(dataUsuario):
    
    #Abrir la página
    browser.get("https://accounts.google.com/v3/signin/identifier?dsh=S-2129829861%3A1684347406204440&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F%253FthemeRefresh%253D1&ec=65620&hl=en&ifkv=Af_xneEu71-I4UyEljjfcqWcMTjcyj-crZTxaDE1HiI3V8rE8SnXJyiQB4zM1uljcKLGmxR_tG6M&passive=true&service=youtube&uilel=3&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

    mail = dataUsuario['mail']
    #Guardo usuario
    usuario = WebDriverWait(browser, 60).until(
    EC.presence_of_element_located((By.ID, "identifierId"))
    )
    usuario.send_keys(mail)
    usuario.send_keys(Keys.ENTER)

    contraseña = dataUsuario['password']
    #Guardo password
    password = WebDriverWait(browser, 60).until(
    EC.visibility_of_element_located((By.NAME, "Passwd"))
    )
    time.sleep(1)
    password.send_keys(contraseña)
    password.send_keys(Keys.ENTER)

def busquedaVideo(nombreVideo):
    WebDriverWait(browser, 30).until(
    EC.visibility_of_element_located((By.CSS_SELECTOR, "#contents ytd-video-renderer")))
    
    enlaces_videos = browser.find_elements(By.CSS_SELECTOR, value="#contents ytd-video-renderer")
    video_encontrado = None
    for enlace_video in enlaces_videos:
        titulo_video = enlace_video.find_element(By.ID, "video-title").text
        if nombreVideo.lower() in titulo_video.lower():
            video_encontrado = enlace_video.find_element(By.ID, "video-title")
            break
    video_encontrado.click()

def busquedaYoutube(nombreVideo):

    #Guardo búsqueda Youtube
    busqueda = WebDriverWait(browser, 30).until(
    EC.presence_of_element_located((By.NAME, "search_query"))
    )
    busqueda.send_keys(busquedaEnYoutube)
    time.sleep(4)
    busqueda.send_keys(Keys.ENTER)

    while(True):
        try:
            #BUSCA VIDEO:
            busquedaVideo(nombreVideo)
            break
        except:
            #CORRIGE ERROR DE LATENCIA DE S-WIRE
            busqueda.send_keys(busquedaEnYoutube)
            time.sleep(4)
            busqueda.send_keys(Keys.ENTER)

def cargarSeccionComentarios():
    #Hacer que cargue la sección de comentarios:
    while(True):
        try:
            element = browser.find_element(By.ID,"expand")
            element.click()
            break
        except:
            pass

    element = browser.find_element(By.ID,"collapse")

    actions = ActionChains(browser)
    actions.move_to_element(element).perform()
    element.location_once_scrolled_into_view

def comentar(listaComentarios,indice):
    cargarSeccionComentarios()
    time.sleep(5)
    comentario = listaComentarios[indice]
    modificarIndice(indice,listaComentarios)

    while(True):
        try:
            cajaComentario = WebDriverWait(browser, 60).until(
            EC.visibility_of_element_located((By.ID, "placeholder-area"))
            )
            cajaComentario.click()
            break
        except:
            pass
    
    inputComentario = browser.find_element(By.ID, value="contenteditable-root")
    inputComentario.send_keys(comentario)

    botonComentario = browser.find_element(By.ID,value="submit-button")
    botonComentario.click()

def interaccionVideo(listaComentarios,indice):

    #LIKE:
    botonLike = WebDriverWait(browser, 60).until(
    EC.presence_of_element_located((By.ID, "segmented-like-button"))
    )
    #Evita dar like a un video si ya está likeado
    try:
        browser.find_element(By.XPATH, "//*[@aria-pressed='true' and @class='yt-spec-button-shape-next yt-spec-button-shape-next--tonal yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m yt-spec-button-shape-next--icon-leading yt-spec-button-shape-next--segmented-start ']")
    except:
        botonLike.click()

    #SUBSCRIPCIÓN:
    botonSuscripcion = WebDriverWait(browser, 60).until(
    EC.presence_of_element_located((By.XPATH,"//div[@id='subscribe-button' and @class='style-scope ytd-watch-metadata'][1]"))
    )
    botonSuscripcion.click()

    comentar(listaComentarios,indice)
    
    time.sleep(5)


def obtenerData(archivoUsuarios):
    archivoObj = open(archivoUsuarios,"r")
    dataUsuarios = []
    for linea in archivoObj:
        mail,password = linea.split()
        dataUsuarios.append({'mail':mail,'password':password})
    return dataUsuarios

def obtenerComentarios(archivoComentarios):
    archivoObj = open(archivoComentarios,"r")
    comentarios = []
    for linea in archivoObj:
        comentarios.append(linea)
    return comentarios

def obtenerIndice():
    try:
        archivoIndice = open("indice.txt",'r+')
        indice = archivoIndice.read()
        archivoIndice.close()
        return int(indice)
    except:
        archivoIndice = open("indice.txt",'a')
        archivoIndice.close()
        return 0


#DOBLE VERIFICACIÓN:
def loginCodigo():
    browserCodigo.get("https://accounts.google.com/ServiceLogin?service=mail&continue=https://mail.google.com/mail/&hl=es")

    #Guardo usuario
    usuario = WebDriverWait(browserCodigo, 30).until(
    EC.presence_of_element_located((By.ID, "identifierId"))
    )
    usuario.send_keys(mailVerificacion)
    usuario.send_keys(Keys.ENTER)

    #Guardo password
    password = WebDriverWait(browserCodigo, 30).until(
    EC.visibility_of_element_located((By.NAME, "Passwd"))
    )
    time.sleep(1)
    password.send_keys(contraseñaVerificacion)
    password.send_keys(Keys.ENTER)

def obtenerCodigo():
    global browserCodigo
    browserCodigo = webdriver.Chrome()
    loginCodigo()

    abrirMail = WebDriverWait(browserCodigo, 600).until(
    #EC.visibility_of_element_located((By.XPATH, "//[contains(@span,'Google Verification Code')]"))
    EC.visibility_of_element_located((By.XPATH, "//*[contains(span,'Google Verification Code')]"))
    )
    abrirMail.click()

    WebDriverWait(browserCodigo, 30).until(
    EC.visibility_of_element_located((By.XPATH, "//*[@style='text-align:center;font-size:24px;font-weight:bold']"))
    )
    codigoCaja = browserCodigo.find_elements(By.XPATH, "//*[@style='text-align:center;font-size:24px;font-weight:bold']")[-1]

    codigo = codigoCaja.text
    print(codigo)
    browserCodigo.quit()
    
    return codigo

def verificarLogin():

    try: #En caso que no se pida código, no ejecutamos esto
        enviarCodigo = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "vxx8jf"))
        )
        enviarCodigo.click()

        codigo = obtenerCodigo()
        cajaCodigo = WebDriverWait(browser, 60).until(
        EC.presence_of_element_located((By.ID, "idvPinId"))
        )
        cajaCodigo.send_keys(codigo)
        cajaCodigo.send_keys(Keys.ENTER)
    except:
        pass


#MANEJO DE EXTENSIÓN:
def instalarExtension():
    global chrome_options
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument(f'--load-extension={ext_path}')

def recargarServers():
    WebDriverWait(browser, 2).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "material-icons"))
    )
    atras = browser.find_elements(By.CLASS_NAME, value="material-icons")[0]
    time.sleep(1)
    atras.click()
    time.sleep(0.5)

def elegirServer(server):
    WebDriverWait(browser, 3).until(
    EC.visibility_of_element_located((By.XPATH, "//span[contains(@id,'country-browsing')]"))
    )
    listaServers = browser.find_elements(By.XPATH, "//span[contains(@id,'country-browsing')]")
    cantidadServers = len(listaServers)
    pais = listaServers[server % cantidadServers]
    time.sleep(1)
    pais.click()
    time.sleep(0.5)

def configurarExtension(server):
    browser.get("chrome-extension://omemipoocikbndjplhdgfepfednlanoe/index.html")
    browser.get("chrome-extension://omemipoocikbndjplhdgfepfednlanoe/#/servers")
    browser.get("chrome-extension://omemipoocikbndjplhdgfepfednlanoe/index.html")
    time.sleep(3)

    while (True):
        browser.get("chrome-extension://omemipoocikbndjplhdgfepfednlanoe/#/servers")
        time.sleep(0.5)
        try:
            elegirServer(server)
            break
        except:
            recargarServers()
    time.sleep(2)


#BOT FINAL:
def bot():
    dataUsuarios = obtenerData(archivoUsuarios)
    listaComentarios= obtenerComentarios(archivoComentarios)
    nombresVideos = open(archivoNombresVideos,"r")

    indice = obtenerIndice()
    server = -1

    for nombreVideo in nombresVideos:
        for dataUsuario in dataUsuarios:
            server+=1
            global browser
            instalarExtension()
            browser = uc.Chrome(options=chrome_options)
            configurarExtension(server)
            login(dataUsuario)
            verificarLogin()
            busquedaYoutube(nombreVideo.strip())
            interaccionVideo(listaComentarios,indice)
            browser.quit()



bot()

time.sleep(5)



