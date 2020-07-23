[English](https://github.com/DessertsLab/Sachima/blob/master/README.md)｜[中文简体](https://github.com/DessertsLab/Sachima/blob/master/doc/README_CN.md)｜[中文繁體](https://github.com/DessertsLab/Sachima/blob/master/doc/README_TC.md)

# Sachima
Sachima是一个灵活的用于开发数据驱动应用的框架。它基于MIT开源协议，所有的代码均由python实现。我们创建它的最初目的是因为数据需求变化太快太频繁，因此需要一个可以让数据分析师修改的逻辑直接上线和可视化的工具。

Sachima拥有非常美观的界面和智能的数据分析功能。

你可以选择把Sachima和BI平台[Superset](https://github.com/apache/incubator-superset)或者[sachima-ui](https://github.com/nocmk2/sachima-ui)整合使用。或者使用它生成的api，开发自己的ui。

[![build status](https://img.shields.io/travis/DessertsLab/Sachima/master.svg?style=flat-square&logo=travis)](https://travis-ci.com/DessertsLab/Sachima)
[![dependencies](https://img.shields.io/librariesio/github/DessertsLab/Sachima?style=flat-square)](https://libraries.io/search?q=sachima)
[![chat](https://img.shields.io/gitter/room/DessertsLab/Sachima?color=purple&logo=gitter&style=flat-square)](https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![github code size](https://img.shields.io/github/languages/code-size/DessertsLab/Sachima?color=pink&style=flat-square)]()
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![commit activity](https://img.shields.io/github/commit-activity/w/DessertsLab/Sachima?style=flat-square)](https://github.com/DessertsLab/Sachima/pulse)
[![doc](https://readthedocs.org/projects/sachima/badge/?version=latest&style=flat-square&color=ff69b4)](http://sachima.readthedocs.io/en/latest/?badge=latest)
[![latest](https://img.shields.io/pypi/v/sachima.svg?style=flat-square&logo=python)](https://pypi.python.org/pypi/sachima/)


特性列表
------------------------------------
|特性|预览|描述|
|----|----|----|
|api||把数据逻辑发布成rpc和http的api|
|BI平台整合|![image](https://user-images.githubusercontent.com/7627381/87924280-3c6cb200-cab1-11ea-9330-93cbe5340594.png)|可以在流行的BI平台上使用|
|消息通知发送||可以把数据报告发送到email或者即时通讯工具|
|数据可视化|![image](https://user-images.githubusercontent.com/7627381/87915432-c4988a80-caa4-11ea-96c3-e2f95e1d2017.png)![image](https://user-images.githubusercontent.com/7627381/87915967-68823600-caa5-11ea-9ca5-093a5688e1b0.png)|一键可视化你的数据.
|命令行工具|![image](https://user-images.githubusercontent.com/7627381/87915185-5d7ad600-caa4-11ea-9c03-4847b8a1d1a1.png)![image](https://user-images.githubusercontent.com/7627381/87915290-8c914780-caa4-11ea-8bf7-da54ad63d6b8.png)|方便的命令行工具.|

开始使用
-----------------------------------
First you should have [python](https://www.python.org/downloads/) and [nodejs](https://nodejs.org/en/download/) installed.
Optionally if you already had a python env and you need a separate environment to run Sachima, you should install [virtualenv](https://pypi.org/project/virtualenv/)

Check your installation by run this in command line

``` shell 
python -V
```

``` shell 
node -v
```
> Sometime you need change python to python3 and pip to pip3.

Install sachima by pip

``` python
pip install -U sachima
```

Check sachima version
``` shell
sachima version
```

Cd into your working dir and init Sachima project with example
``` shell
sachima init
```

Update Sachima to latest version and get latest Waffle which is a Sachima frontend development tool.
``` shell
sachima update
```

Run Sachima dev tools
``` shell
sachima run
```
This will start your sachima dev server and display data in Browser. If you had any problem rerun the last step or ask in [Sachima github issues](https://github.com/DessertsLab/Sachima/issues).

Get middleware(WIP)
-----------------------------------

Working with BI platform
-----------------------------------

### Working with superset(WIP)

### Working with schima-ui(WIP)


