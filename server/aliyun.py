import urllib.parse
import hmac
import base64
import json
import datetime
import random
from hashlib import sha1

def aliyun_generate_sign(url, access_key_secret):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    sorted_params = sorted((k, v[0]) for k, v in query_params.items())
    query_string = urllib.parse.urlencode(sorted_params, quote_via=urllib.parse.quote)
    string_to_sign = 'GET' + '&' + urllib.parse.quote_plus('/') + '&' + urllib.parse.quote_plus(query_string)
    signature = hmac.new((access_key_secret + "&").encode('utf-8'), string_to_sign.encode('utf-8'), sha1).digest()
    signature = base64.b64encode(signature).decode('utf-8')
    signature = urllib.parse.quote_plus(signature)
    signed_url = f"{url}&Signature={signature}"
    return signed_url

def aliyun_beautify_response(response):
    response_text = response.text.encode('utf-8').decode('utf-8')
    response_dict = json.loads(response_text)
    property_status_info = response_dict["Data"]["List"]["PropertyStatusInfo"]
    modified_data = {}
    for item in property_status_info:
        try:
            value = float(item["Value"])
        except ValueError:
            value = item["Value"]
        modified_data[item["Name"]] = value
    modified_data_list = [modified_data]
    modified_data_json = json.dumps(modified_data_list, ensure_ascii=False)
    return modified_data_json

def aliyun_add_authentication(url, access_key_secret):
    current_time = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    url += "&Timestamp=" + current_time
    url += "&SignatureNonce=" + str(random.randint(1, 999999))
    return aliyun_generate_sign(url, access_key_secret)

def aliyun_beautify_response(response):
    try:
        # 确保以 UTF-8 编码解析响应文本
        if isinstance(response, str):
            response_text = response.encode('utf-8').decode('utf-8')
        else:
            response_text = response.text.encode('utf-8').decode('utf-8')
        
        response_dict = json.loads(response_text)
        
        # 检查是否存在需要的键
        if "Data" in response_dict and "List" in response_dict["Data"] and "PropertyStatusInfo" in response_dict["Data"]["List"]:
            property_status_info = response_dict["Data"]["List"]["PropertyStatusInfo"]
        else:
            # 如果不存在，可以返回一个空的JSON字符串或者抛出一个异常
            print("Error: Response does not contain expected data structure.")
            return json.dumps([])  # 返回一个空的列表表示没有数据
        
        # 创建一个空字典来存储修改后的数据
        modified_data = {}
        for item in property_status_info:
            # 尝试将值转换为浮点数，如果失败则保留原始字符串
            try:
                value = float(item["Value"])
            except ValueError:
                value = item["Value"]
            modified_data[item["Name"]] = value
        
        # 将修改后的字典放入列表中
        modified_data_list = [modified_data]
        
        # 搜索响应文本当中的时间戳
        timestamps = [item["Time"] for item in property_status_info]
        
        # 在修改后的数据中添加时间戳
        modified_data_list[0]["time"] = max(timestamps)
        
        # 将修改后的数据以 UTF-8 编码的形式进行编码，确保不转义 Unicode 字符
        modified_data_json = json.dumps(modified_data_list, ensure_ascii=False)
        return modified_data_json
    except KeyError as e:
        print(f"KeyError: {e} not found in response.")
        return json.dumps([])  # 或者返回一个默认值/错误信息
    except Exception as e:
        print(f"An error occurred: {e}")
        return json.dumps([])  # 或者返回一个默认值/错误信息