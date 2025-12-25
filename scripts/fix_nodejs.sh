#!/bin/bash

# 专门修复 Node.js 安装问题的脚本
# 针对 TencentOS 和其他 RHEL 系统优化

set -e

# 颜色输出函数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检测操作系统
detect_os() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$NAME
        VER=$VERSION_ID
    elif type lsb_release >/dev/null 2>&1; then
        OS=$(lsb_release -si)
        VER=$(lsb_release -sr)
    fi
    log_info "检测到操作系统: $OS $VER"
}

# 安装 Node.js 的函数
install_nodejs() {
    log_info "开始修复 Node.js 安装..."
    
    # 先卸载可能存在的旧版本
    if command -v node &> /dev/null; then
        log_info "检测到已安装的 Node.js，版本: $(node --version)"
        read -p "是否要卸载现有版本并重新安装？(y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            log_info "卸载现有 Node.js..."
            sudo yum remove -y nodejs npm 2>/dev/null || true
            sudo rm -rf /usr/local/nodejs 2>/dev/null || true
            sudo rm -f /usr/bin/node /usr/bin/npm /usr/bin/npx 2>/dev/null || true
        else
            log_info "跳过重新安装"
            return
        fi
    fi
    
    # 检测系统架构
    ARCH=$(uname -m)
    case $ARCH in
        x86_64) NODE_ARCH="x64" ;;
        aarch64) NODE_ARCH="arm64" ;;
        *) 
            log_error "不支持的系统架构: $ARCH"
            exit 1
            ;;
    esac
    
    log_info "系统架构: $ARCH (Node.js 架构: $NODE_ARCH)"
    
    # 方法1: 直接下载二进制包 (推荐)
    install_from_binary() {
        log_info "方法1: 从官方二进制包安装 Node.js..."
        
        # 创建临时目录
        TMP_DIR="/tmp/nodejs_install_$(date +%s)"
        mkdir -p $TMP_DIR
        cd $TMP_DIR
        
        # 下载 Node.js 18.x LTS 版本
        NODE_VERSION="18.20.4"
        NODE_TAR="node-v${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz"
        
        # 尝试多个下载源
        DOWNLOAD_URLS=(
            "https://mirrors.tuna.tsinghua.edu.cn/nodejs-release/v${NODE_VERSION}/${NODE_TAR}"
            "https://nodejs.org/dist/v${NODE_VERSION}/${NODE_TAR}"
            "https://mirrors.cloud.tencent.com/nodejs-release/v${NODE_VERSION}/${NODE_TAR}"
        )
        
        DOWNLOADED=false
        
        for URL in "${DOWNLOAD_URLS[@]}"; do
            log_info "尝试从 $URL 下载..."
            if curl -fsSL --connect-timeout 10 --max-time 300 "$URL" -o "$NODE_TAR"; then
                DOWNLOADED=true
                break
            else
                log_warning "下载失败，尝试下一个源..."
            fi
        done
        
        if [ "$DOWNLOADED" = false ]; then
            log_error "所有下载源都失败"
            cd - > /dev/null
            rm -rf $TMP_DIR
            return 1
        fi
        
        log_info "解压 Node.js..."
        tar -xf "$NODE_TAR"
        
        # 移动到 /usr/local
        sudo rm -rf /usr/local/nodejs 2>/dev/null || true
        sudo mv node-v${NODE_VERSION}-linux-${NODE_ARCH} /usr/local/nodejs
        
        # 创建符号链接
        sudo ln -sf /usr/local/nodejs/bin/node /usr/bin/node
        sudo ln -sf /usr/local/nodejs/bin/npm /usr/bin/npm
        sudo ln -sf /usr/local/nodejs/bin/npx /usr/bin/npx
        
        # 清理临时文件
        cd - > /dev/null
        rm -rf $TMP_DIR
        
        log_success "Node.js 二进制安装完成"
    }
    
    # 方法2: 使用 EPEL 仓库
    install_from_epel() {
        log_info "方法2: 使用 EPEL 仓库安装 Node.js..."
        
        # 安装 EPEL 仓库
        sudo yum install -y epel-release
        
        # 安装 Node.js
        sudo yum install -y nodejs npm
        
        log_success "Node.js EPEL 安装完成"
    }
    
    # 方法3: 使用 NVM (Node Version Manager)
    install_from_nvm() {
        log_info "方法3: 使用 NVM 安装 Node.js..."
        
        # 安装 NVM
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
        
        # 加载 NVM
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
        [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
        
        # 安装 Node.js 18.x LTS
        nvm install --lts
        nvm use --lts
        nvm alias default 'lts/*'
        
        log_success "Node.js NVM 安装完成"
    }
    
    # 尝试不同的安装方法
    if install_from_binary; then
        log_success "使用二进制包安装成功"
    elif install_from_epel; then
        log_success "使用 EPEL 仓库安装成功"
    elif install_from_nvm; then
        log_success "使用 NVM 安装成功"
    else
        log_error "所有安装方法都失败了"
        exit 1
    fi
    
    # 验证安装
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        NPM_VERSION=$(npm --version)
        log_success "Node.js 安装成功!"
        log_info "Node.js 版本: $NODE_VERSION"
        log_info "NPM 版本: $NPM_VERSION"
        
        # 配置 npm
        log_info "配置 npm 镜像源..."
        npm config set registry https://registry.npmmirror.com/
        
        # 安装常用全局包
        log_info "安装常用全局包..."
        npm install -g yarn pnpm typescript ts-node nodemon
        
        log_success "Node.js 环境配置完成!"
        
        # 显示安装的全局包
        echo
        log_info "已安装的全局包:"
        npm list -g --depth=0 2>/dev/null || log_warning "无法获取全局包列表"
        
    else
        log_error "Node.js 安装验证失败"
        exit 1
    fi
}

# 主函数
main() {
    log_info "Node.js 安装修复脚本"
    echo "========================"
    
    detect_os
    
    # 检查是否为 root 用户
    if [ "$EUID" -eq 0 ]; then
        log_warning "检测到 root 用户，建议使用普通用户运行"
        read -p "是否继续？(y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 0
        fi
    fi
    
    install_nodejs
    
    echo
    log_success "修复完成! 请重新打开终端或运行 'source ~/.bashrc' 以确保环境变量生效。"
}

# 运行主函数
main "$@"