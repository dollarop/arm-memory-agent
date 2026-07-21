from pathlib import Path
import textwrap

import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "devpost"
OUT.mkdir(exist_ok=True)


def font(size, bold=False):
    names = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for name in names:
        if Path(name).exists():
            return ImageFont.truetype(name, size)
    return ImageFont.load_default()


BG = (245, 249, 250)
INK = (18, 38, 52)
TEAL = (27, 126, 144)
MINT = (56, 177, 146)
GOLD = (238, 188, 75)
CARD = (255, 255, 255)


def rounded(draw, box, radius=24, fill=CARD, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def wrap(draw, text, x, y, max_width, fnt, fill=INK, line_gap=8):
    words = text.split()
    line = ""
    for word in words:
        test = (line + " " + word).strip()
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            line = test
        else:
            draw.text((x, y), line, font=fnt, fill=fill)
            y += fnt.size + line_gap
            line = word
    if line:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def draw_title(draw, title, subtitle, w):
    draw.text((70, 58), title, font=font(56, True), fill=INK)
    draw.text((74, 130), subtitle, font=font(24), fill=(74, 91, 104))
    draw.rounded_rectangle((70, 178, w - 70, 186), radius=6, fill=TEAL)


def gallery_image():
    w, h = 1600, 1067
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    draw_title(d, "Arm Memory Agent", "CPU-friendly prompt memory for Arm64 Cloud AI", w)

    rounded(d, (80, 245, 620, 870), 28, CARD, (210, 225, 228), 2)
    d.text((120, 290), "Problem", font=font(34, True), fill=TEAL)
    wrap(d, "Long-running agents become slow and costly when every note, source, and prior message is appended back into context.", 120, 350, 430, font(26))
    d.text((120, 560), "Optimization", font=font(34, True), fill=TEAL)
    wrap(d, "Normalize memory cards, deduplicate repeated facts, retrieve only relevant evidence, and emit a small auditable prompt pack.", 120, 620, 430, font(26))

    rounded(d, (690, 245, 1520, 870), 28, (14, 34, 49), None)
    d.text((735, 295), "Benchmark Evidence", font=font(38, True), fill=(255, 255, 255))
    metrics = [
        ("180", "memory cards"),
        ("4", "benchmark queries"),
        ("0.0275", "avg compression ratio"),
        ("189,596", "bytes saved vs naive prompts"),
        ("1.0", "avg tag recall"),
        ("3.345 ms", "avg runtime"),
    ]
    x0, y0 = 735, 380
    for i, (num, label) in enumerate(metrics):
        x = x0 + (i % 2) * 365
        y = y0 + (i // 2) * 135
        d.text((x, y), num, font=font(42, True), fill=GOLD if i < 4 else MINT)
        d.text((x, y + 55), label, font=font(23), fill=(218, 234, 236))

    d.rounded_rectangle((735, 760, 1475, 790), radius=15, fill=MINT)
    d.text((735, 820), "Validated by GitHub Actions on ubuntu-24.04 and ubuntu-24.04-arm", font=font(23, True), fill=(220, 244, 238))
    img.save(OUT / "arm-memory-agent-gallery.png", quality=94)


def slide(title, body, accent=TEAL):
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w, 92), radius=0, fill=(12, 54, 70))
    d.text((60, 27), "Arm Memory Agent", font=font(28, True), fill=(255, 255, 255))
    d.rounded_rectangle((60, 135, 1220, 610), radius=28, fill=CARD, outline=(210, 225, 228), width=2)
    d.text((105, 190), title, font=font(46, True), fill=accent)
    y = 275
    for para in body:
        y = wrap(d, para, 110, y, 1030, font(29), fill=INK, line_gap=10) + 22
    d.rounded_rectangle((105, 570, 1180, 585), radius=8, fill=accent)
    return img


def video():
    slides = [
        slide("The bottleneck", ["Useful agents remember notes, files, questions, and feedback.", "Naive long-context prompting gets slower and harder to audit."]),
        slide("The Arm-friendly fix", ["Arm Memory Agent stores compact memory cards, removes duplicate context, and retrieves only the evidence needed for the current query."]),
        slide("Measured compression", ["On the benchmark suite: 180 memory cards, 4 queries, average compression ratio 0.0275, and 189,596 bytes saved versus naive prompts."], GOLD),
        slide("Auditable outputs", ["Every prompt pack includes selected memory IDs, byte counts, runtime, and a deterministic SHA-256 hash for reproducible inspection."], MINT),
        slide("Arm64 validation", ["GitHub Actions passed on both ubuntu-24.04 and ubuntu-24.04-arm, using only Python standard-library runtime for the benchmark logic."]),
        slide("Cloud AI track", ["The project demonstrates a CPU-first agent memory pattern suitable for Arm64 cloud deployments and education/research assistants."], MINT),
    ]
    frames = []
    for s in slides:
        frames.extend([s] * 120)
    imageio.mimsave(OUT / "arm-memory-agent-demo.mp4", frames, fps=24, quality=8, macro_block_size=16)


def script():
    (OUT / "video-script.md").write_text(
        textwrap.dedent(
            """\
            # Arm Memory Agent Demo Script

            Arm Memory Agent is a CPU-friendly memory layer for long-running AI agents on Arm64 cloud infrastructure.

            Instead of appending every prior note and source into context, it converts learner notes into structured memory cards, removes repeated facts, retrieves only relevant evidence, and emits a compact prompt pack.

            The benchmark is reproducible: it generates 180 synthetic learning memory cards and runs four representative queries.

            The current result shows a 0.0275 average compression ratio, 189,596 bytes saved against naive prompts, 1.0 average tag recall, and millisecond-level runtime.

            Every prompt pack includes selected memory IDs, byte counts, timing, and a SHA-256 hash so the output is small and auditable.

            The GitHub Actions workflow validates the same benchmark on ubuntu-24.04 and ubuntu-24.04-arm, making the Cloud AI optimization evidence repeatable.
            """
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    gallery_image()
    video()
    script()
    print(OUT / "arm-memory-agent-gallery.png")
    print(OUT / "arm-memory-agent-demo.mp4")
    print(OUT / "video-script.md")
