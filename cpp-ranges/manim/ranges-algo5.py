from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo5.py RangesFill
# manim render -pql ranges-algo5.py RangesGenerate

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


def _scene_label(scene, text):
    """Add a persistent bottom-left scene label."""
    lbl = Text(text, font="monospace", font_size=24, color="#74b860")
    lbl.set_opacity(0.7).to_corner(DL, buff=0.25)
    scene.add(lbl)
    return lbl

# ---- narration lines ----
LINES = {
    # Scene 11: ranges::fill
    "fill_intro": (
        "Ranges fill assigns the same value to every element in a range. "
        "It's the simplest way to initialise or reset a container."
    ),
    "fill_run": (
        "We start with a vector of five zeros. "
        "Fill overwrites each element with the value 42, one by one."
    ),
    "fill_note": (
        "There is also fill n, which fills only the first n elements. "
        "Fill always covers the entire range."
    ),

    # Scene 12: ranges::generate
    "gen_intro": (
        "Ranges generate assigns values by calling a generator function for each element. "
        "Unlike fill, every element can receive a different value."
    ),
    "gen_run": (
        "Our generator is a lambda that captures a counter by reference. "
        "Each call returns the current counter value and then increments it, "
        "producing the sequence 0, 1, 2, 3, and so on."
    ),
    "gen_summary": (
        "Fill gives every element the same value. "
        "Generate gives each element a potentially different value from a callable. "
        "Common uses include sequential numbers, random values, or computed sequences."
    ),
}


def make_array(values, cell_color=GREY, text_color=OFFWHITE, cell_size=0.6,
               highlight_idx=None, highlight_color=TEAL):
    """Create a row of boxes with values inside."""
    grp = VGroup()
    for i, v in enumerate(values):
        sc = cell_color if highlight_idx != i else highlight_color
        cell = RoundedRectangle(
            width=cell_size, height=cell_size, corner_radius=0.06,
            stroke_color=sc, stroke_width=2,
            fill_color=SURF, fill_opacity=1,
        )
        lbl = Text(str(v), font="monospace", color=text_color).scale(0.35)
        lbl.move_to(cell)
        grp.add(VGroup(cell, lbl))
    grp.arrange(RIGHT, buff=0.1)
    return grp


def make_code(text, font_size=20):
    """Create a styled code block."""
    code_text = Text(text, font="monospace", color=OFFWHITE, font_size=font_size)
    bg = RoundedRectangle(
        width=code_text.width + 0.6,
        height=code_text.height + 0.4,
        corner_radius=0.1,
        stroke_color=GREY, stroke_width=1,
        fill_color=SURF, fill_opacity=1,
    )
    code_text.move_to(bg)
    return VGroup(bg, code_text)


def make_watermark():
    watermark = Text("© CodePuz", font="Arial", font_size=18,
                     color="#ffffff", weight=NORMAL)
    watermark.set_opacity(0.35).to_corner(DR, buff=0.25)
    return watermark


class RangesFill(VoiceoverScene):
    """Scene 11: std::ranges::fill demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Fill with a value")

        # ---- title ----
        title = Text("std::ranges::fill", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["fill_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- fill animation ----
        code = make_code(
            "std::vector<int> filled(5);\n"
            "std::ranges::fill(filled, 42);", 18
        )
        code.to_edge(UP, buff=0.5)

        init_vals = [0, 0, 0, 0, 0]
        src_label = Text("filled", font="monospace", color=GREY, font_size=16)
        arr = make_array(init_vals, cell_size=0.7)
        arr.move_to(ORIGIN)
        src_label.next_to(arr, LEFT, buff=0.3)

        fill_val_label = Text("value: 42", font="monospace",
                              color=GOLD, font_size=16)
        fill_val_label.next_to(arr, RIGHT, buff=0.5)

        with self.voiceover(LINES["fill_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))
            self.play(FadeIn(fill_val_label))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            for i in range(len(init_vals)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.2)

                # Replace the label with 42
                new_lbl = Text("42", font="monospace", color=GREEN).scale(0.35)
                new_lbl.move_to(arr[i][1].get_center())
                self.play(
                    arr[i][0].animate.set_stroke(GREEN, width=3),
                    FadeOut(arr[i][1]),
                    FadeIn(new_lbl),
                    run_time=0.3,
                )
                arr[i].remove(arr[i][1])
                arr[i].add(new_lbl)

                # Reset stroke after a beat
                self.play(
                    arr[i][0].animate.set_stroke(GREY, width=2),
                    run_time=0.1,
                )

            self.play(FadeOut(scanner))

            result = Text("filled = {42, 42, 42, 42, 42}",
                          font="monospace", color=GREEN, font_size=18)
            result.next_to(arr, DOWN, buff=0.5)
            self.play(FadeIn(result))
            self.wait(max(0.2, tracker.duration - 4.0))

        # ---- fill_n note ----
        with self.voiceover(LINES["fill_note"]) as tracker:
            note = Text("fill → entire range    fill_n → first n elements",
                        font="monospace", color=ORANGE, font_size=16)
            note.next_to(result, DOWN, buff=0.4)
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 1.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesGenerate(VoiceoverScene):
    """Scene 12: std::ranges::generate demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Generate values")

        # ---- title ----
        title = Text("std::ranges::generate", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["gen_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- generate animation ----
        code = make_code(
            "std::vector<int> generated(10);\n"
            "int counter = 0;\n"
            "std::ranges::generate(generated,\n"
            "    [&counter]() { return counter++; });", 17
        )
        code.to_edge(UP, buff=0.4)

        init_vals = [0] * 10
        src_label = Text("generated", font="monospace", color=GREY, font_size=16)
        arr = make_array(init_vals, cell_size=0.55)
        arr.move_to(UP * 0.0)
        src_label.next_to(arr, LEFT, buff=0.3)

        # Counter display
        counter_label = Text("counter = 0", font="monospace",
                             color=GOLD, font_size=16)
        counter_label.next_to(arr, DOWN, buff=0.5)

        with self.voiceover(LINES["gen_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.04))
            self.play(FadeIn(counter_label))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            for i in range(10):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.15)

                # Replace label with counter value
                new_lbl = Text(str(i), font="monospace", color=BLUE).scale(0.35)
                new_lbl.move_to(arr[i][1].get_center())

                # Update counter display
                new_counter = Text(f"counter = {i + 1}", font="monospace",
                                   color=GOLD, font_size=16)
                new_counter.move_to(counter_label)

                self.play(
                    arr[i][0].animate.set_stroke(BLUE, width=3),
                    FadeOut(arr[i][1]),
                    FadeIn(new_lbl),
                    Transform(counter_label, new_counter),
                    run_time=0.25,
                )
                arr[i].remove(arr[i][1])
                arr[i].add(new_lbl)

                self.play(
                    arr[i][0].animate.set_stroke(GREY, width=2),
                    run_time=0.08,
                )

            self.play(FadeOut(scanner))

            result = Text("generated = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}",
                          font="monospace", color=BLUE, font_size=17)
            result.next_to(counter_label, DOWN, buff=0.4)
            self.play(FadeIn(result))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- summary ----
        with self.voiceover(LINES["gen_summary"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("ranges::fill(range, val)", "same value for all", GREEN),
                ("ranges::generate(range, fn)", "different value per element", BLUE),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=18)
                row_r = Text(desc, font="monospace", color=GREY, font_size=18)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=1.0))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            uses = Text("generate uses: sequences, random values, computed data",
                        font="monospace", color=ORANGE, font_size=15)
            uses.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.3))
            self.play(FadeIn(uses))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
