# 配置系统

支持多配置文件和优先级的配置系统，使用yaml格式

## 配置文件

1. 默认配置文件

位于项目下的yaml.d文件夹中，按文件名顺序加载，后加载的优先级高

2. 脚本配置文件

位于gfhelper/script下的所有yaml文件

3. 用户配置文件

位于~/.config/gfhelper/config.yaml，优先级最高
