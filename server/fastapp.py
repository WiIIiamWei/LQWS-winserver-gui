from typing import Annotated, Optional
from fastapi import FastAPI, Body, Query, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from email.mime.text import MIMEText
from email.header import Header
import os
import requests
import json
import argparse
import smtplib
import logging

from aliyun import aliyun_beautify_response, aliyun_add_authentication
from huawei import HuaweiIAMTokenManager, huawei_get_data

app = FastAPI(
    title="API 代理服务",
    version="2.0",
)

class SendMailRequest(BaseModel):
    subject: str
    address: str
    body: str

@app.head("/", summary="服务状态检查", responses={200: {"description": "Service is running"}})
async def service_status():
    """
    检查服务是否正常运行。
    """
    return JSONResponse(content={"status": "Service is running"})

@app.get("/GetDVData", summary="获取全部数据", responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "GetDVData": {
                        "summary": "获取全部数据",
                        "description": "返回 final.json 文件中的数据。",
                        "value": {
                            "data": [
                                {"id": 1, "name": "Item 1"},
                                {"id": 2, "name": "Item 2"}
                            ]
                        }
                    }
                }
            }
        }
    },
    500: {"description": "Internal Server Error"}
})
async def get_dv_data():
    """
    返回 `final.json` 文件中的数据。
    """
    try:
        final_file_path = os.path.expanduser('final.json')
        with open(final_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        return JSONResponse(content=json_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"JSON文件读取失败: {str(e)}")

@app.get("/GetSingleData", summary="获取单个数据", responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "GetSingleData": {
                        "summary": "获取单个数据",
                        "description": "根据 id 和 key 返回 output.json 文件中的数据。",
                        "value": {
                            "name": "Item 1"
                        }
                    }
                }
            }
        }
    },
    400: {"description": "Invalid Request"},
    404: {"description": "Not Found"},
    500: {"description": "Internal Server Error"}
})
async def get_single_data(
    id: Annotated[str, Query(description="数据ID", example="123")],
    key: Annotated[str, Query(description="数据键", example="name")]
):
    """
    根据 `id` 和 `key` 字段的值，返回 `output.json` 文件中的数据。
    """
    if not id or not key:
        raise HTTPException(status_code=400, detail="缺少必要的字段")
    
    try:
        output_file_path = os.path.expanduser('output.json')
        with open(output_file_path, 'r', encoding='utf-8') as file:
            data_dict = json.load(file)
        
        if id in data_dict and key in data_dict[id]:
            return JSONResponse(content={key: data_dict[id][key]})
        
        raise HTTPException(status_code=404, detail="缺少必要的字段")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"输出文件处理失败: {str(e)}")

@app.get("/aliyun", summary="阿里云物联网平台 API 代理", responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "ProxyURL": {
                        "summary": "代理请求URL",
                        "description": "代理请求指定的 URL 并返回响应。",
                        "value": {
                            "status": "success",
                            "data": {"key": "value"}
                        }
                    }
                }
            }
        }
    },
    400: {"description": "Invalid Request"},
    404: {"description": "Not Found"},
    500: {"description": "Internal Server Error"}
})
async def aliyun_api_handler(
    url: Annotated[str, Query(description="需要代理的URL", example=r"http://example.com/api/data")]
):
    """
    代理请求阿里云物联网平台 URL 并返回响应。此处的 URL 不需要加入签名和时间戳信息。
    
    阿里云对于应用端的 URL 希望加入时间戳、签名等参数。请在你的配置文件中定义 AccessKeySecret，服务器会自动处理签名等步骤。
    """
    access_key_secret = app.state.secret
    authenticated_url = aliyun_add_authentication(url, access_key_secret)
    log_request(url, authenticated_url)
    try:
        response = requests.get(authenticated_url)
    except:
        raise HTTPException(status_code=500, detail="请求失败")
    response_content = aliyun_beautify_response(response)
    print(response_content)
    return JSONResponse(content=json.loads(response_content), status_code=response.status_code)

@app.get("/huawei", summary="华为云物联网平台 API 代理", responses={
    200: {
        "description": "Successful Response",
        "content": {
            "application/json": {
                "examples": {
                    "GetData": {
                        "summary": "获取数据",
                        "description": "根据 URL 返回数据。",
                        "value": {
                            "status": "success",
                            "data": {"key": "value"}
                        }
                    }
                }
            }
        }
    },
    400: {"description": "Invalid Request"},
    500: {"description": "Internal Server Error"}
})
async def huawei_api_handler(
    url: Annotated[str, Query(description="需要代理的URL", example="http://example.com/api/data")]
):
    """
    代理请求华为云物联网平台 URL 并返回响应。此处的请求不需要加入 Token 或 AK/SK 签名信息。
    
    请在你的配置文件中定义华为云 IAM 用户名、密码、区域和域名，服务器会自动处理 Token 的生成。
    
    请求的 URL 错误时，将返回原始的状态码，详见[华为云物联网平台 API 文档](https://support.huaweicloud.com/api-iothub/ErrorCode.html)。
    """
    token = app.state.huawei_token_manager.get_iam_token(
        username=app.state.huawei_token_manager.username,
        password=app.state.huawei_token_manager.password,
        area=app.state.huawei_token_manager.area,
        domain_name=app.state.huawei_token_manager.domain_name
    )
    try:
        response_data = huawei_get_data(token, url)
        return JSONResponse(content=response_data)
    except Exception as e:
        error_message = str(e)
        if "Failed to get data" in error_message:
            # 提取原始状态码
            status_code = int(error_message.split(":")[1].strip().split()[0])
            raise HTTPException(status_code=status_code, detail=f"请求失败: {error_message}")
        raise HTTPException(status_code=500, detail=f"请求失败: {error_message}")

