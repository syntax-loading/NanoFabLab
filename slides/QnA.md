# LAB3 · Gate Formation — Q&A 答问手册

配 `lab3_process_flow.html` 和 `SCRIPT.md` 用。讲完之后（或被打断时）看这个。

## 怎么用

1. **任何问题都按三句回答**：一句结论 → 一个数 → 一句边界（"that is the only number we measured" / "we did not record that"）。不要重讲流程，问什么答什么。
2. **不知道就说不知道**，然后补一句为什么（配方是设备内部设定，学生读不到）。§8 有六个现成句子，直接念。
3. **数字只有一个口径**：先说是什么数，再说它是什么（均值 / 上界 / 间距 / 时间），别让提问的人替你定义。

图例：**✅** 已核实 · **❓** 未核实或推断 · **⚠️** 陷阱（容易答错的地方）

正文里带引号的英文 = 照念；`> ` 开头的中文 = 给你看的，不念。

---

## 0 · 先记住这些

**十个必须脱口而出的数**

| 数 | 是什么 | 口径 |
|---|---|---|
| **37.02 nm** | 硬掩模沉积后厚度 | 五点均值 37.0198，s² 0.0144，n 1.5216 |
| **33.06 nm** | 主刻后厚度 | 五点均值 33.0558，s² 0.7631 |
| **3.96 nm** | 损失 | = 37.02 − 33.06，占原厚 **10.7 %**，剩 89.3 % |
| **0.198 nm/s** | SiO₂ 在 Cl 化学中的刻蚀速率 | 3.96 nm / 20 s，**上界** |
| **25–40 : 1** | 选择比 | 按 0.198 算得 25，按 0.124 算得 40；对外只说这个区间 |
| **≈ 11 s** | 过刻安全窗 | 让栅氧掉 30 %（2.25 nm）的过刻量 |
| **100 nm** | n⁺ a-Si 栅电极厚度 | 主刻 20 s 刻透 ⇒ 5.0 nm/s（假设值） |
| **7.5 nm** | 栅氧 | 沉积所得，刻蚀必须停在这上面 |
| **145 / 725** | BOX / 手柄 | nm / µm，别把单位说错 |
| **112.5 mJ/cm²** | 曝光剂量 | i-line 365 nm |

**三个工艺时间**：PECVD 13 s · 破口 12 s · 主刻 20 s。

**一句话总结（10 秒版）**
> "We put forty nanometres of oxide on the stack, patterned it with resist, transferred the pattern into the oxide, stripped the resist, and etched the gate in chlorine. The mask lost four nanometres, and the gate oxide stayed inside its over-etch budget. The only etch rate this lab measures is the oxide's."

---

## 1 · 定场三句

被问"先一句话说说你们做了什么"：

**A** — "We added the hard mask to an SOI wafer that already had the active islands and the gate stack. We printed the gate pattern, transferred it into the oxide, and used that oxide to etch the gate. The wafer leaves with the lines intact and the cap still on."

被问"你们自己做了什么"：见 Q40。

---

## 2 · 叠层与设计选择

### Q1 · 你们的叠层是什么？ / "What is the stack?" ✅
**A** — "From the top: thirty-seven nanometres of PECVD oxide from this lab, then a hundred nanometres of n-doped amorphous silicon, the gate electrode. Then seven and a half nanometres of gate oxide, and under that the SOI film — thirty nanometres of silicon, a hundred and forty-five of buried oxide, and a seven-hundred-and-twenty-five-micrometre handle wafer. Two hundred millimetres across."

> 六个数：37 / 100 / 7.5 / 30 / 145 / 725（单位 nm 除最后 µm）。
> ⚠️ 别说 "poly-Si"；别说 "185 nm BOX"、别说 "725 nm handle"——这是同学草稿的错（记录 §6-1、§6-2）。
> ⚠️ 讲义 L02 p6 写 top Si 是 **20 nm**，我们这份是 TA 手绘标注的 **30 nm**。被问就按自己记录答，并说明依据是 TA 标注的剖面。
> 前两步：LAB1 = 对准标记，LAB2 = active islands（deck p1–p2）。

