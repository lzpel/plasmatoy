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
