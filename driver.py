import os.path

from selenium import webdriver


def get_options(user_name):
    options = webdriver.ChromeOptions()
    # options.add_extension(CG_VPN_CRX_FILE)  # crx file path
    options.add_argument('--no-sandbox')
    options.add_argument('--autoplay-policy=no-user-gesture-required')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-blink-features")
    options.add_argument('--start-maximized')
    options.add_argument("--disable-features=ChromeWhatsNewUI")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument("--enable-javascript")
    options.add_argument("--disable-notifications")
    options.add_argument("--enable-popup-blocking")
    options.add_argument("--disable-web-security")
    options.add_argument('--disable-infobars')
    options.add_argument('--no-proxy-server')
    options.add_argument('--icognito')
    options.add_experimental_option("prefs",{"download.default_directory" : "D:\\Dump_Folder\\Dump"})
    #options.headless=True
    options.add_argument('--disable-blink-features=AutomationControlled')
    full_path = os.path.abspath(f'./profiles/{str(user_name)}')
    options.add_argument(f'--user-data-dir={full_path}')
    # options.add_argument(f"--profile-directory=./profiles/{str(user_name)}")
    options.add_experimental_option('useAutomationExtension', False)
    options.add_experimental_option("excludeSwitches", [
        "enable-logging",
        "enable-automation",
        "ignore-certificate-errors",
        "safebrowsing-disable-download-protection",
        "safebrowsing-disable-auto-update",
        "disable-client-side-phishing-detect"
        "ion"])
    options.add_argument("disable-infobars")
    prefs = {"credentials_enable_service": False,
             "profile.password_manager_enabled": False}
    options.add_experimental_option("prefs", prefs)

    # 2 Captcha extension
    # options.add_extension(os.path.join(BASE_DIR, "store/2_captcha_extension.crx"))
    return options