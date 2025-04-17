import json
import os


class ConfigManager:
    """配置文件管理工具"""
    
    def load_config(self, file_path):
        """
        加载配置文件
        
        Args:
            file_path: 配置文件路径
            
        Returns:
            配置数据字典
        
        Raises:
            FileNotFoundError: 文件不存在
            json.JSONDecodeError: JSON解析错误
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"配置文件不存在: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_config(self, config, file_path):
        """
        保存配置到文件
        
        Args:
            config: 配置数据字典
            file_path: 保存路径
        
        Raises:
            PermissionError: 没有写入权限
        """
        # 确保目录存在
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)