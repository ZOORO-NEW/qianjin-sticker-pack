---
name: qianjin-sticker-pack
description: "动态表情包生成技能：把任意两张图片合成一张 240×240 的 GIF 动态表情包。支持 交替/淡入/滑入/弹入 四种动画模式，可一键把中文文案烤进底部，输出永久循环、可直接发到微信/Telegram/Discord 的 GIF。也支持先由 IP 形象生成两帧再合成。"
version: 2.1.1
slug: qianjin-sticker-pack
displayName: 动态表情包生成器
summary: "两张图 → 240×240 动态 GIF 表情包。四种动画模式（交替/淡入/滑入/弹入）+ 中文文案烤入，一键合成可发微信的动态表情。"
license: MIT
category: 设计创作
platforms:
  - workbuddy
  - claude-code
  - cursor
  - windsurf
  - codex
author: qianjin
tags:
  - sticker
  - gif
  - dynamic-emoji
  - expression-pack
  - ip-design
  - animation
license: MIT
---

# 动态表情包生成器 · qianjin-sticker-pack v2

> **输入两张图 → 输出一张 240×240 的 GIF 动态表情包（永久循环、可直发微信/Telegram/Discord）。**
> 四种动画模式（交替 / 淡入 / 滑入 / 弹入），可选把中文文案烤进底部。

本技能是 `qianjin-ip-design`（IP 设计）的**下游**：上游负责"造出一个角色 + 它的两个瞬间"，本技能负责"把这两个瞬间合成一张会动的表情"。如果你手里已经有两张现成图片（同一角色两种表情、或任何想做动静对比的两张图），直接进流程即可。

---

## 一、技能定位

| 项目 | 说明 |
|------|------|
| 输入 | 两张图（jpg/png/webp）：**同一主体两个瞬间**最佳（两种表情 / 两个动作 / 前后对比） |
| 输出 | **一张 240×240 GIF 动态表情包**，永久循环；可选带底部中文文案 |
| 动画 | 4 种模式：`blink` 交替 / `fade` 淡入 / `slide` 滑入 / `pop` 弹入（见第二节） |
| 合成 | 调用 `scripts/make_gif.py`（Pillow）统一裁切 240×240、按模式生成多帧、合成 GIF |
| 文案 | 可选 `--caption`，中文白字+黑描边烤进底部，不画进源图（AI 画中文不稳，后期合成更清晰） |
| 平台 | 微信 / Telegram / Discord / 飞书 表情均兼容（GIF、240 方、循环） |

**输出语言规则**：脚本参数与提示词用英文/拼音思路喂给绘图模型；说明与文案用简体中文。

---

## 二、四步流程

```
① 准备两图  →  ② 选动画模式  →  ③ (可选) 定文案  →  ④ 跑 make_gif.py 出 GIF
```

### ① 准备两图（核心：两帧要"同一主体"）
- **最推荐**：同一角色/IP 的两种瞬间（如笑脸↔哭脸、正常↔炸毛、闭眼↔睁眼）。动态表情的灵魂就是"动那一下"。
- **对比类**：前后状态（干净↔脏乱、满杯↔空杯），适合"打脸/吐槽"梗。
- 两张图**尽量已接近正方形、主体居中**；脚本会自动居中裁切/缩放成 240×240（可用 `--fit contain` 避免裁掉边缘）。
- 若你**没有现成图**，见 `references/frame-prompt-guide.md`，用 ImageGen 先出两帧（同一角色两种表情），再回来合成。

### ② 选动画模式

| 模式 | 效果 | 最像什么 | 默认节奏 |
|------|------|----------|----------|
| `blink` | A ↔ B 乒乓交替 | 微信"变脸/打脸"表情、眨眼 | 每帧 420ms |
| `fade` | A 与 B 交叉溶解 | 柔和过渡、氛围感 | 8fps，6 中间帧 |
| `slide` | B 从某方向滑入盖住 A 再滑出 | 卡片翻面、弹幕划过 | 8fps，6 中间帧 |
| `pop` | B 从中心由小放大"砰"弹出再缩回 | 强调、震惊、点题 | 8fps，6 中间帧 |

> 全部用**往返（ping-pong）**实现无缝循环，不会在 A↔B 衔接处"跳帧"。

### ③（可选）定文案
- 给一句短中文（≤6 字最佳），如"你礼貌吗""我裂开""退退退"。
- 用 `--caption` 烤进 240×240 底部（白字+黑描边，微信风）。参考 `references/caption-library.md` 取梗。
- 不要字就省略该参数。

### ④ 跑 make_gif.py
```bash
# 默认：blink 交替 + 文案
python scripts/make_gif.py --img1 a.png --img2 b.png --output out.gif --caption "你礼貌吗"

# 淡入过渡（无字）
python scripts/make_gif.py --img1 a.png --img2 b.png --mode fade --output out.gif

# 滑入：从上方滑进
python scripts/make_gif.py --img1 a.png --img2 b.png --mode slide --direction top --output out.gif

# 弹入强调
python scripts/make_gif.py --img1 a.png --img2 b.png --mode pop --caption "我裂开" --output out.gif
```
> 运行前需 Pillow：`pip install Pillow`（或技能自带的隔离 venv）。详见 `scripts/requirements.txt`。

输出即一张 `out.gif`，240×240、永久循环，可直接拖进微信表情添加。

---

## 三、make_gif.py 参数速查

