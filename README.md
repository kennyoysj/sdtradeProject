<h1 style="text-align: center" >flask基础后台服务器</h1>

> 基本的服务器代码提供基本功能以供扩展

---
## 🎉 功能

- [x] flask 定时任务
- [x] flask api 接口
- [x] pymongo 连接
- [x] redis 连接，工具类
- [x] 加密工具类
- [x] 后台常用工具类
- [x] 短信工具类

## 🔄 更新
- 增加了定时任务功能，定时任务增加对HK和A股的处理具体逻辑在scheduler文件夹的SchedulerMethod下面
- 增加了定时任务功能, 定时任务的配置在在scheduler文件夹的SchedulerConfig下面
- 增加了股票技术指标的计算，相关的公式实现在utils下的stockUtil下面

## 环境部署 centos
- 安装python3环境，yum install python3
- 安装mongodb
- 初始化运行环境 pip install -r requirements.txt 
- 运行项目 需要在appBackend.py目录下 运行 sh ./server.sh
- 或者启动命令启动 nohup python -u ./appBackend.py > socket.log 2>&1 &
