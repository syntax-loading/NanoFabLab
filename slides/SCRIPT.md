# LAB3 · Gate Formation — 配音稿

配 `lab3_process_flow.html` 念。单人、照稿、只看一个动作：**什么时候按 →**。

**怎么用这个文件**

- 正文（英文段落）＝ 一个字一个字念出来的词。
- `> ` 开头的灰字是给你的说明，**不念**。
- `[顿]` ＝ 停半秒到一秒，不要念出来。
- `▶ 按 →` ＝ 这一页念完了，按右方向键翻页。**全篇只有这一个动作需要卡时间。**
- 每页标题后的时间是该页预算，按视频旁白的节奏再放宽了一点；全部写完再统一收紧。
- 动画在翻到该页时自动播一次，然后停在最终状态。稿子不依赖"动画正放到第几秒"，念到哪都能对上。

---
## 01 · Opening — ~20 s

> 目的：只交代分工（前人做到哪、我们做哪一道），然后翻页。叠层和"停在栅氧上"都留给 P2。

Two patterns are already on the wafer. Alignment marks came first, then the active
islands. After that the gate stack was deposited. Our task is the gate stripes. The next page shows what we are cutting into.

▶ **按 →**

> 已经压到 20 秒。若还要短，删掉 "After that the gate stack was deposited."，剩 15 秒。

---
## 02 · Where we start — ~95 s

> 目的：把五个数一次立住，后面每页都在减它们。剖面和"不按比例"在这一页交代。
> 实测前四段 80 s；末尾加一句过渡到 PECVD，全页约 95 s。

This is the stack we are cutting into. 

The panel under the photo is a cross-section through one single island. The thicknesses differ by up to five orders of magnitude. So the drawing lies about thickness on purpose, to keep all layers visible.

The top layer is the one we are going to cut. A hundred nanometres of
n-doped amorphous silicon. Under it, there's seven and a half nanometres of
gate oxide: the thinnest film on the wafer. The gate etching has to stop on it,
and leave it intact.

The three below are the ones we must not cut. Thirty nanometres of silicon — the
active island, the film the transistor channel is actually built in. 145 nanometres of BOX. And then 725 micrometres of handle silicon.

Before any etching, one more film will be deposited on top of the stack. That
film is the hard mask.

▶ **按 →**

> 已砍掉、不念（被问到再补）：① 剖面不平、中间那道台阶是 active island；
> ② 顶部显微图是 50×、上排 NFET 下排 PFET 画得略宽、无 work-function 金属 ⇒ 两者目前电学相同。
> 若还要短：P2 并进 P1，P4 只留三个数（30 / 145 / 725 µm）。

---
## 03 · PECVD SiO₂ hard mask — ~30 s

> 目的：说明"还要再加一层膜"、40 nm 是给后面的刻蚀留的。
> 动画 30 s，长膜就在画面里，头两句跟着长膜说。左下角有反应式和 400 °C / 13 s 的横标，参数不念。

One more film goes on top of the stack: forty nanometres of silicon dioxide, put
down by PECVD (plasma-enhanced chemical vapour deposition).

Silane and nitrous oxide go in; the plasma breaks them into radicals, and the
radicals build the oxide on the surface. The layer growing on the cross-section is
that film.

Forty nanometres is chosen for what comes later: this is the hard mask, and it has
to survive the silicon etch.

▶ **按 →**

> 被问到再补：① 等离子体的作用就是替温度提供能量，所以 400 °C 就能长，底下已有的膜
> 不会被高温动到；② PECVD 氧化层不如炉管氧化层致密（含氢、密度低、颗粒多），但作为
> 掩模不需要致密，需要的是均匀和够厚。

---
## 04 · PECVD dual — ~30 s

> 目的：两片并排 —— 上面是产品片（顶上多了硬掩模），下面是监控片（裸硅 + 同一层氧化层）。
> 原来写在 P3 末尾、[翻页] 之后的那三句监控片内容挪到这里：这页才是两片同时在画面里。

