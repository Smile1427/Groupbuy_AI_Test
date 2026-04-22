from playwright.sync_api import sync_playwright
import time


def test_详情页_无效商品ID():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("http://localhost:8001/detail.html?id=999", timeout=10000)
            page.wait_for_timeout(2000)
            
            # 验证跳转回列表页或显示错误提示
            current_url = page.url
            if "detail" in current_url:
                # 检查是否有错误提示
                error_shown = page.locator("text=商品不存在").count() > 0
                assert error_shown, "应显示商品不存在提示"
            
            print("✅ 无效ID处理测试通过")
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            raise
        finally:
            browser.close()
