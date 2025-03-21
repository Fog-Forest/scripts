def parse_proxy(proxy_config: dict) -> dict:
    """智能解析代理配置"""
    if not proxy_config.get("server"):
        return None

    server = proxy_config["server"]

    # 从URL提取认证信息
    if "@" in server:
        auth_part, server_part = server.split("@", 1)
        username, password = auth_part.split(":", 1)
        return {
            "server": server_part,
            "username": proxy_config.get("username") or username,
            "password": proxy_config.get("password") or password
        }

    return {
        "server": server,
        "username": proxy_config.get("username"),
        "password": proxy_config.get("password")
    }