The thickness is set by the deposition time, so it has to be measured — and it's hard for an
ellipsometry to do it on a patterned wafer. So a second wafer, bare silicon, goes through the same process and gets measured instead.

[顿] And that wafer will be measured twice today: once now, and once after the main etch.

▶ **按 →**

> 若超时：把第二段压成 "The thickness is set by the deposition time, so it has to be
> measured — and not on a patterned wafer."

---
## 05 · Ellipsometry — ~60 s

> 目的：说明椭偏仪量的不是厚度，而是反射对偏振的改变；再由五个点得出"膜是均匀的"。
> 动画 50 s（五个点各 10 s：移动 → 光束 → 重画拟合 → 出数），所以前两段要在前 20 s 内讲完。
> 屏幕上已经有 37.020 ± 0.120、37.009、n=1.518，五个值不要逐个念。

Ellipsometry does not measure thickness directly. It sends polarised light in and reads the
polarisation that comes back: linear before the wafer, elliptical after it. The two
angles are the measurement — psi is the amplitude ratio, delta the phase difference.

Fit them across a range of wavelengths and two things come out at once: refractive
index and thickness. Here we get film is 37.02 nanometres. 

We measure five points: the centre, and four at sixty millimetres out.

The five agree to plus or minus 0.12 nanometres. That means the film is uniform.

Against the forty-nanometre target it is 7.4 per cent thin, inside the
ten-nanometre window. It passes.

▶ **按 →**

> 若超时：删掉 "psi is the amplitude ratio, delta the phase difference"（省 ~8 s），
> 只留 "the two angles are the measurement"。
> 被问到再补：单波长只有两个角量、却要解两个未知数（n 和 d），所以现代椭偏仪扫一段
> 波长，用整条谱去拟合；n 若定错，d 会跟着偏，两个数必须成对报告。

---
## 06 · Surface prep (VPO) — ~45 s

> 目的：说明为什么涂胶前还要多一道表面处理，以及"一道弱工序在多久之后才暴露"。
> 动画 15 s，分四幕，左下角小标签自己会翻：bake · pump down → HMDS vapour → reaction → purge · vent。
> 稿子的第二段正好踩这四幕；不要念参数表（Chamber / Dehydration / HMDS / Result）。

The oxide we just deposited is hydrophilic: it ends in OH groups, it holds water,
and resist does not stick to that. So there is one more step before the resist —
dry the wafer, then make it repel water. 

We pump down and bake: the water leaves. HMDS vapour goes in and reacts with the OH groups. What is left is a
monolayer — one end bonded to the oxide, the methyl end pointing out. Then purge,
and vent.

One molecule thick. It changes no geometry; it changes the surface energy. The oxide
now repels water instead of holding it.

▶ **按 →**

> 被问到再补：HMDS = hexamethyldisilazane；反应放出 NH₃，把 Si–OH 换成
> Si–O–Si(CH₃)₃，所以表面从亲水变疏水。失败机理：胶与氧化层之间留着水膜，显影液从
> 界面渗进去，细线先倒——光学检查在显影之后才看得见，所以这条工序的错误总是"迟到的"。

---
## 07 · Spin coating & edge bead — ~45 s

> 目的：dynamic dispense（晶圆已经在转）、转速定厚度、以及边缘胶珠为什么必须在湿的时候洗掉。
> 动画 15.4 s：落胶打湿 → 铺满 → 高速旋转（图形拖成模糊）→ 减速停 → 边缘冲洗 → 背面冲洗；
> 左下角小标签依次是 rim rinse / backside rinse。稿子照这个顺序走。

Resist, 1.2 micrometres — and it goes onto a wafer that is spinning: 5000 rpm, 30 seconds. The film is still liquid while it spins up, and that is when the thickness is decided — faster spin, thinner film.

The spin also throws resist to the rim, where it piles up into a bead several times
thicker than the film. That bead dries unevenly, flakes, and dirties everything the wafer touches next. So it is rinsed off from the wafer: the rim first, then the backside.

