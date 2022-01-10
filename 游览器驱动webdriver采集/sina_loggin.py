from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class sina_loggin(object):
    def __init__(self):
        self.user_data = {"user":"15731624659","pwd":"qq1161081779"}


        pass
    def chrome_Opthons(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1366,768")
        return chrome_options

    def user_loggin(self,su,sp):
        driver = webdriver.Chrome(chrome_options=self.chrome_Opthons())
        driver.get("https://weibo.com/")
        wait = WebDriverWait(driver,10)
        input_su = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginname"]')))
        input_sp = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pl_login_form"]/div/div[3]/div[2]/div/input')))
        input_su.clear()
        input_sp.clear()
        input_su.send_keys(self.user_data["user"])
        input_sp.send_keys(self.user_data["pwd"])
        login_click = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="pl_login_form"]/div/div[3]/div[6]/a')))
        login_click.click()
        print(driver.title)
        time.sleep(5)
        driver.quit()

sina_login = sina_loggin()
sina_login.user_loggin()