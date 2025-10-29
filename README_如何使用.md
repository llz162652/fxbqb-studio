# 反向拼字表情工坊 (fxbqb-studio)

一句话 → 九宫格/多宫格表情，或**拆分成多张小图**方便逐张发。支持简体中文、描边、投影、纯色/渐变背景、圆角等，一键生成；本地运行、无需外网、不开启公网分享。

## 特性
- 自动/手动网格（3x3/4x4/5x5…）
- 渐变/纯色背景、圆角卡片、描边/阴影
- 支持中文字体（本地路径），不分发字体文件
- CLI 与本地网页端（仅 127.0.0.1）

## 预览
![demo](examples/demo_grid.png)

## 快速开始
```bash
# 方式 A：CLI
pip install -r requirements.txt
python cli.py --text "你好，今天也要元气满满！" --grid auto --out out/grid.png --split out/slices

# 方式 B：Web（Gradio）
pip install -r requirements.txt
python app.py  # 浏览器自动打开
```

## 功能特点
- 自动计算网格（默认 √N，尽量接近正方形）或手动选择 2x2 / 3x3 / 4x4 / 5x5
- 字体自动探测（Windows 优先使用微软雅黑）；可传入自定义字体路径
- 文本描边/阴影、圆角、边距、单元格内边距、行列间距
- 背景样式：纯色、线性渐变（水平/垂直/对角）
- 输出：合成大图；可选**拆分导出**每个格子的 PNG 到文件夹
- 完全离线运行

## 进阶参数（CLI）
```bash
python cli.py --help
```
会显示全部参数说明，例如：字体大小、描边宽度/颜色、阴影大小/偏移、背景类型/颜色等。

## 目录结构
```
.
├─ app.py                 # Gradio 网页端
├─ cli.py                 # 命令行
├─ src/
│   └─ fxbqb.py          # 核心逻辑（绘制/布局/导出）
├─ examples/
│   ├─ demo_grid.png     # 示例大图
│   └─ demo_slices/      # 示例小图（部分）
├─ out/                   # 你的输出会到这里
├─ requirements.txt
├─ LICENSE
└─ README.md
```

## License
MIT