▶ **按 →**

> 被问到再补：厚度大致按 1/√ω 走（离心力与黏性阻力平衡），所以转速是唯一能定厚度的
> 旋钮；dynamic dispense 省胶、且避免静止落胶先局部干掉。

---
## 08 · Soft bake — ~30 s

> 目的：把"低温烘"讲成两件事——把溶剂赶走、把膜定住；并交代这一页定下的东西后面收不回来。
> 画面：热板从下面升上来，膜里飘出标着 solvent 的字；左下角 95 °C · soft bake。

The plate comes up under the wafer at 95 degrees. The film left the spinner full of
solvent. The solvent leaves here.

95 degrees sits below the glass transition so the film won't flow. The solvent
leaves, and the film hardens. It does not melt.

Two things are settled here: One is the
adhesion to the oxide. The other is the stress the spin left in the film.

▶ **按 →**

> 被问到再补：软烘不足的典型后果是显影后 CD 偏移、边缘发黏；过度则感光度下降，等于
> 偷偷降低了剂量。95 °C 同时低于玻璃化转变和光敏剂开始分解的温度，两个约束夹出来的。

---
## 09 · Stepper exposure — ~30 s

> 目的：说明"一场一场曝光"是什么、光只改溶解速率、剂量是旋钮；最后落到唯一可能出错的地方——对准。
> 注意：这张图里**晶圆盘本身不变化**，变化在右上角截面卡：resist 那一行一段一段变暗，就是一场一场曝光完。
> 稿子的第三段要把观众的眼睛引到那里去。

A stepper does not expose the whole wafer at once. It projects the reticle onto one
field, steps, and repeats.

Field by field means the lens only has to be good over a few square centimetres, and
the reticle only has to carry one copy of the pattern.

The light does not draw a shape. It changes how fast the resist will dissolve. The
shape only appears at development.

▶ **按 →**

> 被问到再补：步进机的存在理由是视场——镜头只在几厘米内成像好，所以掩模只需装一片
> 图形，靠台子移动铺满整片；对准靠 LAB1 的标记，标记是被后续沉积盖住的形貌台阶，靠
> 衍射信号找回来。

---
## 10 · Post-exposure bake — ~30 s

> 目的：按"干涉导致不均匀 → 加热扩散变均匀"讲，不要一上来先介绍流程。
> 画面时序：热板先冷，右上卡片是浓度-深度曲线，波动的；约 5 s 起曲线拉直、resist 里的
> 横带消失，左下角小标签由 no heat 换成 110 °C。

The light does not stop at the surface. It goes through the resist, reflects off the
silicon underneath, and comes back up. Incident and reflected interfere, so the
intensity ripples with depth. So the film is not exposed uniformly along height.

At 110 degrees the photoproduct diffuses from high to low. That flattens the concentration profile. 

▶ **按 →**

> 被问到再补：i-line 的 DNQ/酚醛体系不是化学放大胶，这里没有"酸扩散"；PEB 是让光产物
> 在膜内扩散、把驻波（周期约 λ/2n ≈ 110 nm）抹平，同时提高显影对比度。驻波来自曝光光
> 在 resist/衬底界面反射后与入射光干涉。

---
## 11 · Development — ~35 s

> 目的：把"图案第一次变成实物"说清，并交代湿法显影唯一的控制量是时间。
> 画面：晶圆上出现橙色栅线条；右上截面卡里，orange 的 resist 只剩在栅上，场区露到硬掩模。
> 这张图没有动画（进页即是终态），所以直接描述看到的。

TMAH, 2.6 per cent. Thirty seconds, then thirty seconds again. Where the resist was
exposed it dissolves. Where it was not, it stays.

It is a positive resist, so the light removes. The mask was dark over the gates, so the
stripes that survive are the gates.

The cross-section shows it. The orange is left on the gate only, and the field is
down to bare oxide. The pattern finally shows up.

