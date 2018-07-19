# -*- coding:utf-8 -*-
"""
182.150.21.232:10081中inhand-chenzhiz机构中存在一设备：
autotest
预置机型
APP修改编号和设备，后还原
不接机器
主柜串口ttyO2
"""
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
    host = 'http://182.150.21.232:10081'
    request_url = "/oauth2/access_token"
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36 '
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
    logPrint("测试初始化：")
    data = urllib.parse.urlencode(get_token_value).encode('utf-8')
    url = host + request_url
    request = urllib.request.Request(url, data, token_headers)
    token_response = urllib.request.urlopen(request).read().decode('utf-8')
    logPrint(token_response)
    access_token = json.loads(token_response)['access_token']

    request_url = "/api/automatv2/5b45b0831ab68b7e4d775299?access_token=" + access_token
    url = host + request_url
    bind_model_json = '{"location":{"longitude":"104.03113","latitude":"30.679943","region":""},' \
                      '"siteId":"5ab4badea476c4f1512cf45e","siteName":"一大哥私人点位2","siteNumber":"1521793744",' \
                      '"modelConfigsNew":{"modelId":"5b45a2061ab662a79a99f170","modelName":"syncModel-10drink",' \
                      '"masterTypeNew":"1","vender":"富士冰山","venderNum":"fuji"},"config":{"vender":"fuji",' \
                      '"protocol":"1","port":"ttyO2"},"masterType":"1","lineId":"5ab4b7d1a476c4f1512cf458",' \
                      '"lineName":"一大哥区域1线路1","payConfig":[{"payId":"5a4b3421ad34e9e9587cf304","payName":"WECHAT"},' \
                      '{"payId":"5a4dda8fa476105d788caf3e","payName":"UNIONPAY"},{"payId":"5a4ddc06a476105d788caf3f",' \
                      '"payName":"BAIDU"},{"payId":"5addb3aef1d68f692a6c3748","payName":"UNICOMPAY"},' \
                      '{"payId":"5b1a44b3bb544cb9c273c6c3","payName":"YIFUBAO"},{"payId":"5a4c8e03a476105d788caf3c",' \
                      '"payName":"QRCODEPAY"},{"payId":"5a4b344fad34e9e9587cf305","payName":"ALIPAY"}],' \
                      '"refundConfig":[],"name":"apptest","assetId":"apptest","alipay_store_id":"","deviceType":"0",' \
                      '"qrcodepay_mchid":"","containersNew":[{"cid":"1","modelId":"5b45a3911ab662a79a99f171",' \
                      '"modelName":"syncModel-15spring","type":"2","vender":"富士冰山","venderNum":"fuji",' \
                      '"serial":"ttyO3","vmcNum":"1","plugIn":"1","shelves":[{"location_id":"1","status":1},' \
                      '{"location_id":"2","status":1},{"location_id":"3","status":1},{"location_id":"4","status":1},' \
                      '{"location_id":"5","status":1},{"location_id":"6","status":1},{"location_id":"7","status":1},' \
                      '{"location_id":"8","status":1},{"location_id":"9","status":1},{"location_id":"10","status":1},' \
                      '{"location_id":"11","status":1},{"location_id":"12","status":1},{"location_id":"13",' \
                      '"status":1},{"location_id":"14","status":1},{"location_id":"15","status":1}]},{"cid":"2",' \
                      '"modelId":"5b45a3cf1ab662a79a99f172","modelName":"syncModel-5grid","type":"3","vender":"富士冰山",' \
                      '"venderNum":"fuji","serial":"ttyO4","vmcNum":"2","plugIn":"1","shelves":[{"location_id":"1",' \
                      '"status":1},{"location_id":"2","status":1},{"location_id":"3","status":1},{"location_id":"4",' \
                      '"status":1},{"location_id":"5","status":1}]}],"cpemail":"chenzhiz@inhand.com.cn",' \
                      '"createPerson":"chenzhiz"} '
    bind_model_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36 '
    }
    bind_model_data = bytes(bind_model_json, encoding="utf8")
    request = urllib.request.Request(url, bind_model_data, bind_model_headers, method='PUT')
    bind_model_response = urllib.request.urlopen(request).read().decode('utf-8')
    logPrint(bind_model_response)

    encode_machineId = base64.b64encode('apptest'.encode('utf-8'))
    machine_id_base64 = str(encode_machineId, 'utf-8')
    print(machine_id_base64)
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.push_file("/sdcard/inbox/config/machine_id.txt", machine_id_base64)
    pushFile_opts = {'command': 'cat',
                     'args': ['/sdcard/inbox/config/machine_id.txt']}
    driver.execute_script("mobile: shell", pushFile_opts)
    restart_app(driver)
    sleep(10)
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步配置']").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步机型']").click()
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    loadMask_locator = ("xpath", "//android.widget.ProgressBar")
    try:
        WebDriverWait(driver, 180).until_not(EC.presence_of_element_located(loadMask_locator))
        completeFlag = True
    except Exception as e:
        completeFlag = False
    if completeFlag:
        logPrint("同步结果出现：PASS")
    else:
        logPrint("同步结果出现：FAIL!!")
    sleep(5)
    opts = {'command': 'md5',
            'args': ['/sdcard/inbox/config/smartvm_cfg.xml']}
    md5 = driver.execute_script("mobile: shell", opts)
    md5 = md5.split("  ")[0]
    logPrint(md5)
    if md5 == "4333312e7a266703b784461fcf2dd00c":
        logPrint("验证md5：PASS")
    else:
        logPrint("验证md5：FAIL!!")
    sleep(8)
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='货道配置']").click()
    vm_grid_list = driver.find_elements_by_xpath("//android.widget.GridView/android.widget.RelativeLayout")
    if len(vm_grid_list) == 3:
        logPrint("验证货柜数目3：PASS")
    else:
        logPrint("验证货柜数目3：FAIL")
