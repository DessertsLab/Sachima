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
|数据可视化|![image](https://user-images.githubusercontent.com/7627381/87915432-c4988a80-caa4-11ea-96c3-e2f95e1d2017.png)![image](https://user-images.githubusercontent.com/7627381/87915967-68823600-caa5-11ea-9ca5-093a5688e1b0.png)![heatmap](https://user-images.githubusercontent.com/7627381/89003496-80be4480-d332-11ea-9cf6-c53d80df1377.gif)![44331558-5d2ec600-a49c-11e8-9406-ee71ac94b52c](https://user-images.githubusercontent.com/7627381/89003512-8a47ac80-d332-11ea-9d5d-391cdf67162c.gif)<img width="1082" alt="44331788-083f7f80-a49d-11e8-9fad-5668b53ab954" src="https://user-images.githubusercontent.com/7627381/89003523-90d62400-d332-11ea-86c4-6d10882ddf92.png">![48402607-fcdfb580-e766-11e8-9fe4-68f1a995d4f6](https://user-images.githubusercontent.com/7627381/89003527-9469ab00-d332-11ea-9406-55831eadc1f1.jpg)|一键可视化你的数据.
|命令行工具|![image](https://user-images.githubusercontent.com/7627381/87915185-5d7ad600-caa4-11ea-9c03-4847b8a1d1a1.png)![image](https://user-images.githubusercontent.com/7627381/87915290-8c914780-caa4-11ea-8bf7-da54ad63d6b8.png)|方便的命令行工具.|

开始使用
-----------------------------------
首先你需要安装 [python](https://www.python.org/downloads/) 和 [nodejs](https://nodejs.org/en/download/).
如果你不想影响到你现有的python环境可以选择安装虚拟环境 [virtualenv](https://pypi.org/project/virtualenv/)

通过以下命令检查你的python和nodejs是否安装正确

``` shell 
python -V
```

``` shell 
node -v
```
> 根据你环境的配置你可能需要执行python3和pip3而不是python和pip.

安装sachima

``` python
pip install -U sachima
```

查看sachima版本

``` shell
sachima version
```

切换到你的工作目录并初始化sachima项目(默认会自带例子)

``` shell
sachima init
```

更新sachima到最新版本并下载Waffle到同级目录
``` shell
sachima update
```

运行sachima
``` shell
sachima run
```
这时你的sachima开发环境的服务会在命令行启动并且自动打开浏览器展示数据。如果你遇到任何问题可以尝试重新执行最后一步或者在[Sachima github issues](https://github.com/DessertsLab/Sachima/issues)提问题

获取中间件
-----------------------------------

获取数据透视表插件

``` shell
sachima get DessertsLab/pivot_table
```

Working with BI platform
-----------------------------------

### Working with superset(WIP)

### Working with schima-ui(WIP)