### Q2 · 为什么用 SOI？ / "Why SOI?" ✅
**A** — "Because the channel sits on an oxide. The transistors are isolated from each other by the buried oxide, so there is no latch-up path, and the isolation step becomes a simple etch instead of a trench process with CMP. A film that thin is also fully depleted, so the gate has full control of the channel."

> 代价：mesa 隔离没有 CMP，栅氧跨过岛边角，会有一个寄生 corner device（记录 §8）。我们没有测它。

### Q3 · 为什么栅氧要做 7.5 nm 这么厚？ / "Isn't that ancient?" ✅
**A** — "In a modern flow it would be one or two nanometres. Seven and a half is a design choice forced by this process. There is no separate stop layer, so the gate oxide itself is the stop. A thicker oxide plus a selectivity of twenty-five to forty to one is what makes a timed over-etch safe."

> 这是本 lab 最"有设计感"的一个数，答好了很加分。代价：C_ox 低 5–7 倍，驱动电流低（记录 §8）。

### Q4 · 栅氧为什么不热氧化？ / "Why deposited?" ✅
**A** — "Because growing it would eat the channel. Thermal oxidation takes about zero point four four nanometres of silicon for every nanometre of oxide, so seven and a half nanometres of oxide would consume about three point three of the thirty-nanometre film — a ninth of it. So the oxide is deposited instead, and it covers the island top and the slope."

> 单位换算 0.44 × 7.5 ≈ 3.3 nm ≈ 30 nm 的 11 %。
> 第二层理由：温度预算 400 °C（L02 p13：全流程以 ~400 °C 退火收尾）。

### Q5 · 为什么是 a-Si 不是 poly-Si？ / "Why amorphous?" ✅
**A** — "Temperature. Polysilicon needs about six hundred degrees to crystallise, and this flow never goes above four hundred. So the gate stays amorphous. It is heavily doped so that it conducts, and that is all an electrode has to do here."

> ⚠️ 说 poly-Si 就等于说错整条流程。400 °C 天花板有三处依据：PECVD 范围 300–450（L09 p3）、全片 a-Si、末道退火 400 °C（L02 p13）。

### Q6 · 为什么没有 TiN？为什么 NFET 和 PFET 一样？ ✅
**A** — "Because both transistors get the same gate. The whole film is n-doped, so the NFET and the PFET are physically identical at this point. A dual-gate flow needs a work-function metal to shift the PFET threshold. We do not have one, so the PFET threshold will land high — of the order of a volt."

> 记录 §8 第一条差异。**分化在 LAB4**（L02 p11：spacer + 掺杂激活）。
> ⚠️ 数字"1 V 量级"是估算，不要说成"测出来 1.5 V"。

### Q7 · 40 nm ±10 nm 这个判据为什么放得这么松？ ✅
**A** — "Because there is a hundred nanometres of silicon under the mask acting as a stop. If the oxide comes out three nanometres thin, the timed etch just runs three nanometres further into that silicon — three per cent of it. The tolerance is loose because the stop layer is generous."

> 记录 §8 末段。⚠️ 但"多刻的那 3 nm"会转成开窗的横向偏差 —— 见 Q25。

---

## 3 · 硬掩模与 PECVD

### Q8 · 为什么不直接用胶当掩模？ / "Why a hard mask?" ✅
**A** — "Because the main etch has oxygen in it, and oxygen is exactly what removes resist. The resist could not hold a chlorine etch with oxygen in it. So the pattern is transferred into the oxide first, and the oxide carries it through the main etch. That is what the extra PECVD step is for."

> 讲义 L08 p24 有原话：C in chamber reduces selectivity to SiO₂ ⇒ 用 SiO₂ 硬掩模、加破口、加终点。
> 顺序陷阱见 Q26。

### Q9 · 为什么用 PECVD，不用炉管或 LPCVD？ ✅
**A** — "Temperature. LPCVD is five hundred to eight hundred degrees and a furnace oxidation is higher still. PECVD runs at four hundred because the plasma supplies the energy instead of the wafer. Whatever is already on the wafer stays where it is."

> L09 p3（PECVD 300–450 °C）、L09 p18（SiH₄ + N₂O，T ≤ 400 °C）。
> 反应式（deck 左下角）：SiH₄ + 2 N₂O → SiO₂ + 2 N₂ + 2 H₂。

