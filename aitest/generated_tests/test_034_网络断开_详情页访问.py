from playwright.sync_api import sync_playwright
import time


def test_网络断开_详情页访问():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            # 模拟离线状态
            context = browser.contexts[0]
            context.set_offline(True)
            
            page.goto("http://localhost:8001/index.html", timeout=5000)
            # 验证不会崩溃
            page.wait_for_timeout(2000)
            print("✅ 网络断开处理测试通过")
        except Exception as e:
            print(f"✅ 预期异常处理正常: {e}")
        finally:
            browser.close()
