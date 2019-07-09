# oa

#### 项目介绍
精简版OA系统


### 一、环境要求
Python版本:3.7
Django版本:2.2.1
其他的版本要求见项目requirements.txt文件 

### 二、初始化环境

1. 拉取项目并安装项目环境依赖包
```
$ git clone https://github.com/iAutoAdmin/oa.git
$ cd oa
$ pip install -r requirements.txt
```

2. 初始化项目
```
$ python manage.py makemigrations
$ python manage.py migrate
```

3. 运行项目
```
python manage.py runserver 0.0.0.0:8000
```

此时根据你的IP地址进行访问即可。

### 三、OA项目说明

