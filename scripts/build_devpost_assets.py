from pathlib import Path
import math
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


def ease(t):
    t = max(0, min(1, t))
    return 0.5 - math.cos(t * math.pi) / 2


def lerp(a, b, t):
    return a + (b - a) * ease(t)


def draw_arrow(draw, start, end, fill=TEAL, width=6):
    draw.line((start, end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = 18
    left = (end[0] - head * math.cos(angle - 0.55), end[1] - head * math.sin(angle - 0.55))
    right = (end[0] - head * math.cos(angle + 0.55), end[1] - head * math.sin(angle + 0.55))
    draw.polygon([end, left, right], fill=fill)


def draw_card(draw, x, y, w, h, title, body, accent=TEAL):
    rounded(draw, (x, y, x + w, y + h), 18, CARD, (207, 222, 226), 2)
    draw.rounded_rectangle((x, y, x + 12, y + h), radius=6, fill=accent)
    draw.text((x + 28, y + 24), title, font=font(25, True), fill=accent)
    wrap(draw, body, x + 28, y + 62, w - 55, font(19), fill=INK, line_gap=5)


def draw_metric(draw, x, y, value, label, color=GOLD, scale=1.0):
    draw.text((x, y), value, font=font(int(44 * scale), True), fill=color)
    draw.text((x, y + int(55 * scale)), label, font=font(int(20 * scale)), fill=(213, 231, 234))


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
    w, h, fps = 1280, 720, 24
    duration = 36
    frames = []

    def base():
        img = Image.new("RGB", (w, h), BG)
        d = ImageDraw.Draw(img)
        d.rounded_rectangle((0, 0, w, 78), radius=0, fill=(12, 54, 70))
        d.text((54, 22), "Arm Memory Agent", font=font(30, True), fill=(255, 255, 255))
        d.text((940, 27), "Cloud AI on Arm64", font=font(22, True), fill=(202, 239, 234))
        return img, d

    for frame in range(duration * fps):
        t = frame / fps
        img, d = base()

        if t < 6:
            p = t / 6
            d.text((70, 115), "Long agent context gets heavy", font=font(44, True), fill=INK)
            cards = [
                ("Learner note", "Grid storage needs flexible demand."),
                ("Source quote", "Renewables require firm capacity."),
                ("Prior answer", "Use evidence, not loose summary."),
                ("Teacher plan", "Explain, test, then teach back."),
                ("Follow-up", "Compare nuclear, storage, and grid."),
            ]
            for i, (title, body) in enumerate(cards):
                x = int(lerp(-360, 90 + i * 38, min(1, p * 1.7 - i * 0.13)))
                y = 190 + i * 78
                draw_card(d, x, y, 455, 68, title, body, TEAL if i % 2 else MINT)
            d.text((705, 230), "Naive prompt:", font=font(32, True), fill=TEAL)
            naive = int(lerp(0, 48748, p))
            d.text((705, 290), f"{naive:,} bytes", font=font(58, True), fill=GOLD)
            wrap(d, "Every old note is appended again, so the agent grows slower and harder to audit.", 710, 375, 430, font(26))

        elif t < 12:
            p = (t - 6) / 6
            d.text((70, 115), "Normalize memory, then retrieve only what matters", font=font(38, True), fill=INK)
            xs = [70, 70, 70, 70]
            ys = [210, 315, 420, 525]
            labels = ["notes", "files", "questions", "feedback"]
            for i, lab in enumerate(labels):
                draw_card(d, xs[i], ys[i], 265, 76, lab.title(), "structured memory card", MINT)
            draw_arrow(d, (370, 360), (570, 360), TEAL, 7)
            rounded(d, (590, 205, 930, 555), 28, (14, 34, 49), None)
            d.text((630, 250), "Memory store", font=font(34, True), fill=(255, 255, 255))
            for i in range(9):
                yy = 315 + i * 22
                alpha_w = int(lerp(0, 235, min(1, p * 1.3 - i * 0.04)))
                d.rounded_rectangle((635, yy, 635 + alpha_w, yy + 10), radius=5, fill=(70, 177, 155))
            draw_arrow(d, (955, 360), (1120, 360), GOLD, 7)
            d.text((1032, 287), "query", font=font(28, True), fill=INK)
            d.rounded_rectangle((1025, 333, 1190, 388), radius=18, fill=GOLD)
            d.text((1058, 348), "retrieve", font=font(24, True), fill=INK)

        elif t < 18:
            p = (t - 12) / 6
            d.text((70, 115), "Compact prompt pack", font=font(44, True), fill=INK)
            raw_w = int(lerp(940, 120, p))
            opt_w = int(lerp(80, 620, p))
            d.text((90, 210), "Full workspace", font=font(26, True), fill=INK)
            d.rounded_rectangle((90, 255, 1030, 305), radius=20, fill=(219, 230, 232))
            d.rounded_rectangle((90, 255, 90 + raw_w, 305), radius=20, fill=(172, 191, 197))
            d.text((90, 355), "Selected memory", font=font(26, True), fill=INK)
            d.rounded_rectangle((90, 400, 1030, 450), radius=20, fill=(219, 230, 232))
            d.rounded_rectangle((90, 400, 90 + opt_w, 450), radius=20, fill=MINT)
            ratio = lerp(1.0, 0.0275, p)
            saved = int(lerp(0, 189596, p))
            rounded(d, (760, 505, 1190, 650), 24, (14, 34, 49), None)
            draw_metric(d, 795, 530, f"{ratio:.4f}", "compression ratio", GOLD)
            draw_metric(d, 990, 530, f"{saved:,}", "bytes saved", MINT, 0.84)

        elif t < 24:
            p = (t - 18) / 6
            d.text((70, 115), "Auditable output, not a black box", font=font(44, True), fill=INK)
            rounded(d, (90, 190, 780, 610), 28, (14, 34, 49), None)
            lines = [
                "{",
                '  "selected_cards": ["synthetic-175", "synthetic-169"],',
                '  "optimized_prompt_bytes": 1345,',
                '  "tag_recall": 1.0,',
                '  "prompt_hash": "44252cc8d8e8..."',
                "}",
            ]
            for i, line in enumerate(lines):
                max_chars = int(lerp(0, len(line), min(1, p * 2.0 - i * 0.13)))
                d.text((130, 235 + i * 50), line[:max_chars], font=font(22), fill=(218, 238, 241))
            rounded(d, (835, 260, 1168, 525), 24, CARD, (210, 225, 228), 2)
            d.text((875, 305), "Every run reports:", font=font(28, True), fill=TEAL)
            for i, item in enumerate(["memory IDs", "byte counts", "runtime", "SHA-256 hash"]):
                y = 365 + i * 36
                d.ellipse((875, y + 4, 891, y + 20), fill=MINT)
                d.text((905, y), item, font=font(24), fill=INK)

        elif t < 30:
            p = (t - 24) / 6
            d.text((70, 115), "Validated on Arm64", font=font(48, True), fill=INK)
            rounded(d, (115, 210, 1165, 585), 28, (14, 34, 49), None)
            d.text((165, 270), "GitHub Actions", font=font(38, True), fill=(255, 255, 255))
            jobs = [("ubuntu-24.04", "success"), ("ubuntu-24.04-arm", "success")]
            for i, (name, status) in enumerate(jobs):
                y = 355 + i * 88
                d.rounded_rectangle((165, y, 1115, y + 58), radius=18, fill=(26, 68, 85))
                d.text((200, y + 15), name, font=font(24, True), fill=(230, 245, 247))
                check = int(lerp(0, 1, p * 2 - i * 0.4))
                if check:
                    d.ellipse((945, y + 12, 980, y + 47), fill=MINT)
                    d.line((954, y + 30, 963, y + 39, 974, y + 20), fill=(255, 255, 255), width=5)
                    d.text((995, y + 15), status, font=font(24, True), fill=MINT)
            d.text((165, 515), "Run 4: github.com/dollarop/arm-memory-agent/actions/runs/29870665281", font=font(19), fill=(205, 226, 231))

        else:
            p = (t - 30) / 6
            d.text((70, 120), "Cloud AI: smaller prompts for CPU-first agents", font=font(38, True), fill=INK)
            rounded(d, (120, 230, 1160, 560), 30, CARD, (210, 225, 228), 2)
            d.text((175, 285), "0.0275", font=font(68, True), fill=GOLD)
            d.text((175, 360), "avg compression ratio", font=font(26), fill=INK)
            d.text((510, 285), "189,596", font=font(68, True), fill=TEAL)
            d.text((510, 360), "bytes saved", font=font(26), fill=INK)
            d.text((865, 285), "Arm64", font=font(68, True), fill=MINT)
            d.text((865, 360), "Actions success", font=font(26), fill=INK)
            repo = "github.com/dollarop/arm-memory-agent"
            d.text((330, 492), repo, font=font(30, True), fill=TEAL)
            d.rounded_rectangle((120, 600, int(120 + lerp(0, 1040, p)), 612), radius=6, fill=MINT)

        frames.append(img)

    imageio.mimsave(OUT / "arm-memory-agent-demo.mp4", frames, fps=fps, quality=8, macro_block_size=16)


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
