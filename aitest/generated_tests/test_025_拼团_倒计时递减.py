from playwright.sync_api import sync_playwright
import time


def test_拼团_倒计时递减():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            page.locator(".goods-card").first.click()
            page.wait_for_selector(".group-btn", timeout=10000)
            page.locator(".group-btn:has-text('我要开团')").click()
            
            page.wait_for_selector(".countdown", timeout=5000)
            countdown_text = page.locator(".countdown").text_content()
            print(f"倒计时显示: {countdown_text}")
            assert ":" in countdown_text
            
            # 等待5秒验证倒计时变化
            time.sleep(5)
            new_countdown = page.locator(".countdown").text_content()
            print(f"5秒后倒计时: {new_countdown}")
            assert new_countdown != countdown_text
            
            print("✅ 倒计时测试通过")
        except Exception as e:
            page.screenshot(path="reports/screenshots/拼团-倒计时递减_error.png")
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
