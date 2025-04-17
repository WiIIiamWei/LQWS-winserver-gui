from PySide6 import QtWidgets, QtGui

from views.dialogs.body import MailBodyDialog
from views.dialogs.recipients import MailRecipientsDialog


class EmailAlertsTab(QtWidgets.QWidget):
    """邮箱警报标签页"""
    
    def __init__(self):
        super().__init__()
        
        # 创建布局
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # 创建SMTP服务器输入
        self._create_server_input()
        
        # 创建SMTP端口输入
        self._create_port_input()
        
        # 创建邮箱账号输入
        self._create_username_input()
        
        # 创建邮箱密码输入
        self._create_password_input()
        
        # 创建警报等级选择
        self._create_alert_level_selection()
        
        # 创建收件人和正文设置按钮
        self._create_recipient_body_buttons()
        
        # 初始化对话框实例
        self.mail_recipients_dialog = MailRecipientsDialog()
        self.mail_body_dialog = MailBodyDialog()
        
        # 连接信号槽
        self._connect_signals()
        
        # 存储收件人和正文设置
        self.recipients = []
        self.body_format = {}
    
    def _create_server_input(self):
        """创建SMTP服务器输入"""
        server_layout = QtWidgets.QHBoxLayout()
        server_label = QtWidgets.QLabel('SMTP服务器：')
        self.server_input = QtWidgets.QLineEdit()
        self.server_input.setPlaceholderText('输入SMTP服务器地址')
        self.server_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.server_input.setObjectName('email_server')
        server_layout.addWidget(server_label)
        server_layout.addWidget(self.server_input)
        self.layout.addLayout(server_layout)
    
    def _create_port_input(self):
        """创建SMTP端口输入"""
        port_layout = QtWidgets.QHBoxLayout()
        port_label = QtWidgets.QLabel('SMTP端口：')
        self.port_input = QtWidgets.QLineEdit()
        self.port_input.setPlaceholderText('输入SMTP端口')
        self.port_input.setValidator(QtGui.QIntValidator())
        self.port_input.setText('465')  # 默认值
        self.port_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.port_input.setObjectName('email_port')
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)
        self.layout.addLayout(port_layout)
    
    def _create_username_input(self):
        """创建邮箱账号输入"""
        username_layout = QtWidgets.QHBoxLayout()
        username_label = QtWidgets.QLabel('邮箱账号：')
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText('输入邮箱账号')
        self.username_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.username_input.setObjectName('email_username')
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        self.layout.addLayout(username_layout)
    
    def _create_password_input(self):
        """创建邮箱密码输入"""
        password_layout = QtWidgets.QHBoxLayout()
        password_label = QtWidgets.QLabel('邮箱密码：')
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText('输入邮箱密码')
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.password_input.setObjectName('email_password')
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        self.layout.addLayout(password_layout)
    
    def _create_alert_level_selection(self):
        """创建警报等级选择"""
        alert_level_layout = QtWidgets.QHBoxLayout()
        alert_level_label = QtWidgets.QLabel('警报等级：')
        alert_level_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        alert_level_layout.addWidget(alert_level_label)
        
        self.alert_level_group = QtWidgets.QButtonGroup()
        alert_levels = ['关闭', '黄色警报', '橙色警报', '红色警报']
        
        for level in alert_levels:
            radio_button = QtWidgets.QRadioButton(level)
            radio_button.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
            self.alert_level_group.addButton(radio_button)
            alert_level_layout.addWidget(radio_button)
        
        # 设置默认选择
        self.alert_level_group.buttons()[0].setChecked(True)
        self.layout.addLayout(alert_level_layout)
    
    def _create_recipient_body_buttons(self):
        """创建收件人和正文设置按钮"""
        buttons_layout = QtWidgets.QHBoxLayout()
        
        self.recipients_button = QtWidgets.QPushButton('收件人设置')
        self.recipients_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        
        self.body_button = QtWidgets.QPushButton('正文设置')
        self.body_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        
        buttons_layout.addWidget(self.recipients_button)
        buttons_layout.addWidget(self.body_button)
        self.layout.addLayout(buttons_layout)
    
    def _connect_signals(self):
        """连接信号槽"""
        self.recipients_button.clicked.connect(self.open_recipients_dialog)
        self.body_button.clicked.connect(self.open_body_dialog)
    
    def open_recipients_dialog(self):
        """打开收件人设置对话框"""
        if not self.mail_recipients_dialog.isVisible():
            # 先更新对话框中的收件人列表
            self.mail_recipients_dialog.load_recipients(self.recipients)
            result = self.mail_recipients_dialog.exec()
            if result == QtWidgets.QDialog.Accepted:
                # 保存收件人设置
                self.recipients = self.mail_recipients_dialog.get_recipients()
    
    def open_body_dialog(self):
        """打开正文设置对话框"""
        if not self.mail_body_dialog.isVisible():
            # 先更新对话框中的正文格式
            self.mail_body_dialog.load_body(self.body_format)
            result = self.mail_body_dialog.exec()
            if result == QtWidgets.QDialog.Accepted:
                # 保存正文设置
                self.body_format = self.mail_body_dialog.get_body()
    
    def update_from_config(self, config_item):
        """从配置更新UI"""
        # 更新SMTP服务器
        self.server_input.setText(config_item.get('host', ''))
        
        # 更新SMTP端口
        self.port_input.setText(str(config_item.get('port', '465')))
        
        # 更新邮箱账号
        self.username_input.setText(config_item.get('sender', ''))
        
        # 更新邮箱密码
        self.password_input.setText(config_item.get('password', ''))
        
        # 更新警报等级
        alert_level = config_item.get('alert_level', 0)
        radio_buttons = self.alert_level_group.buttons()
        if 0 <= alert_level < len(radio_buttons):
            radio_buttons[alert_level].setChecked(True)
        
        # 保存收件人和正文设置
        self.recipients = config_item.get('receivers', [])
        self.body_format = config_item.get('format', {})
    
    def get_config(self):
        """获取当前配置"""
        # 获取警报等级
        alert_level = 0
        for i, button in enumerate(self.alert_level_group.buttons()):
            if button.isChecked():
                alert_level = i
                break
        
        return {
            'setting': 'mail',
            'host': self.server_input.text(),
            'port': int(self.port_input.text() or 465),
            'sender': self.username_input.text(),
            'password': self.password_input.text(),
            'alert_level': alert_level,
            'receivers': self.recipients,
            'format': self.body_format
        }