# 表情包主题内容库 · theme-library

> 内置 6 大主题，每主题预置 12 个表情（场景/动作 + 推荐中文文案 + 英文动作关键词）。
> 生成提示词时：从本库取「英文动作关键词」填入 SKILL.md 第四节的模板 `{本表情英文动作关键词}` 位置；中文文案存入 `captions.json` 供 `assemble.py` 合成。

**用法**：用户选定主题后，默认取全部 12 个；也可让用户挑选其中若干张、或跨主题混搭。文案可原样使用，也支持用户自定义替换（保持"一个表情 = 一个明确情绪/动作 + 一句短文案"的原则）。

---

## 主题一：工作表情包（打工人）

| # | 场景/动作 | 推荐中文文案 | 英文动作关键词（EN） |
|---|-----------|--------------|----------------------|
| 1 | 刚上班，萎靡开机 | 早… | just arrived at desk, still waking up, sleepy half-closed eyes, holding phone |
| 2 | 摸鱼，偷瞄四周 | 先摸会儿 | sneaking to slack off, looking around sneakily, mischievous smile |
| 3 | 收到需求，强颜欢笑 | 收到，马上改 | nodding reluctantly, forced smile, sweating slightly |
| 4 | 开会神游，眼神放空 | 在听了 | sitting in a meeting, eyes glazed, mind wandering, blank stare |
| 5 | 周一崩溃，趴桌 | 不想上班 | collapsed on desk, dread face, monday blues |
| 6 | 加班，端咖啡硬撑 | 我还能肝 | exhausted, droopy eyes, tiny sweat drop, holding a coffee cup |
| 7 | 方案被否，假笑重做 | 好的，我重做 | sighing, defeated pose, thumbs up reluctantly |
| 8 | 老板画饼，礼貌微笑 | 好的老板 | polite smile, nodding, eyes dead inside |
| 9 | deadline 临近，抓狂 | 通宵也要上 | panic, wide eyes, surrounded by papers, desperate |
| 10 | 工资到账，惊喜查手机 | 有工资了？ | checking phone, surprised happy, eyes widen |
| 11 | 通知团建，毫无波澜 | 又团建？ | unenthusiastic, flat mouth, dread |
| 12 | 下班，撒腿就跑 | 溜了溜了 | running away happily, waving, backpack, sense of freedom |

---

## 主题二：聊天表情包（日常对话）

| # | 场景/动作 | 推荐中文文案 | 英文动作关键词（EN） |
|---|-----------|--------------|----------------------|
| 1 | 探头挥手 | 在吗？ | peeking from behind, waving hand, curious |
| 2 | 大笑仰头 | 哈哈哈 | laughing out loud, head tilted back, tears of joy |
| 3 | 比赞点头 | 好的 | thumbs up, cheerful nod |
| 4 | 敬礼秒回 | 收到 | salute, smart nod |
| 5 | 双手合十鞠躬 | 谢谢 | bowing gratefully, hands together |
| 6 | 双手合十道歉 | 抱歉 | apologetic, hands together praying, sweating |
| 7 | 托腮思考 | 让我想想 | thinking pose, finger on chin, looking up |
| 8 | 面无表情 | 无语 | deadpan stare, flat mouth, no expression |
| 9 | 大赞带星光 | 赞 | big thumbs up, sparkle, proud |
| 10 | 双手比心 | 比心 | making a heart shape with hands, cute smile |
| 11 | 张开双臂 | 抱抱 | arms open for a hug, warm smile |
| 12 | 挥手告别 | 拜拜 | waving goodbye, happy, walking away |

---

## 主题三：搞笑表情包（沙雕/梗）

| # | 场景/动作 | 推荐中文文案 | 英文动作关键词（EN） |
|---|-----------|--------------|----------------------|
| 1 | 身体裂开 | 我裂开了 | splitting apart comically, cracked body, shocked |
| 2 | 甩锅否认 | 这不是我 | denying, pointing away, sweating |
| 3 | 真香现场 | 真香 | eating happily, changed mind, delighted |
| 4 | 社死捂脸 | 社死现场 | hiding face with hands, embarrassed, red face |
| 5 | 大哭崩溃 | 我太难了 | crying with huge tears, collapsing, overwhelmed |
| 6 | 满头问号 | ？？？ | confused, question marks around head, head tilt |
| 7 | 直接躺平 | 摆烂了 | lying flat, giving up, lazy sprawl |
| 8 | 草丛暗中观察 | 暗中观察 | peeking from a bush, one eye, sneaky |
| 9 | 顿悟指天 | 我悟了 | lightbulb moment, pointing up, enlightened |
| 10 | 笑到打滚 | 笑不活了 | rolling on floor laughing, tears of laughter |
| 11 | 端碗冲饭 | 干饭了 | holding a bowl, rushing to eat, happy |
| 12 | 悠闲躺平 | 躺平最香 | lying down relaxed, peaceful, content |

