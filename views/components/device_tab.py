from PySide6 import QtWidgets, QtGui


class DeviceTab(QtWidgets.QWidget):
    """设备列表标签页"""
    
    def __init__(self):
        super().__init__()
        
        # 创建布局
        self.layout = QtWidgets.QVBoxLayout(self)
        
        # 设备选择器
        self._create_device_selector()
        
        # 添加/删除设备按钮
        self._create_device_buttons()
        
        # 设备详情
        self._create_device_details()
        
        # 存储所有设备信息
        self.devices = []
        
        # 连接信号槽
        self._connect_signals()
    
    def _create_device_selector(self):
        """创建设备选择器"""
        device_select_layout = QtWidgets.QHBoxLayout()
        device_select_label = QtWidgets.QLabel('选择设备：')
        self.device_select = QtWidgets.QComboBox()
        self.device_select.setObjectName('device_select')
        device_select_layout.addWidget(device_select_label)
        device_select_layout.addWidget(self.device_select)
        self.layout.addLayout(device_select_layout)
    
    def _create_device_buttons(self):
        """创建添加/删除设备按钮"""
        device_button_layout = QtWidgets.QHBoxLayout()
        self.add_device_button = QtWidgets.QPushButton('添加设备')
        self.add_device_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        self.delete_device_button = QtWidgets.QPushButton('删除设备')
        self.delete_device_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        device_button_layout.addWidget(self.add_device_button)
        device_button_layout.addWidget(self.delete_device_button)
        self.layout.addLayout(device_button_layout)
    
    def _create_device_details(self):
        """创建设备详情区域"""
        # 设备ID
        device_id_layout = QtWidgets.QHBoxLayout()
        device_id_label = QtWidgets.QLabel('设备ID：')
        self.device_id = QtWidgets.QLineEdit()
        self.device_id.setPlaceholderText('输入设备ID')
        self.device_id.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.device_id.setObjectName('device_id')
        device_id_layout.addWidget(device_id_label)
        device_id_layout.addWidget(self.device_id)
        self.layout.addLayout(device_id_layout)
        
        # 设备URL
        device_url_layout = QtWidgets.QHBoxLayout()
        device_url_label = QtWidgets.QLabel('设备URL：')
        self.device_url = QtWidgets.QLineEdit()
        self.device_url.setPlaceholderText('输入设备URL')
        self.device_url.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.device_url.setObjectName('device_url')
        device_url_layout.addWidget(device_url_label)
        device_url_layout.addWidget(self.device_url)
        self.layout.addLayout(device_url_layout)
        
        # 警报阈值 - 黄色
        alert_yellow_layout = QtWidgets.QHBoxLayout()
        alert_yellow_label = QtWidgets.QLabel('黄色警报阈值：')
        self.alert_yellow = QtWidgets.QLineEdit()
        self.alert_yellow.setPlaceholderText('输入数字')
        self.alert_yellow.setValidator(QtGui.QDoubleValidator())
        self.alert_yellow.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.alert_yellow.setObjectName('alert_yellow')
        alert_yellow_layout.addWidget(alert_yellow_label)
        alert_yellow_layout.addWidget(self.alert_yellow)
        self.layout.addLayout(alert_yellow_layout)
        
        # 警报阈值 - 橙色
        alert_orange_layout = QtWidgets.QHBoxLayout()
        alert_orange_label = QtWidgets.QLabel('橙色警报阈值：')
        self.alert_orange = QtWidgets.QLineEdit()
        self.alert_orange.setPlaceholderText('输入数字')
        self.alert_orange.setValidator(QtGui.QDoubleValidator())
        self.alert_orange.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.alert_orange.setObjectName('alert_orange')
        alert_orange_layout.addWidget(alert_orange_label)
        alert_orange_layout.addWidget(self.alert_orange)
        self.layout.addLayout(alert_orange_layout)
        
        # 警报阈值 - 红色
        alert_red_layout = QtWidgets.QHBoxLayout()
        alert_red_label = QtWidgets.QLabel('红色警报阈值：')
        self.alert_red = QtWidgets.QLineEdit()
        self.alert_red.setPlaceholderText('输入数字')
        self.alert_red.setValidator(QtGui.QDoubleValidator())
        self.alert_red.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.alert_red.setObjectName('alert_red')
        alert_red_layout.addWidget(alert_red_label)
        alert_red_layout.addWidget(self.alert_red)
        self.layout.addLayout(alert_red_layout)
    
    def _connect_signals(self):
        """连接信号和槽函数"""
        self.device_select.currentIndexChanged.connect(self.on_device_selected)
        self.add_device_button.clicked.connect(self.add_device)
        self.delete_device_button.clicked.connect(self.delete_device)
    
    def on_device_selected(self, index):
        """处理设备选择变化"""
        if 0 <= index < len(self.devices):
            self.display_device(self.devices[index])
    
    def display_device(self, device):
        """显示设备详情"""
        self.device_id.setText(device.get('id', ''))
        self.device_url.setText(device.get('url', ''))
        self.alert_yellow.setText(str(device.get('alert_yellow', '')))
        self.alert_orange.setText(str(device.get('alert_orange', '')))
        self.alert_red.setText(str(device.get('alert_red', '')))
    
    def add_device(self):
        """添加新设备"""
        # 首先保存当前设备的更改
        self.save_current_device()
        
        # 创建新设备
        new_device = {
            'id': f'设备{len(self.devices) + 1}',
            'url': '',
            'alert_yellow': '',
            'alert_orange': '',
            'alert_red': ''
        }
        self.devices.append(new_device)
        
        # 更新下拉框
        self.device_select.addItem(new_device['id'])
        self.device_select.setCurrentIndex(len(self.devices) - 1)
    
    def delete_device(self):
        """删除当前设备"""
        current_index = self.device_select.currentIndex()
        if current_index >= 0 and len(self.devices) > 0:
            self.devices.pop(current_index)
            self.device_select.removeItem(current_index)
            
            # 更新显示
            if self.devices:
                new_index = min(current_index, len(self.devices) - 1)
                self.device_select.setCurrentIndex(new_index)
            else:
                self.clear_device_form()
    
    def save_current_device(self):
        """保存当前设备信息"""
        current_index = self.device_select.currentIndex()
        if current_index >= 0 and current_index < len(self.devices):
            device = self.devices[current_index]
            device['id'] = self.device_id.text()
            device['url'] = self.device_url.text()
            device['alert_yellow'] = self.alert_yellow.text()
            device['alert_orange'] = self.alert_orange.text()
            device['alert_red'] = self.alert_red.text()
            
            # 更新下拉框显示的名称
            self.device_select.setItemText(current_index, device['id'])
    
    def clear_device_form(self):
        """清空设备详情表单"""
        self.device_id.clear()
        self.device_url.clear()
        self.alert_yellow.clear()
        self.alert_orange.clear()
        self.alert_red.clear()
    
    def update_from_config(self, config_item):
        """从配置项更新设备列表"""
        devices = config_item.get('value', [])
        self.devices = devices.copy()
        
        # 更新下拉框
        self.device_select.clear()
        for device in self.devices:
            self.device_select.addItem(device.get('id', ''))
        
        # 显示第一个设备
        if self.devices:
            self.device_select.setCurrentIndex(0)
        else:
            self.clear_device_form()
    
    def get_config(self):
        """获取设备配置"""
        # 保存当前设备的更改
        self.save_current_device()
        
        return {
            'setting': 'device_list',
            'value': self.devices
        }