"""测试执行引擎模块 - 支持多种报告格式"""
import subprocess
import os
import time
from datetime import datetime


def save_test_code(filename: str, code: str, output_dir: str = "generated_tests") -> str:
    """保存生成的测试代码到文件"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{filename}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    return filepath


def run_test(test_file_path: str, report_dir: str = "reports") -> dict:
    """
    执行测试文件，生成多种格式报告

    支持的报告:
    - HTML报告 (pytest-html)
    - JUnit XML报告 (便于CI集成)
    - 覆盖率报告 (pytest-cov)
    - Allure原始数据 (allure-pytest)
    """
    os.makedirs(report_dir, exist_ok=True)

    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 报告文件路径
    html_report = os.path.join(report_dir, f"report_{timestamp}.html")
    junit_report = os.path.join(report_dir, f"junit_{timestamp}.xml")
    allure_dir = os.path.join(report_dir, "allure_raw")
    cov_report_dir = os.path.join(report_dir, "coverage")
    screenshot_dir = os.path.join(report_dir, "screenshots")

    # 确保目录存在
    os.makedirs(allure_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)
    os.makedirs(cov_report_dir, exist_ok=True)

    # 构建pytest命令
    cmd = [
        "pytest",
        test_file_path,
        f"--html={html_report}",
        "--self-contained-html",  # 报告自包含，不需要额外文件
        f"--junitxml={junit_report}",
        f"--alluredir={allure_dir}",
        f"--cov=.",
        f"--cov-report=html:{cov_report_dir}",
        f"--cov-report=term",  # 终端显示覆盖率
        "-v",
        "--tb=short"
    ]

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120  # 120秒超时
        )
        end_time = time.time()

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": round(end_time - start_time, 2),
            "test_file": test_file_path,
            "reports": {
                "html": html_report,
                "junit": junit_report,
                "allure_dir": allure_dir,
                "coverage": cov_report_dir
            }
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "return_code": -1,
            "stdout": "",
            "stderr": "测试执行超时（120秒）",
            "duration": 120,
            "test_file": test_file_path,
            "reports": {}
        }
    except Exception as e:
        return {
            "success": False,
            "return_code": -2,
            "stdout": "",
            "stderr": str(e),
            "duration": 0,
            "test_file": test_file_path,
            "reports": {}
        }


def run_all_tests(test_dir: str = "generated_tests", report_dir: str = "reports") -> dict:
    """
    批量运行所有生成的测试文件

    Args:
        test_dir: 测试文件目录
        report_dir: 报告输出目录

    Returns:
        汇总结果
    """
    import glob

    test_files = glob.glob(os.path.join(test_dir, "test_*.py"))

    if not test_files:
        return {"error": "没有找到测试文件", "total": 0, "passed": 0, "failed": 0}

    # 运行所有测试（一次性）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(report_dir, exist_ok=True)

    html_report = os.path.join(report_dir, f"full_report_{timestamp}.html")
    junit_report = os.path.join(report_dir, f"full_junit_{timestamp}.xml")
    allure_dir = os.path.join(report_dir, "allure_raw")
    cov_report_dir = os.path.join(report_dir, "coverage")
    screenshot_dir = os.path.join(report_dir, "screenshots")

    os.makedirs(allure_dir, exist_ok=True)
    os.makedirs(screenshot_dir, exist_ok=True)

    cmd = [
        "pytest",
        test_dir,
        f"--html={html_report}",
        "--self-contained-html",
        f"--junitxml={junit_report}",
        f"--alluredir={allure_dir}",
        f"--cov=.",
        f"--cov-report=html:{cov_report_dir}",
        f"--cov-report=term",
        "-v",
        "--tb=short"
    ]

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600
        )
        end_time = time.time()

        # 解析输出获取通过/失败数量
        stdout = result.stdout
        passed = 0
        failed = 0
        for line in stdout.split('\n'):
            if 'passed' in line and 'failed' in line:
                # 解析类似 "10 passed, 2 failed" 的行
                import re
                passed_match = re.search(r'(\d+)\s+passed', line)
                failed_match = re.search(r'(\d+)\s+failed', line)
                if passed_match:
                    passed = int(passed_match.group(1))
                if failed_match:
                    failed = int(failed_match.group(1))
                break

        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": stdout,
            "stderr": result.stderr,
            "duration": round(end_time - start_time, 2),
            "total": passed + failed,
            "passed": passed,
            "failed": failed,
            "reports": {
                "html": html_report,
                "junit": junit_report,
                "allure_dir": allure_dir,
                "coverage": cov_report_dir
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "total": 0,
            "passed": 0,
            "failed": 0,
            "reports": {}
        }


def generate_allure_report(allure_raw_dir: str, output_dir: str = "allure_report"):
    """生成Allure HTML报告（需要安装allure命令行）"""
    try:
        subprocess.run(
            ["allure", "generate", allure_raw_dir, "-o", output_dir, "--clean"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✅ Allure报告已生成: {output_dir}/index.html")
        return True
    except FileNotFoundError:
        print("⚠️ 未安装allure命令行工具，跳过Allure报告生成")
        print("   安装方法: brew install allure (Mac) / 下载allure命令行工具(Windows)")
        return False
    except Exception as e:
        print(f"❌ Allure报告生成失败: {e}")
        return False


if __name__ == "__main__":
    # 测试批量运行
    print("运行所有测试...")
    result = run_all_tests()

    print(f"\n{'='*50}")
    print("测试汇总")
    print(f"{'='*50}")
    print(f"总计: {result.get('total', 0)}")
    print(f"通过: {result.get('passed', 0)}")
    print(f"失败: {result.get('failed', 0)}")
    print(f"耗时: {result.get('duration', 0)}秒")

    reports = result.get('reports', {})
    if reports:
        print(f"\n📊 报告文件:")
        print(f"   HTML报告: {reports.get('html', '未生成')}")
        print(f"   覆盖率报告: {reports.get('coverage', '未生成')}/index.html")