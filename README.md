# discord-qq-bot

一个能在Discord和QQ之间双向传递消息的Bot

# 概述

运行环境理论上要求Python 3.5+，已在Python 3.6上测试通过。

依赖[discord.py](https://github.com/Rapptz/discord.py)和[qqbot](https://github.com/pandolia/qqbot)

由于我对Python一点基础都没，所以代码乱七八糟的，~~尤其是处理async的时候。~~

~~能跑起来不就行了呗 \#摊手~~

# 环境配置

当然你需要一个Discord bot和一个不用的QQ号。。。QQ号你肯定会自己弄，无需赘述。Discord bot可以参考Discord bot的开发教程获得。

运行以下命令安装依赖：

```
pip install discord.py
pip install qqbot
```

然后请仔细阅读[qqbot的文档](https://github.com/pandolia/qqbot)，先尝试使用qqbot单独登陆你的QQ号以测试性能。记得配置qqbot的相关设置，因为本项目不负责帮你配置这些。

当你确信你的qqbot可以正常工作了，再进行下一步

# 配置设置

项目根目录下已经有一个 *bot-example.cfg* 文件了。此文件是此bot的设置模板。请复制一份并改名为 *bot.cfg* 。请勿在创建此文件之前运行主程序。

模板内容如下：

```
testToken
#
1,
2,
3,
4
#
233,
666
#
Wiki编写组,
中文
#
转发专用群
```

各个大的项目之间使用 ```#``` 进行分割，大项中的小项使用 ```,``` 分割

换行不是必须的，程序在读取的时候会删掉所有回车。不要包含空格（除了名字里的空格），文件最后一行不要是空行。请勿写入注释，因为此文件中的所有文本都会被当作数据处理。文件格式请选用UTF-8 without BOM格式

* *testToken* 是你的Discord bot的Token，如果你的Token中含有 ```#``` 或 ```,``` 的话，请尝试重新生成一个
* *1，2，3，4* 是你要监听的Disocrd频道的ID。当你进入一个频道时，频道ID会显示在网页URL的最后一部分（用 ```/``` 分割）
* *233,666* 表示你将要把QQ消息转发到哪个Discord频道，也是以ID形式提供
* *Wiki编写组,中文* 监听的QQ群的名称
* *转发专用群* 转发Discord信息到哪个QQ群，同样是群名称

**特别注意：本程序采用的是广播形式，这就意味着如果你监听A，转发在B和C，那么消息是永远无法被转发到A的，且会在B和C中各发一份信息。**

配置完成后，保存配置文件即可。

# 运行

运行下面的指令以运行bot：

```
py discord-qq-bot.py
```

当你的屏幕上出现```QQ is ready```和```[Discord] Logged in as```的时候，即表明已经成功运行

如果想要停止运行，按任意键+回车即可。但是由于各种奇怪的原因，有时候进程结束不干净，你可以一路Ctrl+C和回车尝试关闭。你也可以暴力```taskkill```掉所有Python进程...

# 缺点

* 继承[qqbot](https://github.com/pandolia/qqbot)的所有缺点
* 有时候会显示2次Discord登陆信息，怀疑是qqbot作祟
* 会产生2个Python进程，一个是本体，一个是qqbot
* 一定的消息传送延迟