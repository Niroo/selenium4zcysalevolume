from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup as bs
import time

def wf(soup,url,catalog,pname,sname):

    f = open('html.txt','a+',encoding='utf-8')
    tr = soup.select('.item-tab-dealrecord-table > tr')
    
    try:
        for i in tr[1:]:
            f.write(catalog+'!'+pname+'!')
            for item in i.children:
                #f.write(item.string)
                if item.string == None:
                    item = soup.select('.item-tab-dealrecord-table > tr:nth-child(2) > td:nth-child(3) > p:nth-child(1)')[0]
                if not item.string.isspace():
                #ll.append(item.string)
                    f.write(item.string+'!')
            f.write(sname+'\r\n')
    except:
        f.close()
        with open("error.txt","a+") as fe:
            fe.write(url+'   ---E3  \r\n')
            fe.close()

    f.close()

def dopage(driver,url):
    catalog,url = url.split(';')

    driver.get(url)
    try:
        wait = WebDriverWait(driver, timeout=10)
        time.sleep(3)
        #wait.until(expected.visibility_of_element_located((By.NAME, 'q'))).send_keys('headless firefox' + Keys.ENTER)
        #wait.until(expected.visibility_of_element_located((By.CSS_SELECTOR, '#ires a'))).click()
        driver.find_element_by_id('tab-dealrecord').click()

        soup = bs(driver.page_source,'lxml')
        try:
            num = soup.select('li.number')[-1].string
            print("一共有 %s 页成交记录"%(num))
        except:
            name = soup.select('.sh-content__intro--name')
            sname = name[0].string

            print(sname)

            name = soup.select('.content')
            pname = name[0].string
            print(pname)
            wf(soup,url,catalog,pname,sname)
            return 

        name = soup.select('.sh-content__intro--name')
        sname = name[0].string

        print(sname)

        name = soup.select('.content')
        pname = name[0].string
        print(pname)

    except:
        with open("error.txt","a+") as fe:
            fe.write(url+'   ---E2 \r\n')
            fe.close()
        return

    
    wf(soup,url,catalog,pname,sname)
    for i  in  range(int(num)-1):
        driver.find_element_by_class_name('btn-next').click()

        soup = bs(driver.page_source,'lxml')
        wf(soup,url,catalog,pname,sname)


        

if __name__ == "__main__":
    options = Options()
    options.add_argument('-headless')
    driver = Firefox(executable_path='geckodriver', options=options)
    #wait = WebDriverWait(driver, timeout=10)
    f = open('url.txt','r',encoding='utf-8')
    a=1
    while True:
        if a%1000==0:
            driver.quit()
            driver = Firefox(executable_path='geckodriver', options=options)
        url = f.readline()
        if not url:
            break
        if url.isspace() :
            continue
        print("第"+str(a)+'个链接')
        try:
        	dopage(driver,url)
        except:
        	with open("error.txt","a+",encoding="utf-8") as fl:
        		fl.write(url+"   ---E1\r\n")
        a+=1
        time.sleep(1)
    #url='https://www.zcygov.cn/items/34524293?searchType=1'
    f.close()
    driver.quit()
