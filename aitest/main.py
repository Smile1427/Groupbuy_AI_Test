"""AI测试平台主入口 - 逐个运行模式（显示进度）"""
import os
import yaml
import webbrowser
from core import test_runner
import simple_generator as ai_generator


def load_test_cases(yaml_file: str):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    return data


def main():
    print("=" * 50)
    print("AI驱动测试平台 - 拼团H5完整测试套件")
    print("=" * 50)

    # 创建必要目录
    os.makedirs("reports/screenshots", exist_ok=True)
    os.makedirs("generated_tests", exist_ok=True)

    # 1. 加载测试用例
    yaml_file = "test_cases/all_cases.yaml"
    if not os.path.exists(yaml_file):
        print(f"错误: 找不到用例文件 {yaml_file}")
        return

    test_data = load_test_cases(yaml_file)
    url = test_data.get("url", "")
    cases = test_data.get("cases", [])

    print(f"\n目标URL: {url}")
    print(f"加载测试用例: {len(cases)} 个\n")

    # 2. 确认开始
    confirm = input("\n是否开始生成并执行测试？(y/n): ")
    if confirm.lower() != 'y':
        print("已取消")
        return

    # 3. 生成所有测试代码
    print("\n" + "=" * 50)
    print("第一阶段：生成测试代码")
    print("=" * 50)

    test_files = []
    for i, case in enumerate(cases):
        print(f"[{i+1}/{len(cases)}] 生成: {case['name']}")
        code = ai_generator.generate_test_code(
            case['name'],
            case.get('type', 'normal'),
            case['text'],
            url
        )
        safe_name = case['name'].replace(' ', '_').replace('-', '_').replace('/', '_')
        filename = f"test_{i+1:03d}_{safe_name}"
        filepath = test_runner.save_test_code(filename, code)
        test_files.append(filepath)

    print(f"\n✅ 已生成 {len(cases)} 个测试文件")

    # 4. 逐个执行测试（显示进度）
    print("\n" + "=" * 50)
    print("第二阶段：执行测试（逐个运行）")
    print("=" * 50)

    results = []
    passed = 0
    failed = 0

    for i, (case, filepath) in enumerate(zip(cases, test_files)):
        print(f"\n{'='*40}")
        print(f"[{i+1}/{len(cases)}] 正在执行: {case['name']}")
        print(f"类型: {case.get('type', 'normal')}")
        print(f"{'='*40}")

        result = test_runner.run_test(filepath, "reports")

        if result['success']:
            passed += 1
            print(f"✅ 测试通过 (耗时 {result['duration']}秒)")
        else:
            failed += 1
            print(f"❌ 测试失败 (耗时 {result['duration']}秒)")
            if result.get('stderr'):
                error_msg = result['stderr'][:300]
                print(f"错误: {error_msg}")

        results.append(result)

    # 5. 输出汇总报告
    print("\n" + "=" * 50)
    print("测试汇总报告")
    print("=" * 50)

    total = len(cases)
    print(f"总计: {total} 个用例")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    print(f"⏱️  总耗时: {sum(r.get('duration', 0) for r in results):.2f} 秒")

    # 6. 生成HTML汇总报告
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_html = f"reports/summary_{timestamp}.html"

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>测试报告汇总</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #333; }}
        .summary {{ background: #f0f0f0; padding: 15px; border-radius: 5px; margin-bottom: 20px; }}
        .pass {{ color: green; }}
        .fail {{ color: red; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
    </style>
</head>
<body>
    <h1>拼团H5自动化测试报告</h1>
    <div class="summary">
        <p><strong>执行时间:</strong> {timestamp}</p>
        <p><strong>目标URL:</strong> {url}</p>
        <p><strong>总用例数:</strong> {total}</p>
        <p><strong class="pass">通过:</strong> {passed}</p>
        <p><strong class="fail">失败:</strong> {failed}</p>
        <p><strong>通过率:</strong> {passed/total*100:.1f}%</p>
    </div>
    <h2>详细结果</h2>
    <table>
        <thead>
            <tr><th>序号</th><th>用例名称</th><th>类型</th><th>状态</th><th>耗时(秒)</th></tr>
        </thead>
        <tbody>
"""

    for i, (case, result) in enumerate(zip(cases, results)):
        status = "✅ 通过" if result['success'] else "❌ 失败"
        status_class = "pass" if result['success'] else "fail"
        html_content += f"""
            <tr>
                <td>{i+1}</td>
                <td>{case['name']}</td>
                <td>{case.get('type', 'normal')}</td>
                <td class="{status_class}">{status}</td>
                <td>{result.get('duration', 0)}</td>
            </tr>"""

    html_content += """
        </tbody>
    </table>
</body>
</html>
"""

    with open(summary_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"\n📊 汇总报告已生成: {summary_html}")

    open_report = input("\n是否打开汇总报告？(y/n): ")
    if open_report.lower() == 'y':
        webbrowser.open(summary_html)

    print("\n✅ 测试完成！")


if __name__ == "__main__":
    main()