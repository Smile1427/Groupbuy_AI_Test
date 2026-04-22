from playwright.sync_api import sync_playwright
import time


def test_详情页_正常显示():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            page.locator(".goods-card").first.click()
            
            page.wait_for_selector(".detail-name", timeout=10000)
            assert page.locator(".detail-name").is_visible()
            assert page.locator(".group-btn").is_visible()
            
            page.screenshot(path="reports/screenshots/详情页-正常显示.png")
            print("✅ 详情页测试通过")
        except Exception as e:
            page.screenshot(path="reports/screenshots/详情页-正常显示_error.png")
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
