from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo0.py RangesIntro

# ---- colour palette ----
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

# ---- narration ----
LINES = {
    "hook": (
        "What if I told you that most of the verbose iterator code you write "
        "in C++ could be replaced with a single, clean line? "
        "Welcome to C++ 20 Ranges."
    ),
    "pain": (
        "In traditional C++, algorithms require you to spell out begin and end "
        "iterators everywhere. It's repetitive, error-prone, and hard to read."
    ),
    "solution": (
        "Ranges fix this. A range is simply anything that has a begin and an end. "
        "Vectors, arrays, strings, they're all ranges. "
        "Algorithms now accept the container directly."
    ),
    "preview": (
        "In this series, we'll explore 20 range algorithms, from sorting and searching "
        "to views and pipelines. Each one, visualized step by step. "
        "Let's get started."
    ),
}


class RangesIntro(VoiceoverScene):
    """Intro scene: hook the audience and introduce C++20 Ranges."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        # watermark
        watermark = Text("© CodePuz", font="Arial", font_size=18,
                         color="#ffffff", weight=NORMAL)
        watermark.set_opacity(0.35).to_corner(DR, buff=0.25)
        self.add(watermark)

        # ========== HOOK ==========
        hook_text = Text("What if one line could replace all this?",
                         font="monospace", color=OFFWHITE, font_size=28)

        # Show messy old-style code
        old_code = Code(
            code_string=(
                "std::sort(vec.begin(), vec.end());\n"
                "auto it = std::find(vec.begin(), vec.end(), 7);\n"
                "std::copy_if(v.begin(), v.end(),\n"
                "             std::back_inserter(out), pred);"
            ),
            language="cpp",
            add_line_numbers=False,
            formatter_style="monokai",
            background="rectangle",
        ).scale(0.85)

        with self.voiceover(LINES["hook"]) as tracker:
            self.play(FadeIn(hook_text, shift=DOWN * 0.3), run_time=0.6)
            self.wait(0.5)
            self.play(hook_text.animate.to_edge(UP, buff=0.5), run_time=0.4)
            self.play(FadeIn(old_code, shift=UP * 0.3), run_time=0.6)
            self.wait(max(0.2, tracker.duration - 2.0))

        # ========== THE PAIN ==========
        # Strike-through / redden the old code
        cross = Cross(old_code, stroke_color=RED, stroke_width=3)

        with self.voiceover(LINES["pain"]) as tracker:
            self.play(Create(cross), old_code.animate.set_opacity(0.4), run_time=0.8)
            self.wait(max(0.2, tracker.duration - 1.0))

        self.play(FadeOut(old_code), FadeOut(cross), FadeOut(hook_text))

        # ========== THE SOLUTION ==========
        new_code = Code(
            code_string=(
                "std::ranges::sort(vec);\n"
                "auto it = std::ranges::find(vec, 7);\n"
                "std::ranges::copy_if(v, std::back_inserter(out), pred);"
            ),
            language="cpp",
            add_line_numbers=False,
            formatter_style="monokai",
            background="rectangle",
        ).scale(0.85)

        ranges_title = Text("C++20 Ranges", font="monospace",
                            color=TEAL, font_size=40)
        ranges_sub = Text("Pass the container. Skip the boilerplate.",
                          font="monospace", color=GREY, font_size=20)
        ranges_title.to_edge(UP, buff=0.6)
        ranges_sub.next_to(ranges_title, DOWN, buff=0.25)

        with self.voiceover(LINES["solution"]) as tracker:
            self.play(
                Write(ranges_title),
                FadeIn(ranges_sub, shift=UP * 0.2),
                run_time=0.8,
            )
            self.play(FadeIn(new_code, shift=UP * 0.3), run_time=0.6)
            # Highlight the clean calls
            self.play(
                new_code.animate.set_opacity(1),
                run_time=0.3,
            )
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(FadeOut(new_code), FadeOut(ranges_sub))

        # ========== SERIES PREVIEW ==========
        # Quick flash of algorithm names
        algos = [
            "sort", "find", "count_if", "transform",
            "copy_if", "min/max", "reverse", "unique",
            "fill", "partition", "views | pipeline",
        ]
        algo_texts = VGroup(*[
            Text(f"ranges::{a}", font="monospace", color=OFFWHITE, font_size=20)
            for a in algos
        ]).arrange_in_grid(rows=3, buff=(0.6, 0.35)).next_to(ranges_title, DOWN, buff=0.6)

        with self.voiceover(LINES["preview"]) as tracker:
            self.play(
                LaggedStart(*[
                    FadeIn(t, shift=UP * 0.15, scale=0.9)
                    for t in algo_texts
                ], lag_ratio=0.08),
                run_time=1.5,
            )
            self.wait(max(0.2, tracker.duration - 2.5))

        # Final fade
        self.play(
            LaggedStart(*[FadeOut(t, shift=DOWN * 0.2) for t in algo_texts],
                        lag_ratio=0.05),
            FadeOut(ranges_title),
            run_time=1.0,
        )
        self.wait(0.3)
