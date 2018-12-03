# DevilYuan股票量化系统
### 简介
DevilYuan股票量化系统由python编写，支持python3.4及以上版本，有如下功能：
- 可视化（基于PyQT的界面）
- 多线程事件引擎
- 四大功能
    - 股票数据
    - 选股
    - 策略回测
    - 实盘交易
- 历史数据均免费来自于网络
    - Wind免费个人接口
    - TuShare(TuSharePro)
    - 通达信
- 实盘微信提醒及交互
- 一键挂机
- 全自动交易
- 模拟交易，支持9个模拟账号
- 实盘和回测共用同一策略代码，支持tick和分钟级别
- 实盘策略编写模板
- 选股策略编写模板
- 自动下载历史数据到MongoDB数据库
    - 股票代码表
    - 交易日数据
    - 个股，指数和ETF历史日线数据
    - 个股和ETF历史分笔数据
- 集成基本的统计功能
- 实盘单账户多策略

### 运行后的界面
![image](https://github.com/moyuanz/DevilYuan/blob/master/docs/main.png)

# 运行前的准备
- 支持的操作系统：Windows 7/8/10
- 安装[Anaconda](https://www.anaconda.com/download/)，python3.4及以上版本 64位版本(32位应该也可以，但没测试过)
- 安装[MongoDB](https://www.mongodb.com/download-center#production)，并将[MongoDB配置为系统服务](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/#configure-a-windows-service-for-mongodb-community-edition)
    -  如果你想下载更多的个股历史分笔数据，建议配备比较大的的硬盘。毛估估，现在一年的全市场个股分笔数据可能有80G左右。
    -  [MogonDB客户端](https://robomongo.org/download)
-  实盘交易
    - 银河证券，由于官网最新版可能做了防程序控制界面，请到[这儿](https://github.com/moyuanz/Box/blob/master/BinaryStar3.2.exe)安装PC客户端
        - 银河证券的客户端需要做如下配置，不然会导致下单时价格出错以及客户端超时锁定
            - 系统设置 > 界面设置: 界面不操作超时时间设为 0
            - 系统设置 > 交易设置: 默认买入价格/买入数量/卖出价格/卖出数量 都设置为 空
            - 同时客户端不能最小化也不能处于精简模式
        - 登录界面设置
            - ![image](https://github.com/moyuanz/DevilYuan/blob/master/docs/trade/yhLoginUI.jpg)
    - 同花顺，由于官网最新版可能做了防程序控制界面，请到[这儿](https://github.com/shidenggui/easytrader/issues/272)安装通用版同花顺
        - 同花顺的xiadan客户端需要做如下配置，不然会导致下单时价格出错以及客户端超时锁定
            - 系统设置 > 界面设置: 界面不操作超时时间设为 0
            - 系统设置 > 交易设置: 默认买入价格/买入数量/卖出价格/卖出数量 都设置为 空
            - 同时客户端不能最小化也不能处于精简模式
        - **运行同花顺交易接口之前，务必先手动启动同花顺下单程序并登录**
- 安装[Wind个人免费Python接口](http://dajiangzhang.com/document) **(可选)**
    - 若不安装Wind接口，股票代码表，交易日数据和历史日线数据将使用TuShare接口。TuShare这一块的数据更新速度比较慢。并且Wind的复权因子数据比较准确，建议安装Wind。但Wind的接口对数据流量有限制。或者你可以使用TuSharePro，请到[这儿](https://tushare.pro/register?reg=124019)注册自己的token。
- 到[Server酱](http://sc.ftqq.com/3.version)注册一个SCKEY，这样实盘时的信号可以微信铃声通知 **(可选)**
- 安装[Vistual Studio社区版](https://www.visualstudio.com/zh-hans/)，并勾选Python插件 **(可选)**
    - 本项目是用VS2017开发的。你可以选择是用VS2017，或者用其他IDE 
- 需要安装的Python包
    - tushare
    - pytdx(由于tushare可能包含老版本的pytdx，请先pip uninstall pytdx，然后再pip install pytdx)
    - pymongo
    - qdarkstyle
    - pytesseract
    - pywinauto
    - talib，请到[这儿](https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib)安装对应的whl版本
    - aiohttp
    - pyqrcode
    - mpl_finance
        - `pip install https://github.com/matplotlib/mpl_finance/archive/master.zip`
    - pypng
    - **PyQt5**
        - 如果你安装的是Anaconda5.3(Python3.7)，并且出现以下错误
        ```
        from PyQt5 import QtCore, QtGui, QtWidgets
        ImportError: DLL load failed: The specified procedure could not be found.
        ```
        请执行`pip install pyqt5`
- VS调试时报异常的包，不调试时不会报错，可选安装
    - datrie
    - crypto
    - gunicorn

# 运行
因为程序需要读写文件，请到DevilYuan目录夹下以管理者权限运行`python DyMainWindow.py`

# 运行后的步骤
1. [配置DevilYuan系统](https://github.com/moyuanz/DevilYuan/blob/master/docs/Config.md)
2. [下载历史数据](https://github.com/moyuanz/DevilYuan/blob/master/docs/data/DownloadHistoryData.md)
3. [写一个实盘策略](https://github.com/moyuanz/DevilYuan/blob/master/docs/trade/WriteATradeStrategy.md)

# 文档
- 架构
    - [股票交易模块](https://github.com/moyuanz/DevilYuan/blob/master/docs/trade/trade_xmind.png)

# 感谢
项目的开发过程中借鉴了如下几个开源项目，向以下项目的作者表示衷心的感谢
- [vnpy](https://github.com/vnpy/vnpy)
- [tushare](https://github.com/waditu/tushare)
- [easyquotation](https://github.com/shidenggui/easyquotation)
- [easytrader](https://github.com/shidenggui/easytrader)
- [wxBot](https://github.com/liuwons/wxBot)

# 交流

QQ群：293368752

# License
MIT

