import json

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor, QBrush

from views.components.title_bar import CustomTitleBar
from views.components.file_selector import FileSelector
from views.components.device_tab import DeviceTab
from views.components.auto_update_tab import AutoUpdateTab
from views.components.api_server_tab import ApiServerTab
from views.components.email_alerts_tab import EmailAlertsTab
from views.dialogs.server import StartDialog
from utils.config_manager import ConfigManager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = ''
        self.config_manager = ConfigManager()
        
        # 初始化窗口属性
        self._setup_window_properties()
        
        # 创建主布局
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        # 添加标题栏
        self.title_bar = CustomTitleBar('路桥卫士服务器管理', self)
        self.main_layout.addWidget(self.title_bar)
        
        # 添加分隔线
        self.block_line = QtWidgets.QLabel('')
        self.main_layout.addWidget(self.block_line)
        
        # 添加文件选择器
        self.file_selector = FileSelector()
        self.main_layout.addLayout(self.file_selector.get_layout())
        
        # 添加配置按钮行
        self._setup_config_buttons()
        
        # 创建标签页容器
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        
        # 添加各标签页
        self.device_tab = DeviceTab()
        self.auto_update_tab = AutoUpdateTab()
        self.api_server_tab = ApiServerTab()
        self.email_alerts_tab = EmailAlertsTab()
        
        self.tab_widget.addTab(self.device_tab, '设备列表')
        self.tab_widget.addTab(self.auto_update_tab, '自动更新数据')
        self.tab_widget.addTab(self.api_server_tab, 'API服务器')
        self.tab_widget.addTab(self.email_alerts_tab, '邮箱警报')
        
        self.main_layout.addWidget(self.tab_widget)
        
        # 添加底部运行按钮
        self._setup_bottom_buttons()
        
        # 设置状态标签
        self._setup_status_label()
        
        # 主布局边距设置
        self.main_layout.setContentsMargins(20, 15, 20, 15)
        
        # 设置动画效果
        self._setup_animation()
        
        # 连接信号槽
        self._connect_signals()

    def _setup_window_properties(self):
        """设置窗口基本属性"""
        self.window().setStyleSheet(u"color:white; border-radius: 5px")
        self.setWindowTitle('路桥卫士服务器管理')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(450, 500)

    def _setup_config_buttons(self):
        """设置配置按钮行"""
        button_layout = QtWidgets.QHBoxLayout()
        
        self.load_config_button = QtWidgets.QPushButton('加载配置')
        self.load_config_button.setStyleSheet("""
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
        
        self.save_config_button = QtWidgets.QPushButton('保存配置')
        self.save_config_button.setStyleSheet("""
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
        
        button_layout.addWidget(self.load_config_button)
        button_layout.addWidget(self.save_config_button)
        self.main_layout.addLayout(button_layout)

    def _setup_bottom_buttons(self):
        """设置底部按钮"""
        bottom_button_layout = QtWidgets.QHBoxLayout()
        
        self.start_button = QtWidgets.QPushButton('运行服务器')
        self.start_button.setStyleSheet("""
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
        
        bottom_button_layout.addWidget(self.start_button)
        self.main_layout.addLayout(bottom_button_layout)

    def _setup_status_label(self):
        """设置状态标签"""
        self.status_label = QtWidgets.QLabel('准备就绪')
        self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt')
        self.status_label.setTextFormat(Qt.PlainText)
        self.status_label.setWordWrap(False)
        self.status_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        self.status_label.setMinimumWidth(200)
        self.status_label.setMaximumHeight(25)
        self.status_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.main_layout.addWidget(self.status_label)

    def _setup_animation(self):
        """设置窗口动画效果"""
        self.anim = QtCore.QPropertyAnimation(self.window(), b'geometry')
        self.anim.setDuration(100)
        x = 550
        y = 200
        self.anim.setStartValue(QtCore.QRect(x, y, 450, 500))
        self.anim.setEndValue(QtCore.QRect(x, y - 50, 450, 500))
        self.anim.start()

    def _connect_signals(self):
        """连接信号和槽"""
        self.file_selector.file_selected.connect(self.on_file_selected)
        self.load_config_button.clicked.connect(self.load_config)
        self.save_config_button.clicked.connect(self.save_config)
        self.start_button.clicked.connect(self.open_start_dialog)

    def paintEvent(self, event):
        """绘制窗口背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = self.rect()
        color = QColor(255, 255, 255)
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

    def mousePressEvent(self, event):
        """处理鼠标按下事件"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件"""
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def on_file_selected(self, file_path):
        """处理文件选择事件"""
        self.config_path = file_path

    def load_config(self):
        """加载配置文件"""
        file_path = self.file_selector.get_file_path()
        if not file_path:
            self.update_status('错误：未选择配置文件', is_error=True)
            return

        try:
            config = self.config_manager.load_config(file_path)
            self.update_all_tabs(config)
            self.update_status(f'成功加载配置文件：{file_path}')
        except Exception as e:
            self.update_status(f'错误：加载配置文件失败：{e}', is_error=True)

    def save_config(self):
        """保存配置文件"""
        file_path = self.file_selector.get_file_path()
        if not file_path:
            self.update_status('错误：未指定保存路径', is_error=True)
            return

        try:
            config = self.collect_config_from_tabs()
            self.config_manager.save_config(config, file_path)
            self.update_status(f'成功保存配置文件：{file_path}')
        except Exception as e:
            self.update_status(f'错误：保存配置文件失败：{e}', is_error=True)

    def update_all_tabs(self, config):
        """更新所有标签页的内容"""
        for item in config:
            setting = item.get('setting')
            if setting == 'device_list':
                self.device_tab.update_from_config(item)
            elif setting == 'request_cycle':
                self.auto_update_tab.update_from_config(item)
            elif setting == 'api':
                self.api_server_tab.update_from_config(item)
            elif setting == 'mail':
                self.email_alerts_tab.update_from_config(item)

    def collect_config_from_tabs(self):
        """从所有标签页收集配置数据"""
        config = []
        config.append(self.device_tab.get_config())
        config.append(self.auto_update_tab.get_config())
        config.append(self.api_server_tab.get_config())
        config.append(self.email_alerts_tab.get_config())
        return config

    def update_status(self, message, is_error=False):
        """更新状态标签信息"""
        self.status_label.setText(message)
        if is_error:
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; color: #ffffff')
        else:
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; color: #ffffff')

    def open_start_dialog(self):
        """打开服务器启动对话框"""
        config_path = self.file_selector.get_file_path()
        
        if not config_path:
            self.update_status('错误：未选择配置文件，无法启动服务器', is_error=True)
            return
        
        try:
            # 启动服务器对话框
            self.dlg = StartDialog(config_path=config_path)
            self.dlg.exec()
        except Exception as e:
            self.update_status(f'启动服务器失败：{str(e)}', is_error=True)