### Q10 · PECVD 氧化层是不是质量更差？ ✅
**A** — "Yes, in the ways that matter for a dielectric. It is less dense, it contains hydrogen, it can have pinholes, and it etches five to ten times faster in HF than a thermal oxide. For a mask none of that matters. A mask has to be uniform and thick enough, not dense."

> L09 p18 原话。这是"选对指标"型答案 —— 承认短板，说明为什么不影响用途。

---

## 4 · 光刻

### Q11 · 为什么还要一个监控片？ / "Why a second wafer?" ✅
**A** — "Because you cannot measure a thin film on a patterned wafer with an ellipsometer. So a bare silicon wafer goes through the same deposition and it is measured instead. It comes back a second time, for the measurement after the etch."

> 两层理由：① 图形片上有台阶与图形，椭偏拟合不成立；② 裸片没有埋氧层要减。
> 它**不是**备用片：同一腔、同一 32 s（12 + 20）。

### Q12 · 椭偏仪怎么测厚度？ ✅
**A** — "It does not measure thickness. It sends polarised light in and reads the polarisation that comes back. Two angles change with the film, psi and delta. Fitted across a range of wavelengths they give two numbers at once, index and thickness. Here that is thirty-seven point zero two nanometres at an index of one point five two one six."

> ⚠️ 被问 n：**1.5216** 是五点均值；不要用单点 1.518（那是第 3/4 点的值）。
> 为什么必须扫谱：单波长只有两个角量却要解两个未知数（n 和 d），所以 n 定错 d 会跟着偏，两个数必须成对报告。

### Q13 · 五个点怎么取的？均匀性多少？ ✅
**A** — "The centre and four points at sixty millimetres out, along x and y. The five sit within zero point three one nanometres of each other, one sigma is zero point one two. That is zero point eight per cent of the film — the deposition is uniform."

> 200 mm 片半径 100 mm，60 mm 采样到 60 % 半径。
> ⚠️ "±0.120" 是 1σ，不是极差的一半；极差是 0.308 nm。被追问就说清楚。

### Q14 · 比目标薄 2.98 nm，算不合格吗？ ⚠️
**A** — "The window is ten nanometres on thickness and we are two point nine eight short of forty. That is inside. The seven point four per cent is the same gap written as a percentage of the target — it is not the criterion."

> ⚠️ 这是同学草稿的经典错：把 "Deviation −7.42 %" 和 "±10 nm" 放在一起比，量纲不对（记录 §6-5）。
> deck 页面写 −7.42 %，按我们自己的数算是 −7.45 %。对外**只说两件事**：差 2.98 nm，约 7.4 %。不要说具体到小数第二位，避免被抓。

### Q15 · HMDS 是干什么的？ ✅
**A** — "The oxide is hydrophilic. It ends in hydroxyl groups, it holds water, and resist does not stick to that. HMDS replaces the hydroxyl end with a methyl end, so the surface repels water instead. It is one molecule thick, so nothing changes geometrically."

> 反应放出 NH₃：Si–OH + (CH₃)₃Si–NHSi(CH₃)₃ → Si–O–Si(CH₃)₃。
> 失败长什么样：界面留水膜，显影时细线先倒 —— 而光学检查在显影之后才看得见，所以这种错总是"迟到的"。

### Q16 · 胶为什么 1.2 µm、5000 rpm？ ✅
**A** — "The speed sets the thickness — roughly as one over the square root of omega — so five thousand revolutions per minute for thirty seconds is what makes it one point two micrometres. Both numbers come from the track's recipe. The thickness has to be enough to survive the fluorine etch, and one point two micrometres does that with a large margin."

> dispense 是 **dynamic**：晶圆已经在转的时候落胶，所以它一下就铺开，**随后的升速**才定厚度。
> 省胶、也避免静止落胶先局部干掉。

### Q17 · 边缘胶珠为什么要洗掉？ ⚠️
**A** — "Because it is several times thicker than the film. It dries unevenly, it flakes, and the flakes land on the bake plate, the chuck, and everything the wafer touches next. So the rim and the backside are rinsed while the resist is still wet."

