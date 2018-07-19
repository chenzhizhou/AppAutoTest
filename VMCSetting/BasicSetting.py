# -*- coding:utf-8 -*-
import random
import datetime
from selenium.webdriver.support.wait import WebDriverWait
import properties
from time import sleep
import os
import xml.etree.ElementTree as ET

from appium import webdriver

configuresDict = {'机构名称': 'org-name', '服务器地址': 'server-address', '从VMC同步价格': 'syncPriceFromVmc',
                  '同步价格到VMC': 'writePriceToVMC', 'POS模式': 'POSMode', '一卡通POS模式': 'onecardPos',
                  'POS协议': 'POSProtocol', 'POS串口': 'POSSerial', '综合机是否基于库存': 'comMachBaseStock',
                  '售空商品往后排': 'backSoldout', '浏览模式': 'browseMode', '扫描头型号': 'ScanDevModel',
                  '扫描头连接方式': 'scannConnMode', '格子机选货是否用键盘': 'GridBrowseMode',
                  '弹簧机交替出货': 'ComAlternateVendout', 'VIP系统': 'VipSystem',
                  '食品机选货是否用键盘': 'SpringBrowseMode', "出货超时": "DeliverTimeout", '心跳间隔时间': 'HeartBeatInterval',
                  '支付页面超时时间(30~120)': 'PaymentViewTimeout', '掌纹支付串口': 'PalmSerial'}
checkboxesDict = {'从VMC同步价格': 'syncPriceFromVmc',
                  '同步价格到VMC': 'writePriceToVMC',
                  'POS模式': 'POSMode',
                  '一卡通POS模式': 'onecardPos',
                  '综合机是否基于库存': 'comMachBaseStock',
                  '售空商品往后排': 'backSoldout',
                  '格子机选货是否用键盘': 'GridBrowseMode',
                  '弹簧机交替出货': 'ComAlternateVendout',
                  '食品机选货是否用键盘': 'SpringBrowseMode'}
spinnerDict = {'POS协议': 'POSProtocol',
               'POS串口': 'POSSerial',
               '浏览模式': 'browseMode',
               '扫描头型号': 'ScanDevModel',
               '扫描头连接方式': 'scannConnMode',
               'VIP系统': 'VipSystem',
               '掌纹支付串口': 'PalmSerial',
               'MDB-232串口': 'MDB232SerialPort'}
editTextDict = {"出货超时": "DeliverTimeout",
                '心跳间隔时间': 'HeartBeatInterval',
                '支付页面超时时间(30~120)': 'PaymentViewTimeout'}
spinnerAssertContent = {"JW": "京微",
                        "JW-FUJI": "富士",
                        "SODO": "升途",
                        "SODO_XP100": "升途_XP100",
                        "LF280": "朗方280",
                        "LF280_SIM": "朗方280_SIM",
                        "LF282": "朗方282",
                        "BaDaTong": "八达通",
                        "USB": "USB",
                        "INTERNAL": "内置",
                        "ttyO2": "ttyO2",
                        "ttyO3": "ttyO3",
                        "ttyO4": "ttyO4",
                        "ttyO5": "ttyO5",
                        "ttyO6": "ttyO6",
                        "ttyO7": "ttyO7",
                        "Newland": "Newland",
                        "Superlead": "Superlead",
                        "Dewo": "Dewo",
                        "VGuang": "VGuang",
                        "WeChatVip": "微信VIP",
                        "BankPoints": "积分银行二维码",
                        "CNTYPay": "天楹积分",
                        "UPYoCard": "UP悠品卡",
                        "0": "否",
                        "1": "是",
                        None: "----"

                        }


# configuresTagList = ['org-name', 'server-address', 'syncPriceFromVmc', 'writePriceToVMC', 'POSMode', 'onecardPos',
# 'POSProtocol', 'POSSerial', 'comMachBaseStock', 'backSoldout', 'browseMode', 'ScanDevModel', 'scannConnMode',
# 'GridBrowseMode', 'ComAlternateVendout', 'VipSystem', 'SpringBrowseMode', 'HeartBeatInterval',
# 'PaymentViewTimeout', 'PalmSerial']

def logPrint(logstr):
    pyfileName = str(__file__).split(".py")[0].split("/")[-1]
    filepath = ".\\log\\" + pyfileName + '-runlog.log'
    now = str(datetime.datetime.now())
    logstr = now + ' ' + logstr
    with open(filepath, 'a', encoding='utf-8') as f:
        print(logstr)
        f.write(logstr + '\t\n')

