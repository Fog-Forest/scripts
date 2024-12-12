#!/bin/bash
# Income 工具部署脚本(宿主机)
set -e

# 脚本变量
GITHUB_PROXY="https://ghp.ci/"

# 平台信息
DEVICE_ID=$(hostname) # 设备ID(自行定义)
HONEYGAIN_MAIL=""     # Honeygain平台邮箱
HONEYGAIN_PASSWORD="" # Honeygain平台密码
REPOCKET_EMAIL=""     # Repocket平台邮箱
REPOCKET_KEY=""       # Repocket平台Key
PAWNS_MAIL=""         # Pawns平台邮箱
PAWNS_PASSWORD=""     # Pawns平台密码

# 帮助信息
function usage() {
    echo "usage: $(basename "$0") [-h] [-i install] [-x uninstall]"
    echo ""
    echo "Options:"
    echo "  -h, --help                     Show this help message and exit"
    echo "  -i, --install                  Install income software"
    echo "  -x, --uninstall                Uninstall the income software"
    echo ""
    echo "Example usage:"
    echo "curl -sSL https://oss.amogu.cn/linux/deploy/income/deploy-host.sh | bash -s  -- -i"
}

# 解析参数
function parse_parameters() {
    while [[ $# -gt 0 ]]; do
        case $1 in
        -h | --help)
            usage
            exit 0
            ;;
        -i | --install)
            install
            exit 0
            ;;
        -x | --uninstall)
            uninstall
            exit 0
            ;;
        *)
            echo "Unknown argument: $1"
            usage
            exit 1
            ;;
        esac
    done
}

function install() {
    check_system    # 检测系统
    check_glibc     # 检测glibc版本
    check_is_cn     # 检测是否为国内网络
    change_mirror   # 更换软件源
    install_nodejs  # 安装Node.js
    uninstall       # 卸载旧版本
    deploy_software # 部署软件
}

function uninstall() {
    # 移除环境变量
    sed -i '/^# Tool environment variables/,/^export RP_API_KEY=/d' /etc/profile
    source /etc/profile

    # 停止服务
    sync_processes=$(pm2 list | grep sync- | awk '{print $4}')
    if [ ! -z "$sync_processes" ]; then
        echo "$sync_processes" | xargs pm2 stop
        echo "$sync_processes" | xargs pm2 delete
    else
        echo "没有找到以 sync- 开头的进程。"
    fi
    pm2 flush
    pm2 save --force

    # 清理目录
    rm -rf /var/lib/.tools
}

# 系统检测
function check_system() {
    arch=$(uname -m)

    # 检测系统分支
    if [[ -f /etc/redhat-release ]]; then
        release="centos"
    elif [[ -f /etc/openwrt_release ]]; then
        release="openwrt"
    elif cat /etc/issue | grep -q -E -i "debian|buster|bullseye|bookworm"; then
        release="debian"
    elif cat /etc/issue | grep -q -E -i "ubuntu|bionic|focal|jammy|lunar"; then
        release="ubuntu"
    elif cat /etc/issue | grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    elif cat /proc/version | grep -q -E -i "debian"; then
        release="debian"
    elif cat /proc/version | grep -q -E -i "ubuntu"; then
        release="ubuntu"
    elif cat /proc/version | grep -q -E -i "centos|red hat|redhat"; then
        release="centos"
    elif lsb_release -a | grep -q -E -i "debian|buster|bullseye|bookworm"; then
        release="debian"
    elif lsb_release -a | grep -q -E -i "ubuntu|bionic|focal|jammy|lunar"; then
        release="ubuntu"
    else
        echo "不受支持或未知的操作系统分支，退出..."
        exit 1
    fi

    # 获取Linux版本
    if [[ -s /etc/redhat-release ]]; then
        version=$(grep -oE "[0-9.]+" /etc/redhat-release | cut -d . -f 1)
    elif [[ -s /etc/openwrt_release ]]; then
        version=$(grep -oE "[0-9.]+" /etc/openwrt_release | cut -d . -f 1 | head -n 1)
    else
        version=$(grep -oE "[0-9.]+" /etc/issue | cut -d . -f 1)
    fi

    # 判断架构并设置标签
    if [ "$arch" == "x86_64" ]; then
        tag="amd64"
    elif [ "$arch" == "aarch64" ]; then
        tag="arm64"
    else
        tag="arm32"
    fi

    # 判断系统是否满足部署要求
    if [[ "$release" == "centos" && "$version" == "7" ]]; then
        echo "您的系统满足安装要求"
    elif [[ "$release" == "debian" || "$release" == "ubuntu" ]]; then
        echo "您的系统满足安装要求"
    else
        echo "您的系统不满足安装要求，退出..."
        exit 1
    fi
}

# 检测glibc版本
check_glibc() {
    glibc_version=$(ldd --version | awk 'NR==1{print $NF}')
    IFS='.' read -r -a version_array <<<"$glibc_version"

    # 判断GLIBC主版本
    if [[ ${version_array[0]} -lt 2 ]]; then
        isGlibc=false
    else
        # 判断GLIBC次版本
        if [[ ${version_array[0]} -eq 2 && ${version_array[1]} -lt 25 ]]; then
            isGlibc=false
        else
            isGlibc=true
        fi
    fi
}

