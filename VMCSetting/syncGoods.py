# -*- coding:utf-8 -*-
import datetime
import json
import os
import urllib
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import properties
from time import sleep
from appium import webdriver


def logPrint(logstr):
    pyfileName = str(__file__).split(".py")[0].split("/")[-1]
    filepath = ".\\log\\" + pyfileName + '-runlog.log'
    now = str(datetime.datetime.now())
    logstr = now + ' ' + logstr
    with open(filepath, 'a', encoding='utf-8') as f:
        print(logstr)
        f.write(logstr + '\t\n')


def isElementExist(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def find_toast(driver, contains_message):
    '''判断toast信息'''
    locat = ("xpath", '//*[contains(@text,"' + contains_message + '")]')
    try:
        element = WebDriverWait(driver, 2).until(EC.presence_of_element_located(locat))
        return True
    except:
        return False


def restart_app(driver):
    optsRestartAPP = {'command': 'am broadcast -a',
                      'args': ['com.inhand.intent.INBOXCORE_RESTART_APP']}
    driver.execute_script("mobile: shell", optsRestartAPP)


def wifi_disable(driver):
    opts = {'command': 'su 0',
            'args': ['svc wifi disable']}
    driver.execute_script("mobile: shell", opts)

def wifi_enable(driver):
    opts = {'command': 'su 0',
            'args': ['svc wifi enable']}
    driver.execute_script("mobile: shell", opts)

if __name__ == '__main__':
    try:
        logpath = os.getcwd() + "\\log"
        # print(logpath)
        os.mkdir(logpath)
    except:
        pass
    pyfileName = str(__file__).split(".py")[0].split("/")[-1]
    logfilepath = ".\\log\\" + pyfileName + '-runlog.log'
    try:
        os.remove(logfilepath)
    except:
        pass
        host = 'http://182.150.21.232:10081'
        requesturl = "/oauth2/access_token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
        }
        get_token_value = {
            "client_id": "000017953450251798098136",
            "client_secret": "08E9EC6793345759456CB8BAE52615F3",
            "grant_type": "password",
            "username": "chenzhiz@inhand.com.cn",
            "password": "czz123456",
            "password_type": "1",
            "language": "2"
        }
        data = urllib.parse.urlencode(get_token_value).encode('utf-8')
        url = host + requesturl
        request = urllib.request.Request(url, data, headers)
        token_response = urllib.request.urlopen(request).read().decode('utf-8')
        logPrint(token_response)
        access_token = json.loads(token_response)['access_token']

    requesturl = "/api/goods/list?cursor=0&limit=30&name=&access_token=" + access_token
    url = host + requesturl
    response = requests.get(url=url, headers={'Content-Type': 'application/json'})
    goods_count = json.loads(response.text)['total']
    print(goods_count)
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    sleep(0.5)
    wifi_enable(driver)
    sleep(0.5)
    opts1 = {'command': 'rm -rf',
             'args': ['/sdcard/inbox/data/picture']}
    redata = driver.execute_script("mobile: shell", opts1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='货道配置']").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步商品(从平台)']").click()
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    try:
        xpath = "//android.widget.TextView[contains(@text,'总商品数 " + str(goods_count) + "')]"
        logPrint(xpath)
        WebDriverWait(driver, 2, 0.5).until(lambda x: x.find_element_by_xpath(xpath))
        progressFlag = True
    except Exception as e:
        print(e)
        progressFlag = False
    if progressFlag:
        logPrint("同步过程：PASS")
    else:
        logPrint("同步过程：FAIL!!")
    loadmasklocator = ("xpath", "//android.widget.ProgressBar")
    try:
        WebDriverWait(driver, 180).until_not(EC.presence_of_element_located(loadmasklocator))
        completeFlag = True
    except Exception as e:
        completeFlag = False
    if completeFlag:
        logPrint("同步结果出现：PASS")
    else:
        logPrint("同步结果出现：FAIL!!")
    if isElementExist(driver, "//android.widget.TextView[contains(@text,'操作成功')]"):
        logPrint("同步成功：PASS")
    else:
        logPrint("同步成功：FAIL!!")
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    sleep(20)
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='货道配置']").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步商品(从平台)']").click()
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    try:
        WebDriverWait(driver, 180).until_not(EC.presence_of_element_located(loadmasklocator))
        completeFlag = True
    except Exception as e:
        completeFlag = False
    if completeFlag:
        logPrint("同步结果出现：PASS")
    else:
        logPrint("同步结果出现：FAIL!!")
    if isElementExist(driver, "//android.widget.TextView[contains(@text,'已经是最新配置')]"):
        logPrint("已经是最新配置：PASS")
    else:
        logPrint("已经是最新配置：FAIL!!")
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    wifi_disable(driver)
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步商品(从平台)']").click()
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    okdialoglocator = ("xpath", "//android.widget.TextView[contains(@text,'操作失败')]")
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located(okdialoglocator))
        failFlag = True
    except Exception as e:
        failFlag = False
    if failFlag:
        logPrint("断网同步，操作失败：PASS")
    else:
        logPrint("断网同步，操作失败：FAIL!!")
    wifi_enable(driver)
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    opts1 = {'command': 'rm -rf',
             'args': ['/sdcard/inbox/data/picture']}
    redata = driver.execute_script("mobile: shell", opts1)
    sleep(10)
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步商品(从平台)']").click()
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    sleep(5)
    wifi_disable(driver)
    loadmasklocator = ("xpath", "//android.widget.ProgressBar")
    try:
        WebDriverWait(driver, 180).until_not(EC.presence_of_element_located(loadmasklocator))
        completeFlag = True
    except Exception as e:
        completeFlag = False
    if completeFlag:
        logPrint("同步结果出现：PASS")
    else:
        logPrint("同步结果出现：FAIL!!")
    if isElementExist(driver, "//android.widget.TextView[contains(@text,'操作成功')]"):
        logPrint("断网结束同步：PASS")
    else:
        logPrint("断网结束同步：FAIL!!")
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    sleep(12)
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='货道配置']").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步商品(从平台)']").click()
    noNetFlag = find_toast(driver, "平台")
    if noNetFlag:
        logPrint("未与平台建立连接：PASS")
    else:
        logPrint("未与平台建立连接：FAIL!!")
    wifi_enable(driver)
