#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qianjin-sticker-pack · assemble.py
把生成的多张表情图统一缩放为 240x240 正方形，把中文文案烤进贴纸内部（白字+黑描边），
并拼成预览图。

用法：
  # 默认：文案烤进 240x240 贴纸内部
  python assemble.py --input <生图目录> --output <输出目录> --captions captions.json

  # 只要纯图贴纸（不烤字）
  python assemble.py --input <生图目录> --output <输出目录> --captions captions.json --no-text

  # 自定义网格（如 24 张用 6 列 4 行）
  python assemble.py --input <生图目录> --output <输出目录> --cols 6 --rows 4

输出：
  <output>/pack/        N 张 240x240 PNG（贴纸本体，文案已烤入）
  <output>/preview.png  拼图预览（带序号，便于检查整套效果）
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("缺少依赖 Pillow，请先安装：pip install Pillow")


SIZE = 240              # 最终贴纸边长（正方形）
GAP = 14               # 预览格间距
MARGIN = 24            # 预览图外边距
BG = (255, 255, 255)  # 预览背景（白）
TEXT_FILL = (255, 255, 255, 255)     # 文案字色（白）
TEXT_STROKE = (0, 0, 0, 230)         # 文案描边（近黑）
STROKE_W = 3                          # 描边宽度


def find_font(size: int):
    """优先用系统中文字体（Windows 微软雅黑），找不到回退默认。"""
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc",   # 微软雅黑 Bold（贴纸字更醒目）
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/msyh.ttf",
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simsun.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    try:
        return ImageFont.load_default(size)
    except Exception:
        return ImageFont.load_default()


def square_crop(im: Image.Image) -> Image.Image:
    """居中裁剪到正方形（取短边），再缩到 SIZE。"""
    w, h = im.size
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    im = im.crop((left, top, left + s, top + s))
    return im.resize((SIZE, SIZE), Image.LANCZOS)


def load_images(input_dir, captions):
    """读取输入目录图片，按 captions 顺序（或文件名排序）返回 (name, Image)。"""
    valid = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
    files = [f for f in os.listdir(input_dir) if f.lower().endswith(valid)]
    if not files:
        sys.exit(f"输入目录没有图片：{input_dir}")

    if captions:
        ordered = [k for k in captions.keys() if k in files]
        ordered += sorted([f for f in files if f not in ordered])
    else:
        ordered = sorted(files)

    out = []
    for name in ordered:
        path = os.path.join(input_dir, name)
        im = Image.open(path).convert("RGBA")
        out.append((name, im))
    return out


def fit_font(text: str, max_w: int, start: int = 42, min_size: int = 16):
    """自动缩小字号，使文字宽度（不含描边）<= max_w。"""
    size = start
    while size > min_size:
        f = find_font(size)
        tmp = Image.new("RGBA", (10, 10))
        d = ImageDraw.Draw(tmp)
        bbox = d.textbbox((0, 0), text, font=f)
        if (bbox[2] - bbox[0]) <= max_w:
            return f, bbox
        size -= 2
    return find_font(min_size), None


def bake_caption(im: Image.Image, text: str):
    """把文案烤进 240x240 贴纸内部底部（白字+黑描边，不遮挡主体）。"""
    im = im.convert("RGBA")
    if not text:
        return im
    d = ImageDraw.Draw(im)
    max_w = SIZE - 16
    f, _ = fit_font(text, max_w)
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (SIZE - tw) / 2
    y = SIZE - th - 10 - bbox[1]   # 距底部约 10px
    d.text((x, y), text, font=f, fill=TEXT_FILL, stroke_width=STROKE_W, stroke_fill=TEXT_STROKE)
    return im


def build_preview(items, baked_map, cols, rows):
    """拼预览图：每格 240 主图（已烤字）+ 左上角序号。"""
    n = len(items)
    if rows is None:
        rows = (n + cols - 1) // cols
    cell = SIZE
    W = MARGIN * 2 + cols * cell + (cols - 1) * GAP
    H = MARGIN * 2 + rows * cell + (rows - 1) * GAP
    canvas = Image.new("RGBA", (W, H), BG + (255,))
    d = ImageDraw.Draw(canvas)
    num_font = find_font(20)

    for idx, (name, im) in enumerate(items):
        r = idx // cols
        c = idx % cols
        x = MARGIN + c * (cell + GAP)
        y = MARGIN + r * (cell + GAP)
        thumb = baked_map.get(name, square_crop(im))
        canvas.paste(thumb.convert("RGBA"), (x, y))
        # 序号（左上角小色块 + 白字）
        d.rectangle([x, y, x + 26, y + 22], fill=(0, 0, 0, 180))
        d.text((x + 6, y + 2), str(idx + 1), font=num_font, fill=(255, 255, 255, 255))
    return canvas.convert("RGB")


def main():
    ap = argparse.ArgumentParser(description="qianjin-sticker-pack 拼图/缩放工具")
    ap.add_argument("--input", required=True, help="生图目录（含多张表情图）")
    ap.add_argument("--output", required=True, help="输出目录")
    ap.add_argument("--captions", default=None, help="captions.json 路径（文件名->文案）")
    ap.add_argument("--cols", type=int, default=4, help="预览网格列数（默认4）")
    ap.add_argument("--rows", type=int, default=None, help="预览网格行数（默认自动）")
    ap.add_argument("--no-text", action="store_true", help="不烤字，只输出纯图贴纸")
    args = ap.parse_args()

    output_dir = args.output
    pack_dir = os.path.join(output_dir, "pack")
    os.makedirs(pack_dir, exist_ok=True)

    captions = None
    if args.captions and os.path.exists(args.captions):
        with open(args.captions, "r", encoding="utf-8") as f:
            captions = json.load(f)

    items = load_images(args.input, captions)
    print(f"读取 {len(items)} 张图片")

    # 1) 输出 240x240 贴纸（默认烤字进图内）
    baked_map = {}
    for name, im in items:
        sq = square_crop(im)
        text = (captions or {}).get(name, "")
        if text and not args.no_text:
            sq = bake_caption(sq, text)
        baked_map[name] = sq
        base = os.path.splitext(name)[0]
        sq.save(os.path.join(pack_dir, f"{base}_240.png"), "PNG")
    print(f"已输出 {len(items)} 张 240x240 贴纸 -> {pack_dir}")

    # 2) 拼预览图（用烤好字的贴纸）
    preview = build_preview(items, baked_map, args.cols, args.rows)
    preview_path = os.path.join(output_dir, "preview.png")
    preview.save(preview_path, "PNG")
    print(f"已生成预览图 -> {preview_path}")


if __name__ == "__main__":
    main()
