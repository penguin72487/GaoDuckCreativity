import os
import importlib
from flask import Blueprint

# 主 Blueprint
api = Blueprint('api', __name__)

# 自動導入 api 資料夾下的所有 Blueprint
current_folder = os.path.dirname(__file__)

for filename in os.listdir(current_folder):
    if filename.endswith(".py") and filename != "__init__.py":
        module_name = f"api.{filename[:-3]}" 
        module = importlib.import_module(module_name)

        # 檢查是否存在 Blueprint，並註冊
        if hasattr(module, "api"):
            print(f"Registering Blueprint from {module_name}")
            api.register_blueprint(module.api)
