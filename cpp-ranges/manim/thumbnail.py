from manim import *

# manim render -qh --format png -o thumbnail.png thumbnail.py Thumbnail

INK      = "#1a1a18"
OFFWHITE = "#e8e6df"
TEAL     = "#00b4d8"
GOLD     = "#d4a017"
GREEN    = "#74b860"
RED      = "#c84b2f"
GREY     = "#7a7875"
SURF     = "#2a2a27"
BLUE     = "#4a90d9"
ORANGE   = "#e8913a"


class Thumbnail(Scene):
    """YouTube thumbnail – 1920x1080 static frame."""

    def construct(self):
        self.camera.background_color = INK

        # ---- big title ----
        title = Text("C++20 Ranges", font="monospace", color=TEAL,
                      font_size=72, weight=BOLD)
        title.to_edge(UP, buff=0.8)

        # ---- subtitle ----
        subtitle = Text("20 Algorithms Visualized", font="monospace",
                         color=OFFWHITE, font_size=36)
        subtitle.next_to(title, DOWN, buff=0.3)

        # ---- decorative line ----
        line = Line(LEFT * 5, RIGHT * 5, stroke_color=TEAL, stroke_width=2)
        line.next_to(subtitle, DOWN, buff=0.35)

        # ---- old vs new code comparison ----
        old_label = Text("Before", font="monospace", color=RED, font_size=24)
        old_code = Text(
            "std::sort(v.begin(), v.end());",
            font="monospace", color=GREY, font_size=22,
        )
        old_strike = Line(
            old_code.get_left() + LEFT * 0.1,
            old_code.get_right() + RIGHT * 0.1,
            stroke_color=RED, stroke_width=3,
        )

        new_label = Text("After", font="monospace", color=GREEN, font_size=24)
        new_code = Text(
            "std::ranges::sort(v);",
            font="monospace", color=OFFWHITE, font_size=28, weight=BOLD,
        )

        # Glow rectangle behind new code
        glow = RoundedRectangle(
            width=new_code.width + 0.6, height=new_code.height + 0.4,
            corner_radius=0.1, stroke_color=TEAL, stroke_width=2,
            fill_color=TEAL, fill_opacity=0.08,
        )

        old_group = VGroup(old_label, VGroup(old_code, old_strike)).arrange(DOWN, buff=0.15)
        new_group = VGroup(new_label, VGroup(glow, new_code)).arrange(DOWN, buff=0.15)
        comparison = VGroup(old_group, new_group).arrange(RIGHT, buff=1.5)
        comparison.next_to(line, DOWN, buff=0.5)

        # ---- algorithm chips at the bottom ----
        algos = [
            "sort", "find", "count_if", "transform", "copy_if",
            "min/max", "reverse", "unique", "partition", "views",
        ]
        chips = VGroup()
        for a in algos:
            bg = RoundedRectangle(
                width=2.2, height=0.45, corner_radius=0.08,
                stroke_color=TEAL, stroke_width=1,
                fill_color=SURF, fill_opacity=1,
            )
            lbl = Text(a, font="monospace", color=OFFWHITE, font_size=16)
            lbl.move_to(bg)
            chips.add(VGroup(bg, lbl))
        chips.arrange_in_grid(rows=2, buff=(0.2, 0.15))
        chips.to_edge(DOWN, buff=0.6)

        # ---- watermark ----
        watermark = Text("© CodePuz", font="Arial", font_size=20,
                         color="#ffffff", weight=NORMAL)
        watermark.set_opacity(0.5).to_corner(DR, buff=0.25)

        # ---- add everything ----
        self.add(title, subtitle, line, comparison, chips, watermark)
