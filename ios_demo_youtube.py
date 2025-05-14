from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import time
from appium.options.ios import XCUITestOptions
import tkinter as tk
from tkinter import messagebox

def scroll_to_element(driver, locator, max_swipes=5):
    """
    Cuộn màn hình để tìm phần tử theo locator.
    
    Args:
        driver: Appium driver
        locator: Tuple (by, value) - ví dụ: (AppiumBy.XPATH, "//XCUIElementTypeStaticText[@name='Notifications']")
        max_swipes: Số lần cuộn tối đa
        
    Returns:
        WebElement: Phần tử được tìm thấy
        
    Raises:
        Exception: Nếu không tìm thấy phần tử sau max_swipes
    """
    by, value = locator
    for _ in range(max_swipes):
        try:
            element = driver.find_element(by, value)
            return element
        except:
            # Cuộn màn hình từ dưới lên
            size = driver.get_window_size()
            start_x = size['width'] * 0.5
            start_y = size['height'] * 0.8
            end_y = size['height'] * 0.2
            driver.swipe(start_x, start_y, start_x, end_y, 500)
            time.sleep(1)
    raise Exception(f"Không tìm thấy phần tử với locator: {by}, value: {value}")

def scroll_up_screen():
    # Cuộn màn hình từ dưới lên
    size = driver.get_window_size()
    start_x = size['width'] * 0.5
    start_y = size['height'] * 0.8
    end_y = size['height'] * 0.2
    driver.swipe(start_x, start_y, start_x, end_y, 500)
    time.sleep(1)

desired_caps = {
    "platformName": "iOS",
    "platformVersion": "18.3",  # Thay bằng version iOS thiết bị bạn
    "deviceName": "iPhone 15 prm",  # Hoặc UDID nếu chạy trên thiết bị thật
    "udid": "00008130-0006008418A1401C",  # Bắt buộc nếu chạy thiết bị thật
    "automationName": "XCUITest",
    "bundleId": "com.google.ios.youtube",  # Mở Youtube
    "noReset": False,
    "fullReset": False
}

# Kết nối đến Appium Server
appium_server_url = 'http://localhost:4723/wd/hub'
driver = webdriver.Remote(appium_server_url, options=XCUITestOptions().load_capabilities(desired_caps))

try:
    # Kiểm tra xem ứng dụng đã mở chưa
    print("Đang kiểm tra trạng thái ứng dụng...")
    time.sleep(2)  # Chờ thêm để đảm bảo ứng dụng mở

    # Chờ giao diện Youtube sẵn sàng
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//XCUIElementTypeOther[@name='id.yoodle.logo']/XCUIElementTypeOther"))
    )

    # Cuộn và tìm "Shorts"
    locator = (AppiumBy.XPATH, "//XCUIElementTypeButton[@name='id.ui.pivotbar.FEshorts.button']")
    # Tìm và cuộn đến phần tử "Shorts" (thay "Shorts" nếu cần)
    shorts_element = scroll_to_element(driver, locator) 
    # Nhấp vào "Shorts"
    shorts_element.click()

    print(f"✅ Đã mở mục {shorts_element} thành công.")

    time.sleep(3)  # Cho xem trước khi kết thúc
    #Cuộn màn hình từ dưới lên
    scroll_up_screen()
    time.sleep(3)  # Cho xem trước khi kết thúc

    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Ket qua", "✅Test PASSED")

except Exception as e:
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Ket qua", f"Test FAILED\nloi: {str(e)}")
    raise


finally:
    driver.quit()
