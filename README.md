# 反向拼字表情工坊 (fxbqb-studio)

一句话 → 九宫格/多宫格表情，一键生成。  
本地运行，无需联网，**由 AI 协助开发完成**。

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Local Only](https://img.shields.io/badge/Run-127.0.0.1-lightgrey)
![Made with AI](https://img.shields.io/badge/Made%20with-AI-orange)

> **本地安全运行**：`app.py` 以 `server_name="127.0.0.1"`、`share=False` 启动，仅本机访问，不暴露公网接口；**不调用外部付费 API**。

---

## 目录
- [✨ 特性](#-特性)
- [🖼 预览](#-预览)
- [🧰 环境要求](#-环境要求)
- [🚀 快速开始](#-快速开始)
- [🖥️ 命令行用法（可选）](#️-命令行用法可选)
- [🎛️ 常用参数速查](#️-常用参数速查)
- [🧩 目录结构](#-目录结构)
- [🔤 字体与合规](#-字体与合规)
- [🛠️ 常见问题（FAQ）](#️-常见问题faq)
- [📝 版本与发布](#-版本与发布)
- [🤝 贡献与建议](#-贡献与建议)
- [🤖 AI 协作声明](#-ai-协作声明)
- [📄 许可证](#-许可证)
- [🙏 致谢](#-致谢)

---

## ✨ 特性

- 自动/手动网格：`auto`、`2x2`、`3x3`、`4x4`、`5x5`
- 渐变/纯色背景、圆角卡片、描边/阴影、留白与间距可调
- 同时导出整图与拆分小图（自动打包为 zip）
- **本地网页端 + 命令行** 双模式；**不调用外部付费 API**
- 支持中文字体（本地路径），跨平台可用开源字体

---

## 🖼 预览
![示例：3x3 拼字表情](https://github.com/llz162652/fxbqb-studio/blob/main/examples/demo_grid.png)

---

## 🧰 环境要求
- **Python** 3.9+
- Windows / macOS / Linux（均可本地运行）
- 建议使用虚拟环境（如 venv）

---

## 🚀 快速开始

```bash
# 1) 安装依赖
pip install -r requirements.txt

# 2) 启动本地网页端（推荐）
python app.py
````

* 浏览器将自动打开本地页面（仅 `127.0.0.1` 可访问）。
* 在左侧填写文本与参数，点击「生成」即可在右侧看到合成图，并可下载拆分小图 zip。

> 首次运行前创建 `out/` 目录更清晰（也可由程序自动创建）。

---

## 🖥️ 命令行用法（可选）

```bash
python cli.py --text "你好，今天也要元气满满！" --grid auto --out out/grid.png --split out/slices
# 查看全部参数：
# python cli.py -h
```

---

## 🎛️ 常用参数速查

* `--font "C:\Windows\Fonts\msyh.ttc"` 指定本地字体文件（仅本机使用，**不要**随仓库分发）
* `--grid 3x3` 手动网格；或 `--grid auto` 自动
* `--bg_type gradient|solid`、`--bg_color1 #4285F4`、`--bg_color2 #F4B400`
* `--cell_size 256`、`--font_size 128`、`--margin 40`、`--gap 12`、`--padding 16`
* `--stroke_width 6`、`--shadow` / `--no-shadow`

---

## 🧩 目录结构

```
.
├─ app.py                # 本地网页端（Gradio）
├─ cli.py                # 命令行入口
├─ src/
│  └─ fxbqb.py           # 核心渲染逻辑 (render_grid 等)
├─ requirements.txt      # 依赖
└─ out/                  # 输出图片与 zip（建议加入 .gitignore）
```

---

## 🔤 字体与合规

* 程序**不会分发**任何商用字体文件；如需中文显示，请在界面或命令行**填写本地字体路径**（如 Windows 的 `C:\Windows\Fonts\msyh.ttc`）。
* 若需跨平台打包或发放，建议改用 **开源字体 Noto Sans SC（思源黑体）**（OFL 许可，允许再分发）。
* 建议在 `.gitignore` 中排除字体文件与输出产物。

---

## 🛠️ 常见问题（FAQ）

**Q1：中文不显示或是方块？**
A：在网页端“字体路径”输入框填入本地中文字体路径；或命令行加 `--font "路径\到\字体文件"`。

**Q2：输出太小/太大？**
A：调整 `--cell_size` 与 `--font_size`；同时可微调 `--margin`、`--gap`、`--padding`。

**Q3：只想用命令行，不开网页？**
A：直接运行 `cli.py` 即可；网页端与命令行互不依赖。

**Q4：是否联网，是否会产生费用？**
A：默认**不联网**、**不调用付费 API**；网页仅在本机 `127.0.0.1` 运行。

---

## 📝 版本与发布

* 最新版本请见：[Releases](https://github.com/llz162652/fxbqb-studio/releases)
* 发行包不包含任何第三方商用字体文件

---

## 🤝 贡献与建议

欢迎提交 Issue / PR。为便于评审，请在 PR 描述中**按以下格式列出变更点**：

* **涉及文件/类**
* **新增的方法/函数**
* **修改的方法/函数**
* **新增/修改的变量**
* **行为变化与兼容性影响**

---

## 🤖 AI 协作声明

本项目的代码与文档由 **人工 + AI（GPT）** 协同完成：

* AI：代码框架建议、参数设计、UI 结构、文档草案
* 人工：调试与验证、逻辑整合、性能与兼容性优化

> 本仓库遵循“人机协作”的透明原则：**这确实是 AI 协助开发的项目**。

---

## 📄 许可证

* 代码：**MIT License**
* 生成的图片：归使用者所有
* 禁止将第三方商用字体文件纳入仓库或随发行包分发

---

## 🙏 致谢

* Gradio / Pillow
* 开源字体社区（Noto / 思源系列）
* 所有提供反馈与灵感的朋友

```

---
