# -*- coding:utf-8 -*-
"""
182.150.21.232:10081中inhand-chenzhiz机构中存在一设备：
autotest
预置机型

APP修改编号和设备，后还原
不接机器
配置货道
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
    bind_channel_json_have_data = '{"oid":"5a46053a1d41c84ada000002","name":"apptest","assetId":"apptest","online":0,' \
                                  '"deviceStatus":0,"activationTime":1531980503,"siteId":"5ab4badea476c4f1512cf45e",' \
                                  '"siteName":"一大哥私人点位2","siteNumber":"1521793744","serialNumber":"BT3101745001785",' \
                                  '"gwId":"5a66f500a4762bcdf126f1d2","modelConfigsNew":{' \
                                  '"modelId":"5b45a2061ab662a79a99f170","modelName":"syncModel-10drink",' \
                                  '"masterTypeNew":1,"vender":"富士冰山","venderNum":"fuji"},"location":{"region":"",' \
                                  '"longitude":104.03113,"latitude":30.679943},"userDefine":0,"masterType":1,' \
                                  '"masterArr":[10],"goodsConfigs":[{"location_id":"1","status":"1"},' \
                                  '{"location_id":"2","status":"1"},{"location_id":"3","status":"1"},' \
                                  '{"location_id":"4","status":"1"},{"location_id":"5","status":"1"},' \
                                  '{"location_id":"6","status":"1"},{"location_id":"7","status":"1"},' \
                                  '{"location_id":"8","status":"1"},{"location_id":"9","status":"1"},' \
                                  '{"location_id":"10","status":"1"}],"containers":[{"cid":"1","type":2,"shelves":[{' \
                                  '"location_id":"1","status":"1"},{"location_id":"2","status":"1"},' \
                                  '{"location_id":"3","status":"1"},{"location_id":"4","status":"1"},' \
                                  '{"location_id":"5","status":"1"},{"location_id":"6","status":"1"},' \
                                  '{"location_id":"7","status":"1"},{"location_id":"8","status":"1"},' \
                                  '{"location_id":"9","status":"1"},{"location_id":"10","status":"1"},' \
                                  '{"location_id":"11","status":"1"},{"location_id":"12","status":"1"},' \
                                  '{"location_id":"13","status":"1"},{"location_id":"14","status":"1"},' \
                                  '{"location_id":"15","status":"1"}],"shelvesArr":[15]},{"cid":"2","type":3,' \
                                  '"shelves":[{"location_id":"1","status":"1"},{"location_id":"2","status":"1"},' \
                                  '{"location_id":"3","status":"1"},{"location_id":"4","status":"1"},' \
                                  '{"location_id":"5","status":"1"}],"shelvesArr":[5]}],"goodsConfigsNew":[{' \
                                  '"location_id":"1"},{"location_id":"2","alipay_url":""},{"location_id":"3",' \
                                  '"goods_id":"595b2f2a0cf2c3cb08b99f0d","goods_name":"海苔",' \
                                  '"goods_type":"5a4c9e1fa476e414a29138e8","goods_typeName":"食品","price":"111",' \
                                  '"img_cdn":"","img":"5b32d334bb5420c6de865daf",' \
                                  '"imagemd5":"b40b11bdd9b76b35e8f71fdddc20a687","capacity":"11","valve":"1"},' \
                                  '{"location_id":"4"},{"location_id":"5"},{"location_id":"6"},{"location_id":"7"},' \
                                  '{"location_id":"8"},{"location_id":"9"},{"location_id":"10"}],"containersNew":[{' \
                                  '"modelId":"5b45a3911ab662a79a99f171","modelName":"syncModel-15spring","cid":"1",' \
                                  '"type":2,"vender":"富士冰山","venderNum":"fuji","serial":"ttyO3","vmcNum":"1",' \
                                  '"plugIn":"1","shelves":[{"location_id":"1","alipay_url":""},{"location_id":"2"},' \
                                  '{"location_id":"3","goods_id":"595b2f2a0cf2c3cb08b99f0d","goods_name":"海苔",' \
                                  '"goods_type":"5a4c9e1fa476e414a29138e8","goods_typeName":"食品","price":"111",' \
                                  '"img_cdn":"","img":"5b32d334bb5420c6de865daf",' \
                                  '"imagemd5":"b40b11bdd9b76b35e8f71fdddc20a687","capacity":"11","valve":"1"},' \
                                  '{"location_id":"4"},{"location_id":"5"},{"location_id":"6"},{"location_id":"7"},' \
                                  '{"location_id":"8"},{"location_id":"9"},{"location_id":"10"},{"location_id":"11"},' \
                                  '{"location_id":"12"},{"location_id":"13"},{"location_id":"14"},' \
                                  '{"location_id":"15"}]},{"modelId":"5b45a3cf1ab662a79a99f172",' \
                                  '"modelName":"syncModel-5grid","cid":"2","type":3,"vender":"富士冰山",' \
                                  '"venderNum":"fuji","serial":"ttyO4","vmcNum":"2","plugIn":"1","shelves":[{' \
                                  '"location_id":"1"},{"location_id":"2"},{"location_id":"3",' \
                                  '"goods_id":"595b2f2a0cf2c3cb08b99f0d","goods_name":"海苔",' \
                                  '"goods_type":"5a4c9e1fa476e414a29138e8","goods_typeName":"食品","price":"111",' \
                                  '"img_cdn":"","img":"5b32d334bb5420c6de865daf",' \
                                  '"imagemd5":"b40b11bdd9b76b35e8f71fdddc20a687","capacity":"1","valve":"0"},' \
                                  '{"location_id":"4"},{"location_id":"5"}]}],"inboxConfig":{"fireware":"IHv2.0.17",' \
                                  '"apps":[{"name":"AdService","version":"1.345.r6680"},' \
                                  '{"name":"DeviceManagerService","version":"1.346.r6680"},{"name":"InBoxCore",' \
                                  '"version":"1.88.r6521"},{"name":"Install","version":"Install1.1.r6"},' \
                                  '{"name":"PayService","version":"1.344.r6680"},{"name":"SmartVM",' \
                                  '"version":"Aucma2.343.r6680"},{"name":"VendingCloudService",' \
                                  '"version":"2.353.r6680"},{"name":"VideoPlayer","version":"SplitScreen.284.r6680"},' \
                                  '{"name":"VMCService","version":"Aucma2.685.r6680"},{"name":"VMCSettings",' \
                                  '"version":"2.348.r6680"},{"name":"Appium Settings","version":"2.3"},' \
                                  '{"name":"Unlock","version":"2.0.0"}],"vendingData":[{"name":"ad","type":"8001",' \
                                  '"version":"ad.1527746976"}]},"vendingState":{"doorState":0,"isSale":0,' \
                                  '"coin5Count":0,"coin10Count":0,"vmcOnline":1,"faultCode":[0,0,0,0,0,0,0,0,0,0,0,0,' \
                                  '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,' \
                                  '0,0,0,0,0,0,0,0,0,0,0],"shelvesState":[{"cid":"9","shelvesId":"11","state":1},' \
                                  '{"cid":"9","shelvesId":"13","state":1},{"cid":"9","shelvesId":"15","state":1},' \
                                  '{"cid":"9","shelvesId":"21","state":1},{"cid":"9","shelvesId":"22","state":1},' \
                                  '{"cid":"9","shelvesId":"23","state":1},{"cid":"9","shelvesId":"24","state":1},' \
                                  '{"cid":"9","shelvesId":"25","state":1},{"cid":"9","shelvesId":"26","state":1},' \
                                  '{"cid":"9","shelvesId":"31","state":1},{"cid":"9","shelvesId":"32","state":1},' \
                                  '{"cid":"9","shelvesId":"33","state":1},{"cid":"9","shelvesId":"35","state":1},' \
                                  '{"cid":"9","shelvesId":"41","state":1},{"cid":"9","shelvesId":"42","state":1},' \
                                  '{"cid":"9","shelvesId":"43","state":1},{"cid":"9","shelvesId":"44","state":1},' \
                                  '{"cid":"9","shelvesId":"45","state":1},{"cid":"9","shelvesId":"46","state":1},' \
                                  '{"cid":"9","shelvesId":"51","state":1},{"cid":"9","shelvesId":"52","state":1},' \
                                  '{"cid":"9","shelvesId":"53","state":1},{"cid":"9","shelvesId":"54","state":1},' \
                                  '{"cid":"9","shelvesId":"55","state":1},{"cid":"9","shelvesId":"56","state":1},' \
                                  '{"cid":"9","shelvesId":"57","state":1},{"cid":"9","shelvesId":"58","state":1},' \
                                  '{"cid":"9","shelvesId":"61","state":1},{"cid":"9","shelvesId":"62","state":1},' \
                                  '{"cid":"9","shelvesId":"63","state":1},{"cid":"9","shelvesId":"64","state":1},' \
                                  '{"cid":"9","shelvesId":"65","state":1},{"cid":"9","shelvesId":"66","state":1},' \
                                  '{"cid":"9","shelvesId":"67","state":1},{"cid":"9","shelvesId":"68","state":1},' \
                                  '{"cid":"2","shelvesId":"3","state":0},{"cid":"1","shelvesId":"1","state":0},' \
                                  '{"cid":"apptest","shelvesId":"1","state":1}],"vendingFault":[]},"config":{' \
                                  '"vender":"fuji","protocol":"1","port":"ttyO2"},"coin_capacity":[30,20,0],' \
                                  '"lineId":"5ab4b7d1a476c4f1512cf458","lineName":"一大哥区域1线路1","payConfig":[{' \
                                  '"payId":"5a4b3421ad34e9e9587cf304","payName":"WECHAT"},' \
                                  '{"payId":"5a4dda8fa476105d788caf3e","payName":"UNIONPAY"},' \
                                  '{"payId":"5a4ddc06a476105d788caf3f","payName":"BAIDU"},' \
                                  '{"payId":"5addb3aef1d68f692a6c3748","payName":"UNICOMPAY"},' \
                                  '{"payId":"5b1a44b3bb544cb9c273c6c3","payName":"YIFUBAO"},' \
                                  '{"payId":"5a4c8e03a476105d788caf3c","payName":"QRCODEPAY"},' \
                                  '{"payId":"5a4b344fad34e9e9587cf305","payName":"ALIPAY"}],"sessionId":"WebSocket ' \
                                  'session id=380","sync":1,"onlineType":0,"createTime":1531293827,' \
                                  '"updateTime":1531980503,"lastAlive":1531980503,"host":"10.5.16.1:3311",' \
                                  '"shelfcount":0,"containerNum":0,"alipay_store_id":"","adFileList":{"fileList":[{' \
                                  '"dir":"ads","files":[{"name":"dibai.mp4"}]},{"dir":"ads/S0","files":[{' \
                                  '"name":"dibai.mp4"},{"name":"pic370.png"}]}]},"refundConfig":[],' \
                                  '"qrcodepay_mchid":"","deviceType":0,"_id":"5b45b0831ab68b7e4d775299"} '
    bind_channel_json_empty = '{"oid":"5a46053a1d41c84ada000002","name":"apptest","assetId":"apptest","online":0,' \
                              '"deviceStatus":0,"activationTime":1531968714,"siteId":"5ab4badea476c4f1512cf45e",' \
                              '"siteName":"一大哥私人点位2","siteNumber":"1521793744","serialNumber":"BT3101745001785",' \
                              '"gwId":"5a66f500a4762bcdf126f1d2","modelConfigsNew":{' \
                              '"modelId":"5b45a2061ab662a79a99f170","modelName":"syncModel-10drink",' \
                              '"masterTypeNew":1,"vender":"富士冰山","venderNum":"fuji"},"location":{"region":"",' \
                              '"longitude":104.03113,"latitude":30.679943},"userDefine":0,"masterType":1,' \
                              '"masterArr":[10],"goodsConfigs":[{"location_id":"1","status":"1"},{"location_id":"2",' \
                              '"goods_id":"595b2f2a0cf2c3cb08b99f0d","goods_name":"海苔","price":"22.2",' \
                              '"img":"5b32d334bb5420c6de865daf","payment_url":"",' \
                              '"imagemd5":"b40b11bdd9b76b35e8f71fdddc20a687","status":"1","capacity":22,"valve":2},' \
                              '{"location_id":"3","status":"1"},{"location_id":"4","status":"1"},{"location_id":"5",' \
                              '"status":"1"},{"location_id":"6","status":"1"},{"location_id":"7","status":"1"},' \
                              '{"location_id":"8","status":"1"},{"location_id":"9","status":"1"},{"location_id":"10",' \
                              '"status":"1"}],"containers":[{"cid":"1","type":2,"shelves":[{"location_id":"1",' \
                              '"goods_id":"595b2f2a0cf2c3cb08b99f0d","goods_name":"海苔","price":"11.1",' \
                              '"img":"5b32d334bb5420c6de865daf","payment_url":"",' \
                              '"imagemd5":"b40b11bdd9b76b35e8f71fdddc20a687","status":"1","capacity":11,"valve":1},' \
                              '{"location_id":"2","status":"1"},{"location_id":"3","status":"1"},{"location_id":"4",' \
                              '"status":"1"},{"location_id":"5","status":"1"},{"location_id":"6","status":"1"},' \
                              '{"location_id":"7","status":"1"},{"location_id":"8","status":"1"},{"location_id":"9",' \
                              '"status":"1"},{"location_id":"10","status":"1"},{"location_id":"11","status":"1"},' \
                              '{"location_id":"12","status":"1"},{"location_id":"13","status":"1"},' \
                              '{"location_id":"14","status":"1"},{"location_id":"15","status":"1"}],"shelvesArr":[' \
                              '15]},{"cid":"2","type":3,"shelves":[{"location_id":"1","status":"1"},' \
                              '{"location_id":"2","status":"1"},{"location_id":"3",' \
                              '"goods_id":"595b2f2a0cf2c3cb08b99f0d","goods_name":"海苔","price":"33.3",' \
                              '"img":"5b32d334bb5420c6de865daf","payment_url":"",' \
                              '"imagemd5":"b40b11bdd9b76b35e8f71fdddc20a687","status":"1","capacity":1,"valve":0},' \
                              '{"location_id":"4","status":"1"},{"location_id":"5","status":"1"}],"shelvesArr":[5]}],' \
                              '"goodsConfigsNew":[{"location_id":"1"},{"location_id":"2","alipay_url":"",' \
                              '"capacity":"","valve":""},{"location_id":"3"},{"location_id":"4"},{"location_id":"5"},' \
                              '{"location_id":"6"},{"location_id":"7"},{"location_id":"8"},{"location_id":"9"},' \
                              '{"location_id":"10"}],"containersNew":[{"modelId":"5b45a3911ab662a79a99f171",' \
                              '"modelName":"syncModel-15spring","cid":"1","type":2,"vender":"富士冰山",' \
                              '"venderNum":"fuji","serial":"ttyO3","vmcNum":"1","plugIn":"1","shelves":[{' \
                              '"location_id":"1","alipay_url":"","capacity":"","valve":""},{"location_id":"2"},' \
                              '{"location_id":"3"},{"location_id":"4"},{"location_id":"5"},{"location_id":"6"},' \
                              '{"location_id":"7"},{"location_id":"8"},{"location_id":"9"},{"location_id":"10"},' \
                              '{"location_id":"11"},{"location_id":"12"},{"location_id":"13"},{"location_id":"14"},' \
                              '{"location_id":"15"}]},{"modelId":"5b45a3cf1ab662a79a99f172",' \
                              '"modelName":"syncModel-5grid","cid":"2","type":3,"vender":"富士冰山","venderNum":"fuji",' \
                              '"serial":"ttyO4","vmcNum":"2","plugIn":"1","shelves":[{"location_id":"1"},' \
                              '{"location_id":"2"},{"location_id":"3","alipay_url":"","capacity":1,"valve":0},' \
                              '{"location_id":"4"},{"location_id":"5"}]}],"inboxConfig":{"fireware":"IHv2.0.17",' \
                              '"apps":[{"name":"AdService","version":"1.345.r6680"},{"name":"DeviceManagerService",' \
                              '"version":"1.346.r6680"},{"name":"InBoxCore","version":"1.88.r6521"},' \
                              '{"name":"Install","version":"Install1.1.r6"},{"name":"PayService",' \
                              '"version":"1.344.r6680"},{"name":"SmartVM","version":"Aucma2.343.r6680"},' \
                              '{"name":"VendingCloudService","version":"2.353.r6680"},{"name":"VideoPlayer",' \
                              '"version":"SplitScreen.284.r6680"},{"name":"VMCService","version":"Aucma2.685.r6680"},' \
                              '{"name":"VMCSettings","version":"2.348.r6680"},{"name":"Appium Settings",' \
                              '"version":"2.3"},{"name":"Unlock","version":"2.0.0"}],"vendingData":[{"name":"ad",' \
                              '"type":"8001","version":"ad.1527746976"}]},"vendingState":{"doorState":0,"isSale":0,' \
                              '"coin5Count":0,"coin10Count":0,"vmcOnline":1,"faultCode":[0,0,0,0,0,0,0,0,0,0,0,0,0,0,' \
                              '0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,' \
                              '0,0,0,0,0,0,0],"shelvesState":[{"cid":"9","shelvesId":"11","state":1},{"cid":"9",' \
                              '"shelvesId":"13","state":1},{"cid":"9","shelvesId":"15","state":1},{"cid":"9",' \
                              '"shelvesId":"21","state":1},{"cid":"9","shelvesId":"22","state":1},{"cid":"9",' \
                              '"shelvesId":"23","state":1},{"cid":"9","shelvesId":"24","state":1},{"cid":"9",' \
                              '"shelvesId":"25","state":1},{"cid":"9","shelvesId":"26","state":1},{"cid":"9",' \
                              '"shelvesId":"31","state":1},{"cid":"9","shelvesId":"32","state":1},{"cid":"9",' \
                              '"shelvesId":"33","state":1},{"cid":"9","shelvesId":"35","state":1},{"cid":"9",' \
                              '"shelvesId":"41","state":1},{"cid":"9","shelvesId":"42","state":1},{"cid":"9",' \
                              '"shelvesId":"43","state":1},{"cid":"9","shelvesId":"44","state":1},{"cid":"9",' \
                              '"shelvesId":"45","state":1},{"cid":"9","shelvesId":"46","state":1},{"cid":"9",' \
                              '"shelvesId":"51","state":1},{"cid":"9","shelvesId":"52","state":1},{"cid":"9",' \
                              '"shelvesId":"53","state":1},{"cid":"9","shelvesId":"54","state":1},{"cid":"9",' \
                              '"shelvesId":"55","state":1},{"cid":"9","shelvesId":"56","state":1},{"cid":"9",' \
                              '"shelvesId":"57","state":1},{"cid":"9","shelvesId":"58","state":1},{"cid":"9",' \
                              '"shelvesId":"61","state":1},{"cid":"9","shelvesId":"62","state":1},{"cid":"9",' \
                              '"shelvesId":"63","state":1},{"cid":"9","shelvesId":"64","state":1},{"cid":"9",' \
                              '"shelvesId":"65","state":1},{"cid":"9","shelvesId":"66","state":1},{"cid":"9",' \
                              '"shelvesId":"67","state":1},{"cid":"9","shelvesId":"68","state":1},{"cid":"2",' \
                              '"shelvesId":"3","state":0},{"cid":"1","shelvesId":"1","state":0},{"cid":"apptest",' \
                              '"shelvesId":"2","state":1,"soldoutTime":"1531968718"}],"vendingFault":[]},' \
                              '"config":{"vender":"fuji","protocol":"1","port":"ttyO2"},"coin_capacity":[30,20,0],' \
                              '"lineId":"5ab4b7d1a476c4f1512cf458","lineName":"一大哥区域1线路1","payConfig":[{' \
                              '"payId":"5a4b3421ad34e9e9587cf304","payName":"WECHAT"},' \
                              '{"payId":"5a4dda8fa476105d788caf3e","payName":"UNIONPAY"},' \
                              '{"payId":"5a4ddc06a476105d788caf3f","payName":"BAIDU"},' \
                              '{"payId":"5addb3aef1d68f692a6c3748","payName":"UNICOMPAY"},' \
                              '{"payId":"5b1a44b3bb544cb9c273c6c3","payName":"YIFUBAO"},' \
                              '{"payId":"5a4c8e03a476105d788caf3c","payName":"QRCODEPAY"},' \
                              '{"payId":"5a4b344fad34e9e9587cf305","payName":"ALIPAY"}],"sessionId":"WebSocket ' \
                              'session id=36d","sync":1,"onlineType":0,"createTime":1531293827,' \
                              '"updateTime":1531968714,"lastAlive":1531968714,"host":"10.5.16.1:3283","shelfcount":0,' \
                              '"containerNum":0,"alipay_store_id":"","adFileList":{"fileList":[{"dir":"ads",' \
                              '"files":[{"name":"dibai.mp4"}]},{"dir":"ads/S0","files":[{"name":"dibai.mp4"},' \
                              '{"name":"pic370.png"}]}]},"refundConfig":[],"qrcodepay_mchid":"","deviceType":0,' \
                              '"_id":"5b45b0831ab68b7e4d775299"} '
    bind_channel_headers = {
        "Content-Type": "application/json;charset=UTF-8",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/67.0.3396.87 Safari/537.36 '
    }
    bind_channel_data = bytes(bind_channel_json_empty, encoding="utf8")
    request = urllib.request.Request(url, bind_channel_data, bind_channel_headers, method='PUT')
    bind_channel_response = urllib.request.urlopen(request).read().decode('utf-8')
    # logPrint(bind_channel_response)

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
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步货道']").click()
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
    if isElementExist(driver, "//android.widget.TextView[contains(@text,'操作成功')]"):
        logPrint("同步成功：PASS")
    else:
        logPrint("同步成功：FAIL!!")
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    sleep(8)
    first_last_xpath = "//android.widget.LinearLayout/android.widget.TextView[contains(@text,'货道')] "
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='货道配置']").click()
    vm_grid_list = driver.find_elements_by_xpath("//android.widget.GridView/android.widget.RelativeLayout")
    for elevm in vm_grid_list:
        elevm.click()
        # driver.find_element_by_xpath("//android.widget.TextView[@text='主 柜']").click()
        if not swipeToElementByXpath(driver,
                                     xpath_for_find="//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout",
                                     frist_last_xpath=first_last_xpath):
            logPrint("同步空配置：PASS")
        else:
            logPrint("同步空配置：FAIL!!")
        driver.find_element_by_xpath("//android.widget.TextView[@text='返回']").click()

    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    bind_channel_data = bytes(bind_channel_json_have_data, encoding="utf8")
    request = urllib.request.Request(url, bind_channel_data, bind_channel_headers, method='PUT')
    bind_channel_response = urllib.request.urlopen(request).read().decode('utf-8')
    # logPrint(bind_channel_response)
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步配置']").click()
    driver.find_element_by_xpath("//android.widget.TextView[@text='同步货道']").click()
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
    if isElementExist(driver, "//android.widget.TextView[contains(@text,'操作成功')]"):
        logPrint("同步成功：PASS")
    else:
        logPrint("同步成功：FAIL!!")
    driver.find_element_by_xpath("//android.widget.Button[@text='确定']").click()
    sleep(8)
    first_last_xpath = "//android.widget.LinearLayout/android.widget.TextView[contains(@text,'货道')]"
    driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', properties.desired_caps)
    driver.find_element_by_xpath("//android.widget.TextView[@text='货道配置']").click()
    vm_grid_list = driver.find_elements_by_xpath("//android.widget.GridView/android.widget.RelativeLayout")
    for elevm in vm_grid_list:
        elevm.click()
        if swipeToElementByXpath(driver,
                                 xpath_for_find="//android.widget.RelativeLayout/android.widget.LinearLayout/android.widget.LinearLayout",
                                 frist_last_xpath=first_last_xpath) \
                and swipeToElementByXpath(driver,xpath_for_find="//android.widget.TextView[@text='名称:海苔']",frist_last_xpath=first_last_xpath) \
                and swipeToElementByXpath(driver,xpath_for_find="//android.widget.TextView[@text='价格:111.00']",frist_last_xpath=first_last_xpath):
            logPrint("同步配置：PASS")
        else:
            logPrint("同步配置：FAIL!!")
        driver.find_element_by_xpath("//android.widget.TextView[@text='返回']").click()
