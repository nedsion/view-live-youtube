import os
import zipfile

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from win32api import GetSystemMetrics




class Helper:
    def __init__(self) -> None:
        pass

    def setPositionChrome(self, width, height, count):
        width_scr, height_scr = GetSystemMetrics(0), GetSystemMetrics(1)
        index = 0
        index2 = 0
        x = width
        y = height
        for i in range(count):
            if int(width_scr/width) == index: index = 0; y = height; index2 += 1
            if int(height_scr/height) == index2: index = 0; index2 = 0  
            x_new, y_new = index*x, index2*y
            yield (x_new, y_new)
            index += 1
    
    def create_driver(self, headless=False, proxy=None, window_size=None, position=None):
        options = Options()
        options.headless = headless
        
        if proxy:
            if proxy.split(':') == 2:
                options.add_argument(f'--proxy-server={proxy}')
            else:
                options.add_extension(self.create_extension_proxy(proxy))

        if window_size:
            x, y = window_size
            options.add_argument(f'--window-size={x},{y}')

        if position:
            x, y = position
            options.add_argument(f'--window-position={x},{y}')


        driver = webdriver.Chrome(options=options)

        return driver


    def create_extension_proxy(self, proxy: str):
        ip, port, user, password = proxy.split(':')

        manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

        background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (ip, port, user, password)
        
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        pluginfile = os.path.abspath(pluginfile)
        return pluginfile
        
        
    def watch_live(self, driver, url):
        driver.get(url)
        
        current_url = driver.current_url
        while current_url == url:
            sleep(1)
            current_url = driver.current_url
        return current_url
    