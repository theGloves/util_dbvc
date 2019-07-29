import os

work_dir = "db_vc"

def _get_path_work_dir():
    return os.path.join(os.getcwd(), work_dir)

def _get_path_history():
    return os.path.join(os.getcwd(), work_dir, "db_history.json")

def _get_path_sqlscripts():
    return os.path.join(os.getcwd(), work_dir, "sqlscripts")

# 如果文件夹不存在就返回false
def _check_dir_exist():
    dir_path = _get_path_work_dir()
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        # 进一步检查sqlscripts和json是否存在
        dir_sql = _get_path_sqlscripts()
        file_json = _get_path_history()
        if os.path.isdir(dir_sql) and os.path.isfile(file_json):
            return True
    return False