From here the resist is the mask that the next etch obeys.

▶ **按 →**

> 被问到再补：TMAH 是碱性水溶液，正胶的曝光区羧基化后溶于碱；两道 30 s 是配方给的
> 总时间 60 s。显影是等向的，靠的是溶解速率对比（几个数量级），不是靠方向性——所以
> 对比度差就会侧蚀、线条变细。

---
## 12 · Inspection ① — ~23 s

> 目的：停车检查页，只说到"图形在、没缺没重"为止；其余（pitch 与 CD 的区别、返工代价、
> 后面还有哪些检查）都留到被问到再说。
> 画面：150× 光学图占了大半屏，两处标了 8.16 / 8.08 µm，是两条线之间的**间距**；没有动画。

This is the second checkpoint. Development is finished, and the wafer goes under the
microscope at a hundred and fifty times.

The pattern is in the right position, and nothing is missing, doubled or broken.

We can go to the next step.


▶ **按 →**

> 被问到再补，三层：
> ① 屏幕上两个数（8.16 / 8.08 µm）是显微软件标出的两条线间距 = **pitch，不是线宽**，本次
>   没有独立 CD 测量；掩模上的线宽是另一组数（0.72–1.33 µm），到成品页再讲。
> ② 这一步出错只要一轮光刻（去胶→重涂→曝光→显影）就能回到原点；代价随工序往后递增。
> ③ 硬掩模刻坏还能剥掉重新沉积（= 新沉积 + 新光刻）；只有刻穿栅氧才真的没救。所以后面
>   还有检查：硬掩模刻完一次、去胶后再一次。

---
## 13 · Hard-mask etch — ~45 s

> 目的：交代"为什么必须先把图形转进氧化层"，以及 F 化学没有方向性 ⇒ 会侧蚀
> （卡片顶部自己写着 no direction, so it undercuts）。
> 画面：整屏是"一个窗口"的放大卡，进页时氧化层还是整片；约 1 s 起窗口处往下开，
> 边缘是圆弧（侧蚀），最后开到 a-Si。

The resist cannot carry this pattern through the whole gate etch. That etch is
chlorine with oxygen in it, and oxygen is what ashes resist. So we transfer the pattern to
the oxide first.

That is this step: CHF₃ and CF₄, fluorine chemistry, opening the oxide where the resist
is open. It is timed, not endpointed, and it finishes a little way into the silicon
below.

Fluorine etches sideways as fast as it etches down, so the window comes out wider than
the resist opening.


▶ **按 →**

> 被问到再补：F 基刻蚀的配方与时间没有记录（这是本 lab 最关键的空缺）；卡片上那句
> "chemical only — no direction" 就是等向刻蚀，侧蚀量的上限约等于被刻掉的膜厚（37 nm），
> 这点侧蚀会把掩模上的线宽略微放大。

---
## 14 · Resist strip — ~20 s

> 目的：三件事，各一句——去胶、掩模任务交给氧化层、显微镜检查。机理全部留到被问。
> 画面：STRIP 卡片（O₂ 从各方向吃胶）；右下方 20× 显微图（硬掩模已开口）。


We use oxygen plasma to remove resist. The masking job passes to the oxide. From here the pattern is carried by thirty-seven nanometres of SiO₂.

Then we check under the microscope, making sure the pattern is still correct.

Then the main etch.

▶ **按 →**

> 被问到再补：① 顺序之所以反直觉，是因为 O₂ 既是氯刻蚀的侧壁钝化剂、又正是烧胶的东西
> （见本页 note）；② 去胶不需要方向性，胶下面就是硬掩模，吃过头也只停在氧化层上；
> ③ 腔体要求 organic-free，避免有机物跟着片子进氯化学。

---
## 15 · Main etch · breakthrough — ~25 s

