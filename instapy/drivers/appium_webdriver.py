"""
Class to define everything needed to work with Appium
"""

from appium import webdriver
from adb.client import Client as AdbClient
from time import sleep


class AppiumWebDriver():
    """
    Appium WebDriver class
    """

    driver = None

    @classmethod
    def construct_webdriver(cls,devicename: str = "",devicetimeout: int = 600,client_host: str = "127.0.0.1",client_port: int = 5037):
        if cls.driver is None:
            cls.driver = AppiumWebDriver(devicename,devicetimeout,client_host,client_port)
        else:
            pass

    def __init__(
        self,
        devicename: str = "",
        devicetimeout: int = 600,
        client_host: str = "127.0.0.1",
        client_port: int = 5037,
    ):

        self.adb_client = AdbClient(host=client_host, port=client_port)
        self.adb_devices = self._get_adb_devices()

        __desired_caps = {}

        if any(devicename in device for device in self.adb_devices):
            self.devicename = devicename
            __desired_caps["platformName"] = "Android"
            __desired_caps["deviceName"] = devicename
            __desired_caps["appPackage"] = "com.instagram.android"
            __desired_caps["appActivity"] = "com.instagram.mainactivity.MainActivity"
            __desired_caps["automationName"] = "UiAutomator2"
            __desired_caps["noReset"] = True
            __desired_caps["fullReset"] = False
            __desired_caps["unicodeKeyboard"] = True
            __desired_caps["resetKeyboard"] = True
            __desired_caps["newCommandTimeout"] = devicetimeout

            try:
                driver = webdriver.Remote(
                    "http://{}:4723/wd/hub".format(client_host), __desired_caps
                )
                print("Succesfully connected to the {} device!".format(self.devicename))
                sleep(5)
            except:
                # self.logger.error("Could not create webdriver, is Appium running?")
                print("Could not create webdriver; please make sure Appium is running")

        else:
            # self.logger.error("Invalid Device Name")
            print(
                "Invalid Device Name. \nList of available devices: {}".format(
                    ", ".join(self.adb_devices)
                )
            )

    def _get_adb_devices(self):
        """
        protected function to check the current running simulators
        :return:
        """
        devices = []

        for device in self.adb_client.devices():
            devices.append(device.serial)

        return devices

    @classmethod
    def get_driver(cls):
        """
        wrapper for find_element by_xpath
        :param xpath:
        :return:
        """
        return cls.driver

    @classmethod
    def find_element_by_xpath(cls,xpath: str = ""):
        """
        wrapper for find_element by_xpath
        :param xpath:
        :return:
        """
        return cls.driver.find_element_by_xpath(xpath)

    @classmethod
    def find_element_by_id(cls,resource_id: str = ""):
        """
        wrapper for find_element_by_id
        :param resource_id:
        :return:
        """
        return cls.driver.find_element_by_id(resource_id)

    @classmethod
    def find_element_by_uiautomator(cls,uiautomator: str = ""):
        """
        wrapper for find_element_by_android_uiautomator
        :param uiautomator:
        :return:
        """
        return cls.driver.find_element_by_android_uiautomator(uiautomator)

    @staticmethod
    def click(webelem):
        """
        wrapper for element clicking
        :param webelem:
        :return:
        """
        webelem.click()
