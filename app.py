import gradio as gr, os, tempfile, shutil
from src.fxbqb import render_grid

def go(text, grid, font_path, font_size, cell_size, margin, gap, padding,
       bg_type, color1, color2, grad_dir, cell_radius, cell_fill, text_fill,
       stroke_width, stroke_fill, shadow, shadow_offset, shadow_radius, keep_space,
       split_export):
    if not text or len(text.strip())==0:
        return None, None, "请输入文本"

    # 颜色来自 gr.ColorPicker -> '#RRGGBB'
    def hex2rgb(h):
        h=h.lstrip("#")
        return tuple(int(h[i:i+2],16) for i in (0,2,4))

    # 输出到临时文件夹
    tempdir = tempfile.mkdtemp(prefix="fxbqb_")
    out_path = os.path.join(tempdir, "grid.png")
    split_dir = os.path.join(tempdir, "slices") if split_export else None

    out, slices = render_grid(
        text=text,
        out_path=out_path,
        grid_mode="auto" if grid=="auto" else "manual",
        manual_grid=grid if grid!="auto" else "3x3",
        font_path=font_path if font_path and len(font_path.strip())>0 else None,
        font_size=int(font_size),
        cell_size=int(cell_size),
        margin=int(margin),
        gap=int(gap),
        padding=int(padding),
        bg_type=bg_type,
        bg_color1=hex2rgb(color1),
        bg_color2=hex2rgb(color2),
        grad_dir=grad_dir,
        cell_radius=int(cell_radius),
        cell_fill=hex2rgb(cell_fill),
        cell_outline=None,
        text_fill=hex2rgb(text_fill),
        stroke_width=int(stroke_width),
        stroke_fill=hex2rgb(stroke_fill),
        shadow=shadow,
        shadow_offset=tuple(int(x) for x in shadow_offset.split(",")),
        shadow_radius=int(shadow_radius),
        keep_space=keep_space,
        split_dir=split_dir
    )

    zip_path = None
    if split_export and slices:
        # 打包成 zip 供下载
        zip_path = os.path.join(tempdir, "slices.zip")
        import zipfile
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
            for p in slices:
                z.write(p, arcname=os.path.basename(p))
    return out_path, zip_path, "完成"

with gr.Blocks(title="反向拼字表情包生成器") as demo:
    gr.Markdown("## 反向拼字表情包生成器")
    with gr.Row():
        with gr.Column(scale=1):
            text = gr.Textbox(label="输入文本", value="你好，今天也要元气满满！")
            grid = gr.Dropdown(choices=["auto","2x2","3x3","4x4","5x5"], value="auto", label="网格")
            font_path = gr.Textbox(label="字体路径（可留空，Windows 默认尝试 微软雅黑）", value="")
            with gr.Accordion("样式参数", open=False):
                font_size = gr.Slider(64, 256, value=128, step=2, label="字体大小")
                cell_size = gr.Slider(160, 360, value=256, step=2, label="单元格大小")
                margin = gr.Slider(10, 80, value=40, step=1, label="外边距")
                gap = gr.Slider(0, 40, value=12, step=1, label="行列间距")
                padding = gr.Slider(0, 40, value=16, step=1, label="单元格内边距")
                bg_type = gr.Radio(choices=["gradient","solid"], value="gradient", label="背景类型")
                color1 = gr.ColorPicker(value="#4285F4", label="背景颜色1/纯色")
                color2 = gr.ColorPicker(value="#F4B400", label="背景颜色2（渐变）")
                grad_dir = gr.Dropdown(choices=["horizontal","vertical","diagonal"], value="diagonal", label="渐变方向")
                cell_radius = gr.Slider(0, 80, value=32, step=1, label="圆角半径")
                cell_fill = gr.ColorPicker(value="#FFFFFF", label="单元格底色")
                text_fill = gr.ColorPicker(value="#222222", label="文字颜色")
                stroke_width = gr.Slider(0, 12, value=6, step=1, label="描边宽度")
                stroke_fill = gr.ColorPicker(value="#FFFFFF", label="描边颜色")
                shadow = gr.Checkbox(value=True, label="开启阴影")
                shadow_offset = gr.Textbox(value="3,3", label="阴影偏移 (dx,dy)")
                shadow_radius = gr.Slider(0, 10, value=2, step=1, label="阴影模糊半径")
                keep_space = gr.Checkbox(value=False, label="保留空格")
                split_export = gr.Checkbox(value=True, label="同时导出拆分小图（zip）")
            btn = gr.Button("生成", variant="primary")
        with gr.Column(scale=1):
            out_img = gr.Image(label="合成大图（PNG）", interactive=False)
            zip_file = gr.File(label="拆分小图（zip 下载）")
            status = gr.Textbox(label="状态", interactive=False)
    btn.click(go, inputs=[text, grid, font_path, font_size, cell_size, margin, gap, padding,
                          bg_type, color1, color2, grad_dir, cell_radius, cell_fill, text_fill,
                          stroke_width, stroke_fill, shadow, shadow_offset, shadow_radius, keep_space,
                          split_export],
              outputs=[out_img, zip_file, status])
    gr.Markdown("提示：如果中文显示为方块，请在“字体路径”填入 Windows 字体文件，如 `C:\\Windows\\Fonts\\msyh.ttc`。")

if __name__ == "__main__":
    # 仅本机可访问，不开启公网分享
    demo.launch(server_name="127.0.0.1", share=False)
