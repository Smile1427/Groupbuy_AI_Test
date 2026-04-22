from playwright.sync_api import sync_playwright
import time


def test_拼团_正常开团():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            page.locator(".goods-card").first.click()
            page.wait_for_selector(".group-btn", timeout=10000)
            
            # 点击开团
            page.locator(".group-btn:has-text('我要开团')").click()
            page.wait_for_selector(".countdown", timeout=5000)
            
            assert page.locator(".countdown").is_visible()
            print("✅ 开团功能测试通过")
        except Exception as e:
            page.screenshot(path="reports/screenshots/拼团-正常开团_error.png")
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
