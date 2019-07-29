import os
from queue import LifoQueue
from json import loads

from sqlalchemy import create_engine
from pretty_logging import pretty_logger

from utils import work_dir, _get_path_work_dir, _get_path_history, _get_path_sqlscripts, _check_dir_exist

# 起源种子
init_version = "85ca7af0-ae78-11e9-afd6-525400f7cc8d"

def _execute_sql_file(con, filename):
    pretty_logger.info("ready to execute script: {}".format(filename))
    sql_list = []
    with open(filename) as f:
        # 以":"分割
        sql_list = f.read().split(';')[:-1]
        # 将每段sql里的换行符改成空格
        sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list] 
        pretty_logger.debug("read success")
    # 执行sql文件
    for sql_item in sql_list:
        con.execute(sql_item)

def get_update_list(current_version):
    file_list = LifoQueue()
    # 读取json
    js_data = {}
    path_json = _get_path_history()
    with open(path_json) as f:
        js_data = loads(f.read())
    # 找到当前最新版本
    latest = js_data["current_version"]
    pretty_logger.info("lastest db version: {}".format(latest))
    history = js_data["history"]
    
    # 递归遍历
    while latest!=current_version and latest != init_version:
        if history[latest]["auto"]:
            file_list.put((history[latest]["filename"], latest))
        latest = history[latest]["prev"]
    return file_list


def get_version(db_conn):
    try:
        sql = 'select version from db_version'
        res = db_conn.execute(sql).first()
        return res["version"] if res is not None else init_version
    except:
        return init_version


def upgrade():
    database_url = os.getenv("SQLALCHEMY_DATABASE_URI")
    engine=create_engine(database_url)
    db_conn = engine.connect()

    pretty_logger.info("current db version: {}".format(get_version(db_conn)))
    file_list = get_update_list(get_version(db_conn))
    while not file_list.empty():
        files, version = file_list.get()
        filename = os.path.join(_get_path_sqlscripts(), files)
        try:
            _execute_sql_file(db_conn, filename)
            update_sql = 'UPDATE db_version SET version=\"{}\"'.format(version)
            db_conn.execute(update_sql)
            pretty_logger.info("execute {} success".format(filename))
        except Exception as e:
            # 根据版本号的yy，如果yy非0则打印信息，不影响程序运行
            yy = int(version.split("-")[2])
            if yy == 0:
                pretty_logger.error("version: {} sqlfile:{} execute failed. exit.".format(version, files))
                raise e
            else:
                pretty_logger.error("version: {} sqlfile:{} execute failed. please perform if locally.".format(version, files))
    db_conn.close()
    
if __name__ == "__main__":
    upgrade()