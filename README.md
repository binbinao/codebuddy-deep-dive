# CodeBuddy Deep Dive

深度学习知识库项目，专注于提供高质量的深度学习学习文档和可视化资源。

## 📚 文档资源

### 核心学习文档

所有文档位于 `docs/` 目录，每个文档都提供 Markdown 和 PDF 格式：

1. **[神经网络激活函数详解](docs/神经网络激活函数详解.md)** ([PDF](docs/神经网络激活函数详解.pdf))
   - 文件大小: 4.52 MB

2. **[深度学习优化器详解](docs/深度学习优化器详解.md)** ([PDF](docs/深度学习优化器详解.pdf))
   - 文件大小: 2.44 MB

3. **[模型编译优化指标详解](docs/模型编译优化指标详解.md)** ([PDF](docs/模型编译优化指标详解.pdf))
   - 文件大小: 2.79 MB

4. **[模型编译优化指标速查表](docs/模型编译优化指标速查表.md)** ([PDF](docs/模型编译优化指标速查表.pdf))
   - 文件大小: 1.38 MB

5. **[AI核心算法全景图](docs/AI核心算法全景图.md)** ([PDF](docs/AI核心算法全景图.pdf))
   - 文件大小: 2.09 MB

6. **[CodeBuddy架构指南](docs/CodeBuddy_架构指南.md)** ([PDF](docs/CodeBuddy_架构指南.pdf))
   - 文件大小: 985 KB

7. **[Spec-Kit指南](docs/Spec-Kit-指南.md)** ([PDF](docs/Spec-Kit-指南.pdf))
   - 文件大小: 484 KB

## 🎨 可视化图表

项目包含丰富的可视化图表资源，位于 `images/` 目录：

- **激活函数图表** (`images/activation_functions/`)
  - 包含18张高质量PNG图表
  - 涵盖Sigmoid、Tanh、ReLU、Leaky ReLU、ELU、GELU、Swish等函数

- **优化器图表** (`images/optimizers/`)
  - 包含6张优化器可视化图表
  - 展示梯度下降、收敛曲线和特性对比

- **模型指标图表** (`images/model_metrics/`)
  - 包含6张模型性能指标图表
  - 涵盖延迟、吞吐量、内存使用等关键指标

## 🚀 快速开始

### 环境设置

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖（如果尚未安装）
pip install weasyprint playwright markdown reportlab matplotlib numpy scipy
playwright install chromium
```

### PDF文档生成

使用内置工具生成PDF文档：

```bash
source .venv/bin/activate
python generate_learning_pdf.py docs/<文档名称>.md

# 示例：生成神经网络激活函数文档的PDF
python generate_learning_pdf.py docs/神经网络激活函数详解.md
```

## 📂 项目结构

```
codebuddy-deep-dive/
├── docs/                           # 学习文档目录（7个核心文档）
│   ├── 神经网络激活函数详解.md + .pdf
│   ├── 深度学习优化器详解.md + .pdf
│   ├── 模型编译优化指标详解.md + .pdf
│   ├── 模型编译优化指标速查表.md + .pdf
│   ├── AI核心算法全景图.md + .pdf
│   ├── CodeBuddy_架构指南.md + .pdf
│   └── Spec-Kit-指南.md + .pdf
├── images/                         # 图表资源目录
│   ├── activation_functions/      # 激活函数图表（18张）
│   ├── optimizers/                # 优化器图表（6张）
│   └── model_metrics/             # 模型指标图表（6张）
├── scripts/                       # 工具脚本目录
│   ├── install_dev_tools.sh       # 开发工具安装脚本
│   └── fix_nodejs.sh              # Node.js环境修复脚本
├── generate_learning_pdf.py        # PDF文档生成主脚本
├── CODEBUDDY.md                   # CodeBuddy开发指南
├── README.md                      # 项目说明文档
├── LICENSE                        # MIT许可证
└── .venv/                         # Python虚拟环境
```

## 🔧 开发工具

项目提供以下开发工具：

- **PDF生成工具** (`generate_learning_pdf.py`): 专业的文档转换工具，支持中英文双语PDF生成
- **环境配置脚本** (`scripts/install_dev_tools.sh`): 一键安装开发环境所需工具
- **环境修复脚本** (`scripts/fix_nodejs.sh`): 解决Node.js环境相关问题

## 📖 文档特色

- **专业内容**: 涵盖深度学习核心概念和算法
- **双语支持**: 完美支持中英文内容展示
- **高质量图表**: 专业级可视化图表资源
- **完整PDF**: 每个文档都提供精美的PDF版本

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 🤝 贡献

欢迎提交Issue和Pull Request来改进文档质量！

---

*项目维护: CodeBuddy团队*  
*最后更新: 2024年12月*
