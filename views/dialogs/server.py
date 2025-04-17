import os
import sys
import subprocess
import threading
import time
import psutil
from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPainter, QColor, QBrush


class LogUpdater(QtCore.QObject):
    """日志更新器，用于从服务器进程读取输出并发送信号"""
    log_updated = Signal(str)
    process_ended = Signal()
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        self.running = True
        
    def run(self):
        """在单独线程中运行，读取进程输出"""
        try:
            # 持续读取输出直到进程结束或被标记为停止
            while self.running and self.process and self.process.poll() is None:
                try:
                    # 非阻塞读取一行
                    line = self.process.stdout.readline()
                    if line:
                        self.log_updated.emit(line.decode('utf-8', errors='replace'))
                    else:
                        # 如果没有输出，让线程短暂休眠避免CPU占用
                        time.sleep(0.1)
                except Exception as e:
                    self.log_updated.emit(f"读取输出错误: {str(e)}")
                    break
            
            # 进程已结束，读取剩余输出
            if self.process and self.process.poll() is not None:
                remaining = self.process.stdout.read()
                if remaining:
                    self.log_updated.emit(remaining.decode('utf-8', errors='replace'))
        
        except Exception as e:
            self.log_updated.emit(f"日志监控异常: {str(e)}")
        finally:
            # 通知进程已结束
            self.process_ended.emit()


class ServerTerminator(QtCore.QObject):
    """服务器终止器，用于在单独的线程中停止服务器进程，避免GUI阻塞"""
    termination_status = Signal(str)
    termination_completed = Signal()
    
    def __init__(self, process):
        super().__init__()
        self.process = process
        
    def terminate_process(self):
        """终止进程的方法，在单独线程中运行"""
        try:
            if not self.process or self.process.poll() is not None:
                self.termination_status.emit("进程已经不存在")
                self.termination_completed.emit()
                return
            
            # 获取进程ID
            pid = self.process.pid
            self.termination_status.emit(f"正在终止进程 PID: {pid}...")
            
            # 尝试优雅终止进程及其子进程
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                
                # 首先尝试温和地终止进程
                self.termination_status.emit("正在尝试优雅关闭...")
                
                # 终止子进程
                for child in children:
                    try:
                        child.terminate()
                    except:
                        pass
                
                # 终止主进程
                self.process.terminate()
                
                # 给进程一些时间自行关闭
                gone, alive = psutil.wait_procs([parent] + children, timeout=3)
                
                # 如果有进程仍然存活，强制终止它们
                if alive:
                    self.termination_status.emit("进程未响应，正在强制终止...")
                    for p in alive:
                        try:
                            p.kill()
                        except:
                            pass
                    
                    # 强制杀死主进程
                    if self.process.poll() is None:
                        self.process.kill()
                
                # 等待主进程结束
                self.process.wait(timeout=2)
                
                self.termination_status.emit("进程已成功终止")
                
            except psutil.NoSuchProcess:
                self.termination_status.emit("进程已不存在")
            except Exception as e:
                self.termination_status.emit(f"终止进程时出错: {str(e)}")
                # 最后手段 - 直接强制杀死
                try:
                    if self.process.poll() is None:
                        self.process.kill()
                        self.process.wait(timeout=1)
                        self.termination_status.emit("已强制终止进程")
                except:
                    self.termination_status.emit("无法终止进程，可能需要手动结束")
            
        except Exception as e:
            self.termination_status.emit(f"终止过程发生错误: {str(e)}")
        finally:
            self.termination_completed.emit()


