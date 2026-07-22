"""
generates the schematic/illustrative README images - not real training curves,
just diagrams of what's in this notebook grab-bag.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from PIL import Image
import io

DARK = "#15161a"
GOLD = "#d4af37"
GOLD_DIM = "#c9a227"
INK = "#e8e6df"
MUTED = "#8b8d95"
BLUE = "#3987e5"
ORANGE = "#d95926"
AQUA = "#199e70"

plt.rcParams["font.family"] = "DejaVu Sans"


def new_fig(w=9, h=5.5):
    fig, ax = plt.subplots(figsize=(w, h), dpi=180)
    fig.patch.set_facecolor(DARK)
    ax.set_facecolor(DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, color=INK, sub=None):
    b = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        linewidth=1.4, edgecolor=color, facecolor="#1d1e24",
    )
    ax.add_patch(b)
    ax.text(x + w / 2, y + h / 2 + (0.14 if sub else 0), label,
            ha="center", va="center", color=INK, fontsize=10.5, fontweight="bold")
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.22, sub,
                ha="center", va="center", color=MUTED, fontsize=8)


def arrow(ax, p0, p1, color=GOLD_DIM):
    a = FancyArrowPatch(p0, p1, arrowstyle="-|>", mutation_scale=14,
                         linewidth=1.6, color=color)
    ax.add_patch(a)


# 1. the six projects, mapped out
fig, ax = new_fig()
ax.text(5, 5.6, "what's in this grab-bag", ha="center", color=GOLD, fontsize=14, fontweight="bold")

projects = [
    ("linear_regression_ecommerce", "regression", BLUE),
    ("cnn_from_scratch", "CNN (numpy)", AQUA),
    ("cnn_tensorflow", "CNN (TF)", AQUA),
    ("deep_nn_from_scratch", "L-layer NN (numpy)", ORANGE),
    ("facial_emotion_detection", "CNN + keypoints", ORANGE),
    ("sf_crimes_map", "folium map", BLUE),
]
cols = 3
for i, (name, label, color) in enumerate(projects):
    r, c = divmod(i, cols)
    x = 0.5 + c * 3.05
    y = 4.2 - r * 1.6
    box(ax, x, y, 2.6, 1.1, label, color=color, sub=name)

ax.text(5, 0.5, "six independent notebooks - no shared pipeline between them",
        ha="center", color=MUTED, fontsize=9, style="italic")
fig.savefig("assets/diagram_project_map.png", facecolor=DARK)
plt.close(fig)


# 2. from-scratch vs framework split
fig, ax = new_fig()
ax.text(5, 5.6, "from-scratch vs framework (schematic)", ha="center", color=GOLD, fontsize=14, fontweight="bold")

box(ax, 0.6, 3.2, 4.0, 1.3, "numpy from scratch", color=AQUA,
    sub="cnn_from_scratch, deep_nn_from_scratch")
box(ax, 5.4, 3.2, 4.0, 1.3, "keras / tensorflow", color=ORANGE,
    sub="cnn_tensorflow, facial_emotion_detection")

ax.text(5, 2.2, "same underlying ideas (conv/forward/backward passes),\ntwo different levels of abstraction",
        ha="center", color=MUTED, fontsize=9, style="italic")
ax.text(5, 1.0, "illustrative diagram - not a benchmark, no real numbers implied",
        ha="center", color=MUTED, fontsize=8)
fig.savefig("assets/diagram_scratch_vs_framework.png", facecolor=DARK)
plt.close(fig)


# 3. notebook shape (generic pipeline: data -> model -> plot)
fig, ax = new_fig()
ax.text(5, 5.6, "typical notebook shape here", ha="center", color=GOLD, fontsize=14, fontweight="bold")

box(ax, 0.4, 3.6, 2.6, 1.0, "load data", color=BLUE, sub="csv / h5 / drive")
box(ax, 3.4, 3.6, 2.6, 1.0, "build model", color=AQUA, sub="numpy or keras")
box(ax, 6.4, 3.6, 3.0, 1.0, "train + plot", color=GOLD, sub="loss curve / preds")

arrow(ax, (3.0, 4.1), (3.4, 4.1))
arrow(ax, (6.0, 4.1), (6.4, 4.1))

ax.text(5, 1.6, "each project follows roughly this shape, independently of the others",
        ha="center", color=MUTED, fontsize=9, style="italic")
fig.savefig("assets/diagram_notebook_shape.png", facecolor=DARK)
plt.close(fig)

print("wrote assets/diagram_project_map.png, diagram_scratch_vs_framework.png, diagram_notebook_shape.png")


# --- motion graphic: looping GIF, gold sweep across the project tiles ---
frames = []
n_frames = 36
tiles = [(0.4, ORANGE), (2.9, AQUA), (5.4, BLUE), (7.9, GOLD)]

for f in range(n_frames):
    fig, ax = new_fig(w=9, h=4.2)
    ax.set_ylim(0, 4.5)
    t = f / n_frames

    for x, color in tiles:
        box(ax, x, 2.0, 2.1, 1.0, "", color=color)

    sweep_x = 0.4 + t * 9.4
    ax.plot([sweep_x, sweep_x], [1.7, 3.3], color=GOLD, linewidth=2.5, alpha=0.9)
    glow = plt.Circle((sweep_x, 2.5), 0.22, color=GOLD, alpha=0.35)
    ax.add_patch(glow)

    ax.text(5, 3.8, "Machine_learning_projects", ha="center", color=GOLD,
            fontsize=13, fontweight="bold")
    ax.text(5, 0.5, "illustrative sweep across the notebook grab-bag - not live output",
            ha="center", color=MUTED, fontsize=8, style="italic")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", facecolor=DARK)
    plt.close(fig)
    buf.seek(0)
    frames.append(Image.open(buf).convert("RGB"))

frames[0].save(
    "assets/motion_project_sweep.gif",
    save_all=True,
    append_images=frames[1:],
    duration=45,
    loop=0,
)
print("wrote assets/motion_project_sweep.gif")
