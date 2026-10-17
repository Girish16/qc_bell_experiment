"""Generate the scientific-editorial LinkedIn graphic.

Run: python -m src.render_post
Exports: assets/bell_state_post.png (1200x1500) and .svg.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from .bell_state import BASIS, probabilities

ROOT = Path(__file__).resolve().parents[1]
PALETTE = {
    "paper": "#F5F2EA", "forest": "#173E32", "sage": "#739584",
    "clay": "#C4775B", "ink": "#1D302B", "muted": "#61756F",
    "line": "#D5DCD2", "pale": "#E8EBE3", "white": "#FFFDF8",
}


def render(destination: Path | None = None, dpi: int = 100) -> tuple[Path, Path]:
    dest = destination or ROOT / "assets"
    dest.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "mathtext.fontset": "cm",
        "svg.fonttype": "none", "axes.unicode_minus": False,
    })
    c = PALETTE
    fig = plt.figure(figsize=(12, 15), facecolor=c["paper"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")

    def t(x, y, s, size=14, color="ink", family="DejaVu Sans",
          weight="normal", ha="left"):
        ax.text(x, y, s, fontsize=size, color=c.get(color, color),
                fontfamily=family, fontweight=weight, ha=ha, va="center")

    def line(x0, y0, x1, y1, color="line", width=1):
        ax.plot([x0, x1], [y0, y1], color=c.get(color, color),
                lw=width, solid_capstyle="round")

    # Quiet, science-journal masthead; no decoration or artificial figures.
    t(.07, .966, "QUANTUM COMPUTING   /   FIELD NOTES", 11, "muted", weight="bold")
    t(.93, .966, "NO. 01", 11, "muted", ha="right")
    line(.07, .941, .93, .941)
    t(.07, .888, "From two qubits", 51, "forest", family="DejaVu Serif", weight="bold")
    t(.07, .823, "to entanglement", 51, "forest", family="DejaVu Serif", weight="bold")
    t(.07, .771, "One Hadamard. One CNOT. A pair of entangled qubits.", 15, "muted")
    line(.07, .737, .93, .737)

    t(.07, .712, "01   /   THE CIRCUIT", 12, "forest", weight="bold")
    t(.07, .681, r"Start in $|00\rangle$, apply H to q0, then CNOT from q0 to q1.", 12, "muted")
    y0, y1 = .603, .544
    for q, y in ((0, y0), (1, y1)):
        t(.075, y, rf"$q_{q}$", 16)
        t(.114, y, r"$|0\rangle$", 17)
        line(.166, y, .588, y, "forest", 1.4)
    ax.add_patch(Rectangle((.296, y0-.024), .048, .048,
                           facecolor=c["forest"], edgecolor="none"))
    t(.320, y0, "H", 16, "white", weight="bold", ha="center")
    xc = .497
    line(xc, y0, xc, y1, "forest", 1.5)
    ax.add_patch(Circle((xc, y0), .0075, facecolor=c["forest"], edgecolor="none"))
    ax.add_patch(Circle((xc, y1), .0162, facecolor=c["paper"], edgecolor=c["forest"], lw=1.4))
    line(xc-.011, y1, xc+.011, y1, "forest", 1.4)
    line(xc, y1-.011, xc, y1+.011, "forest", 1.4)
    ax.add_patch(FancyBboxPatch((.635, .526), .294, .133,
                                boxstyle="round,pad=.009,rounding_size=.010",
                                facecolor=c["pale"], edgecolor=c["line"], linewidth=.8))
    t(.661, .629, "FINAL STATE   /   BELL PAIR", 10.5, "forest", weight="bold")
    t(.661, .575, r"$|\Phi^+\rangle=\frac{1}{\sqrt{2}}(|00\rangle+|11\rangle)$", 20, "forest")

    line(.07, .501, .93, .501)
    t(.07, .475, "02   /   MEASUREMENT PROBABILITIES", 12, "forest", weight="bold")
    t(.07, .447, "The outcomes change as the quantum state evolves.", 13, "muted")
    titles = ("INITIAL", "AFTER HADAMARD", "AFTER CNOT")
    ket_labels = (
        r"$|00\rangle$",
        r"$\frac{1}{\sqrt{2}}(|00\rangle+|01\rangle)$",
        r"$\frac{1}{\sqrt{2}}(|00\rangle+|11\rangle)$",
    )
    starts = (.070, .367, .664)
    for idx, ((stage, probs), title, state_label, start) in enumerate(
            zip(probabilities().items(), titles, ket_labels, starts)):
        if idx:
            line(start-.019, .410, start-.019, .183)
        t(start, .410, title, 10.9, "forest", weight="bold")
        t(start, .372, state_label, 17)
        chart = fig.add_axes([start+.018, .220, .239, .126])
        chart.set_facecolor(c["paper"])
        bars = chart.bar(range(4), probs, width=.58,
                         color=[c["forest"], c["clay"], c["sage"], c["clay"]], zorder=2)
        chart.set(xlim=(-.58, 3.57), ylim=(0, 1.10))
        chart.set_yticks([0, .5, 1.0], ["0", "0.5", "1.0"])
        chart.set_xticks(range(4), BASIS)
        chart.tick_params(axis="both", colors=c["muted"], labelsize=10, length=0, pad=5)
        chart.grid(axis="y", color=c["line"], lw=.7, linestyle="--")
        chart.set_axisbelow(True)
        for spine in chart.spines.values():
            spine.set_visible(False)
        for bar, value in zip(bars, probs):
            if value > 1e-8:
                chart.text(bar.get_x()+bar.get_width()/2, value+.035, f"{value:.2f}",
                           fontsize=10, fontweight="bold", ha="center",
                           va="bottom", color=c["ink"])

    line(.07, .175, .93, .175)
    t(.07, .145, "THE IMPORTANT DISTINCTION", 10.5, "forest", weight="bold")
    t(.07, .114, "The 50/50 histogram is not proof of entanglement.",
      18.5, "forest", family="DejaVu Serif", weight="bold")
    t(.07, .085, "A classical mixture can have the same Z-basis results. Next: how to tell them apart.",
      11.5, "muted")
    line(.07, .054, .93, .054)
    t(.07, .032, "Basis labels: |q1 q0> (Qiskit convention); q0 is the rightmost bit.", 9, "muted")
    t(.93, .032, "PYTHON  /  NUMPY  /  MATPLOTLIB", 9, "muted", ha="right")
    png, svg = dest / "bell_state_post.png", dest / "bell_state_post.svg"
    fig.savefig(png, dpi=dpi, facecolor=c["paper"])
    fig.savefig(svg, facecolor=c["paper"])
    plt.close(fig)
    return png, svg


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dpi", type=int, default=100)
    args = parser.parse_args()
    for output in render(dpi=args.dpi):
        print(output)
