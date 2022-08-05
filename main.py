import sys
import time
import datetime

from PySide6.QtWidgets import QMainWindow, QApplication

from ui import Ui_MainWindow

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pyperclip


def find(chrome, css):
  wait = WebDriverWait(chrome, 5)
  return wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css)))

def find_all(chrome, css):
  find(chrome, css)
  return chrome.find_elements_by_css_selector(css)

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    #selenium up
    chrome = webdriver.Chrome('./chromedriver.exe')
    

    # naver login
    chrome.get("https://mail.naver.com")
    input_id = find(chrome, "#id")
    input_pw = find(chrome, "#pw")
    
    # id_copy
    pyperclip.copy("sjk5838")
    time.sleep(1)
    input_id.click()
    input_id.send_keys(Keys.CONTROL, "v")

    # id_copy
    pyperclip.copy("rlatjdwls00@K")
    time.sleep(1)
    input_pw.click()
    input_pw.send_keys(Keys.CONTROL, "v")
    input_pw.send_keys("\n")

    time.sleep(2)

    # 네이버 등록하기 버튼 클릭
    new_save_btn = chrome.find_element_by_id("new.save")
    new_save_btn.click()

    time.sleep(2)

    # 메일의 date만 출력
    for mail in find_all(chrome, "ol.mailList > li"):
      date = mail.find_element_by_css_selector("li.iDate").text

      # 22:00
      # 08-05 22:00
      # 22-08-05 22:00
      now = datetime.datetime.now()
      if len(date) < 6:
        date = f"{now.month}-{now.day} {date}"
      date = f"{now.year}-{date}"
      date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
      print(date)

if __name__ == "__main__":
  app = QApplication()
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

