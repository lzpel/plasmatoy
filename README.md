# plasmatoy

バイクのマフラーを覆う形の密閉トーラス内でプラズマ発光させるデバイス
- 川崎区や足立区のガラの悪いバイカーに売る
- 12V usbまたはシガーソケットから電源を取る
- シリンダー表面を雷が走っているように見えることが要件

![img](https://github.com/user-attachments/assets/fb40cf00-6960-478c-9c27-7100a594e514)

## 購入

### ポンプ ─ ホース ─ バルブ ─ T字（真空計）─ タケノコ変換 ─ ゴム管 ─ ガラス排気口

- 真空ポンプ 4800円:https://jp.mercari.com/shops/product/2JYrS7stMz2pu74uF2nMNp
	- WEIMALL A68N10
	- https://github.com/user-attachments/assets/181646c4-0ee0-4290-84fd-c161c2a93fe4
- ホースとバルブ https://jp.mercari.com/item/m27967269826
- 真空計測器
	- [aliexpress1](https://ja.aliexpress.com/item/1005013250326643.html?spm=a2g0o.productlist.main.11.4e805328NhSQ3F&algo_pvid=27da4710-6f25-42e4-9ed3-2d37917989eb&algo_exp_id=27da4710-6f25-42e4-9ed3-2d37917989eb-10&pdp_ext_f=%7B%22order%22%3A%22121%22%2C%22spu_best_type%22%3A%22price%22%2C%22eval%22%3A%221%22%2C%22fromPage%22%3A%22search%22%7D&pdp_npi=6%40dis%21JPY%2120932%2110051%21%21%21128.99%2161.94%21%40212e37eb17955937683534311e0c93%2112000060667426057%21sea%21JP%210%21ABX%211%210%21n_tag%3A-29910%3Bd%3Acee88a2c%3Bm03_new_user%3A-29895%3BpisId%3A5000000220123542&curPageLogUid=uIim4Uqr85bi&utparam-url=scene%3Asearch%7Cquery_from%3A%7Cx_object_id%3A1005013250326643%7C_p_origin_prod%3A)

## 段取り

部分部分で市販版と自作版を用意

- 減圧透明ガラスG
	- 市販版G0：球型白熱電球
	- 自作版G1：
	- 量産版G2：
- 回路C
	- 市販版C0：CCFLインバーター
	- 自作版C1：555 + MOSFET + フライバックトランス
	- 量産版C2：PCBサービスで作る
- ソフトウェアS
	- 自作版S0：何V・何Torrで光り始めるか

## 図の生成

```sh
make run   # = uv run main.py → out/figure_*.svg を出力
```

### 回路図（自作版C1: 555 + MOSFET + フライバックトランス）

![回路図](https://lzpel.github.io/plasmatoy/figure_circuit.svg)

- ブレッドボードに載せるのは 12V 側（U1, R1〜R4, C1〜C4）だけ。Q1 は放熱器付きで、T1 の二次側（数kV）は空中配線にする
- T1 は **整流ダイオードが入っていない AC 出力のフライバック**を使う（最近のブラウン管用は内部で整流された DC 出力が多い）
- R2 で発振周波数を 20〜40 kHz に合わせる

### パッシェン曲線（ソフトウェアS0: 何V・何Torrで光り始めるか）

![パッシェン曲線](https://lzpel.github.io/plasmatoy/figure_paschen.svg)

- V_b = B·pd / (ln(A·pd) − ln(ln(1 + 1/γ)))。A, B は Raizer "Gas Discharge Physics" の概算値、γ = 0.01
- 直流・平行平板の理論値。数十kHz の交流（誘電体バリア放電）で動かす実機では、これより低い電圧で光る見込み
