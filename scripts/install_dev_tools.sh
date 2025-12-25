#!/bin/bash

# 安装主流开发工具的Shell脚本
# 支持 git, uv, python, curl, wget, vim, docker, node.js 等工具

set -e  # 遇到错误时立即退出

# 颜色输出函数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    else
        log_error "无法检测操作系统版本"
        exit 1
    fi
    log_info "检测到操作系统: $OS $VER"
}

# 更新包管理器
update_package_manager() {
    log_info "更新包管理器..."
    case $OS in
        *"Ubuntu"*|*"Debian"*)
            sudo apt update && sudo apt upgrade -y
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
            if command -v dnf &> /dev/null; then
                sudo dnf update -y
            else
                sudo yum update -y
            fi
            ;;
        *"Arch"*)
            sudo pacman -Syu --noconfirm
            ;;
        *)
            log_warning "未知的操作系统，跳过更新"
            ;;
    esac
    log_success "包管理器更新完成"
}

# 安装基础工具
install_basic_tools() {
    log_info "安装基础开发工具..."
    case $OS in
        *"Ubuntu"*|*"Debian"*)
            sudo apt install -y curl wget git vim build-essential cmake make gcc g++ \
                software-properties-common apt-transport-https ca-certificates \
                gnupg lsb-release unzip htop tree
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
            if command -v dnf &> /dev/null; then
                sudo dnf groupinstall -y "Development Tools"
                sudo dnf install -y curl wget git vim cmake make gcc gcc-c++ \
                    unzip htop tree
            else
                sudo yum groupinstall -y "Development Tools"
                sudo yum install -y curl wget git vim cmake make gcc gcc-c++ \
                    unzip htop tree
            fi
            ;;
        *"Arch"*)
            sudo pacman -S --noconfirm base-devel curl wget git vim cmake \
                make gcc unzip htop tree
            ;;
        *)
            log_warning "未知的操作系统，跳过基础工具安装"
            ;;
    esac
    log_success "基础工具安装完成"
}

# 安装 Python
install_python() {
    log_info "安装 Python..."
    
    # 检查是否已安装 Python3
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        log_info "Python3 已安装，版本: $PYTHON_VERSION"
    else
        case $OS in
            *"Ubuntu"*|*"Debian"*)
                sudo apt install -y python3 python3-pip python3-venv python3-dev
                ;;
            *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
                if command -v dnf &> /dev/null; then
                    sudo dnf install -y python3 python3-pip python3-devel
                else
                    sudo yum install -y python3 python3-pip python3-devel
                fi
                ;;
            *"Arch"*)
                sudo pacman -S --noconfirm python python-pip
                ;;
            *)
                log_warning "未知的操作系统，跳过 Python 安装"
                ;;
        esac
    fi
    
    # 升级 pip
    if command -v pip3 &> /dev/null; then
        python3 -m pip install --upgrade pip
        log_success "Python 和 pip 安装/升级完成"
    fi
}

# 安装 uv (现代 Python 包管理器)
install_uv() {
    log_info "安装 uv..."
    if command -v uv &> /dev/null; then
        UV_VERSION=$(uv --version)
        log_info "uv 已安装，版本: $UV_VERSION"
        log_info "更新 uv 到最新版本..."
        uv self update
    else
        log_info "下载并安装 uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        # 添加到 PATH
        export PATH="$HOME/.cargo/bin:$PATH"
        echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.bashrc
        echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc 2>/dev/null || true
    fi
    
    if command -v uv &> /dev/null; then
        log_success "uv 安装完成"
    else
        log_error "uv 安装失败"
    fi
}