> ⚠️ **不要说"因为接触式曝光"** —— 这台是 Nikon NSR 投影步进机。理由是颗粒 / 热板 / 背面平整度（slides/README 明确记着这条已被删）。

### Q18 · 软烘为什么 95 °C？ ✅
**A** — "Two jobs. It drives the solvent out of the film, and it hardens the film without letting it flow — ninety-five is below the glass transition. What gets set here is what the rest of the process lives with, the adhesion and the stress in the film."

> 软烘不足 → 显影后 CD 偏、边缘发黏；过度 → 感光度下降，等于偷偷降了剂量。95 °C 是被"低于 Tg"和"低于光敏剂分解"两个约束夹出来的。

### Q19 · 步进机在做什么？剂量是什么？ ✅
**A** — "It exposes one field at a time. The reticle is projected onto a few square centimetres, then the stage steps and repeats — so the lens only has to be good over that field, and the reticle only has to carry one copy. The dose is the energy per area. It decides how far the reaction goes in the resist; the shape only appears at development."

> 参数：i-line 365 nm、112.5 mJ/cm²、step and repeat。
> ⚠️ 曝光不画图形，只改溶解速率 —— 这是最常被追问的一句。

### Q20 · 为什么要 PEB？是不是化学放大胶？ ⚠️⚠️
**A** — "No, it is not a chemically amplified resist. This is an i-line DNQ resist, so there is no acid diffusing anywhere. The bake does something simpler. Light comes down, reflects off the silicon, and interferes with itself, so the exposure ripples with depth. At a hundred and ten degrees the photoproduct diffuses and that ripple flattens."

> **本 lab 最容易被抓的一处。** i-line = DNQ/酚醛，非 CAR ⇒ 没有"酸扩散"。
> 驻波周期 ≈ λ/2n ≈ 365 / (2×1.6) ≈ 110 nm。讲义 L07 p7（PEB 抑制驻波）、p19（DNQ 的 Wolff 重排 → 羧酸，溶于碱性显影液）。

### Q21 · 显影是什么化学？为什么两道 30 s？ ✅
**A** — "TMAH, two point six per cent — a basic developer. Exposure turns the resist into a carboxylic acid and the base dissolves it. It is a positive resist, so the exposed part goes. The mask was dark over the gates, so the stripes that survive are the gates. Thirty seconds, then thirty seconds again — the recipe's sixty in total."

> 显影是**等向**的，靠溶解速率对比（几个数量级）而不是方向性 ⇒ 对比度差就侧蚀、线变细。

### Q22 · 图上标的 8.16 µm 是线宽吗？ ⚠️
**A** — "No. That is the pitch, the distance from one line to the next. We do not have an independent line-width measurement in this lab. The widths on the mask are a different set of numbers, seven tenths to one point three micrometres."

> ⚠️ 本 lab 最容易被误读的数（记录 §6-6）。成品页那四个数（0.72 / 0.80 / 0.96 / 1.33 µm）是**版图上本来就有的四种宽度**，不是同一宽度的四次重复 ⇒ **不能当 CD 均匀性读**。
> 被问 "who chose the eight micrometres"：图形是课程测试版图，跟着 lab 来的，不是我们设计的。

---

## 5 · 刻蚀

### Q23 · 为什么先做 F 刻、而且必须停在 a-Si？ ✅
**A** — "Two reasons. The resist cannot survive the chlorine step, so the pattern has to be in the oxide before that step. And the oxide etch has to stop in the silicon below. It is a timed recipe that is allowed to go a little way into the a-Si, so that the window is definitely open everywhere."

> ⚠️ F 刻的**时间与配比没有记录** —— 本 lab 最大的空缺。被问就承认，见 Q42。讲义 L08 p23 有 CHF₃ + CF₄ 调 C/F 比的原话（"that is how we do it in the lab"）。
> ❓ "让它多走一点"的理由是均匀性（保证全片都开窗）—— 这是推断，不是设备说明。

### Q24 · F 刻会侧蚀多少？ ⚠️
**A** — "Fluorine radicals are neutral, so they arrive from every direction. At this carbon-to-fluorine ratio there is not enough polymer on the wall to stop them, so the window comes out wider than the opening in the resist. The lateral extent is at most of the order of the film that was removed — about thirty-seven nanometres."

