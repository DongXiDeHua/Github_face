import time
import pymysql
import re
import tkinter as tk
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import tkinter.messagebox

driver = webdriver.Edge()
driver.maximize_window()
# driver = webdriver.Chrome()

conn = pymysql.connect(host='localhost', user='root', password='root', db='people', port=3306, charset='utf8')
cursor = conn.cursor()
aList = []  # 数据库准备


# client = pymongo.MongoClient('localhost', 27017)
# mydb = client['mydb']
# python = mydb['python']

def tx_video_root():
    driver.get('https://v.qq.com/')
    driver.implicitly_wait(10)

    driver.find_element(By.XPATH,'//*[@id="mod_head_notice_trigger"]').click()
    driver.implicitly_wait(10)
    input("请继续登录，登录成功回车确认:")
    driver.switch_to.window(driver.window_handles[0])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="modHistory"]/a').click()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    new_selector = driver.page_source
    soup = BeautifulSoup(new_selector, 'html.parser')
    soup.prettify()
    # app > div.bili-dyn-home--member > main > section:nth-child(3) > div.bili-dyn-list > div.bili-dyn-list__items > div:nth-child(19)
    try:
        for i in range(1, 20):
            new_hrefs = soup.select(
                'body > div.site_wrapper.cf > div.site_main > div > div:nth-child(3) > div:nth-child(2) > div:nth-child({}) > strong > a'.format(
                    i))
            new_href = new_hrefs[0]['href']
            aList.append('https:' + new_href)
            print(aList)

    except:
        try:
            for j in range(1, 20):
                hrefs = soup.select(
                    'body > div.site_wrapper.cf > div.site_main > div > div:nth-child(4) > div:nth-child(2) > div:nth-child({}) > strong > a'.format(
                        j))
                # hrefs = soup.select('body > div.site_wrapper.cf > div.site_main > div > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > strong > a')
                href = hrefs[0]['href']
                aList.append('https:' + href)
                print(aList)
        except:
            try:
                for n in range(1, 20):
                    hreffs = soup.select(
                        'body > div.site_wrapper.cf > div.site_main > div > div:nth-child(2) > div:nth-child(2) > div:nth-child({}) > strong > a'.format(
                            n))
                    hreff = hreffs[0]['href']
                    aList.append('https:' + hreff)
                    print(aList)
            except:
                for url in aList:
                    new_url = str(url)
                    driver.get(new_url)
                    time.sleep(3)
                    new_selector = driver.page_source
                    soup = BeautifulSoup(new_selector, 'html.parser')
                    soup.prettify()
                    labels = soup.select(
                        '#app > div.page-play.view-content > div > div > div.container-main__wrapper > div > div.container-main__left > div.player-bottom__intro > div.play-intro__desc-wrapper > div.play-intro__tags')
                    label = labels[0].get_text().split()
                    cursor.execute(
                        "insert into tx_video_root (label) value(%s)", str(label))
                    print(label)


