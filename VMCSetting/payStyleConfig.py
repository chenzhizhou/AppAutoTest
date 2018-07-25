# -*- coding:utf-8 -*-

import datetime
import json
import os
import urllib
from time import sleep

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import properties
from appium import webdriver
import base64


def logPrint(log_str):
    py_file_name = str(__file__).split(".py")[0].split("/")[-1]
    file_path = ".\\log\\" + py_file_name + '-runlog.log'
    now = str(datetime.datetime.now())
    log_str = now + ' ' + log_str
    with open(file_path, 'a', encoding='utf-8') as f:
        print(log_str)
        f.write(log_str + '\t\n')


def restart_app(driver):
    optsRestartAPP = {'command': 'am broadcast -a',
                      'args': ['com.inhand.intent.INBOXCORE_RESTART_APP']}
    driver.execute_script("mobile: shell", optsRestartAPP)


def find_toast(driver, contains_message):
    '''判断toast信息'''
    locat = ("xpath", '//*[contains(@text,"' + contains_message + '")]')
    try:
        element = WebDriverWait(driver, 2).until(EC.presence_of_element_located(locat))
        return True
    except:
        return False


def wifi_disable(driver):
    opts = {'command': 'su 0',
            'args': ['svc wifi disable']}
    driver.execute_script("mobile: shell", opts)


def wifi_enable(driver):
    opts = {'command': 'su 0',
            'args': ['svc wifi enable']}
    driver.execute_script("mobile: shell", opts)