| 参数 | 默认 | 说明 |
|------|------|------|
| `--img1` / `--img2` | 必填 | 两张源图路径 |
| `--output` | `dynamic_sticker.gif` | 输出 GIF 路径 |
| `--size` | `240` | 输出边长（正方形） |
| `--mode` | `blink` | `blink`/`fade`/`slide`/`pop` |
| `--caption` | 空 | 底部中文文案（白字+黑描边） |
| `--bg` | `255,255,255` | 合成背景色 R,G,B（过渡类模式需落底） |
| `--transparent` | 关 | 输出透明 GIF（仅 blink 边缘干净；过渡类半透明会被硬处理） |
| `--fit` | `cover` | `cover`=居中裁切铺满 / `contain`=完整内嵌（防裁切用 contain） |
| `--fps` | `8` | 过渡类（fade/slide/pop）帧率 |
| `--duration` | `420` | blink 每帧毫秒 |
| `--loops` | `6` | 过渡类中间帧数（越大越顺滑，也越大体积） |
| `--direction` | `right` | slide 滑入方向：right/left/top/bottom |
| `--no-pingpong` | 关 | 过渡类不往返（直接跳回首帧，可能轻微跳帧） |

---

## 四、如何生成"两帧"（无现成图时）

完整提示词规范见 `references/frame-prompt-guide.md`，要点：
- 两帧**必须同一角色**：有参考图走 image-to-image（`same character as the reference image`），跨帧一致性最强。
- 提示词结构：`风格前缀 + 本帧动作/表情关键词 + 贴纸规范 + 负面词`。
- 两帧只改"表情/动作"那一段，其余（角色、背景、画风）完全锁死，保证合成后只是"动了一下"。
- 规范里务必带 `square composition`、`no text`、`static pose`（动效由脚本做，不用 AI 画运动模糊）。
- **⚠️ ImageGen 水印坑**：本机 ImageGen 会在图右下角加 "AI生成 / WORKBUDDY" 水印，直接合成会被裁进贴纸，必须在合成前清洗。水印有两种形态，位置固定在约 (0.88w, 0.93h)-(1.0, 1.0)：
  - 深色水印（早期）：文字暗于背景，按行采样水印左侧背景色横向覆盖即可，参考 `pingtouge\build_pack.py` 的 `clean_watermark()`。
  - 白色水印（2026-09 后）：白色半透明文字压在纯色底上，**不能整块涂背景色**（会误伤画面内容，如地面红线）。用两段式掩码清洗：① `g > bg_g+10` 抓白字核心与亮过渡；② 强清洗抓极淡 AA 残影（各通道与背景差 5~15，且 `r≈bg_r、g>bg_g-6、b>bg_b-12`，深红内容 g/b 远低天然排除）；掩码膨胀 1px 后填回区域内背景众数色。参考实现 `panda\build_panda.py` 的 `clean_watermark()`。
- **⚠️ ImageGen 并行撞名坑**：批量生成多张动作帧时**必须串行逐张调用**（一次一条消息只发一个生成请求）。并行调用时工具会把所有结果 funnel 进同一个目录，且文件名按秒级时间戳生成——同秒完成的两张图会同名互相覆盖，静默丢图且无任何报错。已实测：6 张并行丢 3 张、8 张并行丢 2 张。串行时 `output_dir` 参数才会被正确尊重。丢图后靠"清点文件数 + 逐张看图比对提示词"找回归属。
  - 2026-09 实测补充：同一条消息里并行 3-4 发、各调用恰好落秒不同时可以全部存活，但 `output_dir` 仍被忽略（全部漏斗到最后一个指定目录）→ 并行发之后必须以返回的 `localPath` 为准并核对数量；想稳妥仍走串行。
  - **构图锁死坑**：`input_fidelity=high` 会把整张构图锁得很死，普通 "NEW POSE" 提示只会让角色挪挪手、构图照旧。要出新动作姿势，提示词必须用 "COMPLETELY NEW COMPOSITION, totally different from the reference" 级别的强指令 + 具体描述火箭与角色的相对位置。6 发强指令实测约一半真正突破。

---

## 五、进阶：分层动画（让画面里的"道具"动起来）

blink 双帧合成只能换"整张图"，画面里的静态元素（火箭、灯泡、篝火等）不会动。让**局部元素动**的方法是拆图层：

1. **主图**：ImageGen 生成/图生图出主场景，为动效元素**预留空间**（如火箭喷口下方留空白）。
2. **动效贴片**：串行生成 N 张该元素的独立贴片（纯白底 + 与主图同风格 + 不同强度档位，如火焰小/中/大）。**必须串行**（见下方并行坑）。
3. **白底抠透明**：四角+边中点 `ImageDraw.floodfill(thresh≈45)` 泛洪白底 → 透明，再清 2 轮贴边白色光晕（与透明区相邻且近白的像素置透明），`getbbox()` 裁剪。**不能用全局白色阈值抠**——会吃掉元素内部的白色高光/白芯。
4. **合成循环帧**：每帧按锚点粘贴不同档位贴片（横向 ±10px 摆动更活），走 bake_caption + save_gif 出 GIF。
5. **文案让位**：动效区在底部时，把烤字 bottom 边距抬高（参考 `bake_caption_high`），避免文字压住动效。

参考实现：`panda\rocket_anim\build_rocket_anim.py`（熊猫抱火箭 + 喷焰三档循环，火焰 rotate 对齐倾斜中轴）。

---

## 六、版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-08-02 | 初始：6 主题×12 静态表情 + 240 方图规范 + assemble.py 拼图 |
| v2.0 | 2026-09-16 | **重构为动态表情包**：两张图 → 240×240 GIF；新增 make_gif.py，支持 blink/fade/slide/pop 四模式 + 文案烤入 + 透明 GIF；移除静态 12 张流水线 |
| v2.1 | 2026-09-16 | 新增**分层动画**方法论：静态道具拆独立图层（白底贴片→泛洪抠透明→多档位循环合成），让画面局部元素（喷焰等）动起来；文案抬高让位动效区 |
