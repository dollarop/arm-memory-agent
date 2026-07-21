from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


BOXES = [
    ("Learner notes\nfiles, goals, sections", 70, 80),
    ("Memory card\nnormalizer", 350, 80),
    ("Deduplicated\nmemory store", 630, 80),
    ("Tag/token\nretriever", 910, 80),
    ("Compact\nprompt pack", 910, 310),
    ("Agent answer\nproof + practice\nteach-back", 630, 310),
    ("Benchmark\nnaive vs optimized", 350, 310),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int]) -> None:
    draw.line([start, end], fill="#17475f", width=5)
    x, y = end
    draw.polygon([(x, y), (x - 14, y - 8), (x - 14, y + 8)], fill="#17475f")


def draw_box(draw: ImageDraw.ImageDraw, text: str, x: int, y: int) -> None:
    draw.rounded_rectangle([x, y, x + 220, y + 115], radius=18, fill="#f8fbfc", outline="#2b8c7f", width=4)
    lines = text.splitlines()
    line_height = 23
    top = y + 26
    for index, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font(22, bold=index == 0))
        draw.text((x + 110 - (bbox[2] - bbox[0]) / 2, top + index * line_height), line, fill="#123040", font=font(22, bold=index == 0))


def main() -> None:
    output = Path("docs/architecture.png")
    output.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1200, 520), "#eef7f6")
    draw = ImageDraw.Draw(image)

    draw.text((70, 28), "Arm Memory Agent Architecture", fill="#123040", font=font(34, bold=True))
    draw.text((70, 455), "Standard-library Python pipeline: persistent memory -> retrieval -> compact prompt -> auditable benchmark.", fill="#38586a", font=font(21))

    draw_arrow(draw, (290, 138), (350, 138))
    draw_arrow(draw, (570, 138), (630, 138))
    draw_arrow(draw, (850, 138), (910, 138))
    draw_arrow(draw, (1020, 195), (1020, 310))
    draw_arrow(draw, (910, 365), (850, 365))
    draw_arrow(draw, (630, 365), (570, 365))
    draw_arrow(draw, (460, 310), (460, 195))

    for text, x, y in BOXES:
        draw_box(draw, text, x, y)

    image.save(output)
    print(output)


if __name__ == "__main__":
    main()
