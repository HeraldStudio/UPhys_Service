# UPhys_Service
格物东南微信号后端服务

# 约定
* 数据库中除_id字段外其他字段若存储id，统一使用字符串

# 注意事项
* 从ORM获得的_id均为字符串格式不必进行转换
* 通过ORM写入的_id均为字符串格式，内部进行转换
* ORM.old为废弃，将在后续版本中剔除