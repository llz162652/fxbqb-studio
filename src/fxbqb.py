import math, os, random
from typing import List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def try_load_font(size: int, font_path: Optional[str]=None) -> ImageFont.FreeTypeFont:
    """
    尝试按顺序加载常见中文字体；可传入 font_path 指定自定义字体。
    """
    candidates = []
    if font_path:
        candidates.append(font_path)
    # Windows 常见中文字体
    candidates += [
        r"C:\Windows\Fonts\msyh.ttc",      # 微软雅黑
        r"C:\Windows\Fonts\simhei.ttf",    # 黑体
        r"C:\Windows\Fonts\msyhbd.ttc",    # 微软雅黑Bold
        r"C:\Windows\Fonts\simkai.ttf",    # 楷体
    ]
    # Linux 常见
    candidates += [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]

    last_err = None
    for p in candidates:
        try:
            # .ttc 可能需要指定索引，Pillow 新版通常可自动处理；失败再试 index=0
            try:
                return ImageFont.truetype(p, size=size)
            except Exception:
                return ImageFont.truetype(p, size=size, index=0)
        except Exception as e:
            last_err = e
            continue
    # 兜底：PIL 自带字体（可能不支持中文）
    try:
        return ImageFont.load_default()
    except Exception as e:
        raise last_err or e

def make_linear_gradient(size: Tuple[int,int], colors: Tuple[Tuple[int,int,int], Tuple[int,int,int]], direction: str="vertical")->Image.Image:
    w, h = size
    base = Image.new("RGB", (w, h), colors[0])
    top = Image.new("RGB", (w, h), colors[1])
    mask = Image.new("L", (w, h))
    pm = mask.load()
    for y in range(h):
        for x in range(w):
            if direction == "vertical":
                t = y / max(1, h-1)
            elif direction == "horizontal":
                t = x / max(1, w-1)
            else: # diagonal
                t = (x + y) / max(1, w + h - 2)
            pm[x, y] = int(t * 255)
    return Image.composite(top, base, mask)

def rounded_rectangle(draw: ImageDraw.ImageDraw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_text_center(img: Image.Image, box, text, font,
                     fill=(255,255,255), stroke_width=4, stroke_fill=(0,0,0),
                     shadow=False, shadow_offset=(2,2), shadow_radius=2):
    """
    在 box（左上x1,y1,右下x2,y2）居中绘制单字符文本，带描边与可选阴影。
    """
    draw = ImageDraw.Draw(img)
    x1, y1, x2, y2 = box
    w, h = x2 - x1, y2 - y1

    # 统一用兼容函数测量尺寸
    tw, th = _measure_text(draw, text, font, stroke_width=stroke_width)
    tx = x1 + (w - tw) / 2
    ty = y1 + (h - th) / 2

    if shadow:
        # 用单独图层做柔和阴影（img 应为 RGBA）
        shadow_layer = Image.new("RGBA", img.size, (0,0,0,0))
        sd = ImageDraw.Draw(shadow_layer)
        sd.text((tx + shadow_offset[0], ty + shadow_offset[1]),
                text, font=font, fill=(0,0,0,200),
                stroke_width=stroke_width, stroke_fill=(0,0,0,200))
        shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=shadow_radius))
        img.alpha_composite(shadow_layer)

    draw.text((tx, ty), text, font=font, fill=fill,
              stroke_width=stroke_width, stroke_fill=stroke_fill)

def compute_grid(n: int, mode: str="auto", manual: Optional[str]=None)->Tuple[int,int]:
    """
    返回 (rows, cols)
    mode="auto"：尽量接近正方形
    manual 例："3x3","4x4"...
    """
    if mode != "auto" and manual:
        try:
            r, c = manual.lower().split("x")
            return int(r), int(c)
        except Exception:
            pass
    if n <= 0:
        return 1, 1
    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    return rows, cols

def text_to_chars(text: str, keep_space=False)->List[str]:
    # 去掉空白；可以选择保留空格
    chars = [ch for ch in text if keep_space or (not ch.isspace())]
    return chars

