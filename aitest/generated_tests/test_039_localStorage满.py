from playwright.sync_api import sync_playwright
import time


def test_localStorage满():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            print("✅ {case_name} 测试通过")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
