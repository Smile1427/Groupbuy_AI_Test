# 拼团系统AI自动化测试

## 项目简介

本项目是一个完整的测试开发实战项目，包含：

- **被测系统**：拼团系统前端页面（商品列表/详情/拼团/倒计时）
- **UI自动化测试**：40个Playwright测试用例，覆盖正常流程、异常处理、边界条件
- **API测试**：15个Postman接口测试，覆盖商品模块和拼团模块
- **性能测试**：Locust 20人并发测试
- **Mock服务**：json-server模拟后端API
- **AI能力**：智谱AI辅助生成测试代码

## 技术栈

| 模块 | 技术 |
|------|------|
| 被测系统 | HTML/CSS/JS |
| UI自动化 | Python + Playwright + Pytest |
| API测试 | Postman + Newman |
| 性能测试 | Locust |
| Mock服务 | json-server |
| 测试报告 | pytest-html + Allure |

## 测试数据总览

| 测试类型 | 用例数 | 通过率 |
|---------|-------|--------|
| UI自动化测试 | 40 | 100% |
| API接口测试 | 15 | 100% |
| 性能测试 | 20人并发 | 响应时间 < 10ms |

## 项目结构
```
groupbuy-project/
├── frontend/ # 被测系统：拼团H5
│ ├── index.html # 商品列表页
│ ├── detail.html # 商品详情页
│ └── style.css # 样式文件
├── aitest/ # AI测试平台
│ ├── core/ # 测试核心模块
│ │ ├── ai_generator.py # AI生成测试代码
│ │ ├── test_runner.py # 测试执行引擎
│ │ └── locator_repair.py # 定位器自动修复
│ ├── test_cases/ # 测试用例（YAML）
│ ├── generated_tests/ # AI生成的测试代码
│ ├── reports/ # 测试报告
│ ├── postman/ # Postman测试集合
│ └── main.py # 主入口
├── backend/ # Mock服务
│ └── db.json # Mock数据
├── BUGS.md # 缺陷报告
└── README.md # 项目说明
```


## 快速开始

### 1. 环境准备

```bash
# 安装Python依赖
cd aitest
pip install -r requirements.txt
playwright install
```

### 2. 启动Mock API服务
```bash
cd backend
json-server --watch db.json --port 3000
```

### 3. 启动前端服务
```bash
cd frontend
python -m http.server 8001
```

### 4. 运行UI自动化测试
```bash
cd aitest
python main.py
```

### 5. 运行API测试
```bash
newman run postman/API_Tests.json -r html --reporter-html-export reports/api_report.html
```

### 6. 运行性能测试
```bash
locust -f performance_test.py --host=http://localhost:8001
# 访问 http://localhost:8089 配置并发用户
```

## 测试报告

所有报告位于 `aitest/reports/` 目录下：

| 报告类型 | 文件路径 |
|------|---------|
| UI功能测试报告 | `aitest/reports/summary_20260421_172812.html` |
| API测试报告 | `aitest/postman/API_Tests.json` |
| 性能测试报告 | `aitest/reports/performance_report.html` |
| Allure报告 | `aitest/reports/allure_report/index.html` |

> 注：具体文件名可能因运行时间不同而变化，请查看 `aitest/reports/` 目录下的最新文件。

### 缺陷报告
详见 BUGS.md

## 核心能力展示
### 1. 测试用例设计
- 40个UI测试用例，覆盖正常、异常、边界、组合场景
- 15个API测试用例，覆盖商品和拼团核心接口

### 2. AI测试生成
- 集成智谱AI，自然语言自动生成Playwright测试代码
- 实现定位器自修复机制

### 3. 性能测试
- 20人并发访问，平均响应时间 < 10ms
- 成功率100%

### 4. 测试报告
- HTML报告 + Allure报告 + 覆盖率报告
- 失败自动截图

## 🤝 贡献
欢迎提交 Issue 和 Pull Request！