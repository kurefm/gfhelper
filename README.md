# GF Helper

> 该项目正在重构中

少女前线护肝片

> 仅支持简中官服，仅支持1080P的设备，暂时只支持Linux



## 出发点

这个工具的出发点是为了减少打捞和练级的精污，而不是一个功能完备的外挂工具。
该工具不会通过任何方式修改或获取游戏数据，只是通过`adb`截图和模拟操作来控制游戏的部分操作

## 安装

1. 克隆本项目
2. 进入项目目录执行`pip install --editable .`


## 功能

1. 封装基本操作可简化编写脚本的工作
1. 脚本执行中断和恢复
1. 多配置文件支持
1. 简单实用的命令行工具

> 以上功能可能因为懒而咕咕咕！！！

## 文档

> 只写了一小部分

1. [设计基础](docs/01-base.md)
2. [命令行](docs/02-cli.md)
3. [配置文件](docs/03-conf.md)
4. API


## 内置脚本

### test

一些开发时的测试命令和工具

```
  test:cv
  test:screenshot  [test] Take a screenshot
  test:test        [test] Developer test
```

### b02
0-2拖尸脚本

```
  b02:auto_battle    [b02] 自动进行一轮战斗
  b02:switch_killer  [b02] 交换打手
  b02:update_killer  [b02] 更新打手的识别hash

```

Tips:
1. 使用前请根据需要修改`gfhelper/script/b02.yaml`中的配置
1. 第一次使用时需要手动将地图缩放的到最小
1. 将打手依次放入第一梯队的打手位置并执行
`gfhelper b02:update_killer killer1`和
`gfhelper b02:update_killer killer2`
1. 首次使用请确保梯队1中的打手补给完成
1. 执行`gfhelper b02:auto_battle`进行自动战斗
1. 打完一轮后执行`gfhelper b02:switch_killer`交换打手

## License

MIT.