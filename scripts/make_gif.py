#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
qianjin-sticker-pack · make_gif.py
把「两张图片」合成一张 240x240 的动态 GIF 表情包。

核心思路：
  读取 img1 / img2 两张图 -> 处理成 240x240 正方形帧 -> 按所选动画模式
  生成多帧 -> 合成一张循环 GIF（可选把中文文案烤进底部）。

支持动画模式（--mode）：
  blink   交替闪烁（A <-> B 乒乓循环，最像微信"打脸/变脸"表情，默认）
  fade    淡入淡出（A 与 B 交叉溶解，柔和过渡）
  slide   滑入切换（B 从指定方向滑入盖住 A，再滑出，无缝循环）
  pop     弹入缩放（B 从中心由小放大"砰"地弹出，再缩回，无缝循环）

可选：
  --caption "文字"   把中文文案烤进 240x240 贴纸内部底部（白字+黑描边）
  --bg R,G,B         合成背景色，默认 255,255,255（白）
  --transparent      输出带透明背景的 GIF（仅 blink 模式边缘干净，
                     过渡类模式因半透明像素会被硬处理，效果略糙）
  --size             输出边长，默认 240
  --fps / --duration 帧率或每帧毫秒（blink 用 duration，过渡类用 fps）
  --loops            过渡类模式的中间帧数（越大越顺滑，默认 6）
  --direction        slide 的滑入方向：right/left/top/bottom，默认 right
  --pingpong         fade/slide/pop 是否往返（默认开，保证无缝循环）

用法示例：
  python make_gif.py --img1 a.png --img2 b.png --output out.gif
  python make_gif.py --img1 a.png --img2 b.png --mode fade --caption "你礼貌吗"
  python make_gif.py --img1 a.png --img2 b.png --mode slide --direction top --bg 255,240,245
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageSequence
except ImportError:
    sys.exit("缺少依赖 Pillow，请先安装：pip install Pillow（或在隔离 venv 中安装）")


# ----------------------------- 基础参数 -----------------------------
SIZE = 240
TEXT_FILL = (255, 255, 255, 255)
TEXT_STROKE = (0, 0, 0, 235)
STROKE_W = 3


def find_font(size: int):
    """优先系统中文字体（Windows 微软雅黑），找不到回退默认。"""
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc",
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


def parse_bg(s: str):
    try:
        parts = [int(x) for x in s.split(",")]
        if len(parts) == 3:
            return tuple(parts)
    except Exception:
        pass
    sys.exit(f"--bg 格式应为 R,G,B，例如 255,255,255，收到：{s}")


