import sys
import time
import datetime

from PySide6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem
from PySide6 import QtWidgets

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

mails = []

class MainWindow(QMainWindow):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    #selenium up
    chrome = webdriver.Chrome('./chromedriver.exe')
    self.chrome = chrome

    # naver login
    chrome.get("https://mail.naver.com")
    input_id = find(chrome, "#id")
    input_pw = find(chrome, "#pw")
    
    # id_copy
    pyperclip.copy("yms06034")
    time.sleep(1)
    input_id.click()
    input_id.send_keys(Keys.CONTROL, "v")

    # id_copy
    pyperclip.copy("rla#tjd#wls00!@")
    time.sleep(1)
    input_pw.click()
    input_pw.send_keys(Keys.CONTROL, "v")
    input_pw.send_keys("\n")

    # time.sleep(2)

    # 네이버 등록하기 버튼 클릭
    # new_save_btn = chrome.find_element_by_id("new.save")
    # new_save_btn.click()

    # time.sleep(2)

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
      site = '네이버'
      sender = mail.find_element_by_css_selector(".mTitle .name a").text
      try:
        mail.find_element_by_css_selector("li.file span.spr:not([title=''])")
        attached = True
      except:
        attached = False
      title = mail.find_element_by_css_selector("strong.mail_title").text
      link = mail.find_element_by_css_selector("div.subject > a").get_attribute("href")
      
      mails.append({
          "date": date,
          "site": site,
          "sender": sender,
          "attached": attached,
          "title": title,
          "link": link,
        })
    

    # table show
    self.ui.table.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
    self.ui.table.setRowCount(len(mails))
    for r, m in enumerate(mails):
      self.ui.table.setItem(r, 0, QTableWidgetItem(str(m["date"])))
      self.ui.table.setItem(r, 1, QTableWidgetItem(m["site"]))
      self.ui.table.setItem(r, 2, QTableWidgetItem(m["sender"]))
      self.ui.table.setItem(r, 3, QTableWidgetItem(str(m["attached"])))
      self.ui.table.setItem(r, 4, QTableWidgetItem(str(m["title"])))

    self.ui.table.cellDoubleClicked.connect(self.open_mail)
  
  def open_mail(self, r, c):
    mail = mails[r]
    link = mail["link"]

    self.chrome.get(link)
    content = find(self.chrome, "#readFrame").text

    self.ui.lb_title.setText(mail["title"])
    self.ui.lb_content.setText(content)

if __name__ == "__main__":
  app = QApplication()
  window = MainWindow()
  window.show()
  sys.exit(app.exec())

