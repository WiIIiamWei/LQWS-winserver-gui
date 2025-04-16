from models.device import DeviceList


class RequestCycle:
    def __init__(self, aliyun_access_key_secret: str, huawei_iam_username: str, huawei_iam_password: str,
                 huawei_iam_domain: str, huawei_iam_area: str, values: list = None):
        self.aliyun_access_key_secret = aliyun_access_key_secret
        self.huawei_iam_username = huawei_iam_username
        self.huawei_iam_password = huawei_iam_password
        self.huawei_iam_domain = huawei_iam_domain
        self.huawei_iam_area = huawei_iam_area
        self.values = values if values is not None else []

    def set_values(self, values: list):
        self.values = values

class APIServer:
    def __init__(self, port: int, access_key_secret: str, huawei_iam_username: str, huawei_iam_password: str,
                 huawei_iam_domain: str, huawei_iam_area: str, enabled: bool):
        self.port = port
        self.access_key_secret = access_key_secret
        self.huawei_iam_username = huawei_iam_username
        self.huawei_iam_password = huawei_iam_password
        self.huawei_iam_domain = huawei_iam_domain
        self.huawei_iam_area = huawei_iam_area
        self.enabled = enabled

class EmailAlert:
    def __init__(self, server: str, port: int, username: str, password: str, alert_level: str, recipients: list = None):
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.alert_level = alert_level
        self.recipients = recipients if recipients is not None else []

    def set_recipients(self, recipients: list):
        self.recipients = recipients

class JSONConfig:
    def __init__(self, device_list: DeviceList, request_cycle: RequestCycle, api_server: APIServer,
                 email_alert: EmailAlert):
        self.device_list = device_list
        self.request_cycle = request_cycle
        self.api_server = api_server
        self.email_alert = email_alert