def prepare(im: Image.Image, size: int, bg, fit: str) -> Image.Image:
    """把任意图处理成 size×size 的 RGBA 帧（居中裁切或完整内嵌）。"""
    im = im.convert("RGBA")
    w, h = im.size
    if fit == "contain":
        # 完整保留内容，等比缩放后居中贴在背景上
        scale = min(size / w, size / h)
        nw, nh = max(1, int(w * scale)), max(1, int(h * scale))
        im = im.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new("RGBA", (size, size), bg + (255,))
        canvas.paste(im, ((size - nw) // 2, (size - nh) // 2), im)
        return canvas
    # cover：居中裁切到正方形再缩放（保证铺满 240x240）
    s = min(w, h)
    left = (w - s) // 2
    top = (h - s) // 2
    im = im.crop((left, top, left + s, top + s))
    return im.resize((size, size), Image.LANCZOS)


def bake_caption(im: Image.Image, text: str, size: int):
    """把中文文案烤进贴纸内部底部（白字+黑描边，不遮挡主体）。"""
    if not text:
        return im
    im = im.convert("RGBA")
    d = ImageDraw.Draw(im)
    max_w = size - 16
    # 自动缩字号
    fs = 42
    while fs > 16:
        f = find_font(fs)
        bbox = d.textbbox((0, 0), text, font=f)
        if (bbox[2] - bbox[0]) <= max_w:
            break
        fs -= 2
    f = find_font(fs)
    bbox = d.textbbox((0, 0), text, font=f)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (size - tw) / 2
    y = size - th - 10 - bbox[1]
    d.text((x, y), text, font=f, fill=TEXT_FILL, stroke_width=STROKE_W, stroke_fill=TEXT_STROKE)
    return im


# ----------------------------- 动画模式 -----------------------------
def frames_blink(a: Image.Image, b: Image.Image, duration: int):
    """A <-> B 乒乓交替。"""
    return [a, b], [duration, duration]


def frames_fade(a, b, loops, fps, pingpong):
    """A 与 B 交叉溶解。"""
    seq, durs = [], []
    steps = max(2, loops)
    if pingpong:
        # 1 -> 混合 -> 2 -> 混合(逆) -> 1，无缝
        seq.append(a)
        for i in range(1, steps):
            t = i / steps
            seq.append(Image.blend(a, b, t))
        seq.append(b)
        for i in range(steps - 1, 0, -1):
            t = i / steps
            seq.append(Image.blend(a, b, t))
    else:
        for i in range(steps + 1):
            t = i / steps
            seq.append(Image.blend(a, b, t))
    fd = int(1000 / max(1, fps))
    return seq, [fd] * len(seq)


def frames_slide(a, b, loops, fps, pingpong, direction):
    """B 从 direction 滑入盖住 A，再滑出。"""
    size = a.size[0]
    seq = []
    steps = max(2, loops)
    offs = [int(size * (1 - i / steps)) for i in range(steps + 1)]  # 0..size
    if direction in ("left", "top"):
        offs = list(reversed(offs))  # 从另一侧进
    axis = 0 if direction in ("left", "right") else 1

    def composite(base, top, off):
        layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
        box = [0, 0]
        box[axis] = off
        layer.paste(top, tuple(box), top)
        return Image.alpha_composite(base, layer)

    if pingpong:
        # 滑入 -> 停留 -> 滑出（回到 A）
        seq.append(a)
        for off in offs[1:]:
            seq.append(composite(a, b, off))
        seq.append(b)
        for off in reversed(offs[1:-1]):
            seq.append(composite(a, b, off))
    else:
        for off in offs:
            seq.append(composite(a, b, off))
    fd = int(1000 / max(1, fps))
    return seq, [fd] * len(seq)


def frames_pop(a, b, loops, fps, pingpong):
    """B 从中心由小放大弹出，再缩回。"""
    size = a.size[0]
    seq = []
    steps = max(2, loops)

    def scaled(im, scale):
        w = max(1, int(size * scale))
        h = max(1, int(size * scale))
        tim = im.resize((w, h), Image.LANCZOS)
        layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        layer.paste(tim, ((size - w) // 2, (size - h) // 2), tim)
        return Image.alpha_composite(a, layer)

    if pingpong:
        seq.append(a)
        for i in range(1, steps):
            seq.append(scaled(b, i / steps))
        seq.append(b)
        for i in range(steps - 1, 0, -1):
            seq.append(scaled(b, i / steps))
    else:
        for i in range(steps + 1):
            seq.append(scaled(b, i / steps))
    fd = int(1000 / max(1, fps))
    return seq, [fd] * len(seq)


# ----------------------------- 输出 -----------------------------
def to_rgb(frame, bg):
    return Image.alpha_composite(Image.new("RGBA", frame.size, bg + (255,)), frame).convert("RGB")


def save_gif(frames, durations, out_path, bg, transparent):
    if transparent:
        # 转调色板 + 透明索引（blink 等硬边帧效果最佳）
        pal_frames = []
        for f in frames:
            rgb = to_rgb(f, bg)
            pal_frames.append(rgb)
        # 用第一张建立调色板，标记背景色为透明
        im = pal_frames[0].convert("P", palette=Image.ADAPTIVE)
        transparent_idx = im.getpixel((0, 0)) if im.getpixel((0, 0)) is not None else 0
        im.save(
            out_path, save_all=True, append_images=pal_frames[1:],
            duration=durations, loop=0, disposal=2, transparency=transparent_idx,
        )
    else:
        rgb_frames = [to_rgb(f, bg) for f in frames]
        rgb_frames[0].save(
            out_path, save_all=True, append_images=rgb_frames[1:],
            duration=durations, loop=0, disposal=2,
        )


def main():
    ap = argparse.ArgumentParser(description="qianjin-sticker-pack 两图合成动态 GIF 表情")
    ap.add_argument("--img1", required=True, help="第一张图路径")
    ap.add_argument("--img2", required=True, help="第二张图路径")
    ap.add_argument("--output", default="dynamic_sticker.gif", help="输出 GIF 路径")
    ap.add_argument("--size", type=int, default=SIZE, help="输出边长（默认 240）")
    ap.add_argument("--mode", default="blink",
                    choices=["blink", "fade", "slide", "pop"],
                    help="动画模式（默认 blink 交替）")
    ap.add_argument("--caption", default="", help="底部中文文案（可选）")
    ap.add_argument("--bg", default="255,255,255", help="背景色 R,G,B（默认白）")
    ap.add_argument("--transparent", action="store_true", help="输出透明 GIF")
    ap.add_argument("--fit", default="cover", choices=["cover", "contain"],
                    help="cover=居中裁切铺满 / contain=完整内嵌")
    ap.add_argument("--fps", type=int, default=8, help="过渡类模式帧率（fade/slide/pop）")
    ap.add_argument("--duration", type=int, default=420, help="blink 每帧毫秒")
    ap.add_argument("--loops", type=int, default=6, help="过渡类中间帧数")
    ap.add_argument("--direction", default="right", choices=["right", "left", "top", "bottom"],
                    help="slide 滑入方向")
    ap.add_argument("--no-pingpong", dest="pingpong", action="store_false",
                    help="过渡类不往返（直接跳回首帧）")
    args = ap.parse_args()

    bg = parse_bg(args.bg)
    a = prepare(Image.open(args.img1), args.size, bg, args.fit)
    b = prepare(Image.open(args.img2), args.size, bg, args.fit)

    if args.caption:
        a = bake_caption(a, args.caption, args.size)
        b = bake_caption(b, args.caption, args.size)

    if args.mode == "blink":
        seq, durs = frames_blink(a, b, args.duration)
    elif args.mode == "fade":
        seq, durs = frames_fade(a, b, args.loops, args.fps, args.pingpong)
    elif args.mode == "slide":
        seq, durs = frames_slide(a, b, args.loops, args.fps, args.pingpong, args.direction)
    else:  # pop
        seq, durs = frames_pop(a, b, args.loops, args.fps, args.pingpong)

    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    save_gif(seq, durs, args.output, bg, args.transparent)
    print(f"已生成 {args.mode} 动态表情 -> {args.output}")
    print(f"帧数: {len(seq)}  尺寸: {args.size}x{args.size}  循环: 永久")


if __name__ == "__main__":
    main()
