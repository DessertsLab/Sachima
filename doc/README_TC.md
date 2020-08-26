[English](https://github.com/DessertsLab/Sachima/blob/master/README.md)｜[中文簡體](https://github.com/DessertsLab/Sachima/blob/master/doc/README_CN.md)｜[中文繁體](https://github.com/DessertsLab/Sachima/blob/master/doc/README_TC.md)

# Sachima
Sachima是一個靈活的用於開發數據驅動應用的框架。它基於MIT開源協議，所有的代碼均由python實現。我們創建它的最初目的是因為數據需求變化太快太頻繁，因此需要一個可以讓數據分析師修改的邏輯直接上線和可視化的工具。

Sachima擁有非常美觀的界麵和智能的數據分析功能。

你可以選擇把Sachima和BI平臺[Superset](https://github.com/apache/incubator-superset)或者[sachima-ui](https://github.com/nocmk2/sachima-ui)整合使用。或者使用它生成的api，開發自己的ui。

[![build status](https://img.shields.io/travis/DessertsLab/Sachima/master.svg?style=flat-square&logo=travis)](https://travis-ci.com/DessertsLab/Sachima)
[![dependencies](https://img.shields.io/librariesio/github/DessertsLab/Sachima?style=flat-square)](https://libraries.io/search?q=sachima)
[![chat](https://img.shields.io/gitter/room/DessertsLab/Sachima?color=purple&logo=gitter&style=flat-square)](https://gitter.im/sachima-python/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![github code size](https://img.shields.io/github/languages/code-size/DessertsLab/Sachima?color=pink&style=flat-square)]()
[![code style](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/ambv/black)
[![commit activity](https://img.shields.io/github/commit-activity/w/DessertsLab/Sachima?style=flat-square)](https://github.com/DessertsLab/Sachima/pulse)
[![doc](https://readthedocs.org/projects/sachima/badge/?version=latest&style=flat-square&color=ff69b4)](http://sachima.readthedocs.io/en/latest/?badge=latest)
[![latest](https://img.shields.io/pypi/v/sachima.svg?style=flat-square&logo=python)](https://pypi.python.org/pypi/sachima/)


特性列錶
------------------------------------
|特性|預覽|描述|
|----|----|----|
|api||把數據邏輯發佈成rpc和http的api|
|BI平臺整合|![image](https://user-images.githubusercontent.com/7627381/87924280-3c6cb200-cab1-11ea-9330-93cbe5340594.png)|可以在流行的BI平臺上使用|
|消息通知發送||可以把數據報告發送到email或者即時通訊工具|
|數據可視化|![image](https://user-images.githubusercontent.com/7627381/87915432-c4988a80-caa4-11ea-96c3-e2f95e1d2017.png)![image](https://user-images.githubusercontent.com/7627381/87915967-68823600-caa5-11ea-9ca5-093a5688e1b0.png)![heatmap](https://user-images.githubusercontent.com/7627381/89003496-80be4480-d332-11ea-9cf6-c53d80df1377.gif)![44331558-5d2ec600-a49c-11e8-9406-ee71ac94b52c](https://user-images.githubusercontent.com/7627381/89003512-8a47ac80-d332-11ea-9d5d-391cdf67162c.gif)<img width="1082" alt="44331788-083f7f80-a49d-11e8-9fad-5668b53ab954" src="https://user-images.githubusercontent.com/7627381/89003523-90d62400-d332-11ea-86c4-6d10882ddf92.png">![48402607-fcdfb580-e766-11e8-9fe4-68f1a995d4f6](https://user-images.githubusercontent.com/7627381/89003527-9469ab00-d332-11ea-9406-55831eadc1f1.jpg)|一鍵可視化你的數據.
|命令行工具|![image](https://user-images.githubusercontent.com/7627381/87915185-5d7ad600-caa4-11ea-9c03-4847b8a1d1a1.png)![image](https://user-images.githubusercontent.com/7627381/87915290-8c914780-caa4-11ea-8bf7-da54ad63d6b8.png)|方便的命令行工具.|

開始使用
-----------------------------------
首先你需要安裝 [python](https://www.python.org/downloads/).
如果你不想影響到你現有的python環境可以選擇安裝虛擬環境 [virtualenv](https://pypi.org/project/virtualenv/)

通過以下命令檢查你的python是否安裝正確

``` shell 
python -V
```

> 根據你環境的配置你可能需要執行python3和pip3而不是python和pip.

安裝sachima

``` python
pip install -U sachima
```

查看sachima版本

``` shell
sachima version
```

切換到你的工作目錄並初始化sachima項目(默認會自帶例子)

``` shell
sachima init YOUR_PROJ_NAME
```

進入你新創建的Sachima工程目錄
``` shell
cd YOUR_PROJ_NAME
```

運行sachima
``` shell
sachima run
```
這時你的sachima會在命令行啓動並且自動打開瀏覽器展示數據。如果你遇到任何問題可以嘗試重新執行最後一步或者在[Sachima github issues](https://github.com/DessertsLab/Sachima/issues)提問題

更新sachima到最新版本
``` shell
sachima update
```

獲取中間件
-----------------------------------

獲取數據透視錶插件

``` shell
sachima get DessertsLab/pivot_table
```

Working with BI platform
-----------------------------------

### Working with superset(WIP)

### Working with schima-ui(WIP)
