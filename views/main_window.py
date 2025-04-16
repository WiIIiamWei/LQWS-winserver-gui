import json

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QBrush

from views.components.title_bar import CustomTitleBar
from views.dialogs.body import MailBodyDialog
from views.dialogs.recipients import MailRecipientsDialog
from views.dialogs.server import StartDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = ''

        # 初始化
        self.window().setStyleSheet(u"color:white; border-radius: 5px")
        self.setWindowTitle('路桥卫士服务器管理')
        self.setWindowFlags(Qt.FramelessWindowHint)  # 隐藏原版标题栏
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 500)
        title_bar = CustomTitleBar('路桥卫士服务器管理', self)
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        main_layout = QtWidgets.QVBoxLayout(centralWidget)

        # Layout - 按钮
        button_layout = QtWidgets.QHBoxLayout()

        load_config_button = QtWidgets.QPushButton('加载配置')
        load_config_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
            QPushButton:hover {
            background:#366ecc;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        # load_config_button.clicked.connect(self.load_config)

        save_config_button = QtWidgets.QPushButton('保存配置')
        save_config_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
            QPushButton:hover {
            background:#366ecc;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        button_layout.addWidget(load_config_button)
        button_layout.addWidget(save_config_button)

        # Layout - 选择配置文件
        file_select_layout = QtWidgets.QHBoxLayout()
        tip_label = QtWidgets.QLabel('配置文件路径：')
        tip_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.config_path = QtWidgets.QLineEdit()
        self.config_path.setPlaceholderText('输入文件路径')
        self.config_path.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; ')
        self.file_select_button = QtWidgets.QPushButton('选择...')
        self.file_select_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        file_select_layout.addWidget(tip_label)
        file_select_layout.addWidget(self.config_path)
        file_select_layout.addWidget(self.file_select_button)
        self.file_select_button.clicked.connect(self.select_file)
        tip_label.setStyleSheet("""
                        QLabel {
                            font-family: Microsoft Yahei;
                            font-size: 10pt;
                            font-weight: bold;
                        }
                    """)

        # 设置项目选择
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')

        # 设备列表 Tab
        device_list_tab = QtWidgets.QWidget()
        device_list_layout = QtWidgets.QVBoxLayout(device_list_tab)

        # 选择设备
        device_select_layout = QtWidgets.QHBoxLayout()
        device_select_label = QtWidgets.QLabel('选择设备：')
        device_select = QtWidgets.QComboBox()
        device_select.addItem('设备1')
        device_select.addItem('设备2')
        device_select.addItem('设备3')
        device_select_layout.addWidget(device_select_label)
        device_select_layout.addWidget(device_select)
        device_list_layout.addLayout(device_select_layout)

        # 添加/删除设备按钮
        add_device_button = QtWidgets.QPushButton('添加设备')
        add_device_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        delete_device_button = QtWidgets.QPushButton('删除设备')
        delete_device_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        device_button_layout = QtWidgets.QHBoxLayout()
        device_button_layout.addWidget(add_device_button)
        device_button_layout.addWidget(delete_device_button)
        device_list_layout.addLayout(device_button_layout)

        # 设备ID
        device_id_layout = QtWidgets.QHBoxLayout()
        device_id_label = QtWidgets.QLabel('设备ID：')
        device_id = QtWidgets.QLineEdit()
        device_id.setPlaceholderText('输入设备ID')
        device_id.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        device_id_layout.addWidget(device_id_label)
        device_id_layout.addWidget(device_id)
        device_list_layout.addLayout(device_id_layout)

        # 设备URL
        device_url_layout = QtWidgets.QHBoxLayout()
        device_url_label = QtWidgets.QLabel('设备URL：')
        device_url = QtWidgets.QLineEdit()
        device_url.setPlaceholderText('输入设备URL')
        device_url.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        device_url_layout.addWidget(device_url_label)
        device_url_layout.addWidget(device_url)
        device_list_layout.addLayout(device_url_layout)

        # 黄色警报阈值
        alert_yellow_layout = QtWidgets.QHBoxLayout()
        alert_yellow_label = QtWidgets.QLabel('黄色警报阈值：')
        alert_yellow = QtWidgets.QLineEdit()
        alert_yellow.setPlaceholderText('输入数字')
        alert_yellow.setValidator(QtGui.QDoubleValidator())
        alert_yellow.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        alert_yellow_layout.addWidget(alert_yellow_label)
        alert_yellow_layout.addWidget(alert_yellow)
        device_list_layout.addLayout(alert_yellow_layout)

        # 橙色警报阈值
        alert_orange_layout = QtWidgets.QHBoxLayout()
        alert_orange_label = QtWidgets.QLabel('橙色警报阈值：')
        alert_orange = QtWidgets.QLineEdit()
        alert_orange.setPlaceholderText('输入数字')
        alert_orange.setValidator(QtGui.QDoubleValidator())
        alert_orange.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        alert_orange_layout.addWidget(alert_orange_label)
        alert_orange_layout.addWidget(alert_orange)
        device_list_layout.addLayout(alert_orange_layout)

        # 红色警报阈值
        alert_red_layout = QtWidgets.QHBoxLayout()
        alert_red_label = QtWidgets.QLabel('红色警报阈值：')
        alert_red = QtWidgets.QLineEdit()
        alert_red.setPlaceholderText('输入数字')
        alert_red.setValidator(QtGui.QDoubleValidator())
        alert_red.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        alert_red_layout.addWidget(alert_red_label)
        alert_red_layout.addWidget(alert_red)
        device_list_layout.addLayout(alert_red_layout)

        tab_widget.addTab(device_list_tab, '设备列表')

        # 自动更新数据 Tab
        auto_update_tab = QtWidgets.QWidget()
        auto_update_layout = QtWidgets.QVBoxLayout(auto_update_tab)
        auto_update_secret_layout = QtWidgets.QHBoxLayout()
        auto_update_secret_label = QtWidgets.QLabel('AccessKeySecret：')
        auto_update_secret = QtWidgets.QLineEdit()
        auto_update_secret.setEchoMode(QtWidgets.QLineEdit.Password)
        auto_update_secret.setPlaceholderText('输入阿里云提供的AccessKeySecret')
        auto_update_secret.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        auto_update_secret_layout.addWidget(auto_update_secret_label)
        auto_update_secret_layout.addWidget(auto_update_secret)
        auto_update_layout.addLayout(auto_update_secret_layout)

        # 增加/减少表格行数
        add_row_button = QtWidgets.QPushButton('添加新字段')
        add_row_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        delete_row_button = QtWidgets.QPushButton('删除字段')
        delete_row_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        row_button_layout = QtWidgets.QHBoxLayout()
        row_button_layout.addWidget(add_row_button)
        row_button_layout.addWidget(delete_row_button)
        auto_update_layout.addLayout(row_button_layout)

        # 表格
        table = QtWidgets.QTableWidget()
        table.setRowCount(5)  # 设置行数
        table.setColumnCount(2)  # 设置列数
        table.setHorizontalHeaderLabels(['字段名', '值'])  # 设置表头

        # 定义字段名和对应值
        fields = ['字段1', '字段2', '字段3', '字段4', '字段5']
        values = ['', '', '', '', '']

        # 填充表格
        for row, (field, value) in enumerate(zip(fields, values)):
            field_item = QtWidgets.QTableWidgetItem(field)
            value_item = QtWidgets.QTableWidgetItem(value)
            table.setItem(row, 0, field_item)
            table.setItem(row, 1, value_item)

        # 允许用户修改表格内容
        table.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)

        # 禁用列宽和列高的修改
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionsClickable(False)
        table.verticalHeader().setSectionsClickable(False)

        # 添加表格到布局，并使其占满剩余空间
        auto_update_layout.addWidget(table)
        auto_update_layout.setStretch(2, 1)

        tab_widget.addTab(auto_update_tab, '自动更新数据')

        # API 服务器 Tab
        api_server_tab = QtWidgets.QWidget()
        api_server_layout = QtWidgets.QVBoxLayout(api_server_tab)
        api_port_layout = QtWidgets.QHBoxLayout()
        api_port_label = QtWidgets.QLabel('API服务器端口：')
        api_port = QtWidgets.QLineEdit()
        api_port.setPlaceholderText('输入端口号')
        api_port.setValidator(QtGui.QIntValidator())
        api_port.setText('5200')
        api_port.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        api_port_layout.addWidget(api_port_label)
        api_port_layout.addWidget(api_port)

        api_access_key_secret_layout = QtWidgets.QHBoxLayout()
        api_access_key_secret_label = QtWidgets.QLabel('AccessKeySecret：')
        api_access_key_secret = QtWidgets.QLineEdit()
        api_access_key_secret.setEchoMode(QtWidgets.QLineEdit.Password)
        api_access_key_secret.setPlaceholderText('输入阿里云提供的AccessKeySecret')
        api_access_key_secret.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        api_access_key_secret_layout.addWidget(api_access_key_secret_label)
        api_access_key_secret_layout.addWidget(api_access_key_secret)

        api_is_enabled_layout = QtWidgets.QHBoxLayout()
        api_is_enabled = QtWidgets.QCheckBox('启用API服务器')
        api_is_enabled.setChecked(True)
        api_is_enabled_layout.addWidget(api_is_enabled)

        api_server_layout.addLayout(api_is_enabled_layout)
        api_server_layout.addLayout(api_port_layout)
        api_server_layout.addLayout(api_access_key_secret_layout)
        tab_widget.addTab(api_server_tab, 'API服务器')

        # 邮箱警报 Tab
        email_alerts_tab = QtWidgets.QWidget()
        email_alerts_layout = QtWidgets.QVBoxLayout(email_alerts_tab)
        email_server_layout = QtWidgets.QHBoxLayout()
        email_server_label = QtWidgets.QLabel('SMTP服务器：')
        email_server = QtWidgets.QLineEdit()
        email_server.setPlaceholderText('输入SMTP服务器地址')
        email_server.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        email_server_layout.addWidget(email_server_label)
        email_server_layout.addWidget(email_server)

        email_port_layout = QtWidgets.QHBoxLayout()
        email_port_label = QtWidgets.QLabel('SMTP端口：')
        email_port = QtWidgets.QLineEdit()
        email_port.setPlaceholderText('输入SMTP端口')
        email_port.setValidator(QtGui.QIntValidator())
        email_port.setText('465')
        email_port.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        email_port_layout.addWidget(email_port_label)
        email_port_layout.addWidget(email_port)

        email_username_layout = QtWidgets.QHBoxLayout()
        email_username_label = QtWidgets.QLabel('邮箱账号：')
        email_username = QtWidgets.QLineEdit()
        email_username.setPlaceholderText('输入邮箱账号')
        email_username.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        email_username_layout.addWidget(email_username_label)
        email_username_layout.addWidget(email_username)

        email_password_layout = QtWidgets.QHBoxLayout()
        email_password_label = QtWidgets.QLabel('邮箱密码：')
        email_password = QtWidgets.QLineEdit()
        email_password.setPlaceholderText('输入邮箱密码')
        email_password.setEchoMode(QtWidgets.QLineEdit.Password)
        email_password.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        email_password_layout.addWidget(email_password_label)
        email_password_layout.addWidget(email_password)

        email_alert_level_layout = QtWidgets.QHBoxLayout()
        email_alert_level_label = QtWidgets.QLabel('警报等级：')
        email_alert_level_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        email_alert_level_layout.addWidget(email_alert_level_label)

        self.alert_level_group = QtWidgets.QButtonGroup(self)
        alert_levels = ['关闭', '黄色警报', '橙色警报', '红色警报']
        for level in alert_levels:
            radio_button = QtWidgets.QRadioButton(level)
            radio_button.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
            self.alert_level_group.addButton(radio_button)
            email_alert_level_layout.addWidget(radio_button)

        # Set default selection
        self.alert_level_group.buttons()[0].setChecked(True)

        # 新窗口 - 收件人设置/正文设置
        email_recipients_layout = QtWidgets.QHBoxLayout()
        email_recipients_button = QtWidgets.QPushButton('收件人设置')
        email_recipients_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        email_recipients_button.clicked.connect(self.open_mail_recipients_dialog)
        email_recipients_layout.addWidget(email_recipients_button)
        email_body_button = QtWidgets.QPushButton('正文设置')
        email_body_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        email_body_button.clicked.connect(self.open_mail_body_dialog)
        email_recipients_layout.addWidget(email_body_button)

        email_alerts_layout.addLayout(email_server_layout)
        email_alerts_layout.addLayout(email_port_layout)
        email_alerts_layout.addLayout(email_username_layout)
        email_alerts_layout.addLayout(email_password_layout)
        email_alerts_layout.addLayout(email_alert_level_layout)
        email_alerts_layout.addLayout(email_recipients_layout)
        tab_widget.addTab(email_alerts_tab, '邮箱警报')

        # Layout - 底部按钮
        bottom_button_layout = QtWidgets.QHBoxLayout()

        start_button = QtWidgets.QPushButton('运行服务器')
        start_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
            QPushButton:hover {
            background:#366ecc;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        start_button.clicked.connect(self.open_start_dialog)

        bottom_button_layout.addWidget(start_button)

        # 创建主 Layout
        main_layout.addWidget(title_bar)
        self.block_line = QtWidgets.QLabel('')
        main_layout.addWidget(self.block_line)
        main_layout.addLayout(file_select_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(tab_widget)
        main_layout.addLayout(bottom_button_layout)
        main_layout.setContentsMargins(20, 15, 20, 15)

        # 状态文字
        self.status_label = QtWidgets.QLabel('准备就绪')
        self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt')
        # 设置文本过长时在末尾显示省略号
        self.status_label.setTextFormat(Qt.PlainText)  # 使用纯文本格式
        self.status_label.setWordWrap(False)  # 不允许换行
        self.status_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        # 设置省略模式为在文本末尾显示省略号
        self.status_label.setMinimumWidth(200)
        self.status_label.setMaximumHeight(25)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        main_layout.addWidget(self.status_label)

        # 启动动画
        self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
        self.anim.setDuration(100)
        x = 550
        y = 200
        self.anim.setStartValue(QtCore.QRect(x, y, 450, 500))
        self.anim.setEndValue(QtCore.QRect(x, y - 50, 450, 500))
        self.anim.start()

        # 为控件设置对象名
        load_config_button.setObjectName('load_config_button')
        self.config_path.setObjectName('config_path')
        device_select.setObjectName('device_select')
        device_id.setObjectName('device_id')
        device_url.setObjectName('device_url')
        alert_yellow.setObjectName('alert_yellow')
        alert_orange.setObjectName('alert_orange')
        alert_red.setObjectName('alert_red')
        auto_update_secret.setObjectName('auto_update_secret')
        table.setObjectName('auto_update_table')
        api_port.setObjectName('api_port')
        api_access_key_secret.setObjectName('api_access_key_secret')
        api_is_enabled.setObjectName('api_is_enabled')
        email_server.setObjectName('email_server')
        email_port.setObjectName('email_port')
        email_username.setObjectName('email_username')
        email_password.setObjectName('email_password')

        # 连接“加载配置”按钮
        load_config_button.clicked.connect(self.load_config)

        # 初始化对话框实例（避免每次点击重新创建）
        self.mail_recipients_dialog = MailRecipientsDialog()
        self.mail_body_dialog = MailBodyDialog()

    def select_file(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, '选择文件', './', 'JSON Files (*.json)')
        self.config_path.setText(file_path[0])

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the rounded rectangle background
        rect = self.rect()
        color = QColor(255, 255, 255)  # Set the desired background color
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def open_mail_recipients_dialog(self):
        if not self.mail_recipients_dialog.isVisible():
            self.mail_recipients_dialog.exec()

    def open_mail_body_dialog(self):
        if not self.mail_body_dialog.isVisible():
            self.mail_body_dialog.exec()

    def open_start_dialog(self):
        self.dlg = StartDialog()
        self.dlg.exec()

    def get_path(self):
        path = self.put_path.text()
        self.path = path.replace('"', '')
        self.path = path.replace('\\', '/')
        self.config_path = self.config_path.text()

    def load_config(self):
        file_path = self.config_path.text()
        if not file_path:
            self.status_label.setText('错误：未选择配置文件')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; color: #ffffff')
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except Exception as e:
            error_msg = f'加载配置文件失败：{e}'
            self.status_label.setText(f'错误：{error_msg}')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; color: #ffffff')
            return

        # 更新界面控件
        self.update_ui_from_config(config)

        # 更新状态文字
        self.status_label.setText(f'成功加载配置文件：{file_path}')
        self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; color: #ffffff')

    def update_ui_from_config(self, config):
        for item in config:
            setting = item.get('setting')
            if setting == 'device_list':
                self.update_device_list(item.get('value', []))
            elif setting == 'request_cycle':
                self.update_auto_update(item)
            elif setting == 'api':
                self.update_api_server(item)
            elif setting == 'mail':
                self.update_email_alerts(item)

    def update_device_list(self, devices):
        device_select = self.findChild(QtWidgets.QComboBox, 'device_select')
        if device_select:
            device_select.clear()
            for device in devices:
                device_select.addItem(device.get('id', ''))
            if devices:
                self.update_device_details(devices[0])

    def update_device_details(self, device):
        device_id = self.findChild(QtWidgets.QLineEdit, 'device_id')
        device_url = self.findChild(QtWidgets.QLineEdit, 'device_url')
        alert_yellow = self.findChild(QtWidgets.QLineEdit, 'alert_yellow')
        alert_orange = self.findChild(QtWidgets.QLineEdit, 'alert_orange')
        alert_red = self.findChild(QtWidgets.QLineEdit, 'alert_red')

        if device_id:
            device_id.setText(device.get('id', ''))
        if device_url:
            device_url.setText(device.get('url', ''))
        if alert_yellow:
            alert_yellow.setText(str(device.get('alert_yellow', '')))
        if alert_orange:
            alert_orange.setText(str(device.get('alert_orange', '')))
        if alert_red:
            alert_red.setText(str(device.get('alert_red', '')))

    def update_auto_update(self, item):
        auto_update_secret = self.findChild(QtWidgets.QLineEdit, 'auto_update_secret')
        if auto_update_secret:
            auto_update_secret.setText(item.get('access-key-secret', ''))

        table = self.findChild(QtWidgets.QTableWidget, 'auto_update_table')
        if table:
            table.setRowCount(0)
            for field in item.get('value', []):
                row = table.rowCount()
                table.insertRow(row)
                for col, (key, value) in enumerate(field.items()):
                    table.setItem(row, 0, QtWidgets.QTableWidgetItem(key))
                    table.setItem(row, 1, QtWidgets.QTableWidgetItem(value))

    def update_api_server(self, item):
        api_port = self.findChild(QtWidgets.QLineEdit, 'api_port')
        if api_port:
            api_port.setText(str(item.get('port', '5200')))

        api_access_key_secret = self.findChild(QtWidgets.QLineEdit, 'api_access_key_secret')
        if api_access_key_secret:
            api_access_key_secret.setText(item.get('access-key-secret', ''))

        api_is_enabled = self.findChild(QtWidgets.QCheckBox, 'api_is_enabled')
        if api_is_enabled:
            api_is_enabled.setChecked(item.get('enabled', True))

    def update_email_alerts(self, item):
        email_server = self.findChild(QtWidgets.QLineEdit, 'email_server')
        if email_server:
            email_server.setText(item.get('host', ''))

        email_port = self.findChild(QtWidgets.QLineEdit, 'email_port')
        if email_port:
            email_port.setText(str(item.get('port', '')))

        email_username = self.findChild(QtWidgets.QLineEdit, 'email_username')
        if email_username:
            email_username.setText(item.get('sender', ''))

        email_password = self.findChild(QtWidgets.QLineEdit, 'email_password')
        if email_password:
            email_password.setText(item.get('password', ''))

        alert_level = item.get('alert_level', 0)
        radio_buttons = self.alert_level_group.buttons()
        if 0 <= alert_level < len(radio_buttons):
            radio_buttons[alert_level].setChecked(True)

        # 更新收件人和正文设置
        self.mail_recipients_dialog.load_recipients(item.get('receivers', []))
        self.mail_body_dialog.load_body(item.get('format', {}))
