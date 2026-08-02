---
name: qianjin-sticker-pack
description: "基于已有 IP 形象（qianjin-ip-design 风格角色 / 山海经神兽 / 用户参考图）生成成套表情包体系。支持工作/聊天/搞笑/情绪/日常/节日等多主题，每套默认 12 张静态表情，正方形 240×240 规范，输出完整英文提示词并一键生图、自动拼图预览。适用于微信/Telegram/Discord 表情包、品牌 IP 衍生品、社群运营素材。"
version: "1.0"
author: qianjin
tags:
  - sticker
  - emoji-pack
  - expression-pack
  - ip-design
  - character-design
  - prompt
  - cartoon
license: MIT
---

# IP 表情包体系生成器 · qianjin-sticker-pack

> **输入一个 IP 形象 → 输出一整套主题表情包（默认 12 张静态、240×240 正方形、完整可复制英文提示词）→ 确认后一键生图并自动拼图预览。**

本技能是 `qianjin-ip-design`（IP 设计）与 `qianjin-shanhaijing-pet`（神兽宠物）的**下游生产线**：上游负责"造出一个角色"，本技能负责"让这个角色活成一套能聊天的表情"。风格语言继承自 `qianjin-ip-design` 的 6 大风格 × 8 维体系，确保表情包与原始 IP 气质一致。

---

## 一、技能定位

| 项目 | 说明 |
|------|------|
| 输入 | ① IP 参考图（jpg/png，最推荐，一致性最强）或 ② IP 风格描述（如"萌系小狐狸" / 直接引用 ip-design 的某风格）或 ③ 神兽名（走 shanhaijing-pet 出图后再做表情） |
| 输出 | 一整套表情包：**默认 12 张静态表情**，每张含「中文场景 + 推荐文案 + 完整英文提示词」；确认后生图并输出 240×240 PNG + 4×3 预览拼图 |
| 主题 | 内置 6 大主题（见 `references/theme-library.md`）：工作 / 聊天 / 搞笑 / 情绪 / 日常 / 节日；每主题预置 12 个表情内容 |
| 规范 | **正方形 240×240 px**、纯色/透明背景、静态、无图内文字（文字走后期合成，保证清晰）、同一角色跨张一致 |
| 生图 | 调用 ImageGen（文生图 / 图生图）；有参考图时走 image-to-image，跨张一致性最佳 |
| 拼图 | 用 `scripts/assemble.py`（Pillow）统一缩放 240×240、可选合成文案、拼 4×3 预览 |

**输出语言规则**：提示词主体用英文（喂绘图模型），设计说明与文案用简体中文。

---

## 二、核心流程（五步）

```
① 锁定 IP  →  ② 选主题&数量  →  ③ 生成 12 条提示词清单  →  ④ 用户确认  →  ⑤ 生图 + 拼图
```

### ① 锁定 IP（决定一致性策略）
- **有参考图**：记录图片路径，后续走 image-to-image（把参考图作为 image 入参），提示词里用 `same character as the reference image` 锚定。→ 跨张一致性最强（推荐）。
- **只有风格/描述**：从下表取对应风格的「风格前缀」写进每条提示词开头，固定角色外观。一致性靠文字锁，略弱于图生图。
- **神兽名**：先按 `qianjin-shanhaijing-pet` 出一张该神兽的 Q 版萌宠图作为参考图，再走本流程。

### ② 选主题 & 数量
- 主题：工作 / 聊天 / 搞笑 / 情绪 / 日常 / 节日（可多选，每主题一套 12 张）。
- 数量：默认 12 张/套；也支持 8 / 16 / 24（拼图网格会自适应）。

### ③ 生成 12 条提示词清单
- 从 `references/theme-library.md` 取该主题的 12 个表情（场景 + 中文文案 + 英文动作关键词）。
- 套用下方「提示词模板」：风格前缀 + 该表情动作词 + 全局规范 + 负面词。
- **整张清单先给用户看**（序号 / 场景 / 文案 / 提示词摘要），不急着生图。

### ④ 用户确认
- 用户可调整：替换某张文案、加减张数、改背景色、要不要图内文字。
- 确认后才进入生图。

### ⑤ 生图 + 拼图
- 逐张调 ImageGen（有参考图走 image-to-image）。
- 全部生成后调 `scripts/assemble.py`：缩放 240×240、可选叠文案、拼预览图。
- 输出到用户工作区 `sticker-pack/<主题>/`（含 12 张 PNG + preview.png + captions.json）。

---

## 三、风格前缀表（继承自 qianjin-ip-design 六风格）

> 仅当用户**未提供参考图**、只用风格描述时，把对应前缀写进每条提示词开头，固定角色外观。

| 风格 | 风格前缀（EN，写进每条提示词开头） |
|------|------|
| 萌系 | cute chibi character, big head small body (2-3 head ratio), huge sparkly eyes, pastel macaron colors, round fluffy shapes, soft vinyl toy texture |
| 潮酷系 | cool street-style character, edgy outfit with bold accessories, asymmetrical pose, high-contrast colors, confident attitude |
| 国风系 | Chinese-style character, elegant traditional clothing, refined facial features, traditional color palette (cinnabar/azure/jade), flowing lines, dignified aura |
| 极简系 | minimalist flat character, geometric shapes, limited color palette (≤3 colors), simple clean lines, bold silhouette |
| 暗黑系 | dark gothic character, sharp contours, deep shadows, eerie glow accents, mysterious and intimidating aura |
| 治愈系 | healing-style cozy character, round soft body, warm cream tones, gentle half-closed eyes, omega-shaped smile, fluffy texture |

