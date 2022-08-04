import sys
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
    print(input_id)

if __name__ == "__main__":
  app = QApplication()
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