---

## 主题四：情绪表情包（喜怒哀乐）

| # | 场景/动作 | 推荐中文文案 | 英文动作关键词（EN） |
|---|-----------|--------------|----------------------|
| 1 | 灿烂笑 | 开心 | big bright smile, sparkling eyes, joyful |
| 2 | 鼓腮生气 | 哼 | angry, puffed cheeks, frowning, steam from ears |
| 3 | 泪奔 | 呜呜 | crying, tears streaming, sad |
| 4 | 张嘴震惊 | 哇 | mouth open wide, eyes huge, shocked |
| 5 | 捂脸害羞 | 人家害羞 | blushing, hiding behind hands, coy |
| 6 | 吐舌得意 | 略略略 | sticking tongue out, smug, proud |
| 7 | 撇嘴委屈 | 委屈 | pouting, watery eyes, wronged |
| 8 | 发抖躲藏 | 怕怕 | trembling, hiding, scared |
| 9 | 打哈欠犯困 | 困了 | sleepy, yawning, half-closed eyes, floating Zzz |
| 10 | 飞吻爱心眼 | 爱你哟 | blowing a kiss, heart eyes, loving |
| 11 | 呆滞放空 | 好无聊 | bored, drooping, staring blankly |
| 12 | 虚弱抱枕 | 不舒服 | sick, thermometer, pale, weak |

---

## 主题五：日常表情包（生活碎片）

| # | 场景/动作 | 推荐中文文案 | 英文动作关键词（EN） |
|---|-----------|--------------|----------------------|
| 1 | 乱发伸懒腰 | 起床了 | just woke up, messy hair, stretching |
| 2 | 举筷开吃 | 开饭 | holding chopsticks, hungry, eager for food |
| 3 | 端杯补水 | 补水 | holding a cup, drinking, refreshed |
| 4 | 举哑铃运动 | 动一动 | exercising, holding a dumbbell, energetic |
| 5 | 戴镜读书 | 看书 | reading a book, focused, wearing glasses |
| 6 | 戴耳机晃头 | 听歌中 | wearing headphones, bobbing to music, enjoying |
| 7 | 抱零食追剧 | 追剧中 | watching a screen, holding popcorn, hooked |
| 8 | 提袋逛街 | 逛街去 | carrying shopping bags, happy, browsing |
| 9 | 泡泡毛巾澡 | 洗澡澡 | surrounded by bubbles, towel, relaxed |
| 10 | 裹被睡觉 | 晚安 | under a blanket, sleepy, moon above |
| 11 | 端咖啡续命 | 续命 | holding coffee cup, awake, energized |
| 12 | 放空发呆 | 放空 | blank stare, floating thoughts, calm |

---

## 主题六：节日表情包（节庆氛围）

| # | 场景/动作 | 推荐中文文案 | 英文动作关键词（EN） |
|---|-----------|--------------|----------------------|
| 1 | 持福字贺年 | 新年好 | festive, holding a 福 character, red, celebratory |
| 2 | 持红包作揖 | 恭喜发财 | holding a red envelope, gold accents, lucky, bowing |
| 3 | 月饼满月 | 中秋团圆 | holding a mooncake, full moon, round lantern |
| 4 | 蛋糕礼帽 | 生日快乐 | birthday cake with candles, party hat, cheerful |
| 5 | 圣诞帽礼物 | 圣诞快乐 | santa hat, gift box, snow, christmas tree |
| 6 | 玫瑰爱心 | 情人节 | heart, rose, love, pink tones |
| 7 | 旗帜烟花 | 国庆快乐 | flag, fireworks, festive red |
| 8 | 粽子龙舟 | 端午安康 | holding zongzi (rice dumpling), dragon boat hint |
| 9 | 南瓜 costume | 不给糖就捣蛋 | pumpkin, cute costume, spooky but adorable |
| 10 | 火鸡感恩 | 感恩 | turkey, thankful, warm tones |
| 11 | 灯笼汤圆 | 元宵灯会 | lantern, tangyuan balls, glowing |
| 12 | 休闲欢呼 | 终于周末 | relaxing, free, cheering |

---

## 混搭与扩展

- **跨主题混搭**：用户可指定"工作 6 张 + 情绪 6 张"，从两个主题各取若干，凑成 12 张一套。
- **自定义文案**：文案栏可整体替换为用户品牌话术（如把"收到，马上改"改成"收到，亲~"），动作关键词不变即可。
- **加张数**：8/16/24 张时，可重复调用本库不同主题，或让用户补充自定义场景（按同样格式：场景 + 文案 + EN 动作词）。