> 若用户给了具体描述（如"戴眼镜的橘猫程序员"），用描述代替上表，但保持"固定外观"原则——所有 12 张用同一段角色描述。

---

## 四、提示词模板与全局规范

### 4.1 文生图模板（无参考图）

```
{风格前缀}, {本表情英文动作关键词}, sticker design, square composition, clean solid color background or transparent background, isolated subject, flat vector illustration style, bold clean outline, no text, no watermark, no signature, full character visible, centered, high contrast, simple shapes, easy to read at small size, static pose, no motion blur
```

### 4.2 图生图模板（有参考图，推荐）

```
same character as the reference image, {本表情英文动作关键词}, sticker design, square composition, clean solid color background or transparent background, isolated subject, flat vector illustration style, bold clean outline, no text, no watermark, no signature, full character visible, centered, high contrast, simple shapes, easy to read at small size, static pose, no motion blur
```

### 4.3 全局规范（每条必须包含，保证"一套表情"的统一感）
- **正方形**：`square composition` + 生图时指定 1:1 比例。
- **抠图友好**：`clean solid color background or transparent background, isolated subject, easy to cutout`。
- **贴纸感**：`sticker design, flat vector illustration style, bold clean outline`（描边让小尺寸也清晰）。
- **静态**：`static pose, no motion blur`（表情包要瞬间可读）。
- **无图内文字**：`no text, no watermark, no signature`——文案走 `assemble.py` 后期合成，中文更清晰可控。
- **小尺寸可读**：`simple shapes, high contrast, easy to read at small size`。

### 4.4 负面词（Negative，生图时附加）
```
text, words, letters, watermark, signature, logo, complex background, photo, realistic, 3d render, blurry, low quality, extra limbs, deformed, partial, cropped
```
> 注意：用户要的是"贴纸风"表情，默认走 2D 扁平插画；若用户明确要 3D 盲盒风表情，去掉 `3d render` 负面词并改 `flat vector` 为 `3d chibi blind-box figure`。

---

## 五、文案合成（关键：中文清晰）

表情包文案**不画进生成图里**（AI 画中文极不稳定），而是用 `scripts/assemble.py` **烤进 240×240 贴纸内部**（白字 + 黑描边，紧贴底部，像微信表情包那样）：

- 每张表情对应一条中文文案（来自 theme-library 默认或用户自定），存 `captions.json`：`{"01.png":"收到，马上改","02.png":"我还能肝",...}`。
- `assemble.py` 默认把文案**烤进图内**（`bake_caption`：白字 + 黑描边宽 3、自动字号 16-42px、距底部约 10px、水平居中），可直接发到微信/社交平台。
- 字体：优先 `msyhbd.ttc`（微软雅黑 Bold）→ `msyh.ttc` → `simhei`，未找到回退 PIL 默认。
- 若用户要"纯图无字"表情，加 `--no-text` 参数即可跳过烤字。

---

## 六、生图与拼图调用

### 6.1 生图（ImageGen）
- 逐张调用，有参考图时传 `image` 参数（参考图路径），`prompt` 用图生图模板。
- 12 张建议分 2 批（每批 6 张）串行生成，避免超时；单张约 5-10 credits，先告知用户成本。
- **防覆盖提示**：ImageGen 默认按时间戳命名输出文件，若多张图在同一秒完成可能重名覆盖。稳妥做法是为每张表情指定独立子目录（如 `output/01/`、`output/02/`），生成后再统一收集。

### 6.2 拼图（assemble.py）
```bash
# 默认：文案烤进 240×240 贴纸内部 + 拼预览
python scripts/assemble.py --input <生图目录> --output <输出目录> --captions captions.json

# 只要纯图贴纸（不烤字）
python scripts/assemble.py --input <生图目录> --output <输出目录> --captions captions.json --no-text

# 自定义网格（如 24 张用 6×4）
python scripts/assemble.py --input <生图目录> --output <输出目录> --cols 6 --rows 4
```

输出：
- `output/pack/`：N 张 240×240 PNG（贴纸本体，默认含烤字）
- `output/preview.png`：拼图预览（每格展示烤好字的贴纸 + 左上角序号）

---

## 七、示例（工作表情包 · 萌系小狐狸，有参考图）

> 参考图：`fox_ref.png`（一只萌系橘狐 IP）

**第 3 张「加班」提示词（图生图）**
```
same character as the reference image, looking exhausted with droopy eyes and a tiny sweat drop, holding a coffee cup, sticker design, square composition, clean solid color background or transparent background, isolated subject, flat vector illustration style, bold clean outline, no text, no watermark, no signature, full character visible, centered, high contrast, simple shapes, easy to read at small size, static pose, no motion blur
```
**中文文案**：`我还能肝`
**负面词**：text, words, letters, watermark, signature, complex background, photo, realistic, blurry, low quality, extra limbs, deformed

生成 12 张后拼图，得到一套可发的「打工人狐狸」表情包。

---

## 八、版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-08-02 | 初始版本：6 主题×12 表情内容库 + 风格一致性前缀 + 240 方图规范 + 提示词模板 + assemble.py 拼图脚本 |