def swipeToElementByXpath(driver, xpath):
    t = 250
    l = driver.get_window_size()
    '''向上滑动屏幕'''
    x1up = l['width'] * 0.5  # x坐标
    y1up = l['height'] * 0.75  # 起始y坐标
    y2up = l['height'] * 0.60  # 终点y坐标
    '''向下滑动屏幕'''
    x1down = l['width'] * 0.5  # x坐标
    y1down = l['height'] * 0.75  # 起始y坐标
    y2down = l['height'] * 0.90  # 终点y坐标

    isBottom = False
    isUp = True
    findFlag = False
    complateFind = 0
    while not findFlag:
        if complateFind >= 2:
            isBottom = False
            isUp = True
            findFlag = False
            print("没找到:", xpath)
            break
        if isBottom is True:
            while isUp is False:
                try:
                    if isElementExist(driver, xpath):
                        findFlag = True
                        isBottom = False
                        isUp = True
                        # print("找到了")
                        break
                    else:
                        findFlag = False
                    driver.swipe(x1down, y1down, x1down, y2down, t)
                    isUp = False
                    isBottom = False
                except Exception as e:
                    isUp = True
                    isBottom = False
                    complateFind += 1
                    # print("到顶了", complateFind)
                    sleep(1)
        if complateFind >= 2:
            isBottom = False
            isUp = True
            findFlag = False
            print("没找到:", xpath)
            break
        if isUp is True:
            while isBottom is False:
                try:
                    if isElementExist(driver, xpath):
                        findFlag = True
                        isBottom = False
                        isUp = True
                        # print("找到了")
                        break
                    else:
                        findFlag = False
                    driver.swipe(x1up, y1up, x1up, y2up, t)
                    isBottom = False
                    isUp = False
                except Exception as e:
                    isBottom = True
                    isUp = False
                    complateFind += 1
                    # print("到底了", complateFind)
                    sleep(1)
    return findFlag