def bili_video_root():
    driver.get('https://www.bilibili.com/')
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,'//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[1]/li/div/div/span').click()
    time.sleep(1)
    # driver.find_element(By.XPATH,'/html/body/div[3]/div/div[4]/div[2]/form/div[1]').click()
    # driver.find_element(By.XPATH,'/html/body/div[5]/div/div[4]/div[2]/form/div[1]').send_keys('13970069700')
    # driver.find_element(By.XPATH,'/html/body/div[5]/div/div[4]/div[2]/form/div[3]').click()
    # driver.find_element(By.XPATH,'/html/body/div[5]/div/div[4]/div[2]/form/div[3]').send_keys('qyh20020314!!!')
    # driver.find_element(By.XPATH,'/html/body/div[5]/div/div[4]/div[2]/div[2]/div[2]').click()
    input('请继续登录，登录成功后回车确认：')
    driver.switch_to.window(driver.window_handles[0])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="i_cecream"]/div[2]/div[1]/div[1]/ul[2]/li[5]/a').click()
    driver.implicitly_wait(10)
    driver.switch_to.window(driver.window_handles[1])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(2)
    new_selector = driver.page_source
    soup = BeautifulSoup(new_selector, 'html.parser')
    soup.prettify()
    # app > div.bili-dyn-home--member > main > section:nth-child(3) > div.bili-dyn-list > div.bili-dyn-list__items > div:nth-child(19)
    try:
        for i in range(10):
            driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
            time.sleep(0.5)
        for j in range(2, 80):
            new_hrefs = soup.select(
                # #history_list > li:nth-child(2) > div.r-info.clearfix > div.r-txt > a
                # #history_list > li:nth-child(3) > div.r-info.clearfix > div.r-txt > a
                # #history_list > li:nth-child(136) > div.r-info.clearfix > div.r-txt > a
                '#history_list > li:nth-child({}) > div.r-info.clearfix > div.r-txt > a'.format(
                    j))
            new_href = new_hrefs[0]['href']
            aList.append('https:' + new_href)
            print(aList)
    except:
        for url in aList:
            new_url = str(url)
            driver.get(new_url)
            time.sleep(3)
            new_selector = driver.page_source
            soup = BeautifulSoup(new_selector, 'html.parser')
            soup.prettify()
            for i in range(10):
                try:
                    labels = soup.select(
                        # #v_tag > div > div:nth-child(1)
                        # #v_tag > div > div:nth-child(2)
                        '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                    label = labels[0].get_text().split()
                    cursor.execute(
                        "insert into bili_video_root (label) value(%s)", str(label))
                    print(label)
                except:
                    print('')
    for url in aList:
        new_url = str(url)
        driver.get(new_url)
        time.sleep(3)
        new_selector = driver.page_source
        soup = BeautifulSoup(new_selector, 'html.parser')
        soup.prettify()
        for i in range(10):
            try:
                labels = soup.select(
                    # #v_tag > div > div:nth-child(1)
                    # #v_tag > div > div:nth-child(2)
                    '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                label = labels[0].get_text().split()
                cursor.execute(
                    "insert into bili_video_root (label) value(%s)", str(label))
                print(label)
            except:
                print('')


def weibo_root():
    driver.get('https://weibo_root.com/')
    driver.implicitly_wait(10)
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="scroller"]/div[1]/div[1]/div/article/div/header/div[2]/button').click()
    time.sleep(1)
    input('请继续登录，登录成功后回车确认：')
    driver.switch_to.window(driver.window_handles[0])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(3)
    driver.find_element(By.XPATH,
        '//*[@id="app"]/div[2]/div[1]/div/div[1]/div/div/div[2]/div/div[1]/a[5]/div/div/div').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="app"]/div[2]/div[2]/div[1]/div/div/div/div/a[2]/div/span').click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(3)
    new_selector = driver.page_source
    soup = BeautifulSoup(new_selector, 'html.parser')
    soup.prettify()
    for i in range(1, 100):
        try:
            labels = soup.select(
                # #scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(1) > div > div > div.woo-box-flex.woo-box-alignCenter.UserFeedCard_item_1wK9O > a > div.woo-box-item-flex.UserFeedCard_con_XW5Tz.UserFeedCard_f12_FyJoV > div:nth-child(2)
                # #scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(2) > div > div > div.woo-box-flex.woo-box-alignCenter.UserFeedCard_item_1wK9O > a > div.woo-box-item-flex.UserFeedCard_con_XW5Tz.UserFeedCard_f12_FyJoV > div:nth-child(2)
                # #scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child(2) > div > div > div.woo-box-flex.woo-box-alignCenter.UserFeedCard_item_1wK9O > a > div.woo-box-item-flex.UserFeedCard_con_XW5Tz.UserFeedCard_f12_FyJoV > div:nth-child(3)
                '#scroller > div.vue-recycle-scroller__item-wrapper > div:nth-child({}) > div > div > div.woo-box-flex.woo-box-alignCenter.UserFeedCard_item_1wK9O > a > div.woo-box-item-flex.UserFeedCard_con_XW5Tz.UserFeedCard_f12_FyJoV > div:nth-child(2)'.format(
                    i))
            label = labels[0].get_text().split()
            cursor.execute(
                "insert into weibo_root (label) value(%s)", str(label))
            print(label)
        except:
            print('')


