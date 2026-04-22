"""定位器自动修复模块"""
from zhipuai import ZhipuAI
import config

client = ZhipuAI(api_key=config.ZHIPU_API_KEY)


def repair_locator(broken_locator: str, page_html_snippet: str, element_description: str = "") -> str:
    """
    当定位器失效时，AI推荐新的定位器

    Args:
        broken_locator: 失效的旧定位器（XPath或CSS）
        page_html_snippet: 当前页面的HTML片段
        element_description: 目标元素的描述（如"登录按钮"）

    Returns:
        新的定位器表达式
    """
    prompt = f"""原来的定位器失效了，请帮我找到新的稳定定位器。

旧定位器：{broken_locator}
目标元素描述：{element_description or "需要定位的目标元素"}
当前页面的HTML片段：
{page_html_snippet[:2000]}

要求：
1. 推荐一个稳定的CSS选择器或XPath
2. 优先使用data-testid、id、class组合
3. 避免使用动态生成的属性
4. 只返回定位器表达式，不要解释
5. 如果是XPath，以.//开头；如果是CSS，直接返回

示例输出：
//button[@data-testid='submit-btn']
或
.submit-button
"""

    try:
        response = client.chat.completions.create(
            model=config.ZHIPU_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
        )
        new_locator = response.choices[0].message.content.strip()
        return new_locator
    except Exception as e:
        return f"# 修复失败: {str(e)}"


def suggest_alternative_selectors(page_html_snippet: str, element_text: str = None) -> list:
    """
    推荐多个备选定位器

    Args:
        page_html_snippet: HTML片段
        element_text: 元素上的文本内容

    Returns:
        推荐的定位器列表
    """
    prompt = f"""分析以下HTML片段，为元素推荐多个稳定的定位器。

HTML片段：
{page_html_snippet[:2000]}

{f'目标元素包含文本：{element_text}' if element_text else ''}

请返回3个定位器，按稳定性从高到低排序，每行一个。
格式示例：
[1] .btn-primary
[2] //button[contains(text(), '登录')]
[3] div[data-id="123"] > button
"""

    try:
        response = client.chat.completions.create(
            model=config.ZHIPU_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        result = response.choices[0].message.content
        # 简单解析返回的定位器
        selectors = []
        for line in result.split('\n'):
            if line.strip() and ('[' in line or '//' in line or '.' in line):
                # 提取定位器表达式
                if ']' in line:
                    selector = line.split(']', 1)[1].strip()
                else:
                    selector = line.strip()
                if selector:
                    selectors.append(selector)
        return selectors[:3]
    except Exception as e:
        return [f"# 推荐失败: {str(e)}"]


if __name__ == "__main__":
    # 测试示例
    html_snippet = '''
    <button class="login-btn" data-testid="login-button" id="btn_login">登录</button>
    '''
    new_locator = repair_locator("//button[@id='old_login']", html_snippet, "登录按钮")
    print(f"新定位器: {new_locator}")