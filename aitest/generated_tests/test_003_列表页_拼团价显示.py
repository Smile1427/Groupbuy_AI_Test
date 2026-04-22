from playwright.sync_api import sync_playwright
import time


def test_列表页_拼团价显示():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/index.html", timeout=10000)
            page.wait_for_selector(".goods-card", timeout=10000)
            print("✅ 页面加载成功")
            
            # 具体断言
            goods_count = page.locator(".goods-card").count()
            print(f"找到 {goods_count} 个商品")
            assert goods_count > 0
            
            page.screenshot(path="reports/screenshots/列表页-拼团价显示.png")
            print("✅ 测试通过")
        except Exception as e:
            page.screenshot(path="reports/screenshots/列表页-拼团价显示_error.png")
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
