import requests
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import os
cookie_loaded=0
main_url='https://xianhua.sanguosha.cn/'
driver=webdriver.Edge()
dis_src='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACgAAAApCAYAAABHomvIAAAAAXNSR0IArs4c6QAABBVJREFUWEftl19oW3UUx7/npkmGm1jXF6WiHYhsasHNBycIijKfxkTQOrt7558t9zZEk3ujzDkcfVAco6y5iXU2Ny2hze3UuAd17Emx4oOCTEXdZNAHZbjoQyFurNia5h65NwnOmr9r2gTs7+mX/M7v/D58z/mde36ENh/U5nxYA1xuhP6fCuqJ1A4w+UHYTMzfAjgekqUvr0XNpisYS5iqxYgshSHAH5LF0UYhmwo4PJa6XbBoxoZg4BIxn2eizQTcACC34FroeWXfvkwjkE0F1I3UWwC9YMNYjHvDivjjsURyu4vdX9lQxOwLKdJYSwCPjo9f7817bXU2AJhWZfFhG2RkZKJr0eOaLap6SJPFIy0B1A3zdQCvOSCEJzWfeNKeRxNmgBkj9twC7QjLez5ddcDo2JTEFk8WD55RZfGOEoRumD8B2ALggiqLtzUC56RFoxtK9ul02pPJ/nkTyHUIgFL8f86yrIfCA3vP2L8joyfuJ8EqlZc3VFk83Oh5VQFjsZiXvRt3M/EgQJtqOL/CJDym+fo/K9lFDTPGwIt1QM1agHxLp+fjvr6+/NX2FQGTyeS6Szn35wDuq3FADoSvrUXPU2F/38WrbaOG+SYDr9YB6Jgw+CVNlobrAtQN8x0AA8U8yFrA5cKcugHuIKIMM8eFeejBoOislRt63HyPCdurQRKoC2D79v8nT8sqmE6nXZnswhyIvCB8ofrEB/9J+qmfAe5hxoSmiM/Wq041u6hhfsDAEwAyqix211Qw8vbkFnIL9u2za8NudUB8f6UAhyYn17vnhSuOf4Kp+kSpNqAxdQ+Bv3PygvlxTZE+XCnAiGE+T8C47V8QhF3B/f2n2gpQj6c+AtEuAFlVFjcuTYWyORhZJQUjyWQn5dzZ4g2OarKkthWgnpgKgjlaCG9+W3D/M05atU2IdcP8BsC2YnnpKXRpbQKoxyduBbl+KZRWDKk+8UC5UtSyHIwYqZcJNORUl7zVG/LvPdtWgLph/gCgF4yzqiL2VirkLVFw2DhxlwCrqBgfVGXpaFsB6gnzCBgHnfKSd23S/E/buVh2tERB3TB/BdANok9U355HK8EVvn5lxkoW6uiY+QhbKLX9AVUWjzcMGBs177QEnHM2WpDUAdFs1rc4EjdHiBCw/f2Vy918IPDc7w0DDk5Pd9w4c3EOgIeZv/csXn4gEAg4HYduLK/d0hPmLBhdBJwOyeLOanAVQ2wvRIzUMQKFi0YZBi4UnPFWgLwA/wHQ+VoH/GudeQOI7na8EPdrPundWvsrtvyDg8l1nd0dKQLZjWRTBwPnruO5rYqi5Go5rvpoisfj7nlav5MBH4CGn4xLD2cgR+AzzDisKdJvteCqhriezathc83v4tWAW1OwGSqvhXi5Kv4NU81ASET1r0QAAAAASUVORK5CYII='
def login(url):
    driver.get(url)
    #若有cookie先尝试cookie，看看是否过期
    if os.path.exists("cookies.json") and cookie_loaded ==0:
        with open("cookies.json", 'r') as f:
            cookies = json.load(f)
        for i in cookies:
            driver.add_cookie(i)
        driver.refresh()
    #根据头像是否为默认头像判断是否已经登录成功
    head = driver.find_elements(By.XPATH,'//img[@src="https://imagexh.sanguosha.com/sgxh-pc/userDefault.png"]')
    if len(head) != 0:
        driver.get(url)
        input("手动完成登录后按回车继续")
        cookies = driver.get_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        with open("cookies.json", 'w') as f:
            json.dump(cookies, f)
        driver.refresh()


#mode为0则遍历主页，否则遍历指定互赞页面
def like(url=main_url,mode=0):
    login(url)
    driver.refresh()
    count=0
    time.sleep(3)
    while(1):
        count+=1
        #botl=driver.find_elements(By.CSS_SELECTOR,'div[style*="align-items: center; display: flex;"')
        botl=driver.find_elements(By.XPATH,f'//img[@class="postIcon" and @src="{dis_src}"]')
        for lkbt in botl:
            try:
                driver.execute_script("arguments[0].scrollIntoView;", lkbt)
                lkbt.click()
                time.sleep(1)
            except Exception as e:
                print(f"点赞失败{e}")
        time.sleep(2)
        #如果是互赞的话就看看要不要加载更多
        if mode != 0:
            admore=driver.find_elements(By.XPATH,'//*[@id="__nuxt"]/div/div/div/div[4]/a')
            nomore=driver.find_elements(By.XPATH,'//p[@class="no-more"]')
            nopost=driver.find_elements(By.XPATH,'//div[@class="no-post"]')
            #到底了/根本没有发
            if len(nomore) != 0 or len(nopost) != 0:
                break
            elif len(admore) != 0:
                admore[0].click()
        else:
            #如果是主页就尝试按刷新键刷新新内容
            rbt=driver.find_elements(By.XPATH,'/html/body/div/div/div/div[4]')
            if len(rbt) != 0:       #避免刷新键没刷出来导致的报错
                try:
                    rbt[0].click()
                except Exception as e:
                    print(f"刷新失败{e}")
            if count >= 11:
                break
    input("结束可看")



if __name__== '__main__' :
    #默认先水一下主页
    like()
    while 1:
        like_id=input("是否要互赞？按0退出,如需要互赞输入其id")
        if like_id == "0" or like_id=="":
            break
        else:
            print(f"id={like_id}")
            like_url="https://xianhua.sanguosha.cn/userCenter?id="+str(like_id)
            like(like_url, 1)
    driver.quit()