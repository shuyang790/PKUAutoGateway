# PKUAutoGateway

用于自动实现PKU网关的检测与连接。

动机在于，补全PKU Helper缺少的功能，实现自动连接与断开，并且在开了全局代理的情况
下照常使用。

## 注意

只测试过macOS下的情况，Linux下可能需要做相应的小改动。

## 特点

- 后台自动连接；
- 连接过多时自动断开之前本机占用的连接；
- 全局代理下也能正常使用（区别于PKU Helper）。

## 配置

- 用户名密码，默认是运行时输入；
- 查询时间间隔(`timeInterval`)，默认20秒;
- 用百度主页来测试联网情况（只获取HEAD）。

## 拓展

个人把它用macOS的Automator包装成一个App，设置后台运行与开机启动。
(<http://stackoverflow.com/questions/6442364/running-script-upon-login-mac>)

运行的时候菜单栏上会出来一个旋转的小齿轮，可以看到脚本在执行。
