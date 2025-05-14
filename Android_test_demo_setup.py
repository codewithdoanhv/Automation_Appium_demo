from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
import time
from appium.options.android import UiAutomator2Options

# Cấu hình desired capabilities (khớp với Appium Inspector)
desired_caps = {
    "platformName": "Android",
    "appium:deviceName": "R5CW92FWKCP",
    "appium:platformVersion": "14",
    "appium:automationName": "UiAutomator2",
    "appium:appPackage": "com.android.settings",
    "appium:appActivity": ".Settings",
    # Loại bỏ các tham số bổ sung để khớp với Appium Inspector
}

def scroll_to_element(driver, locator, max_swipes=5):
    """
    Cuộn màn hình để tìm phần tử theo locator.
    
    Args:
        driver: Appium driver
        locator: Tuple (by, value) - ví dụ: (AppiumBy.XPATH, "//*[contains(@text, 'Connections')]")
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

try:
    # Khởi tạo driver
    appium_server_url = 'http://127.0.0.1:4723/wd/hub'
    driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(desired_caps))

    # Kiểm tra xem ứng dụng Settings đã mở chưa
    print("Đang kiểm tra trạng thái ứng dụng Settings...")
    time.sleep(2)  # Chờ thêm để đảm bảo ứng dụng mở
    current_activity = driver.current_activity
    current_package = driver.current_package
    print(f"Current package: {current_package}, Current activity: {current_activity}")

    # Chờ giao diện Settings sẵn sàng
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((AppiumBy.XPATH, "//*[@resource-id='android:id/content']"))
    )
    print(f"Giao diện {current_package} đã sẵn sàng.")

    # Tìm và cuộn đến phần tử "Location" bằng các locator khác nhau
    # Ví dụ 1: Tìm bằng text (XPath)
    locator = (AppiumBy.XPATH, "//*[contains(@text, 'Location')]")
    
    # Ví dụ 2: Tìm bằng resource-id
    # locator = (AppiumBy.ID, "android:id/title")  # Giả sử "Location" có resource-id là android:id/title
    
    # Ví dụ 3: Tìm bằng XPath tùy chỉnh
    # locator = (AppiumBy.XPATH, "//android.widget.TextView[@resource-id='android:id/title' and @text='Location']")

    # Tìm và cuộn đến phần tử "Location" (thay "Location" nếu cần)
    connections_element = scroll_to_element(driver, locator)  # Thay bằng "Kết nối" nếu giao diện tiếng Việt

    # Nhấp vào "Location"
    connections_element.click()
    
    print(f"Đã mở mục {connections_element} thành công!")
    
    # Đợi để quan sát kết quả
    time.sleep(2)

except Exception as e:
    print(f"Lỗi xảy ra: {str(e)}")

finally:
    # Đóng driver
    if 'driver' in locals():
        driver.quit()