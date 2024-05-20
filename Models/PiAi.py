from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pathlib
import warnings
warnings.simplefilter('ignore')


ScriptDir = pathlib.Path().absolute()
url = "https://pi.ai/talk"
options = uc.ChromeOptions()
# options.page_load_strategy='eager'
# options.add_argument("--disable-images")
# options.add_argument("--disable-javascript")
# options.add_argument("--disable-extensions")
# options.add_argument("--enable-tcp-caching")
# options.add_argument("--disable-gpu")
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-notifications")
# options.add_argument("--disable-logging")
options.add_argument('--profile-directory=Default')
options.add_argument(f'--user-data-dir={ScriptDir}\\chromedata')
# options.add_argument("--headless=new")
service = Service(ChromeDriverManager().install())
driver = uc.Chrome(service=service, options=options)
driver.get(url="https://gplinks.co/Jarvis-Series-DAY-8/?pid=959667&vid=369025601")
from time import sleep as s
s(10000)


def Check_for_loaded():
    while True:
        try:
            print("loading")
            enabled=  driver.find_element(by=By.XPATH,value='/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/div/textarea').is_enabled()
            if enabled:
                print("==> PiAi Loaded!")
                break
        except Exception:
            # print(Exception)
            pass

def disable_speaker():
    driver.find_element(by=By.XPATH, value='/html/body/div/main/div/div/div[3]/div[2]/div[2]/div/div[2]/button').click()    

def Speaker():
    try:
        drop_down= driver.find_element(by=By.XPATH, value='/html/body/div/main/div/div/div[3]/div[2]/div[2]/div/div[2]/button[2]').is_displayed()
        if drop_down:
            pass
        else:
            driver.find_element(by=By.XPATH, value='/html/body/div/main/div/div/div[3]/div[2]/div[2]/div/div[2]/button').click()
    except Exception:
        driver.find_element(by=By.XPATH, value='/html/body/div/main/div/div/div[3]/div[2]/div[2]/div/div[2]/button').click()

def QuerySender(Query):
    XpathInput = '/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/div/textarea'
    driver.find_element(by=By.XPATH, value=XpathInput).send_keys(Query)
    XpathSenderButton = '/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/button'
    driver.find_element(by=By.XPATH, value=XpathSenderButton).click()
    
def WaitForTheAnswer():
    XpathInput = '/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/div/textarea'
    driver.find_element(by=By.XPATH,value=XpathInput).send_keys("Testing....")

    while True:
        Button = driver.find_element(by=By.XPATH,value="/html/body/div/main/div/div/div[3]/div[1]/div[4]/div/button").is_enabled() 
        try:
            if False==Button:
                pass

            else:
                driver.find_element(by=By.XPATH,value=XpathInput).clear()
                break
                
        except:
            pass
    
def ResultScrapper():
        XpathResult = f"/html/body/div/main/div/div/div[3]/div[1]/div[2]/div[1]/div/div/div[3]/div/div/div[2]/div[1]/div"#relpace the changing number with ChatNumber
        Text = driver.find_element(by=By.XPATH , value=XpathResult).text
        return Text

Check_for_loaded()

def Pi_AI(Query, Speak=True):
    driver.get(url=url)
    
    QuerySender(Query=Query)
    if Speak:
        Speaker()
    WaitForTheAnswer()
    text = ResultScrapper()
    return text

if __name__=="__main__":
    while True:
        Query = input("Ask: " )
        print(Pi_AI(Query))    