Lan_info
=======

### 介绍 ###

本工具通过扫描网段内机器的信息，存储到 sqlite数据库中，并提供 web服务来管理信息。

web服务依赖[Flask][f]

### 结构与目录 ###

    .
    ├── data
    │   ├── log\
    │   └── network.db
    ├── scanner
    │   ├── ipmac.py
    │   ├── scan.py
    ├── web
    │   ├── static\
    │   ├── templates\
    │   ├── view.py
    │   └── web.conf
    ├── config.ini
    ├── db.py
    ├── run.py
    ├── runserver.py
    ├── do.bat
    ├── backupDB.bat
    └── schema.sql

* `scanner/` - 扫描网段内机器的信息
* `data/`- 存放数据文件和扫描log
* `web/` - 提供web服务,依赖[Flask][f]
* `config.ini` - 配置文件 
>
    [scan]  
    **dest**            扫描的目标网段  
    **netname** 自动生成的网段名称  
    [db]  
    **path**           数据库文件的相对路径  
    **schema**    数据库表结构文件  
    **abspath**  自动生成的数据库绝对路径
* `db.py` - 数据库操作模块
* `run.py`- 扫描网段并存储信息
* `runserver.py`- 启动http服务，本地测试。
*  `do.bat`- windows下的定时执行脚本
*  `backupDB.bat` - windows下的计划任务执行脚本
*  `schema.sql`- 数据库表结构

### 使用方式 ####











[f]: http://flask.pocoo.org