@app.post("/GetHuaweiIAM", summary="获取华为云 IAM Token", responses={401: {"description": "Unauthorized"}, 500: {"description": "Internal Server Error"}})
async def get_huawei_iam_token(
    iam_username: Optional[str] = None,
    iam_password: Optional[str] = None,
    domain_name: Optional[str] = None,
    area: Optional[str] = None
):
    """
    获取华为云 IAM Token。
    
    如果提供了 `iam_username`、`iam_password`、`domain_name` 和 `area` 参数，则使用这些参数生成 Token。否则，使用已有参数生成 Token。
    """
    try:
        if iam_username and iam_password and domain_name and area:
            token = app.state.huawei_token_manager.get_iam_token(
                username=iam_username,
                password=iam_password,
                area=area,
                domain_name=domain_name
            )
        else:
            token = app.state.huawei_token_manager.get_iam_token(
                username=app.state.huawei_token_manager.username,
                password=app.state.huawei_token_manager.password,
                area=app.state.huawei_token_manager.area,
                domain_name=app.state.huawei_token_manager.domain_name
            )
        return {"token": token}
    except Exception as e:
        if "401" in str(e):
            raise HTTPException(status_code=401, detail="Unauthorized: Invalid credentials")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/mail", summary="发送邮件", responses={500: {"description": "Internal Server Error"}})
async def send_mail_endpoint(request: Annotated[SendMailRequest, Body(
    openapi_examples={
        "example1": {
            "summary": "正常示例",
            "description": "一个正常的邮件发送示例。",
            "value": {
                "subject": "Test Subject",
                "address": "test@example.com",
                "body": "This is a test email body."
            }
        },
        "example2": {
            "summary": "缺少主题",
            "description": "一个缺少主题的邮件发送示例。",
            "value": {
                "address": "test@example.com",
                "body": "This is a test email body."
            }
        }
    }
)]):
    """
    使用给定的 `subject`、`address` 和 `body` 字段的值，发送邮件。
    
    - `subject`：邮件主题。
    - `address`：收件人地址。
    - `body`：邮件正文。
    """
    success, message = send_mail(request.subject, request.address, request.body)
    if success:
        return {"message": message}
    else:
        raise HTTPException(status_code=500, detail=f"邮件发送失败: {message}")

def csv_to_json(csv_data):
    csv_data = csv_data.strip().split("\n")
    csv_headers = csv_data[0].split(",")
    json_data = []
    for row in csv_data[1:]:
        if row:
            row = row.split(",")
            if len(row) == len(csv_headers):
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[csv_headers[i]] = value
                json_data.append(row_dict)
    return json.dumps(json_data, ensure_ascii=False)

def log_request(original_url, authenticated_url):
    log_message = f"Original URL: {original_url}\nAuthenticated URL: {authenticated_url}\n\n"
    log_file_path = os.path.expanduser('log_req.txt')
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message)

def send_mail(subject, address, body):
    sender = app.state.mail_sender
    receivers = [address]
    message = MIMEText(body, 'plain', 'utf-8')
    message['From'] = Header(sender, 'utf-8')
    message['To'] = Header(address, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    try:
        logging.info(f'Sending email to {address} with subject: {subject}')
        smtpObj = smtplib.SMTP(app.state.mail_host, app.state.mail_port)
        smtpObj.login(sender, app.state.mail_password)
        logging.debug(f'SMTP login successful')
        smtpObj.sendmail(sender, receivers, message.as_string())
        return True, 'Successfully sent email'
    except smtplib.SMTPException as e:
        return False, f'Error: unable to send email, {str(e)}'

def main():
    parser = argparse.ArgumentParser(description='启动FastAPI应用')
    parser.add_argument('--verbose', type=str, choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default='INFO', help='设置日志级别')
    parser.add_argument('--config', type=str, default='settings.json', required=False, help='指定settings.json配置文件的位置')
    args = parser.parse_args()
    log_level = getattr(logging, args.verbose, logging.INFO)
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
    with open(args.config, 'r', encoding='utf-8') as file:
        config = json.load(file)
    api_config = next(item for item in config if item["setting"] == "api")
    mail_config = next(item for item in config if item["setting"] == "mail")
    port = int(api_config.get('port', 5200))
    secret = api_config.get('access-key-secret')
    if not secret:
        raise ValueError("阿里云平台的AccessKeySecret未在配置文件中指定")
    app.state.secret = secret
    app.state.mail_host = mail_config.get('host')
    app.state.mail_port = mail_config.get('port') if mail_config.get('port') else 25
    app.state.mail_sender = mail_config.get('sender')
    app.state.mail_password = mail_config.get('password')
    app.state.huawei_token_manager = HuaweiIAMTokenManager()
    app.state.huawei_token_manager.username = api_config.get('huawei_iam_username')
    app.state.huawei_token_manager.password = api_config.get('huawei_iam_password')
    app.state.huawei_token_manager.domain_name = api_config.get('huawei_iam_domain')
    app.state.huawei_token_manager.area = api_config.get('huawei_iam_area')
    logging.info(f'FastAPI Config: {api_config}')
    logging.info(f'Mail Config: {mail_config}')
    import uvicorn
    uvicorn.run(
        app,
        host='0.0.0.0',
        port=port,
        proxy_headers=True,
        forwarded_allow_ips='127.0.0.1'
    )

if __name__ == '__main__':
    main()