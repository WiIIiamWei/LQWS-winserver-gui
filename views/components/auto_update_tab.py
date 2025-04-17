from PySide6 import QtWidgets, QtCore

from views.dialogs.json_editor import JSONEditorDialog


class AutoUpdateTab(QtWidgets.QWidget):
    """自动更新数据标签页，支持直接编辑嵌套JSON结构"""
    
    def __init__(self):
        super().__init__()
        
        # 创建布局
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # 阿里云AccessKeySecret输入框
        self._create_aliyun_secret_input()
        
        # 华为云IAM相关输入框
        self._create_huawei_iam_inputs()
        
        # 添加弹性空间
        self.layout.addItem(QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        ))
        
        # JSON编辑按钮
        self._create_json_edit_button()
        
        # 存储JSON数据
        self.json_data = []
        
        # 连接信号槽
        self._connect_signals()
    
    def _create_aliyun_secret_input(self):
        """创建阿里云AccessKeySecret输入框"""
        # 创建标签
        aliyun_label = QtWidgets.QLabel("阿里云设置")
        aliyun_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.layout.addWidget(aliyun_label)
        
        # AccessKeySecret输入框
        secret_layout = QtWidgets.QHBoxLayout()
        secret_label = QtWidgets.QLabel('AccessKeySecret：')
        self.secret_input = QtWidgets.QLineEdit()
        self.secret_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.secret_input.setPlaceholderText('输入阿里云提供的AccessKeySecret')
        self.secret_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.secret_input.setObjectName('auto_update_secret')
        
        # 设置尺寸策略，允许水平拉伸
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.secret_input.setSizePolicy(size_policy)
        
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
        self.huawei_username.setObjectName('huawei_iam_username')
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
        self.huawei_password.setObjectName('huawei_iam_password')
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.huawei_password)
        self.layout.addLayout(password_layout)
        
        # 华为云IAM域名
        domain_layout = QtWidgets.QHBoxLayout()
        domain_label = QtWidgets.QLabel('域名：')
        self.huawei_domain = QtWidgets.QLineEdit()
        self.huawei_domain.setPlaceholderText('输入华为云IAM域名')
        self.huawei_domain.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.huawei_domain.setObjectName('huawei_iam_domain')
        domain_layout.addWidget(domain_label)
        domain_layout.addWidget(self.huawei_domain)
        self.layout.addLayout(domain_layout)
        
        # 华为云IAM区域
        area_layout = QtWidgets.QHBoxLayout()
        area_label = QtWidgets.QLabel('区域：')
        self.huawei_area = QtWidgets.QLineEdit()
        self.huawei_area.setPlaceholderText('输入华为云IAM区域')
        self.huawei_area.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.huawei_area.setObjectName('huawei_iam_area')
        area_layout.addWidget(area_label)
        area_layout.addWidget(self.huawei_area)
        self.layout.addLayout(area_layout)
        
        # 设置所有输入框的尺寸策略
        for widget in [self.huawei_username, self.huawei_password, self.huawei_domain, self.huawei_area]:
            size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            widget.setSizePolicy(size_policy)
    
    def _create_json_edit_button(self):
        """创建JSON编辑按钮"""
        # 创建标签
        json_header = QtWidgets.QLabel("自动更新数据配置")
        json_header.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.layout.addWidget(json_header)
        
        # 创建按钮和信息布局
        button_layout = QtWidgets.QHBoxLayout()
        
        # 说明标签
        json_label = QtWidgets.QLabel('点击右侧按钮编辑自动更新的数据字段:')
        json_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt;')
        
        # 编辑按钮
        self.edit_json_button = QtWidgets.QPushButton('编辑JSON配置')
        self.edit_json_button.setStyleSheet("""
            QPushButton {
                font-family: Microsoft Yahei;
                font-size: 10pt;
                font-weight: bold;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background:#366ecc;
            }
        """)
        
        button_layout.addWidget(json_label)
        button_layout.addStretch(1)
        button_layout.addWidget(self.edit_json_button)
        self.layout.addLayout(button_layout)
        
        # 添加状态标签
        self.status_label = QtWidgets.QLabel('')
        self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt;')
        self.layout.addWidget(self.status_label)
    
    def _connect_signals(self):
        """连接信号和槽"""
        self.edit_json_button.clicked.connect(self.open_json_editor)
    
    def open_json_editor(self):
        """打开JSON编辑器对话框"""
        dialog = JSONEditorDialog(self, self.json_data)
        result = dialog.exec()
        
        if result == QtWidgets.QDialog.Accepted:
            self.json_data = dialog.get_json()
            self.status_label.setText('JSON配置已更新')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: green;')
    
    def update_from_config(self, config_item):
        """从配置更新UI"""
        # 更新阿里云AccessKeySecret
        self.secret_input.setText(config_item.get('access-key-secret', ''))
        
        # 更新华为云IAM相关设置
        self.huawei_username.setText(config_item.get('huawei_iam_username', ''))
        self.huawei_password.setText(config_item.get('huawei_iam_password', ''))
        self.huawei_domain.setText(config_item.get('huawei_iam_domain', ''))
        self.huawei_area.setText(config_item.get('huawei_iam_area', ''))
        
        # 更新JSON数据
        self.json_data = config_item.get('value', [])
    
    def get_config(self):
        """获取当前配置"""
        return {
            'setting': 'request_cycle',
            'access-key-secret': self.secret_input.text(),
            'huawei_iam_username': self.huawei_username.text(),
            'huawei_iam_password': self.huawei_password.text(),
            'huawei_iam_domain': self.huawei_domain.text(),
            'huawei_iam_area': self.huawei_area.text(),
            'value': self.json_data
        }