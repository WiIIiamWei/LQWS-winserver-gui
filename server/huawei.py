import requests
import datetime
import json

class HuaweiIAMTokenManager:
    def __init__(self):
        self.cached_token = None
        self.token_expiry = None
        self.username = None
        self.password = None
        self.domain_name = None
        self.area = None

    def get_iam_token(self, username, password, area, domain_name):
        # 检查是否有未过期的 Token
        if self.cached_token and self.token_expiry and datetime.datetime.now(datetime.timezone.utc) < self.token_expiry:
            return self.cached_token

        # 请求新的 Token
        iam_url = f"https://iam.{area}.myhuaweicloud.com/v3/auth/tokens"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "name": username,
                            "password": password,
                            "domain": {
                                "name": domain_name
                            }
                        }
                    }
                }
            },
            "scope": {
                "project": {
                    "name": area
                }
            }
        }

        response = requests.post(iam_url, headers=headers, json=payload)
        if response.status_code != 201:
            raise Exception(f"Failed to get IAM token: {response.status_code} {response.text}")

        # 提取 Token 和过期时间
        self.cached_token = response.headers.get("X-Subject-Token")
        token_data = response.json().get("token")
        self.token_expiry = datetime.datetime.strptime(token_data["expires_at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=datetime.timezone.utc)

        return self.cached_token

def huawei_get_data(token, url):
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to get data: {response.status_code} {response.text}")

    return response.json()

def huawei_beautify_response(response):
    try:
        # 如果 response 是字典，直接使用它；否则假设它是字符串并进行解析
        if isinstance(response, dict):
            response_dict = response
        else:
            # 确保以 UTF-8 编码解析响应文本
            response_text = response.encode('utf-8').decode('utf-8')
            response_dict = json.loads(response_text)
        
        # 检查是否存在需要的键
        if "shadow" in response_dict and len(response_dict["shadow"]) > 0 and "reported" in response_dict["shadow"][0] and "properties" in response_dict["shadow"][0]["reported"]:
            property_status_info = response_dict["shadow"][0]["reported"]["properties"]
        else:
            # 如果不存在，可以返回一个空的JSON字符串或者抛出一个异常
            print("Error: Response does not contain expected data structure.")
            return json.dumps([])  # 返回一个空的列表表示没有数据
        
        # 创建一个空字典来存储修改后的数据
        modified_data = {}
        for key, value in property_status_info.items():
            # 尝试将值转换为浮点数，如果失败则保留原始值
            try:
                value = float(value)
            except ValueError:
                pass
            modified_data[key] = value
        
        # 将修改后的字典放入列表中
        modified_data_list = [modified_data]
        
        # 搜索响应文本当中的时间戳并转换为 Unix 时间戳
        event_time_str = response_dict["shadow"][0]["reported"]["event_time"]
        event_time = datetime.datetime.strptime(event_time_str, "%Y%m%dT%H%M%SZ").replace(tzinfo=datetime.timezone.utc)
        unix_timestamp = int(event_time.timestamp())
        
        # 在修改后的数据中添加时间戳
        modified_data_list[0]["time"] = unix_timestamp
        
        # 将修改后的数据以 UTF-8 编码的形式进行编码，确保不转义 Unicode 字符
        modified_data_json = json.dumps(modified_data_list, ensure_ascii=False)
        return modified_data_json
    except KeyError as e:
        print(f"KeyError: {e} not found in response.")
        return json.dumps([])  # 或者返回一个默认值/错误信息
    except Exception as e:
        print(f"An error occurred: {e}")
        return json.dumps([])  # 或者返回一个默认值/错误信息