> 记录 §4.5：侧蚀上限 ≈ 膜厚。
> **方向怎么说才不出错**：开窗**变宽** ⇒ 留下来的氧化层**变窄** ⇒ 栅线比掩模上的线窄。所以只说 "the window widens"，再说 "the line between two windows is narrower"。⚠️ 记录 §4.5 那句写的是 "CD 变宽"，指的是开窗那一侧 —— 别顺着说成"栅变宽"，方向会说反。

### Q25 · 膜薄了 3 nm，怎么会影响 CD？ ✅
**A** — "The oxide etch is timed, so it runs the same time whatever the oxide's thickness is. If the oxide is three nanometres thin, the plasma reaches the silicon three nanometres early and spends that time in the silicon instead. That chemistry is not directional, so the extra depth comes with extra width. A few nanometres, not a few tens."

> 记录 §4.5：对栅高无所谓（3 %），对开窗是几 nm。这就是"±10 nm 的判据不妨碍 CD"那条线的另一半。

### Q26 · 为什么先去胶，再主刻？ ⚠️
**A** — "Because the main etch contains oxygen and oxygen is what removes resist. If the resist were still there it would be ashed during the main etch, and its carbon would end up in the plasma and on the sidewalls. So the masking job is handed to the oxide first, and the resist is stripped before the wafer goes back in."

> 反直觉的顺序，**必须能解释**：O₂ 既是 Cl 刻蚀的侧壁钝化剂、又正是烧胶的东西。所以"要么有胶没钝化，要么有钝化没胶"。
> 去胶是 O₂ 等离子体（等向，不需要方向性），胶下面就是硬掩模，吃过头也只停在氧化层上。

### Q27 · 破口段为什么存在？为什么没有 O₂？为什么只有 12 s？ ✅
**A** — "Silicon always carries a native oxide — one or two nanometres that grows back when it meets air, and chlorine radicals cannot touch silicon dioxide. That layer has to be removed physically, by the ions. And that is why there is no oxygen in those twelve seconds — oxygen would put down the same inhibitor the step is trying to get through. No oxygen also means no sidewall protection, so the step is isotropic. That is also exactly why it lasts only twelve seconds."

> 讲义 L08 p24：破口用更高 RF、不加 O₂、更大流量。
> 侧蚀量正比于这 12 s —— 这就是 12 这个数字的全部意义。

### Q28 · 主刻为什么 Cl₂/HBr，为什么要加 O₂？ ✅
**A** — "Chlorine and bromine form volatile by-products with silicon and they are far more selective to oxide than fluorine is. Oxygen is what makes the etch directional. It arrives from every side and builds a thin Si–O–Cl layer on every exposed face. The ions only come from above, so they clear that layer on the floor and nowhere else. The floor goes down and the walls do not move."

> L08 p24：Cl/Br 的副产物对 SiO₂ 的选择比高于 F；加少量 O₂ 再提高；"C in chamber reduces selectivity to SiO₂，所以用 SiO₂ 硬掩模"。
> a-Si 速率（假设值）：100 nm / 20 s = 5.0 nm/s。

### Q29 · 你凭什么说侧壁是垂直的？ — 你没看到 ⚠️
**A** — "I cannot see it optically, and that is the honest answer. What I can say is the mechanism — the inhibitor on the wall is only removed where the ions land — and that nothing that looks like bowing or notching was visible at a hundred and fifty times. The sidewall angle needs a cross-section in the SEM."

> ⚠️ 永远不要把"没看到"说成"没有"。这一条答得诚实比答得漂亮重要。

### Q30 · 终点怎么判断？ ✅
**A** — "While there is still silicon at the bottom, the chlorine radicals are being consumed by it. When the floor reaches the gate oxide there is no silicon left to consume them, so their concentration in the plasma climbs. That rise is the endpoint signal. After that the recipe keeps going for a fixed over-etch."

> ❓ 实际的终点时刻、过刻秒数我们**没有记录**。被追问就说："the tool decides; we recorded the recipe, not the signal."

