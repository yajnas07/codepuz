from manim import *

# manim render -qh --format png -o cover.png cover.py Cover

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


class Cover(Scene):
    """Blog post cover image – 1920x1080 static frame."""

    def construct(self):
        self.camera.background_color = INK

        # ---- big title ----
        title = Text("Raw Loops to Ranges", font="monospace", color=TEAL,
                      font_size=64, weight=BOLD)
        title.to_edge(UP, buff=0.7)

        # ---- subtitle ----
        subtitle = Text("Views, Pipes, and Laziness in C++20", font="monospace",
                         color=OFFWHITE, font_size=28)
        subtitle.next_to(title, DOWN, buff=0.3)

        # ---- decorative line ----
        line = Line(LEFT * 5, RIGHT * 5, stroke_color=TEAL, stroke_width=2)
        line.next_to(subtitle, DOWN, buff=0.35)

        # ---- three-stage progression ----
        # Stage 1: Raw loop
        stage1_label = Text("① Raw Loop", font="monospace", color=RED, font_size=16)
        stage1_code = Text(
            "for (auto& p : people)\n"
            "  if (p.age >= 18)\n"
            "    names.push_back(p.name);",
            font="monospace", color=GREY, font_size=13,
        )
        stage1 = VGroup(stage1_label, stage1_code).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        # Stage 2: Algorithms
        stage2_label = Text("② Algorithms", font="monospace", color=GOLD, font_size=16)
        stage2_code = Text(
            "copy_if(begin, end,\n"
            "  back_inserter, pred);\n"
            "transform(begin, end,\n"
            "  back_inserter, &name);",
            font="monospace", color=GREY, font_size=13,
        )
        stage2 = VGroup(stage2_label, stage2_code).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        # Stage 3: Ranges + Views
        stage3_label = Text("③ Ranges | Views", font="monospace", color=GREEN, font_size=16)
        stage3_code = Text(
            "auto names = people\n"
            "  | filter(adult)\n"
            "  | transform(&name);",
            font="monospace", color=OFFWHITE, font_size=15, weight=BOLD,
        )
        # Glow behind the ranges code
        glow = RoundedRectangle(
            width=stage3_code.width + 0.5, height=stage3_code.height + 0.3,
            corner_radius=0.1, stroke_color=TEAL, stroke_width=2,
            fill_color=TEAL, fill_opacity=0.06,
        )
        glow.move_to(stage3_code)
        stage3 = VGroup(stage3_label, VGroup(glow, stage3_code)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)

        # Arrange stages with arrows
        arrow1 = Text("→", font="monospace", color=GREY, font_size=24)
        arrow2 = Text("→", font="monospace", color=GREY, font_size=24)

        progression = VGroup(stage1, arrow1, stage2, arrow2, stage3).arrange(
            RIGHT, buff=0.3, aligned_edge=UP
        )
        progression.next_to(line, DOWN, buff=0.45)
        # Ensure it fits within frame width
        if progression.width > 13:
            progression.scale_to_fit_width(13)

        # ---- key concepts at the bottom ----
        concepts = ["views", "pipes |", "lazy eval", "projections", "no copies"]
        chips = VGroup()
        for c in concepts:
            bg = RoundedRectangle(
                width=max(1.8, len(c) * 0.2 + 0.8), height=0.42, corner_radius=0.08,
                stroke_color=TEAL, stroke_width=1,
                fill_color=SURF, fill_opacity=1,
            )
            lbl = Text(c, font="monospace", color=OFFWHITE, font_size=15)
            lbl.move_to(bg)
            chips.add(VGroup(bg, lbl))
        chips.arrange(RIGHT, buff=0.25)
        chips.to_edge(DOWN, buff=0.6)

        # ---- watermark ----
        watermark = Text("© CodePuz", font="Arial", font_size=20,
                         color="#ffffff", weight=NORMAL)
        watermark.set_opacity(0.5).to_corner(DR, buff=0.25)

        # ---- add everything ----
        self.add(title, subtitle, line, progression, chips, watermark)
