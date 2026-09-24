from fastapi.testclient import TestClient

from main import app

# 创建测试客户端实例
client = TestClient(app)


# 编写标准的 pytest 测试函数（必须以 test_ 开头）
def test_read_main():
    response = client.get("/")
    # 4. 使用 assert 断言状态码和返回的 JSON 数据
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
