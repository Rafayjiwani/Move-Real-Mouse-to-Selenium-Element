# 🖱️ Move Real OS Mouse to Selenium Element (Pixel Accurate)

Move the **real system mouse cursor** (OS-level) to a Selenium element with
correct handling of DPI scaling and browser offsets.

This solves the common issue where Selenium element coordinates do not match
desktop screen coordinates.

---

## ✅ What This Solves

- Selenium returns element position in **CSS viewport pixels**
- pyautogui needs **physical screen pixels**
- Windows/macOS DPI scaling breaks naive math
- Browser title bar & borders shift coordinates

This script handles **all of the above**.

---

## ⚙️ Requirements

- Python 3.9+
- Google Chrome

Install dependencies:

```bash
pip install selenium pyautogui
