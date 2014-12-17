LANinfo
=======

### 介绍 ###

本工具通过扫描网段内机器的信息，存储到 sqlite数据库中，并提供 web服务来管理信息。

web服务依赖[Flask][f]

### 结构与目录 ###

    .
    ├── data
    │   ├── schema.sql
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
    └── backupDB.bat

* `scanner/` - 扫描网段内机器的信息
* `data/`- 存放数据文件和扫描log
* `web/` - 提供web服务,依赖[Flask][f]
* `config.ini` - 配置文件

    [scan]  
    **dest**    扫描的目标网段   
    [db]  
    **path**    数据库文件的相对路径  
    **schema**  数据库表结构文件  
    **netname** 自动生成的网段名称,也是数据库表名称
    **abspath** 自动生成的数据库绝对路径  

* `db.py` - 数据库操作模块
* `run.py`- 扫描网段并存储信息
* `runserver.py`- 启动http服务，本地测试。
*  `do.bat`- windows下的定时执行脚本
*  `backupDB.bat` - windows下的计划任务执行脚本
*  `data/schema.sql`- 数据库表结构

### 使用方式 ####

1. 根目录下面创建`config.ini`文件，配置如下:

    [scan]  
    dest = 192.168.1.1/24  

    [db]  
    path = data/network.db   
    schema = data/schema.sql  

2. `python run.py` 进行第一次抓取，并初始化数据库.

3. `python runserver.py` 启动服务

### 注意事项 ####

* 需手动将 windows下的定时执行脚本添加到windows计划任务中

* 本抓取工具在 *nix平台上获取远程mac地址是通过系统shell`arp`命令获取的，可能没有 win平台上获取远程MAC地址完整。

* 本工具是多线程抓取的，没有对线程数进行限制，如果线程太多会造成错误。*nix下通过`ulimit -a`查看限制。`ulimit -n [num]`对打开文件数量上限进行修改，`ulimit -u [num]`对用户最大线程数进行修改。

    以上都是需要改进的地方

[f]: http://flask.pocoo.org



