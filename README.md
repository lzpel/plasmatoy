# plasmatoy

バイクのマフラーを覆う形の密閉トーラス内でプラズマ発光させるデバイス
- 川崎区や足立区のガラの悪いバイカーに売る
- 12V usbまたはシガーソケットから電源を取る
- シリンダー表面を雷が走っているように見えることが要件

![img](https://private-user-images.githubusercontent.com/18492524/718408481-fb40cf00-6960-478c-9c27-7100a594e514.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3OTU1ODkxMTcsIm5iZiI6MTc5NTU4ODgxNywicGF0aCI6Ii8xODQ5MjUyNC83MTg0MDg0ODEtZmI0MGNmMDAtNjk2MC00NzhjLTljMjctNzEwMGE1OTRlNTE0LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjExMjUlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYxMTI1VDA2NDAxN1omWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTE4YjIwMGUyNDkyYWRmMTA3YTU4MWNlYTcxZjY5MDU1MjA5YWRlNDIxNTVlM2I3NzgxZTRiMDRmMDZmMTE4NzkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnJlc3BvbnNlLWNvbnRlbnQtdHlwZT1pbWFnZSUyRnBuZyJ9.Dzw0VSY25CD1L9VwE5i07mO1RVFhw7PXKHsE4QXv-bY)

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
