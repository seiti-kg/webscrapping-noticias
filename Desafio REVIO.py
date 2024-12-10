from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime, timedelta
import time 

def processar_data(data_str):
    agora = datetime.now()
    
    if not data_str:
        return "Data não encontrada"

    if "há" in data_str:
        if "horas" in data_str:
            horas = int(data_str.split(" ")[1])
            data_calculada = agora - timedelta(hours=horas)
            return data_calculada.strftime("%d/%m/%Y %H:%M")
        elif "minutos" in data_str:
            minutos = int(data_str.split(" ")[1])
            data_calculada = agora - timedelta(minutes=minutos) 
            return data_calculada.strftime("%d/%m/%Y %H:%M")
        elif "dia" or "dias" in data_str:
            dias = int(data_str.split(" ")[1])
            data_calculada = agora - timedelta(days=dias)
            return data_calculada.strftime("%d/%m/%Y %H:%M")
    else:
        try:
            data_absoluta = datetime.strptime(data_str, "%d/%m/%Y %Hh%M")
            return data_absoluta.strftime("%d/%m/%Y %H:%M")
        except ValueError:
            return "Formato de data inválido"


PATH = "C:\\chromedriver-win64\\chromedriver.exe"
service = Service(executable_path=PATH)
driver = webdriver.Chrome(service=service)

driver.get("https://g1.globo.com/")
driver.maximize_window()
print(driver.title)

time.sleep(3)

pesquisa = driver.find_element(By.XPATH, '//*[@id="busca-campo"]')
pesquisa.send_keys('Inteligência Artificial')
pesquisa.submit()

time.sleep(3)
 
while True:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        novaPagina = driver.find_element(By.CLASS_NAME, "pagination__load-more")
        novaPagina.click()
    except NoSuchElementException:
        print("Última página alcançada!")
        break
items = []
try:
    listaDeResultado = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'results__list'))
    )   
    noticias = driver.find_elements(By.CLASS_NAME, 'widget--info')
    for noticia in noticias:
        try:
            titulo = noticia.find_element(By.CLASS_NAME, 'widget--info__title').text
            data = noticia.find_element(By.CLASS_NAME, 'widget--info__meta').text
            print(f"Data extraída: {data}")  # Verificando a data extraída
            datas = processar_data(data)
            items.append((titulo, datas))
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
finally:
    driver.quit()

with open('NoticiasSobreInteligenciaArtificial.txt', 'w', encoding='utf-8') as texto:
    for titulo, data in items:
        if data != "Data não encontrada" and data != "Formato de data inválido":
            texto.write(f'Título: {titulo}\nData: {data}\n\n')
        else:
            texto.write(f'Título: {titulo}\nData: Não disponível\n\n')


print("Notícias salvas com sucesso!")