# 境外检测
function check_is_cn() {
    response=$(curl -s ping0.cc/geo)
    if echo "$response" | grep -q "中国"; then
        isCN=true
    else
        isCN=false
    fi
}

# 更换镜像源
function change_mirror() {
    if $isCN; then
        echo "您的系统位于中国，为您更换国内镜像源"
        if [[ "$release" == "centos" && "$version" == "7" ]]; then
            # 对于CentOS 7系统
            bash <(curl -sSL https://linuxmirrors.cn/main.sh) --source mirrors.aliyun.com --protocol https --use-intranet-source false --install-epel true --backup true --upgrade-software false --clean-cache false --ignore-backup-tips
        elif [[ "$release" == "debian" || "$release" == "ubuntu" ]]; then
            # 对于Debian或Ubuntu系统
            bash <(curl -sSL https://linuxmirrors.cn/main.sh) --source mirrors.aliyun.com --protocol https --use-intranet-source false --backup true --upgrade-software false --clean-cache false --ignore-backup-tips
        fi
    else
        echo "您的系统不在中国，无需更换镜像源"
    fi
}

# 安装Node.js和PM2
function install_nodejs() {
    # 检查是否安装了Node.js和PM2
    if command -v node >/dev/null 2>&1 && command -v pm2 >/dev/null 2>&1; then
        echo "Node.js 和 PM2 已安装."
        return
    fi

    if [[ "$release" == "centos" && "$version" == "7" ]]; then
        # 对于CentOS 7系统
        yum install -y nodejs npm
    elif [[ "$release" == "debian" || "$release" == "ubuntu" ]]; then
        # 对于Debian或Ubuntu系统
        apt update
        apt-get install -y nodejs npm
    elif [[ "$release" == "openwrt" ]]; then
        # 对于OpenWrt系统
        opkg update
        opkg install node
        opkg install node-npm
    else
        echo "不受支持或未知的操作系统分支，退出..."
        exit 1
    fi

    # 配置NPM镜像源
    if $isCN; then
        npm config set registry https://registry.npmmirror.com
    fi

    # 安装PM2
    npm install -g pm2
    echo "Node.js 和 PM2 安装完毕."
}

# 部署软件
function deploy_software() {
    # 更新环境变量(Repocket)
    sed -i '/^# Tool environment variables/,/^export RP_API_KEY=/d' /etc/profile
    {
        echo "# Tool environment variables"
        echo "export NODE_ENV=production"
        echo "export RP_EMAIL=$REPOCKET_EMAIL"
        echo "export RP_API_KEY=$REPOCKET_KEY"
    } | tee -a /etc/profile >/dev/null
    source /etc/profile

    # 新建部署目录并进入
    mkdir -p /var/lib/.tools
    cd /var/lib/.tools

    # 开始部署
    deploy_honeygain
    deploy_repocket
    deploy_pawns

    # 设置自启
    pm2 flush
    pm2 startup
    pm2 save --force
}

# Honeygain(Docker&Linux, 对glibc版本有要求)
function deploy_honeygain() {
    if [[ "$release" != "openwrt" && $isGlibc == true ]]; then
        # 移除旧版本
        rm -f sync-hg
        # 下载并安装
        curl -o "sync-hg.tgz" ${GITHUB_PROXY}/https://raw.githubusercontent.com/Fog-Forest/scripts/main/passive-income/software/${tag}/honeygain.tgz
        tar -zxvf sync-hg.tgz
        mv -f honeygain/lib/* /usr/lib/
        mv honeygain/honeygain sync-hg
        rm -rf sync-hg.tgz honeygain
        ldconfig # 更新动态链接库
        chmod +x sync-hg
        pm2 start ./sync-hg --name sync-hg -- -email ${HONEYGAIN_MAIL} -pass ${HONEYGAIN_PASSWORD} -device ${DEVICE_ID}-host -tou-accept
    fi
}

# Repocket(Docker&Linux)
function deploy_repocket() {
    # 移除旧版本
    rm -rf sync-rp
    # 下载并安装
    curl -o "sync-rp.tgz" ${GITHUB_PROXY}/https://raw.githubusercontent.com/Fog-Forest/scripts/main/passive-income/software/${tag}/repocket.tgz
    tar -zxvf sync-rp.tgz
    mv repocket sync-rp
    rm -f sync-rp.tgz
    pm2 start sync-rp/dist/index.js --name sync-rp
}

# Pawns(Docker&Linux)
function deploy_pawns() {
    # 移除旧版本
    rm -rf sync-pa
    # 下载并安装
    curl -o "sync-pa" ${GITHUB_PROXY}/https://raw.githubusercontent.com/Fog-Forest/scripts/main/passive-income/software/${tag}/pawns
    chmod +x sync-pa
    pm2 start ./sync-pa --name sync-pa -- -email=${PAWNS_MAIL} -password=${PAWNS_PASSWORD} -device-name=${DEVICE_ID}-host -accept-tos
}

# 解析参数
parse_parameters "$@"
