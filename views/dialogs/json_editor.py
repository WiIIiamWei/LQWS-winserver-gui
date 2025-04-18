import json

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtGui import QPainter, QColor, QBrush, Qt

from views.components.title_bar import CustomTitleBar


class LineNumberArea(QtWidgets.QWidget):
    """行号区域小部件"""

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        """提供尺寸建议"""
        return QtCore.QSize(self.editor.line_number_area_width(), 0)

    def paintEvent(self, event):
        """绘制行号"""
        self.editor.line_number_area_paint_event(event)


class CodeEditor(QtWidgets.QPlainTextEdit):
    """扩展QPlainTextEdit，添加行号支持"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 设置等宽字体
        self.setFont(self._get_monospace_font())
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)

        # 创建行号区域
        self.line_number_area = LineNumberArea(self)

        # 连接信号
        self.blockCountChanged.connect(self.update_line_number_area_width)
        self.updateRequest.connect(self.update_line_number_area)

        # 初始化行号区域宽度
        self.update_line_number_area_width(0)

    def _get_monospace_font(self):
        """获取等宽字体"""
        font = QtGui.QFont()

        # 尝试常见等宽字体，优先级从高到低
        font_families = ["Consolas", "Courier New", "DejaVu Sans Mono", "Monospace", "Lucida Console"]

        for family in font_families:
            font.setFamily(family)
            if QtGui.QFontInfo(font).fixedPitch():
                break

        # 确保使用等宽字体，即使上面的字体都不可用
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(10)

        return font

    def line_number_area_width(self):
        """计算行号区域宽度"""
        digits = max(1, len(str(self.blockCount())))
        space = 10 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def update_line_number_area_width(self, _):
        """更新行号区域宽度"""
        self.setViewportMargins(self.line_number_area_width(), 0, 0, 0)

    def update_line_number_area(self, rect, dy):
        """更新行号区域"""
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(0, rect.y(), self.line_number_area.width(), rect.height())

        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    def resizeEvent(self, event):
        """处理窗口大小变化事件"""
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.line_number_area.setGeometry(QtCore.QRect(cr.left(), cr.top(),
                                         self.line_number_area_width(), cr.height()))

    def line_number_area_paint_event(self, event):
        """绘制行号区域内容"""
        painter = QtGui.QPainter(self.line_number_area)

        # 设置背景颜色
        bg_color = QtGui.QColor(45, 45, 45)  # 深灰色背景
        painter.fillRect(event.rect(), bg_color)

        # 获取可见的第一个块
        block = self.firstVisibleBlock()
        block_number = block.blockNumber()

        # 计算块的顶部坐标
        top = round(self.blockBoundingGeometry(block).translated(
                    self.contentOffset()).top())
        bottom = top + round(self.blockBoundingRect(block).height())

        # 使用与编辑器相同的等宽字体
        painter.setFont(self.font())

        # 绘制所有可见行号
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(QtGui.QColor(180, 180, 180))  # 浅灰色文本
                painter.drawText(0, top, self.line_number_area.width()-5,
                                self.fontMetrics().height(),
                                QtCore.Qt.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + round(self.blockBoundingRect(block).height())
            block_number += 1


class JSONEditorDialog(QtWidgets.QDialog):
    """JSON编辑器对话框"""

    def __init__(self, parent=None, json_data=None):
        super().__init__(parent)
        self.setWindowTitle('JSON编辑器')
        # 修改窗口标志，同时保持对话框特性
        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint)
        # 确保窗口保持在前面
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(600, 500)

        # 主布局
        self.layout = QtWidgets.QVBoxLayout(self)

        # 添加标题栏
        title_bar = CustomTitleBar('JSON编辑器', self)  # 修正标题
        self.layout.addWidget(title_bar)

        # 创建JSON编辑区
        self._create_json_editor()

        # 创建操作按钮
        self._create_action_buttons()

        # 连接信号槽
        self._connect_signals()

        # 如果提供了JSON数据，加载它
        if json_data:
            self.set_json(json_data)

    def _create_json_editor(self):
        """创建JSON编辑区"""
        # 添加标签
        json_label = QtWidgets.QLabel('请在下方编辑自动更新数据字段配置：')
        json_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold')
        self.layout.addWidget(json_label)

        # 使用CodeEditor
        self.json_editor = CodeEditor()
        self.json_editor.setPlaceholderText('请输入JSON格式的配置数据...')
        self.json_editor.setObjectName('json_editor')

        # 添加到布局
        self.layout.addWidget(self.json_editor)

    def _create_action_buttons(self):
        """创建操作按钮"""
        button_layout = QtWidgets.QHBoxLayout()

        # 格式化按钮
        self.format_button = QtWidgets.QPushButton('格式化JSON')
        self.format_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        button_layout.addWidget(self.format_button)

        # 验证按钮
        self.validate_button = QtWidgets.QPushButton('验证JSON')
        self.validate_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        button_layout.addWidget(self.validate_button)

        # 重置按钮
        self.reset_button = QtWidgets.QPushButton('重置')
        self.reset_button.setStyleSheet("QPushButton:hover{background:#366ecc;}")
        button_layout.addWidget(self.reset_button)

        self.layout.addLayout(button_layout)

        # 添加状态标签
        self.status_label = QtWidgets.QLabel('')
        self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt;')
        self.layout.addWidget(self.status_label)

        # 添加确定/取消按钮
        dialog_buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        dialog_buttons.accepted.connect(self.accept)
        dialog_buttons.rejected.connect(self.reject)
        dialog_buttons.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
            QPushButton:hover {
            background:#366ecc;
            }
        """)
        self.layout.addWidget(dialog_buttons)

    def _connect_signals(self):
        """连接信号和槽"""
        self.format_button.clicked.connect(self.format_json)
        self.validate_button.clicked.connect(self.validate_json)
        self.reset_button.clicked.connect(self.reset_json)

    def format_json(self):
        """格式化JSON"""
        try:
            # 获取当前文本
            current_text = self.json_editor.toPlainText()

            # 如果文本为空，不执行任何操作
            if not current_text.strip():
                return

            # 解析JSON
            json_data = json.loads(current_text)

            # 重新格式化并设置文本
            formatted_text = json.dumps(json_data, indent=2, ensure_ascii=False)
            self.json_editor.setPlainText(formatted_text)

            # 更新状态
            self.status_label.setText('JSON已格式化')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: green;')
        except json.JSONDecodeError as e:
            # 显示错误信息
            self.status_label.setText(f'JSON格式错误: {str(e)}')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: red;')

    def validate_json(self):
        """验证JSON"""
        try:
            current_text = self.json_editor.toPlainText()

            # 如果文本为空，不执行任何操作
            if not current_text.strip():
                self.status_label.setText('请输入JSON数据')
                self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: orange;')
                return

            # 尝试解析JSON
            json.loads(current_text)

            # 验证成功
            self.status_label.setText('JSON格式有效')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: green;')
        except json.JSONDecodeError as e:
            # 显示错误信息
            self.status_label.setText(f'JSON格式错误: {str(e)}')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: red;')

    def reset_json(self):
        """重置JSON编辑器内容"""
        # 确认对话框
        reply = QtWidgets.QMessageBox.question(
            self, '确认重置', '确定要清空当前编辑的内容吗？',
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.json_editor.clear()
            self.status_label.setText('内容已重置')
            self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 9pt; color: blue;')

    def set_json(self, json_data):
        """设置JSON数据"""
        if json_data:
            formatted_json = json.dumps(json_data, indent=2, ensure_ascii=False)
            self.json_editor.setPlainText(formatted_json)

    def get_json(self):
        """获取JSON数据"""
        try:
            json_text = self.json_editor.toPlainText()
            if json_text.strip():
                return json.loads(json_text)
            return []
        except json.JSONDecodeError:
            return []
        
    def paintEvent(self, event):
        """绘制对话框背景"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 绘制圆角矩形背景
        rect = self.rect()
        color = QColor(50, 50, 50)  # 深色背景
        painter.setBrush(QBrush(color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(rect, 20, 20)

    def mousePressEvent(self, event):
        """处理鼠标按下事件，用于拖动窗口"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """处理鼠标移动事件，用于拖动窗口"""
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