### Q31 · 为什么要过刻？余量多大？刻过头会怎样？ ✅
**A** — "Because the etch is not uniform. Our own data show it — after the etch the five points spread by two point two nanometres. So you have to go past the nominal endpoint to clear the last patches. The thing that limits the over-etch is the gate oxide. It etches at zero point one nine eight nanometres per second, so about eleven seconds takes thirty per cent of it, and about thirty-eight seconds would take all of it."

> 也就是**安全窗 ≈ 11 s，总预算 ≈ 38 s**。掩模不是限制项（见 Q38）。
> 记录 §4.3 的表格：3 s → 剩 92 %；5 s → 87 %；8 s → 79 %；11.4 s → 70 %。

### Q32 · 选择比 25–40:1，讲义写 >100:1，矛盾吗？ ⚠️
**A** — "The lecture gives more than a hundred to one as the requirement for a production gate etch, and that requirement exists because a production gate oxide is one or two nanometres thick. Ours is seven and a half, which is why twenty-five to forty is enough here. And our number is the worst case — the monitor is bare, so its oxide sees the whole thirty-two seconds, while the product wafer's oxide is only exposed during the over-etch."

> 顺序是：**先承认 25 比 100 小**，再说明为什么 25 在这里够用（栅氧 7.5 nm，不是 1.5 nm）。⚠️ 不要说"讲义错了"。
> 另外自己的上限也说明白：0.198 是**上界**（因为 12 s 破口段几乎不刻 SiO₂，损失全算在 20 s 上）。

---

## 6 · 数据与结论

### Q33 · 这些数里哪个最可靠？ ✅
**A** — "The two ellipsometry numbers. They are direct readings from a tool, five points each, and the raw files still exist. Everything else is derived from them by one assumption — that the a-Si is fully cleared in the twenty-second main step."

> 这是"分清原始数据与推导量"的答法：2 个原始 + 其余推导。

### Q34 · s² 从 0.014 涨到 0.76，是不是测坏了？ ✅
**A** — "Fifty times, so it is not measurement noise. The five points moved in a pattern rather than at random — one point lost three point one nanometres, another lost five point four. The spread after the etch is two point two nanometres, and an ellipsometer repeats the same point to far better than that. So the variance is the etch, not the tool."

> ❓ 我们没有做同点重复测量，所以"重复性远小于 1 nm"是仪器常识，不是本实验数据。被逼问就承认这一点。

### Q35 · 为什么有一个点偏低？ ❓
**A** — "One point at plus sixty millimetres in y came out two point two nanometres below the centre point. That is real non-uniformity of the plasma, but with five points I cannot tell you its shape. A map needs many more points."

> 记录 §4.4。⚠️ 不要猜"因为边缘"或"因为径向" —— 五个点撑不起形状判断。

### Q36 · 监控片能代表产品片吗？ ✅
**A** — "For the mask loss, yes — that is what it is for. Both wafers went through the same chamber for the same twelve and twenty seconds, and both films are blanket, so nothing shadows anything. What it does not represent is the product wafer's gate oxide, which is only exposed at the very end."

> ⚠️ 不要用监控片去证明"栅氧没被打穿" —— 它上面根本没有栅氧。

### Q37 · 你怎么知道栅氧还在？ ⚠️
**A** — "I do not, directly. The monitor wafer has no gate oxide, so what I measured is the mask. The gate oxide's survival is an inference — the silicon etch ends on it, and the over-etch sits inside the budget that the selectivity allows. A direct check needs a cross-section, and this lab does not do one."

> **这是最容易被专业的 TA 抓住的一处。** 宁可自己先说出来，比被问出来好。

### Q38 · 硬掩模损失 10.7 %，危险吗？ ✅
**A** — "No. The mask is thirty-seven nanometres and loses about four, so it ends at eighty-nine per cent. To eat through it you would need a recipe about nine times longer than the one it saw."

> 37.02 / 0.124 ≈ 298 s vs 实际 32 s ≈ 9×。

### Q39 · 均匀性怎么量化？ ✅
**A** — "Before the etch, the five points span zero point three one nanometres — zero point eight per cent of the film. After the etch, two point two nanometres — six point eight per cent. The deposition is uniform; the etch is what introduced the spread."

---

## 7 · 我方角色与边界

