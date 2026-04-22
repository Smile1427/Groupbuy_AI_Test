"""性能测试 - 只测试静态页面"""
from locust import HttpUser, task, between
import random


class GroupBuyUser(HttpUser):
    """模拟拼团用户行为"""

    wait_time = between(1, 3)

    def on_start(self):
        """用户启动时访问首页"""
        self.client.get("/index.html")

    @task(4)
    def view_product_list(self):
        """查看商品列表"""
        self.client.get("/index.html")

    @task(3)
    def view_product_detail(self):
        """查看商品详情"""
        product_id = random.choice([1, 2, 3])
        self.client.get(f"/detail.html?id={product_id}")

    @task(1)
    def refresh_page(self):
        """刷新页面"""
        page = random.choice(["/index.html", "/detail.html?id=1"])
        self.client.get(page)