# 安装 Docker
install_docker() {
    log_info "安装 Docker..."
    if command -v docker &> /dev/null; then
        DOCKER_VERSION=$(docker --version)
        log_info "Docker 已安装，版本: $DOCKER_VERSION"
    else
        case $OS in
            *"Ubuntu"*|*"Debian"*)
                # 安装 Docker 官方 GPG 密钥
                sudo apt-get install -y ca-certificates curl gnupg
                sudo install -m 0755 -d /etc/apt/keyrings
                curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
                sudo chmod a+r /etc/apt/keyrings/docker.gpg
                
                # 添加 Docker 仓库
                echo \
                    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
                    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
                    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
                
                sudo apt-get update
                sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
                ;;
            *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
                sudo dnf install -y dnf-plugins-core
                sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo
                sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
                ;;
            *)
                log_warning "未知的操作系统，跳过 Docker 安装"
                return
                ;;
        esac
        
        # 启动 Docker 服务
        sudo systemctl start docker
        sudo systemctl enable docker
        
        # 将当前用户添加到 docker 组
        sudo usermod -aG docker $USER
        log_warning "请重新登录以使 docker 组权限生效"
    fi
    
    if command -v docker &> /dev/null; then
        log_success "Docker 安装完成"
    fi
}

# 安装 Node.js (使用 NodeSource)
install_nodejs() {
    log_info "安装 Node.js..."
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        log_info "Node.js 已安装，版本: $NODE_VERSION"
    else
        # 检测系统架构
        ARCH=$(uname -m)
        case $ARCH in
            x86_64) NODE_ARCH="x64" ;;
            aarch64) NODE_ARCH="arm64" ;;
            *) 
                log_error "不支持的系统架构: $ARCH"
                return
                ;;
        esac
        
        log_info "下载 Node.js 18.x LTS 二进制包..."
        
        # 创建临时目录
        TMP_DIR="/tmp/nodejs_install"
        mkdir -p $TMP_DIR
        cd $TMP_DIR
        
        # 下载最新的 Node.js 18.x LTS 版本
        NODE_VERSION="18.20.4"
        NODE_TAR="node-v${NODE_VERSION}-linux-${NODE_ARCH}.tar.xz"
        
        # 使用国内镜像加速下载
        DOWNLOAD_URL="https://mirrors.tuna.tsinghua.edu.cn/nodejs-release/v${NODE_VERSION}/${NODE_TAR}"
        
        log_info "从 ${DOWNLOAD_URL} 下载..."
        
        # 尝试下载
        if curl -fsSL "$DOWNLOAD_URL" -o "$NODE_TAR"; then
            log_info "解压 Node.js..."
            tar -xf "$NODE_TAR"
            
            # 移动到 /usr/local
            sudo mv node-v${NODE_VERSION}-linux-${NODE_ARCH} /usr/local/nodejs
            
            # 创建符号链接
            sudo ln -sf /usr/local/nodejs/bin/node /usr/bin/node
            sudo ln -sf /usr/local/nodejs/bin/npm /usr/bin/npm
            sudo ln -sf /usr/local/nodejs/bin/npx /usr/bin/npx
            
            # 清理临时文件
            rm -rf $TMP_DIR
            
            log_success "Node.js 二进制安装完成"
        else
            log_warning "二进制包下载失败，尝试使用包管理器安装..."
            
            # 备用方案：使用系统包管理器
            case $OS in
                *"Ubuntu"*|*"Debian"*)
                    # 先添加 NodeSource 仓库
                    curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
                    sudo apt-get install -y nodejs
                    ;;
                *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
                    # 对于 RHEL 系系统，使用 EPEL 仓库
                    if command -v dnf &> /dev/null; then
                        sudo dnf install -y epel-release
                        sudo dnf install -y nodejs npm
                    else
                        sudo yum install -y epel-release
                        sudo yum install -y nodejs npm
                    fi
                    ;;
                *)
                    log_warning "未知的操作系统，尝试使用 snap 安装..."
                    if command -v snap &> /dev/null; then
                        sudo snap install node --classic
                    else
                        log_error "无法安装 Node.js，请手动安装"
                        return
                    fi
                    ;;
            esac
        fi
        
        # 返回原目录
        cd - > /dev/null
    fi
    
    if command -v node &> /dev/null; then
        # 安装一些常用的全局包
        log_info "安装 Node.js 全局包..."
        
        # 设置 npm 镜像源为国内镜像
        npm config set registry https://registry.npmmirror.com/
        
        # 安装常用工具
        sudo npm install -g yarn pnpm typescript ts-node nodemon
        
        log_success "Node.js 安装完成"
    else
        log_error "Node.js 安装失败"
    fi
}

