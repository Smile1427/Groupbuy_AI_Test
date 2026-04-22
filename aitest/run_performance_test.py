"""性能测试启动脚本"""
import subprocess
import webbrowser
import time
import os


def run_performance_test(users: int = 10, spawn_rate: int = 1, host: str = "http://localhost:8001"):
    """
    启动Locust性能测试

    Args:
        users: 总用户数
        spawn_rate: 每秒启动用户数
        host: 目标主机
    """
    print("=" * 50)
    print("Locust 性能测试")
    print("=" * 50)
    print(f"目标地址: {host}")
    print(f"总用户数: {users}")
    print(f"启动速率: {spawn_rate} 用户/秒")
    print("=" * 50)
    print("\n启动Locust Web界面...")
    print("访问 http://localhost:8089 开始测试\n")

    # 启动Locust
    cmd = [
        "locust",
        "-f", "performance_test.py",
        "--host", host,
        "--web-port", "8089",
        "--users", str(users),
        "--spawn-rate", str(spawn_rate)
    ]

    # 启动子进程
    process = subprocess.Popen(cmd)

    # 等待2秒后打开浏览器
    time.sleep(2)
    webbrowser.open("http://localhost:8089")

    print("按 Ctrl+C 停止测试...")

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n正在停止性能测试...")
        process.terminate()
        process.wait()
        print("性能测试已停止")


def run_headless_test(users: int = 10, run_time: int = 30):
    """
    无界面模式运行性能测试（自动运行，不打开Web界面）

    Args:
        users: 总用户数
        run_time: 运行时间（秒）
    """
    print("=" * 50)
    print("无界面模式性能测试")
    print("=" * 50)
    print(f"目标地址: http://localhost:8001")
    print(f"总用户数: {users}")
    print(f"运行时间: {run_time} 秒")
    print("=" * 50)

    cmd = [
        "locust",
        "-f", "performance_test.py",
        "--host", "http://localhost:8001",
        "--headless",
        "--users", str(users),
        "--spawn-rate", "1",
        "--run-time", f"{run_time}s",
        "--html", "reports/performance_report.html"
    ]

    subprocess.run(cmd)
    print(f"\n✅ 性能测试完成！报告已保存: reports/performance_report.html")


if __name__ == "__main__":
    print("请选择运行模式：")
    print("1. Web界面模式（手动控制）")
    print("2. 无界面自动模式（运行30秒）")

    choice = input("请输入选项 (1/2): ")

    if choice == "1":
        run_performance_test(users=20, spawn_rate=2)
    elif choice == "2":
        run_headless_test(users=10, run_time=30)
    else:
        print("无效选项")