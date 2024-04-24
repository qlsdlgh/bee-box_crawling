from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, random, pyperclip
import pandas as pd
def login():
    browser.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")
    browser.implicitly_wait(random.randint(3, 5))
    time.sleep(random.randint(3, 5))
    print(browser.get_cookies())
    #browser.execute_async_script('console.log(document.cookie);')
    id_element = browser.find_element(By.ID, "id")
    pyperclip.copy("아이디")
    id_element.send_keys(Keys.CONTROL, "v")
    id_element.click()
    pw_element = browser.find_element(By.ID,"pw")
    pyperclip.copy("비밀번호")
    pw_element.send_keys(Keys.CONTROL, "v")
    pw_element.click()
    time.sleep(5)
    login_element = browser.find_element(By.XPATH, '''//*[@id="log.login"]''')
    login_element.click()
    time.sleep(10)

data = []

browser = webdriver.Chrome()
login()
url = "https://comic.naver.com/webtoon"
browser.get(url)
browser.implicitly_wait(random.randint(3,5))

parent_div = browser.find_element(By.CLASS_NAME, 'WeekdayMainView__daily_all_wrap--UvRFc')
title_tags = parent_div.find_elements(By.CLASS_NAME, 'text')
text_contents = [title.text for title in title_tags]
a_tags = parent_div.find_elements(By.CLASS_NAME, "ContentTitle__title_area--x24vt")
href_values = [a.get_attribute('href') for a in a_tags]

def page_parse():
    titles = []
    while True:
        buttons = WebDriverWait(browser, 10).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, 'Paginate__page--iRmGj'))
        )
        for button in buttons:
            WebDriverWait(browser, 10).until(EC.element_to_be_clickable(button)).click()
            time.sleep(2)
            parent1_div = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'EpisodeListList__episode_list--_N3ks'))
            )
            title_text = parent1_div.find_elements(By.CLASS_NAME, 'EpisodeListList__title--lfIzU')
            current_titles = [b.text for b in title_text]
            titles.extend(current_titles)
            print(current_titles)
        next_button = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'Paginate__next--F6rIk'))
        )
        if next_button.get_attribute('disabled'):
            break
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable(next_button)).click()
    return titles
data = []

for index, href in enumerate(href_values):
    browser.get(href)
    browser.implicitly_wait(random.randint(3,5))
    titles = page_parse()
    for title in titles:
        data.append({'Webtoon Title': text_contents[index], 'Episode Title': title})

df = pd.DataFrame(data)
with pd.ExcelWriter('Webtoons.xlsx', engine='openpyxl') as writer:
    df.to_excel(writer, index=False)

print("Excel 파일이 저장되었습니다.")

browser.quit()