### Q40 · 你们在流程里到底做了什么？ ✅
**A** — "Four mounts, four optical checks, two ellipsometry measurements, and the record. The recipes are fixed on the tools — we select one, we do not set parameters. So the job sits at the boundaries: load, choose, judge, record."

> 记录 §2、§9：LAB3 = 4 次装片 + 4 次判读 + 2 次椭偏 + 记录。

### Q41 · 那你们学到什么？ ✅
**A** — "Where the risk actually sits. Nobody can mis-set a parameter here, so the failures that matter are at the boundaries — the wrong recipe name, the wafer the wrong way round, a check skipped, a number written down wrong or not at all. And how to read a process budget out of two measurements."

### Q42 · 这个实验最大的空缺是什么？ ✅
**A** — "The fluorine etch time. It is a timed recipe and the time is not in our record, so one segment of the budget is open. Everything about the undercut and the CD is a range until that number exists."

> 记录 §7-1。**主动说出来**比被问出来好 —— 这是个"知道自己缺什么"的答案。

### Q43 · 如果重做，你改什么？ ✅
**A** — "Record the fluorine time. Measure the a-Si rate on a blanket wafer instead of assuming a hundred nanometres over twenty seconds. Repeat one ellipsometry point to separate noise from non-uniformity. And cut a cross-section — the sidewall is the one thing we cannot see."

### Q44 · 下一道是什么？ / "What happens next?" ✅
**A** — "Spacers and the source/drain implant — that is LAB4, and that is where the NFET and the PFET finally stop being identical. The oxide cap stays on because LAB4 needs it through the spacer deposition and the implant."

> L02 p11 原话："LAB4: Spacer definition and activation of dopants"。
> 封存交接是 LAB3 的最后一步（记录 §2-15）。❓ "LAB4 需要这层帽子" 来自 deck p18 的注，不是 lab PM 原文 —— 若被追问就照注说，别加码。

---

## 8 · 六个「不知道」—— 照念

被问到以下任何一项，**不要编**。念右列那一句，然后停住等下一个问题。

| 未知项 | 照念 |
|---|---|
| F 基刻蚀时间与配比 | "That time is not in our record. The recipe is timed, so the number exists — we just did not capture it." |
| 去胶的工具与参数 | "Oxygen plasma is what we describe; the tool setting is not in our record." |
| PEB 与软烘的时间 | "The temperatures we have — ninety-five and a hundred and ten. The times are the tool's." |
| 主刻压力 / 功率 / 流量 / 过刻秒数 | "The tool sets those. We read the recipe name, not the parameters." |
| CD 实测值 | "We did not measure CD independently. The numbers on the picture are widths that were already on the mask." |
| n 阱在哪一道做 | "We could not find where the well is formed for the PFET, and we have asked the TA. It is still open." |

> 最后一条是记录 §7-4 的真实开口。**能说出自己流程里查不到的一环，比假装全知道强。**

---

## 9 · 同学版一句话

对方不是做工艺的，就用这一列，不要展开。

| 他问 | 你说 | 中文意思 |
|---|---|---|
| 你们今天干了啥 | "Four wafer loads, four microscope checks, two thickness measurements." | 装四次片、看四次显微镜、测两次厚度 |
| 为什么上面要盖一层氧化层 | "So we have a mask that the etch cannot burn away." | 因为胶会被氧气烧掉，得先换成氧化层当掩模 |
| 为什么不能刻久一点 | "Under the gate there is only seven and a half nanometres of oxide — a few extra seconds is a third of it." | 下面只有 7.5 nm 栅氧，多刻几秒就啃掉三分之一 |
| 你们把片子刻坏了吗 | "No. The lines are continuous, nothing is broken, and the cap is still on." | 没坏，线条连续、没断、帽子还在 |
| 那个 8 µm 是线宽吗 | "No, that is the spacing between lines." | 不是线宽，是线间距 |
| 最难的是哪一步 | "Knowing that the etch stopped where it should — the hard-mask step is timed, so the stop is a number, not a signal." | 难在"停在哪儿"：硬掩模那步靠计时，不靠信号 |
| 结论一句话 | "The mask survives, the etch stops where it should, and one number is missing." | 掩模活着、停在该停的地方、还有一个数没记到 |

