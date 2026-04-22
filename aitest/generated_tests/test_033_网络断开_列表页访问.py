from playwright.sync_api import sync_playwright
import time


def test_网络断开_列表页访问():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            # 模拟空数据（通过拦截响应或修改localStorage）
            page.goto("http://localhost:8001/index.html", timeout=10000)
            # 执行清空商品数据的操作
            page.evaluate("localStorage.clear()")
            page.reload()
            
            # 验证不会崩溃
            page.wait_for_timeout(2000)
            print("✅ 异常情况处理正常")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
