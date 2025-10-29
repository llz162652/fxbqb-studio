import argparse, os
from src.fxbqb import render_grid

def parse():
    ap = argparse.ArgumentParser(description="反向拼字表情包生成器（CLI）")
    ap.add_argument("--text", type=str, required=True, help="要生成的文本")
    ap.add_argument("--grid", type=str, default="auto", help="网格模式：auto 或 手动，如 3x3/4x4/5x5")
    ap.add_argument("--out", type=str, default="out/grid.png", help="合成大图输出路径")
    ap.add_argument("--split", type=str, default=None, help="可选：拆分小图输出目录（如 out/slices）")
    ap.add_argument("--font", type=str, default=None, help="自定义字体路径（如 C:\\Windows\\Fonts\\msyh.ttc）")
    ap.add_argument("--font_size", type=int, default=128)
    ap.add_argument("--cell_size", type=int, default=256)
    ap.add_argument("--margin", type=int, default=40)
    ap.add_argument("--gap", type=int, default=12)
    ap.add_argument("--padding", type=int, default=16)
    ap.add_argument("--bg_type", type=str, default="gradient", choices=["solid","gradient"])
    ap.add_argument("--bg_color1", type=str, default="#4285F4")
    ap.add_argument("--bg_color2", type=str, default="#F4B400")
    ap.add_argument("--grad_dir", type=str, default="diagonal", choices=["horizontal","vertical","diagonal"])
    ap.add_argument("--cell_radius", type=int, default=32)
    ap.add_argument("--cell_fill", type=str, default="#FFFFFF")
    ap.add_argument("--cell_outline", type=str, default=None)
    ap.add_argument("--text_fill", type=str, default="#222222")
    ap.add_argument("--stroke_width", type=int, default=6)
    ap.add_argument("--stroke_fill", type=str, default="#FFFFFF")
    ap.add_argument("--shadow", action="store_true")
    ap.add_argument("--no-shadow", dest="shadow", action="store_false")
    ap.set_defaults(shadow=True)
    ap.add_argument("--shadow_offset", type=str, default="3,3")
    ap.add_argument("--shadow_radius", type=int, default=2)
    ap.add_argument("--keep_space", action="store_true", help="保留空格字符")
    return ap.parse_args()

def hex_to_rgb(s):
    s = s.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s)==6:
        return tuple(int(s[i:i+2],16) for i in (0,2,4))
    raise ValueError("颜色格式必须是 #RRGGBB")

def parse_tuple(s):
    a,b = s.split(",")
    return (int(a), int(b))

if __name__ == "__main__":
    args = parse()
    out, slices = render_grid(
        text=args.text,
        out_path=args.out,
        grid_mode="auto" if "x" not in args.grid else "manual",
        manual_grid=args.grid if "x" in args.grid else "3x3",
        font_path=args.font,
        font_size=args.font_size,
        cell_size=args.cell_size,
        margin=args.margin,
        gap=args.gap,
        padding=args.padding,
        bg_type=args.bg_type,
        bg_color1=hex_to_rgb(args.bg_color1),
        bg_color2=hex_to_rgb(args.bg_color2),
        grad_dir=args.grad_dir,
        cell_radius=args.cell_radius,
        cell_fill=hex_to_rgb(args.cell_fill),
        cell_outline=None if args.cell_outline in (None,"None","none","") else hex_to_rgb(args.cell_outline),
        text_fill=hex_to_rgb(args.text_fill),
        stroke_width=args.stroke_width,
        stroke_fill=hex_to_rgb(args.stroke_fill),
        shadow=args.shadow,
        shadow_offset=parse_tuple(args.shadow_offset),
        shadow_radius=args.shadow_radius,
        keep_space=args.keep_space,
        split_dir=args.split
    )
    print("[OK] 合成大图：", out)
    if slices:
        print("[OK] 小图数量：", len(slices), "目录：", os.path.abspath(args.split))
