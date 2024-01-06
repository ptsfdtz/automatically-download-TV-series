from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://online.njtech.edu.cn/#/video/detail?id=5192"
driver.get(url)

element = driver.find_element(By.XPATH, "//div[@class='dplayer-video-wrap']")
element_text = element.text
print("特定元素的文本信息:", element_text)

driver.quit()