# 安装额外的开发工具
install_extra_tools() {
    log_info "安装额外的开发工具..."
    
    # 安装 oh-my-zsh (如果未安装)
    if [ ! -d "$HOME/.oh-my-zsh" ]; then
        log_info "安装 oh-my-zsh..."
        sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    fi
    
    # 安装 delta (更好的 git diff 工具)
    case $OS in
        *"Ubuntu"*|*"Debian"*)
            sudo apt install -y delta
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y git-delta
            fi
            ;;
    esac
    
    # 安装 ripgrep (快速搜索工具)
    case $OS in
        *"Ubuntu"*|*"Debian"*)
            sudo apt install -y ripgrep
            ;;
        *"CentOS"*|*"Red Hat"*|*"Fedora"*|*"TencentOS"*)
            if command -v dnf &> /dev/null; then
                sudo dnf install -y ripgrep
            fi
            ;;
        *"Arch"*)
            sudo pacman -S --noconfirm ripgrep
            ;;
    esac
    
    log_success "额外开发工具安装完成"
}

# 配置环境
setup_environment() {
    log_info "配置开发环境..."
    
    # 创建开发目录
    mkdir -p ~/dev ~/projects ~/tools
    
    # 配置 git (如果未配置)
    if [ -z "$(git config --global user.name)" ]; then
        log_warning "请配置 Git 用户信息:"
        read -p "请输入您的姓名: " git_name
        read -p "请输入您的邮箱: " git_email
        git config --global user.name "$git_name"
        git config --global user.email "$git_email"
        
        # 配置一些有用的 git 设置
        git config --global init.defaultBranch main
        git config --global pull.rebase false
        git config --global core.editor "vim"
        
        log_success "Git 配置完成"
    fi
    
    log_success "开发环境配置完成"
}

# 显示安装摘要
show_summary() {
    log_info "安装完成！以下是已安装工具的版本信息："
    echo
    echo "=== 基础工具 ==="
    command -v git && echo "Git: $(git --version)"
    command -v curl && echo "Curl: $(curl --version | head -n1)"
    command -v wget && echo "Wget: $(wget --version | head -n1)"
    command -v vim && echo "Vim: $(vim --version | head -n1)"
    echo
    echo "=== Python 相关 ==="
    command -v python3 && echo "Python: $(python3 --version)"
    command -v pip3 && echo "Pip: $(pip3 --version)"
    command -v uv && echo "UV: $(uv --version)"
    echo
    echo "=== 容器化 ==="
    command -v docker && echo "Docker: $(docker --version)"
    echo
    echo "=== Node.js 相关 ==="
    command -v node && echo "Node.js: $(node --version)"
    command -v npm && echo "NPM: $(npm --version)"
    command -v yarn && echo "Yarn: $(yarn --version)"
    echo
    echo "=== 其他工具 ==="
    command -v ripgrep && echo "Ripgrep: $(ripgrep --version)"
    command -v delta && echo "Delta: $(delta --version)"
    command -v htop && echo "Htop: $(htop --version)"
    command -v tree && echo "Tree: $(tree --version)"
    echo
    log_success "所有工具安装完成！建议重新启动终端或运行 'source ~/.bashrc' 以确保所有环境变量生效。"
}

# 主函数
main() {
    log_info "开始安装主流开发工具..."
    
    detect_os
    update_package_manager
    install_basic_tools
    install_python
    install_uv
    install_docker
    install_nodejs
    install_extra_tools
    setup_environment
    show_summary
    
    log_success "安装脚本执行完成！"
}

# 检查是否以 root 用户运行
# if [ "$EUID" -eq 0 ]; then
#     log_error "请不要以 root 用户运行此脚本"
#     exit 1
# fi

# 运行主函数
main "$@"