from PySide6 import QtWidgets, QtGui


class ApiServerTab(QtWidgets.QWidget):
    """API服务器标签页"""
    
    def __init__(self):
        super().__init__()
        
        # 创建布局
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # 创建启用选项
        self._create_enable_option()
        
        # 创建端口输入
        self._create_port_input()
        
        # 创建阿里云标签
        aliyun_label = QtWidgets.QLabel("阿里云设置")
        aliyun_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.layout.addWidget(aliyun_label)
        
        # 创建AccessKeySecret输入
        self._create_secret_input()
        
        # 创建华为云IAM相关输入框
        self._create_huawei_iam_inputs()
        
        # 添加弹性空间
        self.layout.addItem(QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        ))
    
    def _create_enable_option(self):
        """创建启用选项"""
        enable_layout = QtWidgets.QHBoxLayout()
        self.api_enabled = QtWidgets.QCheckBox('启用API服务器')
        self.api_enabled.setChecked(True)
        self.api_enabled.setObjectName('api_is_enabled')
        enable_layout.addWidget(self.api_enabled)
        self.layout.addLayout(enable_layout)
    
    def _create_port_input(self):
        """创建端口输入"""
        port_layout = QtWidgets.QHBoxLayout()
        port_label = QtWidgets.QLabel('API服务器端口：')
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setPlaceholderText('输入端口号')
        self.port_input.setValidator(QtGui.QIntValidator())
        self.port_input.setText('5200')  # 默认值
        self.port_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.port_input.setObjectName('api_port')
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        self.layout.addLayout(port_layout)
    
    def _create_secret_input(self):
        """创建AccessKeySecret输入"""
        secret_layout = QtWidgets.QHBoxLayout()
        secret_label = QtWidgets.QLabel('AccessKeySecret：')
        self.secret_input = QtWidgets.QLineEdit()
        self.secret_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.secret_input.setPlaceholderText('输入阿里云提供的AccessKeySecret')
        self.secret_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.secret_input.setObjectName('api_access_key_secret')
        secret_layout.addWidget(secret_label)
        secret_layout.addWidget(self.secret_input)
        self.layout.addLayout(secret_layout)
    
    def _create_huawei_iam_inputs(self):
        """创建华为云IAM相关输入框"""
        # 创建标签
        huawei_label = QtWidgets.QLabel("华为云IAM设置")
        huawei_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.layout.addWidget(huawei_label)
        
        # 华为云IAM用户名
        username_layout = QtWidgets.QHBoxLayout()
        username_label = QtWidgets.QLabel('用户名：')
        self.huawei_username = QtWidgets.QLineEdit()
        self.huawei_username.setPlaceholderText('输入华为云IAM用户名')
        self.huawei_username.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.huawei_username.setObjectName('api_huawei_iam_username')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.huawei_username)
        self.layout.addLayout(username_layout)
        
        # 华为云IAM密码
        password_layout = QtWidgets.QHBoxLayout()
        password_label = QtWidgets.QLabel('密码：')
        self.huawei_password = QtWidgets.QLineEdit()
        self.huawei_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.huawei_password.setPlaceholderText('输入华为云IAM密码')
        self.huawei_password.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.huawei_password.setObjectName('api_huawei_iam_password')
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.huawei_password)
        self.layout.addLayout(password_layout)
        
        # 华为云IAM域名
        domain_layout = QtWidgets.QHBoxLayout()
        domain_label = QtWidgets.QLabel('域名：')
        self.huawei_domain = QtWidgets.QLineEdit()
        self.huawei_domain.setPlaceholderText('输入华为云IAM域名')
        self.huawei_domain.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.huawei_domain.setObjectName('api_huawei_iam_domain')
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(self.huawei_domain)
        self.layout.addLayout(domain_layout)
        
        # 华为云IAM区域
        area_layout = QtWidgets.QHBoxLayout()
        area_label = QtWidgets.QLabel('区域：')
        self.huawei_area = QtWidgets.QLineEdit()
        self.huawei_area.setPlaceholderText('输入华为云IAM区域')
        self.huawei_area.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.huawei_area.setObjectName('api_huawei_iam_area')
        area_layout.addWidget(area_label)
        area_layout.addWidget(self.huawei_area)
        self.layout.addLayout(area_layout)
        
        # 设置所有输入框的尺寸策略
        for widget in [self.huawei_username, self.huawei_password, self.huawei_domain, self.huawei_area]:
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            widget.setSizePolicy(size_policy)
    
    def update_from_config(self, config_item):
        """从配置更新UI"""
        # 更新是否启用
        self.api_enabled.setChecked(config_item.get('enabled', True))
        
        # 更新端口
        self.port_input.setText(str(config_item.get('port', '5200')))
        
        # 更新阿里云AccessKeySecret
        self.secret_input.setText(config_item.get('access-key-secret', ''))
        
        # 更新华为云IAM相关设置
        self.huawei_username.setText(config_item.get('huawei_iam_username', ''))
        self.huawei_password.setText(config_item.get('huawei_iam_password', ''))
        self.huawei_domain.setText(config_item.get('huawei_iam_domain', ''))
        self.huawei_area.setText(config_item.get('huawei_iam_area', ''))
    
    def get_config(self):
        """获取当前配置"""
        return {
            'setting': 'api',
            'enabled': self.api_enabled.isChecked(),
            'port': int(self.port_input.text() or 5200),
            'access-key-secret': self.secret_input.text(),
            'huawei_iam_username': self.huawei_username.text(),
            'huawei_iam_password': self.huawei_password.text(),
            'huawei_iam_domain': self.huawei_domain.text(),
            'huawei_iam_area': self.huawei_area.text()
        }