> 目的：交代还剩一层东西挡着——自然氧化层；氯自由基碰不动它，只有离子能把它打掉；
> 所以这一段必须无氧，也因此是等向的、只能 12 秒。
> 画面：卡片顶部写着 Cl⁺ sputters the native oxide · Cl• etches a-Si · no O₂，
> 左上角标 native oxide；窗口里 a-Si 被咬出一个浅的圆弧坑（比开口宽）。

The wafer goes in clean and the mask is open. What is still in the way is the native
oxide: a nanometre or two of SiO₂ that grows back whenever silicon meets air.

Chlorine radicals cannot touch it. Only the ions can, and they come straight down.
That is the whole job of these twelve seconds.

▶ **按 →**

> 被问到再补：自然氧化层的厚度是 1–2 nm 量级，它的存在让氯刻蚀硅这件事分成两步：
> 先物理打掉氧化层（离子），再化学刻硅（自由基）。破口段的侧蚀量因此正比于时间，
> 这就是 12 s 这个数字的全部意义。

---

## 16 · Main etch · with oxygen — ~85 s

> 目的：各向异性的来源（氧四面八方来、离子只从上有）＋**停止逻辑**（终点信号 + 过刻）。
> 画面：卡片顶部写着 Cl• + O• → Si–O–Cl on every face · Cl⁺ clears the floor only；
> 右壁细青条标注 inhibitor / Si–O–Cl · a few nm；窗口底部已经开到黄色的栅氧线。

The twelve seconds only opened the surface. An etch with no direction cannot make gates.

So oxygen goes in: twenty seconds of Cl₂, HBr and O₂. Oxygen arrives from every
direction and coats every exposed face with a thin Si–O–Cl layer.

The ions come from above only, so they clear that layer on the floor and nowhere else.
The floor goes down; the walls never move sideways.

And when the floor reaches the gate oxide, there is no silicon left to consume, so the
chlorine radicals stop being used up and their signal climbs. That is the endpoint.

Etching keeps going a few seconds. The oxide etches twenty-five to forty
times slower, so an over-etch clears the last patches without cutting into it.

▶ **按 →**

> 被问到再补：抑制剂是 Si–O–Cl 复合层，几纳米厚，靠 O• 在**所有**暴露面上形成；离子
> 垂直入射，只在底部打掉它，侧壁因此处在被钝化—被溅射的平衡里，横向速率趋近零。
> 端点靠光谱看 Cl 自由基信号上跳；过刻量按选择比 25–40:1 算，留给氧化层的余量 ≈ 11 s。

---

## 17 · Second ellipsometry — ~40 s

> 目的：让实物数据说话——硬掩模到底被刻掉多少；顺带用五点散开了解释为什么要过刻。
> 画面：左边是五点前后柱状图（每组都标了差值 −3.09 / −3.95 / −5.43 / −3.68 / −3.67，
> 底部写着 whole loss is 3.96 nm — 10.7 %，so the bars barely move）；右上角是监控片截面，
> 标着 33.06 nm、虚线 was 37.02 nm。

The monitor wafer goes throught the same main etching recipe and comes back into the ellipsometry.

Oxide stickness was 37.02 nanometres. It is now 33.06. 3.96nm gone, and 89 per cent of
the mask still there. This implies that the hard mask only loss 3.96nm stickness, far from broken.

▶ **按 →**

> 被问到再补：3.96 nm 是破了口之后总损失；若全部算在 20 s 主刻上得 0.198 nm/s，
> 若把 12 s 破口也摊进去则 0.124 nm/s，所以 0.198 是上界。s² 从 0.014 涨到 0.76，说明
> 刻蚀本身不均匀（等离子体分布），不是测量变差。

---

## 18 · Inspection ④ · the result — ~25 s

> 目的：这一页只说结论——图上没看到问题，一切正常，可以交接给下一步。
> 画面：150× 蓝底成品图（caption: AFTER THE MAIN ETCH · GATES OVER ISLANDS），
> 图上标了 0.80 / 1.33 / 0.96 / 0.72 µm 四个宽度；右上截面卡是叠层的模型图，
> 帽的高度来自 P17 的椭偏，不是这张照片看出来的。

