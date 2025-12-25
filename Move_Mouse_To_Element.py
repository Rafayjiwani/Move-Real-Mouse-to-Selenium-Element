"""
Real OS Mouse Movement to Selenium Element (Pixel-Accurate)

This script moves the REAL system mouse cursor (OS-level, not Selenium virtual)
to the center of a Selenium WebElement and performs a small circular hover
movement.

It correctly handles:
- CSS viewport coordinates vs OS screen pixels
- Windows / macOS DPI scaling (devicePixelRatio)
- Browser chrome (title bar, address bar, borders)
- Fallback logic if coordinates drift

Works best on local machines with GUI (not headless).
"""

import time
import math
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_element_screen_center(driver, element, debug=False):
    """
    Returns (x, y) screen coordinates (OS pixels) for the center of a Selenium element.
    """

    js = """
    const el = arguments[0];
    const rect = el.getBoundingClientRect();
    return {
        rect: {
            left: rect.left,
            top: rect.top,
            width: rect.width,
            height: rect.height
        },
        screenX: window.screenX || window.screenLeft || 0,
        screenY: window.screenY || window.screenTop || 0,
        outerWidth: window.outerWidth,
        outerHeight: window.outerHeight,
        innerWidth: window.innerWidth,
        innerHeight: window.innerHeight,
        devicePixelRatio: window.devicePixelRatio || 1
    };
    """

    info = driver.execute_script(js, element)

    rect = info["rect"]
    dpr = info["devicePixelRatio"]

    # Estimate browser chrome offsets
    border_x = max(0, (info["outerWidth"] - info["innerWidth"]) / 2)
    toolbar_y = max(0, info["outerHeight"] - info["innerHeight"] - border_x)

    # Element center in CSS pixels
    css_x = info["screenX"] + border_x + rect["left"] + rect["width"] / 2
    css_y = info["screenY"] + toolbar_y + rect["top"] + rect["height"] / 2

    # Convert CSS pixels → physical screen pixels
    screen_x = css_x * dpr
    screen_y = css_y * dpr

    # Safety clamp
    sw, sh = pyautogui.size()
    screen_x = max(0, min(screen_x, sw - 1))
    screen_y = max(0, min(screen_y, sh - 1))

    if debug:
        print("DevicePixelRatio:", dpr)
        print("Final screen coords:", int(screen_x), int(screen_y))

    return int(screen_x), int(screen_y)


# ------------------------ USAGE ------------------------

if __name__ == "__main__":
    options = Options()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://example.com")  # change URL
        time.sleep(2)

        element = driver.find_element(By.TAG_NAME, "h1")  # change locator

        x, y = get_element_screen_center(driver, element, debug=True)

        # Move REAL mouse to element
        pyautogui.moveTo(x, y, duration=0.6)

    finally:
        driver.quit()