class StartDialog(QtWidgets.QDialog):
    """服务器运行界面"""
    
    def __init__(self, config_path=None):
        super().__init__()
        self.setWindowTitle('服务器运行')
        self.resize(500, 400)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        self.setMinimumSize(QSize(300, 100))
        
        # 保存配置路径
        self.config_path = config_path
        
        # 进程和线程相关变量
        self.process = None
        self.log_thread = None
        self.log_updater = None
        self.terminator_thread = None
        self.server_terminator = None
        
        # 设置UI
        self.setup_ui()
        
        # 启动服务器
        self.start_server()
    
    def setup_ui(self):
        """设置用户界面"""
        # 创建主布局
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        # 添加标题栏
        from views.components.title_bar import CustomTitleBar
        title_bar = CustomTitleBar('服务器运行', self)
        self.main_layout.addWidget(title_bar)
        
        # 日志显示区域
        self.log_display = QtWidgets.QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setStyleSheet('font-family: Consolas, Courier New; font-size: 10pt; color: white; background-color: #1e1e1e;')
        self.main_layout.addWidget(self.log_display)
        
        # 状态标签
        self.status_label = QtWidgets.QLabel("状态: 准备启动")
        self.status_label.setStyleSheet('font-family: Microsoft Yahei; font-size: 10pt; font-weight: bold; color: white;')
        self.main_layout.addWidget(self.status_label)
        
        # 按钮布局
        button_layout = QtWidgets.QHBoxLayout()
        
        # 重启按钮
        self.restart_button = QtWidgets.QPushButton('重启服务器')
        self.restart_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            color: white;
            }
            QPushButton:hover {
            background:#366ecc;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        
        # 停止按钮
        self.stop_button = QtWidgets.QPushButton('停止服务器')
        self.stop_button.setStyleSheet("""
            QPushButton {
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            color: white;
            }
            QPushButton:hover {
            background:#eb4845;
            font-family: Microsoft Yahei;
            font-size: 10pt;
            font-weight: bold;
            }
        """)
        
        # 连接按钮信号
        self.restart_button.clicked.connect(self.restart_server)
        self.stop_button.clicked.connect(self.stop_server)
        
        # 添加按钮到布局
        button_layout.addWidget(self.restart_button)
        button_layout.addWidget(self.stop_button)
        
        # 添加按钮布局到主布局
        self.main_layout.addLayout(button_layout)
        
        # 设置边距
        self.main_layout.setContentsMargins(20, 20, 20, 20)
    
    def start_server(self):
        """启动FastAPI服务器"""
        self.update_status("状态: 正在启动服务器...")
        
        if self.process and self.process.poll() is None:
            self.log_display.append("服务器已在运行中")
            self.update_status("状态: 服务器运行中")
            return
        
        try:
            # 构建命令
            cmd = []
            
            # 使用conda环境中的Python
            if sys.platform == 'win32':
                # Windows 使用 python 直接启动，依赖当前运行环境
                cmd = ['python']
            else:
                # Linux/Mac 直接使用 python
                cmd = ['python']
            
            # 添加脚本路径 - 根据实际路径修改
            server_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'server')
            script_path = os.path.join(server_dir, 'fastapp.py')
            
            # 检查文件是否存在
            if not os.path.exists(script_path):
                self.log_display.append(f"错误: 找不到服务器脚本: {script_path}")
                if not os.path.exists(server_dir):
                    self.log_display.append(f"错误: 服务器目录不存在: {server_dir}")
                    # 尝试列出目录内容
                    parent_dir = os.path.dirname(server_dir)
                    if os.path.exists(parent_dir):
                        self.log_display.append(f"父目录内容: {os.listdir(parent_dir)}")
                self.update_status("状态: 启动失败 - 找不到服务器脚本")
                return
            
            cmd.append(script_path)
            
            # 添加配置文件参数
            if self.config_path:
                cmd.extend(['--config', self.config_path])
            
            # 添加详细日志级别
            cmd.extend(['--verbose', 'DEBUG'])
            
            # 启动服务器进程
            self.log_display.append(f"正在启动服务器...\n命令: {' '.join(cmd)}\n")
            
            # 环境变量设置
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'  # 确保Python输出不缓冲
            
            # 创建进程 - 使用shell=True可以确保在Windows上正确捕获CTRL+C事件
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                stdin=subprocess.PIPE,
                bufsize=0,  # 不缓冲
                universal_newlines=False,
                env=env,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == 'win32' else 0
            )
            
            self.log_display.append(f"服务器进程已启动，PID: {self.process.pid}")
            
            # 创建日志更新器和线程
            self.log_updater = LogUpdater(self.process)
            self.log_updater.log_updated.connect(self.update_log)
            self.log_updater.process_ended.connect(self.on_process_ended)
            
            self.log_thread = QtCore.QThread()
            self.log_updater.moveToThread(self.log_thread)
            self.log_thread.started.connect(self.log_updater.run)
            self.log_thread.start()
            
            self.update_status("状态: 服务器运行中")
            
        except Exception as e:
            self.log_display.append(f"启动服务器时出错: {str(e)}")
            self.update_status("状态: 启动失败")
    
    def stop_server(self):
        """停止服务器并关闭对话框"""
        self.update_status("状态: 正在停止服务器...")
        self.log_display.append("正在停止服务器...")
        
        # 禁用按钮防止重复点击
        self.stop_button.setEnabled(False)
        self.restart_button.setEnabled(False)
        
        if not self.process or self.process.poll() is not None:
            self.log_display.append("服务器已经停止")
            self.update_status("状态: 服务器已停止")
            self.stop_button.setEnabled(True)
            self.restart_button.setEnabled(True)
            return
        
        # 停止日志更新
        if self.log_updater:
            self.log_updater.running = False
        
        # 创建终止器并在单独线程中运行
        self.server_terminator = ServerTerminator(self.process)
        self.server_terminator.termination_status.connect(self.log_display.append)
        self.server_terminator.termination_completed.connect(self.on_termination_completed)
        
        self.terminator_thread = QtCore.QThread()
        self.server_terminator.moveToThread(self.terminator_thread)
        self.terminator_thread.started.connect(self.server_terminator.terminate_process)
        self.terminator_thread.start()
    
    def on_termination_completed(self):
        """当终止进程完成时调用"""
        self.log_display.append("服务器终止操作已完成")
        
        # 重新启用按钮
        self.stop_button.setEnabled(True)
        self.restart_button.setEnabled(True)
        
        # 清理终止器线程
        if self.terminator_thread and self.terminator_thread.isRunning():
            self.terminator_thread.quit()
            self.terminator_thread.wait()
        
        self.update_status("状态: 服务器已停止")
        
        # 清空进程引用
        self.process = None
    
    def on_process_ended(self):
        """当进程自行结束时调用"""
        self.log_display.append("服务器进程已退出")
        self.update_status("状态: 服务器已停止")
        
        # 清空进程引用
        self.process = None
    
    def restart_server(self):
        """重启服务器"""
        self.log_display.append("正在重启服务器...")
        self.update_status("状态: 正在重启服务器...")
        
        # 禁用按钮防止重复点击
        self.stop_button.setEnabled(False)
        self.restart_button.setEnabled(False)
        
        # 如果进程在运行，先停止它
        if self.process and self.process.poll() is None:
            # 创建终止器并连接到重启完成
            self.server_terminator = ServerTerminator(self.process)
            self.server_terminator.termination_status.connect(self.log_display.append)
            self.server_terminator.termination_completed.connect(self.on_restart_termination_completed)
            
            self.terminator_thread = QtCore.QThread()
            self.server_terminator.moveToThread(self.terminator_thread)
            self.terminator_thread.started.connect(self.server_terminator.terminate_process)
            self.terminator_thread.start()
        else:
            # 如果进程没有在运行，直接启动新实例
            self.on_restart_termination_completed()
    
    def on_restart_termination_completed(self):
        """当为重启而终止进程完成时调用"""
        # 清理终止器线程
        if self.terminator_thread and self.terminator_thread.isRunning():
            self.terminator_thread.quit()
            self.terminator_thread.wait()
        
        # 清理日志线程
        if self.log_thread and self.log_thread.isRunning():
            self.log_thread.quit()
            self.log_thread.wait()
        
        # 启动新的服务器实例
        self.process = None  # 确保进程引用被清空
        self.start_server()
        
        # 重新启用按钮
        self.stop_button.setEnabled(True)
        self.restart_button.setEnabled(True)
    
    def update_log(self, text):
        """更新日志显示区域"""
        self.log_display.append(text.rstrip())
        # 滚动到底部
        scrollbar = self.log_display.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def update_status(self, status):
        """更新状态标签"""
        self.status_label.setText(status)
    
    def closeEvent(self, event):
        """处理对话框关闭事件"""
        self.log_display.append("正在关闭窗口，停止服务器...")
        
        # 停止日志更新
        if self.log_updater:
            self.log_updater.running = False
        
        # 终止服务器进程
        if self.process and self.process.poll() is None:
            try:
                # 创建一个阻塞的终止操作
                pid = self.process.pid
                self.log_display.append(f"正在终止进程 PID: {pid}...")
                
                try:
                    # 使用psutil终止进程树
                    parent = psutil.Process(pid)
                    for child in parent.children(recursive=True):
                        try:
                            child.terminate()
                        except:
                            pass
                    
                    self.process.terminate()
                    
                    # 给进程一点时间自行终止
                    time.sleep(0.5)
                    
                    # 如果仍在运行，强制终止
                    if self.process.poll() is None:
                        self.process.kill()
                
                except Exception as e:
                    self.log_display.append(f"终止服务器时出错: {str(e)}")
                    # 如果出错，直接使用kill
                    if self.process.poll() is None:
                        self.process.kill()
            
            except Exception as e:
                self.log_display.append(f"关闭服务器时出错: {str(e)}")
        
        # 清理线程
        if self.log_thread and self.log_thread.isRunning():
            self.log_thread.quit()
            self.log_thread.wait(1000)  # 等待最多1秒
        
        if self.terminator_thread and self.terminator_thread.isRunning():
            self.terminator_thread.quit()
            self.terminator_thread.wait(1000)  # 等待最多1秒
        
        event.accept()
    
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