This is the last look.

The gates are continuous: no break, no bridge, no missing line. The four widths marked on
the picture run from 0.72 to 1.33 micrometres.

The one thing optics cannot judge is the sidewall, and that needs a SEM cross-section.

So the wafer passes, and it goes on to the next lab.

▶ **按 →**

> 被问到再补：四个数是显微软件在图上标注的、版图上本来就有的几种宽度（0.72 / 0.80 /
> 0.96 / 1.33 µm），不是同一版图宽度的重复测量，所以不能当 CD 均匀性读。侧壁角与
> notching 只能靠 SEM 剖面，本 lab 没做——所以"通过"只针对图形，不针对剖面。

---

## 19 · Summary — ~80 s(预计不展示)

> 目的：三个数 + 一个缺口 + 交给 LAB4。不要念参数表，参数在屏幕右边。
> 画面：镜头拉回整片晶圆，右侧是 What the numbers say 与三条参数。

Three numbers, and one that is missing.

The mask loses 0.198 nanometres per second in the main-etch chemistry. That is the only
etch rate this lab actually measured.

From it, the selectivity is twenty-five to forty to one: silicon goes that much faster
than the oxide. Which is why an over-etch is safe by about a factor of five.

And what is missing is the hard-mask etch time. The fluorine step was a timed recipe,
and nobody wrote the time down, so the budget has one hole in it.

What leaves the lab is a gate stack with gates on it and the cap still on top. NFET and
PFET are still identical. They separate in LAB4, at the implant.

▶ **按 →**

> 被问到再补：0.198 nm/s 是上界口径（若把 12 s 破口摊进去是 0.124）；选择比
> S = R_a-Si / R_SiO2 = 5.0 / 0.198 ≈ 25，按 a-Si 速率 5–8 nm/s 取则 25–40。过刻安全
> 系数 ≈ 5× 是量级比较（37 nm 掩模 vs 11 s 过刻 × 0.198 nm/s），不是精确预算。

---

## 时间标记

`标题标定` 是各节标题里的数（由作者填写，助手不改动）；`omni 实测` 是把该节正文交给
Qwen omni 逐字朗读后的音频时长（`_shot/tts_time.py`，结果在同目录 `tts/timing.json`）。

合计：标定 **840 s ≈ 14.0 分钟**，omni 实测 **587 s ≈ 9.8 分钟**。

| 页   | 标题                        | 标题标定 | omni 实测 |
| --- | ------------------------- | ---- | ------- |
| 01  | Opening                   | 20 s | 13.8 s  |
| 02  | Where we start            | 95 s | 58.3 s  |
|     |                           |      |         |
| 03  | PECVD SiO₂ hard mask      | 30 s | 33.8 s  |
| 04  | PECVD dual                | 30 s | 22.6 s  |
| 05  | Ellipsometry              | 60 s | 46.2 s  |
|     |                           |      |         |
| 06  | Surface prep (VPO)        | 45 s | 34.9 s  |
| 07  | Spin coating & edge bead  | 45 s | 34.2 s  |
| 08  | Soft bake                 | 30 s | 25.0 s  |
| 09  | Stepper exposure          | 30 s | 22.7 s  |
| 10  | Post-exposure bake        | 30 s | 24.6 s  |
| 11  | Development               | 35 s | 33.9 s  |
| 12  | Inspection ①              | 23 s | 12.8 s  |
|     |                           |      |         |
| 13  | Hard-mask etch            | 45 s | 38.9 s  |
| 14  | Resist strip              | 20 s | 17.0 s  |
| 15  | Main etch · breakthrough  | 25 s | 23.0 s  |
| 16  | Main etch · with oxygen   | 85 s | 55.4 s  |
| 17  | Second ellipsometry       | 40 s | 22.1 s  |
| 18  | Inspection ④ · the result | 25 s | 21.7 s  |

