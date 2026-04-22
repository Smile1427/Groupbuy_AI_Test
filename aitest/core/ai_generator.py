"""AI生成测试代码模块"""
import re
from zhipuai import ZhipuAI
import config

# 初始化客户端
client = ZhipuAI(api_key=config.ZHIPU_API_KEY)


def generate_test_code(natural_language_case: str, url: str) -> str:
    """
    根据自然语言测试用例，生成Pytest + Playwright测试代码

    Args:
        natural_language_case: 自然语言描述的测试用例
        url: 被测页面URL

    Returns:
        生成的Python测试代码
    """
    prompt = f"""你是一个测试专家。请根据以下自然语言测试用例，生成Pytest + Playwright测试代码。

测试用例：{natural_language_case}
目标URL：{url}

【页面HTML结构说明】
- 商品列表容器：<div class="goods-list">
- 单个商品卡片：<div class="goods-card">
- 商品名称：<div class="goods-name">
- 拼团价格：<span class="group-price">
- 原价：<span class="original-price">
- 拼团标签：<span class="group-tag">
- 开团按钮：<button class="group-btn">
- 倒计时容器：<span class="countdown">
- 拼团状态容器：<div class="group-box">
- 拼团成功提示：<div class="status-tip">包含"拼团成功"文字

【要求】
1. 使用Playwright的同步API：from playwright.sync_api import sync_playwright
2. 使用pytest框架，函数名以test_开头
3. 使用上述真实的选择器，不要用占位符
4. 添加必要的等待：page.wait_for_selector(".goods-card", timeout=10000)
5. 包含明确的断言（assert）
6. 添加失败自动截图：page.screenshot(path="screenshot.png")
7. 浏览器使用非无头模式：headless=False（方便调试）
8. 返回纯代码，不要任何解释文字

【示例模板 - 请严格遵循此格式】
def test_example():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        try:
            page.goto("{url}")
            page.wait_for_selector(".goods-card", timeout=10000)

            # 你的测试步骤
            goods_count = page.locator(".goods-card").count()
            assert goods_count >= 1

            # 可选：截图
            page.screenshot(path="test_result.png")
        finally:
            browser.close()

请严格按照上述格式生成代码，使用真实的选择器，不要输出任何额外解释。"""

    try:
        response = client.chat.completions.create(
            model=config.ZHIPU_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,  # 降低随机性，提高稳定性
        )
        code = response.choices[0].message.content
        # 清理可能出现的markdown代码块标记
        code = clean_code(code)
        return code
    except Exception as e:
        return f"""# 生成失败: {str(e)}
# 请检查API密钥配置

def test_placeholder():
    \"\"\"占位测试，AI生成失败，请检查网络或API配置\"\"\"
    assert True
"""


def clean_code(code: str) -> str:
    """清理AI返回的代码中的markdown标记和多余内容"""
    # 移除markdown代码块标记
    if code.startswith("```python"):
        code = code[9:]
    elif code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]

    # 移除可能的额外解释文字（以#开头的非代码行，但保留代码中的注释）
    lines = code.split('\n')
    cleaned_lines = []
    in_code = False

    for line in lines:
        # 如果是import或from开头，开始代码部分
        if line.strip().startswith('from ') or line.strip().startswith('import '):
            in_code = True
        # 如果是def开头，开始代码部分
        if line.strip().startswith('def '):
            in_code = True
        # 如果是空白行，保留
        if not line.strip():
            cleaned_lines.append(line)
            continue
        # 如果已经进入代码部分，保留所有行
        if in_code:
            cleaned_lines.append(line)
        else:
            # 还在代码前的解释部分，跳过
            if line.strip() and not line.strip().startswith('#'):
                continue
            cleaned_lines.append(line)

    return '\n'.join(cleaned_lines).strip()


def generate_multiple_tests(cases: list, url: str) -> dict:
    """
    批量生成测试用例

    Args:
        cases: 用例列表，每个元素是包含name和text的字典
        url: 被测页面URL

    Returns:
        {用例名: 生成代码} 的字典
    """
    results = {}
    total = len(cases)

    for i, case in enumerate(cases):
        name = case.get('name', f'case_{i + 1}')
        text = case.get('text', '')
        print(f"[{i + 1}/{total}] 正在生成测试用例: {name}")

        code = generate_test_code(text, url)
        results[name] = code

    return results


def validate_generated_code(code: str) -> dict:
    """
    验证生成的代码是否包含必要的元素

    Returns:
        包含验证结果的字典
    """
    issues = []

    # 检查必要导入
    if 'from playwright.sync_api import sync_playwright' not in code:
        issues.append("缺少Playwright导入")

    # 检查必要结构
    if 'def test_' not in code:
        issues.append("缺少测试函数")

    if 'with sync_playwright()' not in code:
        issues.append("缺少Playwright上下文")

    if 'browser.close()' not in code and 'page.close()' not in code:
        issues.append("缺少浏览器关闭逻辑")

    # 检查占位符
    placeholders = ['selector_for_', 'your_selector', 'TODO', 'FIXME']
    for placeholder in placeholders:
        if placeholder in code.lower():
            issues.append(f"代码中包含未替换的占位符: {placeholder}")

    return {
        "is_valid": len(issues) == 0,
        "issues": issues
    }


# 测试代码（单独运行此文件时测试）
if __name__ == "__main__":
    print("=" * 50)
    print("AI测试代码生成器 - 测试模式")
    print("=" * 50)

    # 测试用例
    test_cases = [
        "打开商品列表页，验证三个商品都正常显示",
        "点击第一个商品，进入详情页",
    ]

    target_url = "http://localhost:8001/index.html"

    for case in test_cases:
        print(f"\n生成测试用例: {case[:50]}...")
        code = generate_test_code(case, target_url)

        # 验证代码
        validation = validate_generated_code(code)

        if validation["is_valid"]:
            print("✅ 代码验证通过")
        else:
            print("❌ 代码验证失败:")
            for issue in validation["issues"]:
                print(f"   - {issue}")

        print("\n生成的代码:")
        print("-" * 40)
        print(code[:500] + "..." if len(code) > 500 else code)
        print("-" * 40)