def render_grid(text: str,
                out_path: str,
                grid_mode="auto",
                manual_grid="3x3",
                font_path=None,
                font_size=128,
                cell_size=256,
                margin=40,
                gap=12,
                padding=16,
                bg_type="gradient",
                bg_color1=(66,133,244),
                bg_color2=(244,180,0),
                grad_dir="diagonal",
                cell_radius=32,
                cell_fill=(255,255,255),
                cell_outline=None,
                text_fill=(34,34,34),
                stroke_width=6,
                stroke_fill=(255,255,255),
                shadow=True,
                shadow_offset=(3,3),
                shadow_radius=2,
                keep_space=False,
                split_dir: str=None
                ):
    chars = text_to_chars(text, keep_space=keep_space)
    n = len(chars)
    rows, cols = compute_grid(n, grid_mode, manual_grid)
    W = cols*cell_size + (cols-1)*gap + margin*2
    H = rows*cell_size + (rows-1)*gap + margin*2

    # 背景
    if bg_type == "solid":
        bg = Image.new("RGBA", (W, H), (*bg_color1, 255))
    else:
        g = make_linear_gradient((W, H), (bg_color1, bg_color2), grad_dir)
        bg = Image.new("RGBA", (W, H))
        bg.paste(g, (0,0))

    # 画单元格 + 文字
    font = try_load_font(font_size, font_path=font_path)
    draw = ImageDraw.Draw(bg)
    idx = 0
    boxes = []
    for r in range(rows):
        for c in range(cols):
            x1 = margin + c*(cell_size + gap)
            y1 = margin + r*(cell_size + gap)
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            # cell 背景（圆角）
            rounded_rectangle(draw, (x1, y1, x2, y2), radius=cell_radius, fill=cell_fill, outline=cell_outline, width=2 if cell_outline else 0)
            # 文本盒子（考虑内边距）
            bx1 = x1 + padding
            by1 = y1 + padding
            bx2 = x2 - padding
            by2 = y2 - padding
            boxes.append((bx1, by1, bx2, by2))
            if idx < n:
                draw_text_center(bg, (bx1, by1, bx2, by2), chars[idx], font, fill=text_fill,
                                 stroke_width=stroke_width, stroke_fill=stroke_fill,
                                 shadow=shadow, shadow_offset=shadow_offset, shadow_radius=shadow_radius)
            idx += 1

    # 保存合成大图
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    bg.convert("RGB").save(out_path, "PNG")

    # 可选：拆分小图
    slice_files = []
    if split_dir:
        os.makedirs(split_dir, exist_ok=True)
        idx = 0
        for i, (bx1, by1, bx2, by2) in enumerate(boxes):
            # 从原图裁剪包含整个 cell 的区域（含内边距外观更完整）
            # 改为裁剪 cell 外接框：
            # 需要重新计算 cell 框（不含内边距），所以从 boxes 推回去不方便，这里按网格重算：
            pass
        # 重新按网格裁剪：
        idx = 0
        for r in range(rows):
            for c in range(cols):
                x1 = margin + c*(cell_size + gap)
                y1 = margin + r*(cell_size + gap)
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                tile = bg.crop((x1, y1, x2, y2)).convert("RGB")
                name = f"{idx+1:02d}.png"
                pth = os.path.join(split_dir, name)
                tile.save(pth, "PNG")
                slice_files.append(pth)
                idx += 1
                if idx >= n and (r*cols + c + 1) >= n:
                    # 不强制截满网格；保留空白格，方便朋友圈九宫格
                    pass
    return out_path, slice_files

def _measure_text(draw, text, font, stroke_width=0):
    """
    兼容各版本 Pillow 的文本尺寸测量：
    - 优先用 draw.textbbox（Pillow 8.0+，10+ 推荐）
    - 失败再退回 draw.textsize（老版本）
    - 仍不行就用 font.getbbox
    返回: (tw, th)
    """
    try:
        # Pillow 8.0+ 推荐接口
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font, stroke_width=stroke_width)
        return (right - left, bottom - top)
    except Exception:
        try:
            # 旧接口（在 Pillow 10 里被移除）
            tw, th = draw.textsize(text, font=font, stroke_width=stroke_width)  # 可能报 AttributeError
            return (tw, th)
        except Exception:
            # 最后兜底
            try:
                left, top, right, bottom = font.getbbox(text)
                return (right - left, bottom - top)
            except Exception:
                return (0, 0)