# KCPTUN 客户端
client_linux_amd64 为20201010版，注意更新，如需其他版本请手动下载替换
https://github.com/xtaci/kcptun/releases


### 注意文件权限问题
```bash
chmod +x *.sh
chmod +x client_linux_amd64
```

### 添加开机启动
+ Centos 系统：
```bash
chmod +x /etc/rc.d/rc.local && echo "bash /root/kcptunclient/start.sh" >> /etc/rc.d/rc.local
```

+ Ubuntu/Debian 系统:
```bash
chmod +x /etc/rc.local && echo "bash /root/kcptunclient/start.sh" >> /etc/rc.local
```