def isElementExist(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False


def getElementText(elementName, xpath=None):
    if xpath is None:
        xpath = "//android.widget.TextView[@text='" + elementName + "']//..//android.widget.TextView[3]"
    # print(xpath)
    swipeToElementByXpath(driver, xpath)
    return driver.find_element_by_xpath(xpath).text


def checkToggleButton(elementName, tag):
    xpath = "//android.widget.TextView[@text='" + elementName + "']//..//android.widget.ToggleButton"
    print(xpath)
    if swipeToElementByXpath(driver, xpath) == True:
        driver.find_element_by_xpath(xpath).click()
        WebDriverWait(driver, 3).until(lambda x: x.find_element_by_xpath("//android.widget.Button[@text='取消']")).click()
        opts1 = {'command': 'cat',
                 'args': ['/sdcard/inbox/config/config.xml']}
        configxmldata = driver.execute_script("mobile: shell", opts1)
        configxmlroot = ET.fromstring(configxmldata)
        try:
            checkedFlag = driver.find_element_by_xpath(
                "//android.widget.TextView[@text='" + elementName + "']//..//android.widget.ToggleButton") \
                .get_attribute("checked")
        except:
            checkedFlag = None
        checkedvalue = configxmlroot.find(tag).text
        # print(checkedFlag, type(checkedFlag),checkedvalue,type(checkedvalue))
        if checkedFlag == 'true':
            if checkedvalue == '1':
                logPrint(elementName + "checkbox is PASS")
            else:
                logPrint("ERROR:" + elementName + "checkbox is FAIL")
        elif checkedFlag == 'false':
            if checkedvalue == '0':
                logPrint(elementName + "checkbox is PASS")
            else:
                logPrint("ERROR:" + elementName + "checkbox is FAIL")
        else:
            pass


def checkConfigList(configure, tag):
    try:
        if configure == '机构名称':
            nowText = getElementText(configure)
            nowValue = smartvm_cfgxmlroot.find(tag).text
            print(configure + "：" + nowText + "——" + nowValue)
            if nowText == nowValue:
                logPrint(configure + "：" + nowValue + " PASS")
            else:
                logPrint(configure + "：" + nowValue + " FAIL!!")
        elif configure == '服务器地址' or configure == '心跳间隔时间' or configure == '支付页面超时时间(30~120)':
            nowText = getElementText(configure)
            nowText = nowText.split(' ')[0]
            nowValue = configxmlroot.find(tag).text
            print(configure + "：" + nowText + "——" + nowValue)
            if nowText == nowValue:
                logPrint(configure + "：" + nowValue + " PASS")
            else:
                logPrint(configure + "：" + nowValue + " FAIL!!")
        else:
            nowText = getElementText(configure)
            nowValue = configxmlroot.find(tag).text
            if nowText == "----":
                nowText = None
            elif nowText == "翻页":
                nowText = "否"
            elif nowText == "滑动":
                nowText = "是"
            elif nowText == "VMC自带POS机":
                nowText = "----"
            elif nowText == "":
                nowText = "----"
            if nowText == spinnerAssertContent.get(nowValue):
                print(configure, nowValue, "++++", nowText)
                logPrint(configure + ":" + nowText + " PASS")
            else:
                print(configure, nowValue, "---------", nowText)
                logPrint(configure + ":" + nowText + " FAIL!!")
    except:
        pass


def checkSpinner(elementName, tag):
    xpath = "//android.widget.TextView[@text='" + elementName + "']//..//android.widget.Spinner//android.widget.TextView"
    # print(xpath)
    if swipeToElementByXpath(driver, xpath) == True:
        spinnerEle = driver.find_element_by_xpath(xpath)
        spinnerEle.click()
        eleInListCount = len(driver.find_elements_by_xpath("//android.widget.ListView//android.widget.TextView"))
        # print(eleInListCount)
        for ele in range(eleInListCount):
            # print(ele)
            WebDriverWait(driver, 3).until(
                lambda x: x.find_element_by_xpath(
                    "//android.widget.ListView//android.widget.TextView[" + str(ele + 1) + "]")).click()
            try:
                WebDriverWait(driver, 3).until(
                    lambda x: x.find_element_by_xpath("//android.widget.Button[@text='取消']")).click()
                opts = {'command': 'cat',
                        'args': ['/sdcard/inbox/config/config.xml']}
                configxmldata = driver.execute_script("mobile: shell", opts)
                configxmlroot = ET.fromstring(configxmldata)
                nowValue = configxmlroot.find(tag).text
                nowText = driver.find_element_by_xpath(xpath).text
                if nowText == "----":
                    nowText = None
                if nowText == spinnerAssertContent.get(nowValue):
                    print(elementName, nowValue, "++++", nowText)
                    logPrint(elementName + ":" + nowText + " PASS")
                else:
                    print(elementName, nowValue, "---------", nowText)
                    logPrint(elementName + ":" + nowText + " FAIL!!")
                if not ele + 1 == eleInListCount:
                    spinnerEle.click()
            except:
                spinnerEle.click()
        # driver.swipe(0.5, 0.75, 0.5, 0.65, 250)


def checkEditText(elementName, tag):
    xpath = "//android.widget.TextView[@text='" + elementName + "']//..//android.widget.EditText"
    if swipeToElementByXpath(driver, xpath):
        ele = driver.find_element_by_xpath(xpath)
        ele.click()
        driver.keyevent(123)
        txtlength = len(ele.text)
        for i in range(0, txtlength):
            driver.keyevent(67)
        driver.find_element_by_xpath(xpath).send_keys(random.randint(30, 120))
        xpath2 = "//android.widget.TextView[@text='" + elementName + "']"
        driver.find_element_by_xpath(xpath2).click()
        WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath("//android.widget.TextView[@text='应用']")).click()
        WebDriverWait(driver, 3).until(
            lambda x: x.find_element_by_xpath("//android.widget.Button[@text='取消']")).click()
        opts1 = {'command': 'cat',
                 'args': ['/sdcard/inbox/config/config.xml']}
        configxmldata = driver.execute_script("mobile: shell", opts1)
        configxmlroot = ET.fromstring(configxmldata)
        nowText = ele.text
        nowText = nowText.split(' ')[0]
        nowValue = configxmlroot.find(tag).text
        print(configure + "：" + nowText + "——" + nowValue)
        if nowText == nowValue:
            logPrint(configure + "：" + nowValue + " PASS")
        else:
            logPrint(configure + "：" + nowValue + " FAIL!!")


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
    logPrint("初始化：")
    os.popen("adb push " + os.getcwd() + "\\config.xml /sdcard/inbox/config")
    sleep(2)
    os.popen("adb shell am broadcast -a com.inhand.intent.INBOXCORE_RESTART_APP")
    sleep(3)
    logPrint("初始化完成")
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    opts1 = {'command': 'cat',
             'args': ['/sdcard/inbox/config/config.xml']}
    configxmldata = driver.execute_script("mobile: shell", opts1)
    configxmlroot = ET.fromstring(configxmldata)
    opts2 = {'command': 'cat',
             'args': ['/sdcard/inbox/config/smartvm_cfg.xml']}
    smartvm_cfgxmldata = driver.execute_script("mobile: shell", opts2)
    smartvm_cfgxmlroot = ET.fromstring(smartvm_cfgxmldata)
    sleep(1)
    driver.find_element_by_xpath("//android.widget.TextView[@text='基本配置']").click()
    logPrint("读取界面与配置文件中的值")
    for configure, tag in configuresDict.items():
        checkConfigList(configure, tag)
    driver.find_element_by_xpath("//android.widget.TextView[@text='高级设置']").click()
    logPrint("检查可选项功能")
    for configure, tag in checkboxesDict.items():
        checkToggleButton(configure, tag)
    logPrint("检查下拉选项功能")
    spinnerAssertContent['0'] = "翻页"
    spinnerAssertContent['1'] = "滑动"
    for configure, tag in spinnerDict.items():
        checkSpinner(configure, tag)

    logPrint("检查可编辑框功能")
    for configure, tag in editTextDict.items():
        checkEditText(configure, tag)
    logPrint("还原最初环境：")
    os.popen("adb push " + os.getcwd() + "\\config.xml /sdcard/inbox/config")
    sleep(2)
    os.popen("adb shell am broadcast -a com.inhand.intent.INBOXCORE_RESTART_APP")
    sleep(3)
    logPrint("还原最初环境完成")