---

## 10 · 按页索引（被打断时看这里）

| 页 | 标题 | 这页最可能被问 |
|---|---|---|
| 01 | Opening | Q1（叠层一句话） |
| 02 | Where we start | Q1 Q2 Q3 Q4 Q5 Q6 Q7 |
| 03 | PECVD SiO₂ | Q9 Q10 |
| 04 | PECVD dual | Q11 |
| 05 | Ellipsometry | Q12 Q13 Q14 |
| 06 | Surface prep | Q15 |
| 07 | Spin coating | Q16 Q17 |
| 08 | Soft bake | Q18 |
| 09 | Stepper | Q19 |
| 10 | PEB | Q20 ⚠️ |
| 11 | Development | Q21 |
| 12 | Inspection ① | Q22 ⚠️ |
| 13 | Hard-mask etch | Q23 Q24 Q25 |
| 14 | Resist strip | Q26 |
| 15 | Breakthrough | Q27 |
| 16 | Main etch · O₂ | Q28 Q29 Q30 Q31 Q32 |
| 17 | Second ellipsometry | Q33 Q34 Q35 Q36 Q38 Q39 |
| 18 | Inspection ④ | Q37 ⚠️ |
| 19 | Summary | Q40 Q41 Q42 Q43 Q44 |

> 最危险的两页：**p10（PEB 不是化学放大胶）** 和 **p18（"通过"只针对图形，不针对剖面）**。这两处被问住的概率最高。

---

## 11 · 读得准的八个词

| 词 | 读法提示 | 意思 |
|---|---|---|
| ellipsometry | el-lip-**SO**-me-try | 椭偏测量 |
| anisotropy | an-eye-**SOT**-ro-pee | 各向异性 |
| selectivity | se-lec-**TIV**-i-ty | 选择比 |
| undercut | **UN**-der-cut | 侧蚀 / 钻蚀 |
| notching | **NOTCH**-ing | 栅底侧向缺口 |
| native oxide | **NAY**-tive **OX**-ide | 自然氧化层 |
| HMDS | 念字母 H-M-D-S | 六甲基二硅氮烷 |
| TMAH | 念字母 T-M-A-H | 四甲基氢氧化铵 |

> 实在不确定就用字母念缩写（HMDS、TMAH、PECVD、RIE、PEB），北欧课堂里没人会因此扣分。

---

## 12 · 应急句式

| 情况 | 说这句 |
|---|---|
| 没听懂问题 | "Sorry — do you mean the recipe or the measurement?" |
| 需要两秒想 | "Let me take that from the numbers." |
| 只知道一半 | "The short answer is no. The longer one is about the over-etch budget." |
| 完全不知道 | "We did not record that." （然后停住，不要补猜测） |
| 被质疑数据 | "That is a fair point. The number is an upper bound, and here is what it bounds." |
| 时间到了 | "The one number to take away is the mask loss — four nanometres, ten per cent." |

---

## 13 · 出处

| 内容 | 文件 |
|---|---|
| 全部实测值、逐条可信度标记 | `labs/LAB3_record_v2.md` |
| 五点原始数据（两片） | `labs/HT26 Lab 3/SI WAFEFR.txt`、`HARDMASK 12 S bt 20 S mAIN.txt` |
| 讲稿与每页"被问到再补"的注 | `labs/slides/SCRIPT.md` |
| deck 的参数栏与 note（可以直接念） | `labs/slides/lab3_process_flow.html` |
| 讲义页号 | `md/slides/L08_Etching_and_Vacuum_Technology.md` p2 / p3 / p19 / p22 / p23 / p24 |
| | `md/slides/L09_CVD.md` p3 / p18 / p19 |
| | `md/slides/L07_Optical_Lithography.md` p7 / p19 |
| | `md/slides/L02_Planar_Technology_and_Moores_Law.md` p6 / p11 / p13 |
| | `md/slides/L03_Semiconductor_Wafers.md` p17 / p18 |

> 讲义页首的 `<!-- page N -->` 就是 PDF 页码，报告里可以直接引用（例如 "L08, slide 24"）。表里 `md/...` 的路径相对工作区根 `NanoFab/`（git 仓库根是 `labs/`）。