def bili_video(b_name):  # 需要目标完整的b站昵称
    driver.get('https://www.bilibili.com/')
    driver.implicitly_wait(10)
    time.sleep(3)
    driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[1]/input').click()
    driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[1]/input').send_keys(b_name)
    driver.find_element(By.XPATH,'//*[@id="nav-searchform"]/div[1]/input').send_keys(Keys.ENTER)
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(5)
    driver.find_element(By.XPATH,
        '//*[@id="i_cecream"]/div/div[2]/div[1]/div[2]/div/nav/ul/li[7]/span/span[1]').send_keys(Keys.ENTER)
    input('请在该页面选择对应的用户进行点击！回车确认')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    new_url = driver.current_url
    print(new_url)
    driver.get(new_url)
    time.sleep(3)
    new_selector = driver.page_source
    soup = BeautifulSoup(new_selector, 'html.parser')
    soup.prettify()
    bili_video_List = []
    # #page-index > div.col-1 > div:nth-child(7) > div > div:nth-child(1) > a.cover
    # #page-index > div.col-1 > div:nth-child(7) > div > div:nth-child(2) > a.cover
    try:
        for b_url_s in range(1, 20):
            new_href_urls = soup.select(
                '#page-index > div.col-1 > div:nth-child(7) > div > div:nth-child({}) > a.cover'.format(b_url_s))
            new_href = new_href_urls[0]['href']
            aList.append('https:' + new_href)
            print(bili_video_List)
    except:
        for url in aList:
            new_url = str(url)
            driver.get(new_url)
            time.sleep(3)
            new_selector = driver.page_source
            soup = BeautifulSoup(new_selector, 'html.parser')
            soup.prettify()
            for i in range(10):
                try:
                    labels = soup.select(
                        # #v_tag > div > div:nth-child(1)
                        # #v_tag > div > div:nth-child(2)
                        '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                    label = labels[0].get_text().split()
                    cursor.execute(
                        "insert into bili_video_root (label) value(%s)", str(label))
                    print(label)
                except:
                    print('')
    for url in aList:
        new_url = str(url)
        driver.get(new_url)
        time.sleep(3)
        new_selector = driver.page_source
        soup = BeautifulSoup(new_selector, 'html.parser')
        soup.prettify()
        for i in range(10):
            try:
                labels = soup.select(
                    # #v_tag > div > div:nth-child(1)
                    # #v_tag > div > div:nth-child(2)
                    '#v_tag > div > div:nth-child({}) > div > a'.format(i))
                label = labels[0].get_text().split()
                cursor.execute(
                    "insert into bili_video_root (label) value(%s)", str(label))
                print(label)
            except:
                print('')


def root_p():
    tx_video_root()
    bili_video_root()


def tkk():
    root = tk.Tk()
    image_fast = tk.PhotoImage(file="image1.png")
    root.iconbitmap("image1.ico")
    root.title("爬虫及人物画像")
    root.iconbitmap("")
    root.geometry('300x200+100+100')

    frame1 = tk.Frame(root)
    frame1.pack()

    label1 = tk.Label(root, text="请选择爬虫选项!", font=("黑体", 15, "bold"), padx=24, pady=30, image=image_fast,
                      compound="top")
    label1.pack()

    button_user = tk.Button(label1, text="用户视角", bd=1, width=10, command=root_p)
    button_user.place(relx=0.3, rely=0.8, anchor=tk.CENTER)
    button_root = tk.Button(label1, text="管理视角", bd=1, width=10)
    button_root.place(relx=0.7, rely=0.8, anchor=tk.CENTER)

    frame2 = tk.Label(root)
    frame2.pack()
    label2 = tk.Label(root, text="请选择操作！", font=("黑体", 15, "bold"), padx=24, pady=30, image=image_fast,
                      compound="top")
    label2.pack()

    def root_view():
        frame1.pack_forget()
        frame2.pack()

    button_root.config(command=root_view)
    root.mainloop()


if __name__ == '__main__':
    # tx_video_root()
    bili_video_root()
    # weibo_root()
    # bili_video()
    # bili_video('晞和丶')
    # driver.__exit__()
    # conn.commit()
