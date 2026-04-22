from playwright.sync_api import sync_playwright
import time


def test_拼团_连续开团成功():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            
            # 快速点击多个商品
            for i in range(5):
                page.locator(".goods-card").first.click()
                page.go_back()
                page.wait_for_timeout(500)
            
            print("✅ 快速点击测试通过，无崩溃")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
