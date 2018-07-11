# -*- coding:utf-8 -*-
import os

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'BT3101745001785',
    'platformVersion': '4.2.2',
    'appPackage': 'com.inhand.vmcsettings',
    'appActivity': 'com.inhand.vmcsettings.VMCSettings',
	'relaxedSecurityEnabled': 'True'
}
# deveiceName = os.popen("adb devices").read()
# deveiceName = deveiceName.split("\t")[0].split("\n")[1]
# print(deveiceName)
#
# desired_caps['deviceName'] = deveiceName
#
# print(desired_caps)


