from playwright.sync_api import sync_playwright
import time


def test_拼团_模拟成功():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            page.locator(".goods-card").first.click()
            page.wait_for_selector(".group-btn", timeout=10000)
            page.locator(".group-btn:has-text('我要开团')").click()
            page.wait_for_selector(".group-btn:has-text('模拟拼团成功')", timeout=5000)
            page.locator(".group-btn:has-text('模拟拼团成功')").click()
            
            page.wait_for_selector(".group-btn:has-text('已成团')", timeout=5000)
            assert page.locator(".group-btn:has-text('已成团')").is_visible()
            print("✅ 拼团成功测试通过")
        except Exception as e:
            page.screenshot(path="reports/screenshots/拼团-模拟成功_error.png")
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
