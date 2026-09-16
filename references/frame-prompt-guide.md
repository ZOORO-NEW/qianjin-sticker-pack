# 两帧生成提示词规范（无现成图时）

本技能核心是"两张图 → 一张动图"。如果你手头没有合适的两张图，先用 ImageGen 生成**同一角色的两种瞬间**，再回来用 `make_gif.py` 合成。关键只有一句：**两帧只换"表情/动作"，其余全部锁死**。

## 一、风格前缀（固定角色外观）

> 有参考图时优先走 image-to-image，把参考图作为 `image` 入参，提示词用 `same character as the reference image` 锚定，比下方文字前缀一致性更强。下面前缀仅用于"只有文字描述"的情形。

| 风格 | 风格前缀（EN） |
|------|------|
| 萌系 | cute chibi character, big head small body (2-3 head ratio), huge sparkly eyes, pastel macaron colors, round fluffy shapes, soft vinyl toy texture |
| 潮酷系 | cool street-style character, edgy outfit with bold accessories, asymmetrical pose, high-contrast colors, confident attitude |
| 国风系 | Chinese-style character, elegant traditional clothing, refined facial features, traditional color palette (cinnabar/azure/jade), flowing lines, dignified aura |
| 极简系 | minimalist flat character, geometric shapes, limited color palette (≤3 colors), simple clean lines, bold silhouette |
| 暗黑系 | dark gothic character, sharp contours, deep shadows, eerie glow accents, mysterious and intimidating aura |
| 治愈系 | healing-style cozy character, round soft body, warm cream tones, gentle half-closed eyes, omega-shaped smile, fluffy texture |

> 若用户给了具体描述（如"戴眼镜的橘猫程序员"），用描述代替上表，但**所有帧用同一段角色描述**。

## 二、提示词模板（两帧通用）

```
{风格前缀}, {本帧表情/动作关键词}, sticker design, square composition,
clean solid color background or transparent background, isolated subject,
flat vector illustration style, bold clean outline, no text, no watermark,
no signature, full character visible, centered, high contrast,
simple shapes, easy to read at small size, static pose, no motion blur
```

- **帧 A 关键词**（如）：`gentle smile, relaxed eyes, calm expression`
- **帧 B 关键词**（如）：`shocked open mouth, wide eyes, sweat drop, exaggerated surprised face`

两帧只替换"表情/动作关键词"这一段，其余原样复制。

## 三、负面词（生图时附加）

```
text, words, letters, watermark, signature, logo, complex background,
photo, realistic, 3d render, blurry, low quality, extra limbs, deformed, partial, cropped
```

> 要 2D 贴纸风走 `flat vector`；要 3D 盲盒风去掉 `3d render` 负面词并改 `flat vector` 为 `3d chibi blind-box figure`。

## 四、两帧常见"动一下"组合（直接套）

| 情绪/梗 | 帧 A | 帧 B |
|---------|------|------|
| 变脸/打脸 | 微笑 | 怒目/炸毛 |
| 眨眼 | 睁眼 | 闭眼 |
| 震惊 | 平静 | 张嘴流汗 |
| 赞同→反悔 | 点头 | 摇头 |
| 满→空 | 满杯 | 空杯 |
| 乖→皮 | 坐好 | 蹦起 |
| 装→崩 | 淡定 | 裂开 |

生成两帧后，用 `make_gif.py --mode blink`（最像微信变脸）或 `--mode pop`（强调帧 B）合成即可。
