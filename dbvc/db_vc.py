import os
from json import dump, load

import fire
from .database_update import upgrade
from pretty_logging import pretty_logger

from .utils import work_dir, _get_path_work_dir, _get_path_history, _get_path_sqlscripts, _check_dir_exist

class Db_vc(object):
    def upgrade(self):
        pretty_logger.info("ready to update database to latest version.")
        upgrade()
        
    def init(self):
        pretty_logger.info("ready to init config file.")
        # 检查文件夹是否被创建，如果没有则创建
        if _check_dir_exist() == True:
            pretty_logger.info("already init.")
        else:
            # 依次创建./db_vc、./db_vc/sqlscripts/、./db_vc/db_history.json
            dir_path = _get_path_work_dir()
            dir_sql = _get_path_sqlscripts()
            file_json = _get_path_history()
            init_json = {
                "current_version": "dbvc-0-0",
                "history":{
                    "dbvc-0-0":{
                        "auto": True,
                        "filename": "dbvc-0-0.sql",
                        "prev":"85ca7af0-ae78-11e9-afd6-525400f7cc8d"
                    }
                }
            }
            os.makedirs(dir_path, exist_ok=True)
            os.makedirs(dir_sql, exist_ok=True)
            
            with open(file_json, 'w', encoding='utf-8') as f:
                dump(init_json, f, ensure_ascii=False)
                f.close()
            
            # 保存0-0的sql文件
            sql = '''
CREATE TABLE IF NOT EXISTS `db_version`(
    `version` varchar(64) NOT NULL ,
    PRIMARY KEY (`version`) USING BTREE
);
INSERT INTO db_version (version) values ("85ca7af0-ae78-11e9-afd6-525400f7cc8d");
'''
            with open(os.path.join(dir_sql,"dbvc-0-0.sql"), "w", encoding='utf-8') as f:
                f.write(sql)
                f.close()
            pretty_logger.info("init config success.")

    def commit(self, new_version):
        pretty_logger.info("ready to commit a database version.")
        filename = input("sql scripts file name: ")
        print("please move this file ({}) to ./db_vc/sqlscripts.".format(filename))
        
        # 更新history
        history = None
        with open(_get_path_history(), "r", encoding="utf-8") as f:
            history = load(f)
            
        if history is None:
            pretty_logger.error("init first.")
            return
        
        current_version = history["current_version"]
        history["current_version"] = new_version
        node = {
            new_version:{
                "auto": True,
                "filename": filename,
                "prev": current_version
            }
        }
        history["history"].update(node)
        pretty_logger.debug("{}".format(history))
        with open(_get_path_history(), "w", encoding="utf-8") as f:
            dump(history, f, ensure_ascii=False)
            
    
if __name__ == "__main__":
    vc = Db_vc()
    fire.Fire(vc)