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
        
        # 创建AccessKeySecret输入
        self._create_secret_input()
    
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
    
    def update_from_config(self, config_item):
        """从配置更新UI"""
        # 更新是否启用
        self.api_enabled.setChecked(config_item.get('enabled', True))
        
        # 更新端口
        self.port_input.setText(str(config_item.get('port', '5200')))
        
        # 更新AccessKeySecret
        self.secret_input.setText(config_item.get('access-key-secret', ''))
    
    def get_config(self):
        """获取当前配置"""
        return {
            'setting': 'api',
            'enabled': self.api_enabled.isChecked(),
            'port': int(self.port_input.text() or 5200),
            'access-key-secret': self.secret_input.text()
        }