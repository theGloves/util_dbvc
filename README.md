## db_vc - DataBase Verson Control  
个人使用的辅助工具-数据库版本控制
在迭代开发过程中，时不时会对数据库有修改，但是没有引入版本的概念，着实有些危险
借着实习的机会开发个类似git的小工具，能简单的实现数据库版本的迭代
暂时支持的数据库sdk只有sqlalchemy

### 环境变量 
因为可能部署到容器里，所以工具需要的参数一般通过环境变量传递
SQLALCHEMY_DATABASE_URI - 数据库连接地址，格式：mysql+pymysql://(username):(password)@(database address)/(database name)


### 使用步骤
1. 安装依赖
```
pip install -r requirements.txt
```

2. 初始化
```
python db_vc.py init
```

3. 版本提交
```
python db_vc.py commit (自己定义的版本号)
```

4. 更新到最新的数据库
```
python db_vc.py upgrade
```