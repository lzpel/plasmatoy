"""plasmatoy: 回路図とパッシェン曲線を out/figure_*.svg に出力する。"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
import schemdraw
import schemdraw.elements as elm

OUT = Path(__file__).parent / "out"

# 日本語フォント: インストール済みのものだけ使う（findfont の警告を避ける）
_CANDIDATES = ["Yu Gothic", "Meiryo", "Hiragino Sans", "Noto Sans CJK JP", "IPAexGothic"]
_INSTALLED = {f.name for f in font_manager.fontManager.ttflist}
JP_FONTS = [f for f in _CANDIDATES if f in _INSTALLED] + ["sans-serif"]


# ---------------------------------------------------------------------------
# 回路図: 555 非安定発振 → MOSFET → フライバックトランス
# ---------------------------------------------------------------------------
def draw_circuit(path: Path) -> None:
    # matplotlib 経由で文字をパス化して SVG に埋め込む（閲覧環境のフォントに依存しない）
    schemdraw.use("matplotlib")
    plt.rcParams["svg.fonttype"] = "path"
    schemdraw.config(font=JP_FONTS[0], fontsize=12)
    VCC_Y, GND_Y = 9.0, -3.0
    Pin = elm.IcPin

    with schemdraw.Drawing(show=False) as d:
        # 電源と平滑コンデンサ
        elm.Battery().up().at((-9.5, GND_Y)).toy(VCC_Y).label("12V DC", loc="bot")
        elm.Capacitor(polar=True).down().at((-7.5, VCC_Y)).toy(GND_Y).label("C4\n100µF", loc="bot")
        elm.Dot().at((-7.5, VCC_Y))
        elm.Dot().at((-7.5, GND_Y))

        # 555（左: タイミング, 右: 出力, 上: 電源, 下: GND）
        ic = d.add(
            elm.Ic(
                pins=[
                    Pin("TRG", pin="2", side="left"),
                    Pin("THR", pin="6", side="left"),
                    Pin("DIS", pin="7", side="left"),
                    Pin("CTL", pin="5", side="right"),
                    Pin("OUT", pin="3", side="right"),
                    Pin("RST", pin="4", side="top"),
                    Pin("Vcc", pin="8", side="top"),
                    Pin("GND", pin="1", side="bot"),
                ],
                size=(4, 5), pinspacing=1.25, edgepadH=0.75, edgepadW=0.75, leadlen=1,
            ).right().label("U1\nNE555").at((0, 0))
        )
        a = ic.absanchors
        for k in ("RST", "Vcc"):
            elm.Line().at(a[k]).toy(VCC_Y)
            elm.Dot()
        elm.Line().at(a["GND"]).toy(GND_Y)
        elm.Dot()

        # タイミング回路 (R1, R2=可変, C1)
        tx = -3.0
        elm.Dot().at((tx, VCC_Y))
        elm.Resistor().down().at((tx, VCC_Y)).toy(a["DIS"].y).label("R1\n1kΩ", loc="bot")
        elm.Dot()
        elm.Line().tox(a["DIS"].x)
        elm.ResistorVar().down().at((tx, a["DIS"].y)).toy(a["TRG"].y).label("R2\n50kΩ VR", loc="top")
        elm.Dot()
        elm.Line().tox(a["TRG"].x)
        elm.Line().at(a["THR"]).tox(-1.8)
        elm.Line().toy(a["TRG"].y)
        elm.Dot()
        elm.Capacitor().down().at((tx, a["TRG"].y)).toy(GND_Y).label("C1\n1nF", loc="bot")
        elm.Dot()

        # CTL のパスコン
        elm.Line().at(a["CTL"]).right(1)
        elm.Capacitor().down().toy(GND_Y).label("C2\n10nF", loc="bot")
        elm.Dot()

        # ゲート駆動 (R3: ゲート抵抗, R4: プルダウン)
        gx = 11.0
        elm.Resistor().right().at(a["OUT"]).tox(8).label("R3\n47Ω")
        elm.Line().tox(gx)
        elm.Dot().at((9, a["OUT"].y))
        elm.Resistor().down().at((9, a["OUT"].y)).toy(GND_Y).label("R4\n10kΩ", loc="bot")
        elm.Dot()

        fet = d.add(elm.NFet().right().reverse().anchor("gate").at((gx, a["OUT"].y)))
        drain, source = fet.absanchors["drain"], fet.absanchors["source"]
        elm.Label().at((drain.x + 0.4, source.y + 0.3)).label("Q1 IRFP250N", halign="left")
        elm.Line().at(source).toy(GND_Y)

        # フライバックトランス（一次側: +12V → ドレイン）
        tr = d.add(elm.Transformer(t1=4, t2=8).right().anchor("p2").at((drain.x, drain.y + 1.5)))
        p1, p2, s1, s2 = (tr.absanchors[k] for k in ("p1", "p2", "s1", "s2"))
        elm.Label().at((s1.x + 0.3, s1.y + 0.9)).label("T1 フライバック（AC出力品）", halign="left")
        elm.Line().at(drain).toy(p2.y)
        elm.Line().at(p1).toy(VCC_Y)

        # 一次側のサージクランプ (TVS)
        cx = drain.x - 1.5
        elm.Dot().at((drain.x, p2.y))
        elm.Line().at((drain.x, p2.y)).tox(cx)
        elm.Zener().up().at((cx, p2.y)).toy(VCC_Y).label("D1\nTVS", loc="bot")
        elm.Dot()

        # 二次側 → 中心電極 / アース
        elm.Line().at(s1).right(3)
        elm.Dot(open=True).label("中心電極へ\n数kV, 20〜40kHz", loc="right")
        elm.Line().at(s2).right(1.5)
        elm.Line().down(0.5)
        elm.Ground().label("アース", loc="right")

        # 電源レール
        elm.Line().at((-9.5, VCC_Y)).tox(p1.x).label("+12V", loc="top")
        elm.Line().at((-9.5, GND_Y)).tox(source.x).label("GND", loc="bot")

        elm.Label().at((-9.5, GND_Y - 1.6)).label(
            "f ≈ 1.44 / ((R1 + 2·R2)·C1) ≈ 14 kHz〜1.4 MHz → R2 を回して 20〜40 kHz（R2 ≈ 23kΩ で約30kHz）に合わせる",
            halign="left",
        )

    d.save(str(path))


# ---------------------------------------------------------------------------
# パッシェンの法則
#   V_b = B·pd / (ln(A·pd) − ln(ln(1 + 1/γ)))
#   A [1/(cm·Torr)], B [V/(cm·Torr)] は Raizer "Gas Discharge Physics" Table 4.1 の概算値
# ---------------------------------------------------------------------------
GASES = {
    "空気": (15.0, 365.0),
    "N₂": (12.0, 342.0),
    "Ar": (12.0, 180.0),
    "Ne": (4.0, 100.0),
    "He": (3.0, 34.0),
}
GAMMA = 0.01  # 二次電子放出係数（電極材質で変わる）


def paschen(pd: np.ndarray, A: float, B: float, gamma: float = GAMMA) -> np.ndarray:
    denom = np.log(A * pd) - np.log(np.log(1 + 1 / gamma))
    v = B * pd / denom
    return np.where(denom > 0, v, np.nan)  # 分母≤0 は放電しない領域


def draw_paschen(path: Path) -> None:
    plt.rcParams["font.family"] = JP_FONTS
    plt.rcParams["svg.fonttype"] = "path"
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), constrained_layout=True)

    # (a) ガス別の V_b – pd
    pd = np.logspace(-1, 3.5, 600)
    for name, (A, B) in GASES.items():
        ax1.plot(pd, paschen(pd, A, B), label=name)
    ax1.set(
        xscale="log", yscale="log", xlim=(pd[0], pd[-1]), ylim=(50, 1e5),
        xlabel="p·d  [Torr·cm]", ylabel="放電開始電圧 V_b  [V]",
        title=f"(a) パッシェン曲線（直流, γ={GAMMA}）",
    )
    ax1.grid(True, which="both", alpha=0.3)
    ax1.legend()

    # (b) 空気・ギャップ別の V_b – 圧力（フラスコを何Torrまで引くか）
    p = np.logspace(-2, np.log10(760), 600)
    A, B = GASES["空気"]
    for d_cm in (3, 5, 8):
        ax2.plot(p, paschen(p * d_cm, A, B), label=f"空気, d = {d_cm} cm")
    for v, txt in ((1.5e3, "CCFLインバータ ≈1.5kV"), (10e3, "フライバック ≈10kV")):
        ax2.axhline(v, color="gray", ls="--", lw=1)
        ax2.text(1.2e-2, v * 1.1, txt, color="gray")
    ax2.axvline(760, color="k", lw=0.8)
    ax2.text(700, 3e4, "大気圧", ha="right")
    ax2.set(
        xscale="log", yscale="log", xlim=(p[0], 1000), ylim=(50, 1e5),
        xlabel="圧力 p  [Torr]", ylabel="放電開始電圧 V_b  [V]",
        title="(b) 電極–ガラス間距離 d ごとの必要電圧（目安）",
    )
    ax2.grid(True, which="both", alpha=0.3)
    ax2.legend(loc="lower right")

    fig.savefig(path)
    plt.close(fig)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    draw_circuit(OUT / "figure_circuit.svg")
    draw_paschen(OUT / "figure_paschen.svg")
    for f in sorted(OUT.glob("figure_*.svg")):
        print(f"wrote {f}")


if __name__ == "__main__":
    main()