def isElementExist(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def swipeToElementByXpath(driver, xpath_for_find, frist_last_xpath):
    t = 500
    l = driver.get_window_size()
    '''向上滑动屏幕'''
    x1up = l['width'] * 0.5  # x坐标
    y1up = l['height'] * 0.8  # 起始y坐标
    y2up = l['height'] * 0.4  # 终点y坐标
    '''向下滑动屏幕'''
    x1down = l['width'] * 0.5  # x坐标
    y1down = l['height'] * 0.4  # 起始y坐标
    y2down = l['height'] * 0.8  # 终点y坐标

    isBottom = False
    isUp = True
    findFlag = False
    complate_find = 0

    while not findFlag:
        if complate_find >= 2:
            isBottom = False
            isUp = True
            findFlag = False
            print("没找到:", xpath_for_find)
            break
        if isUp is True:
            while isBottom is False:
                if isElementExist(driver, xpath_for_find):
                    findFlag = True
                    isBottom = False
                    isUp = True
                    # print("找到了")
                    break
                else:
                    findFlag = False
                try:
                    list = driver.find_elements_by_xpath(frist_last_xpath)
                    before_swipe_last_text = list[len(list) - 1].text
                    # print(before_swipe_last_text)
                except:
                    print("没有找到判断末尾组元素：", frist_last_xpath)
                try:
                    driver.swipe(x1up, y1up, x1up, y2up, t)
                    sleep(1)
                    list = driver.find_elements_by_xpath(frist_last_xpath)
                    after_swipe_last_text = list[len(list) - 1].text
                    # print(after_swipe_last_text)
                except:
                    sleep(1)
                    list = driver.find_elements_by_xpath(frist_last_xpath)
                    after_swipe_last_text = list[len(list) - 1].text
                    # print(after_swipe_last_text)
                # print("before:", before_swipe_last_text, "after:", after_swipe_last_text)
                if before_swipe_last_text == after_swipe_last_text:
                    isBottom = True
                    isUp = False
                    complate_find += 1
                    # print("到底了", complate_find)
                    sleep(1)
        if complate_find >= 2:
            isBottom = False
            isUp = True
            findFlag = False
            # print("没找到:", xpath_for_find)
            break
        if isBottom is True:
            while isUp is False:
                if isElementExist(driver, xpath_for_find):
                    findFlag = True
                    isBottom = False
                    isUp = True
                    # print("找到了")
                    break
                else:
                    findFlag = False
                try:
                    list = driver.find_elements_by_xpath(frist_last_xpath)
                    before_swipe_last_text = list[0].text
                    # print(before_swipe_last_text)
                except:
                    print("没有找到判断末尾组元素：", frist_last_xpath)
                try:
                    driver.swipe(x1down, y1down, x1down, y2down, t)
                    sleep(1)
                    list = driver.find_elements_by_xpath(frist_last_xpath)
                    after_swipe_last_text = list[0].text
                    # print(after_swipe_last_text)
                except:
                    sleep(1)
                    list = driver.find_elements_by_xpath(frist_last_xpath)
                    after_swipe_last_text = list[0].text
                    # print(after_swipe_last_text)
                # print("before:", before_swipe_last_text, "after:", after_swipe_last_text)
                if before_swipe_last_text == after_swipe_last_text:
                    isBottom = False
                    isUp = True
                    complate_find += 1
                    # print("到顶了", complate_find)
                    sleep(1)
    # print("DONE")
    return findFlag


if __name__ == '__main__':
    try:
        log_path = os.getcwd() + "\\log"
        os.mkdir(log_path)
    except:
        pass
    py_fileName = str(__file__).split(".py")[0].split("/")[-1]
    log_filePath = ".\\log\\" + py_fileName + '-runlog.log'
    try:
        os.remove(log_filePath)
    except:
        pass
    logPrint("初始化：")
    # os.popen("adb push " + os.getcwd() + "\\config.xml /sdcard/inbox/config")
    # sleep(2)
    # os.popen("adb shell am broadcast -a com.inhand.intent.INBOXCORE_RESTART_APP")
    # sleep(3)
    fo = open("config.xml", "r+")
    data = fo.read()
    fo.close()
    encode_configxml = base64.b64encode(data.encode('utf-8'))
    configxml_base64 = str(encode_configxml, 'utf-8')
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.push_file("/sdcard/inbox/config/config.xml", configxml_base64)
    restart_app(driver)
    logPrint("初始化完成")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='支付配置']").click()
    paystyle_list = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout")
    paystyle_name = driver.find_element_by_xpath(
        "//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView").text
    if len(paystyle_list) == 1 and paystyle_name == "现金支付":
        logPrint("只有现金支付：PASS")
    else:
        logPrint("只有现金支付：FAIL!!")
    add_paystyle_xpath = "//android.widget.TextView[@text='增加支付方式']"
    while 1:
        swipeToElementByXpath(driver, xpath_for_find=add_paystyle_xpath,
                              frist_last_xpath="//android.widget.ListView/android.widget.LinearLayout")
        driver.find_element_by_xpath(add_paystyle_xpath).click()
        if isElementExist(driver, "//android.widget.TextView[@text='选择需要添加的支付方式']"):
            driver.find_element_by_xpath("//android.widget.ListView/android.widget.LinearLayout[1]").click()
        else:
            break
    driver.find_element_by_xpath("//android.widget.TextView[@text='应用']").click()
    sleep(0.5)
    if find_toast(driver, "操作"):
        logPrint("添加支付方式：PASS")
    else:
        logPrint("添加支付方式：FAIL!!")
    driver.find_element_by_xpath("//android.widget.TextView[@text='支付配置']").click()
    driver.find_element_by_xpath(
        "//android.widget.ListView/android.widget.LinearLayout[4]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[1]/android.widget.ImageView[1]").click()
    driver.find_element_by_xpath(
        "//android.widget.ListView/android.widget.LinearLayout[3]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[2]/android.widget.ImageView[1]").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='应用']").click()
    if find_toast(driver, "操作"):
        logPrint("支付方式排序：PASS")
    else:
        logPrint("支付方式排序：FAIL!!")
    driver.find_element_by_xpath("//android.widget.TextView[@text='支付配置']").click()
    while isElementExist(driver, "//android.widget.ListView/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[3]/android.widget.ImageView[1]"):
        driver.find_element_by_xpath("//android.widget.ListView/android.widget.LinearLayout[2]/android.widget.RelativeLayout[1]/android.widget.LinearLayout[3]/android.widget.ImageView[1]").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='应用']").click()
    flag = find_toast(driver, "操作")
    driver.find_element_by_xpath("//android.widget.TextView[@text='支付配置']").click()
    paystyle_list = driver.find_elements_by_xpath("//android.widget.ListView/android.widget.LinearLayout")
    paystyle_name = driver.find_element_by_xpath(
        "//android.widget.ListView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView").text
    if len(paystyle_list) == 1 and paystyle_name == "现金支付" and flag == True:
        logPrint("支付方式删除：PASS")
    else:
        logPrint("支付方式删除：FAIL!!")
    driver.find_element_by_xpath("//android.widget.TextView[@text='返回']").click()