driver.find_element_by_xpath("//android.widget.TextView[@text='主 柜']").click()
first_last_xpath = "//android.widget.LinearLayout/android.widget.TextView[contains(@text,'货道')] "
masterCount = 0
pass_number = 10
for i in range(1, pass_number + 1):
    xpath = "//android.widget.TextView[@text='货道:%s']" % str(i)
    if swipeToElementByXpath(driver, xpath_for_find=xpath, frist_last_xpath=first_last_xpath):
        masterCount += 1
if masterCount == pass_number:
    logPrint("验证master货道数目%d：PASS" % pass_number)
else:
    logPrint("验证master货道数目%d：FAIL!!" % pass_number)
driver.find_element_by_xpath("//android.widget.TextView[@text='返回']").click()
driver.find_element_by_xpath("//android.widget.TextView[@text='柜: 1']").click()
slave1Count = 0
pass_number = 15
for i in range(1, pass_number + 1):
    xpath = "//android.widget.TextView[@text='货道:%s']" % str(i)
    if swipeToElementByXpath(driver, xpath_for_find=xpath, frist_last_xpath=first_last_xpath):
        slave1Count += 1
if slave1Count == pass_number:
    logPrint("验证柜1货道数目%d：PASS" % pass_number)
else:
    logPrint("验证柜1货道数目%d：FAIL!!" % pass_number)
driver.find_element_by_xpath("//android.widget.TextView[@text='返回']").click()
driver.find_element_by_xpath("//android.widget.TextView[@text='柜: 2']").click()
slave2Count = 0
pass_number = 5
for i in range(1, pass_number + 1):
    xpath = "//android.widget.TextView[@text='货道:%s']" % str(i)
    if swipeToElementByXpath(driver, xpath_for_find=xpath, frist_last_xpath=first_last_xpath):
        slave2Count += 1
if slave2Count == pass_number:
    logPrint("验证柜2货道数目%d：PASS" % pass_number)
else:
    logPrint("验证柜2货道数目%d：FAIL!!" % pass_number)
