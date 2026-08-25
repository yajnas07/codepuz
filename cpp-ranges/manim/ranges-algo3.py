from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo3.py RangesMinMax
# manim render -pql ranges-algo3.py RangesReverse

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
    # Scene 7: ranges::min / max / minmax
    "minmax_intro": (
        "Ranges min, max, and minmax let you find the smallest and largest "
        "elements in a range. They return the actual values, not iterators."
    ),
    "min_run": (
        "Ranges min scans every element and returns the smallest value. "
        "Here the minimum of our numbers is 1."
    ),
    "max_run": (
        "Ranges max works the same way but returns the largest value. "
        "The maximum here is 10."
    ),
    "minmax_run": (
        "Ranges minmax finds both the minimum and maximum in a single pass. "
        "This is more efficient than calling min and max separately. "
        "The result is unpacked using structured bindings."
    ),
    "minmax_summary": (
        "Use min or max when you only need one extreme. "
        "Use minmax when you need both, it traverses the range just once."
    ),

    # Scene 8: ranges::reverse
    "reverse_intro": (
        "Ranges reverse reverses the elements of a range in place. "
        "It modifies the container directly without returning a new one."
    ),
    "reverse_run": (
        "The algorithm swaps elements from both ends, working inward "
        "until the entire range is reversed."
    ),
    "reverse_note": (
        "For a non-mutating alternative, use std views reverse. "
        "It creates a lazy view without modifying the original container."
    ),
}

# ---- data ----
NUMS = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]


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


class RangesMinMax(VoiceoverScene):
    """Scene 7: std::ranges::min / max / minmax demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Find extremes")

        # ---- title ----
        title = Text("std::ranges::min / max / minmax", font="monospace",
                     color=TEAL, font_size=34)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["minmax_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- min animation ----
        code_min = make_code(
            "auto min_val = std::ranges::min(numbers);", 18
        )
        code_min.to_edge(UP, buff=0.5)

        src_label = Text("numbers", font="monospace", color=GREY, font_size=16)
        arr = make_array(NUMS)
        arr.move_to(UP * 0.2)
        src_label.next_to(arr, LEFT, buff=0.3)

        with self.voiceover(LINES["min_run"]) as tracker:
            self.play(FadeIn(code_min))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            # Track current minimum
            min_val = NUMS[0]
            min_idx = 0
            min_label = Text(f"min = {min_val}", font="monospace",
                             color=GREEN, font_size=18)
            min_label.next_to(arr, DOWN, buff=0.5)

            self.play(
                arr[0][0].animate.set_stroke(GREEN, width=3),
                FadeIn(min_label),
                run_time=0.3,
            )

            for i in range(1, len(NUMS)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.2)
                if NUMS[i] < min_val:
                    # reset old min highlight
                    self.play(
                        arr[min_idx][0].animate.set_stroke(GREY, width=2),
                        run_time=0.1,
                    )
                    min_val = NUMS[i]
                    min_idx = i
                    new_label = Text(f"min = {min_val}", font="monospace",
                                     color=GREEN, font_size=18)
                    new_label.move_to(min_label)
                    self.play(
                        arr[i][0].animate.set_stroke(GREEN, width=3),
                        Transform(min_label, new_label),
                        run_time=0.25,
                    )
                else:
                    self.play(arr[i].animate.set_opacity(0.4), run_time=0.1)

            self.play(FadeOut(scanner))

            result_min = Text(f"min_val = {min_val}", font="monospace",
                              color=GREEN, font_size=20)
            result_min.next_to(min_label, DOWN, buff=0.3)
            self.play(FadeIn(result_min))
            self.wait(max(0.2, tracker.duration - 5.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- max animation ----
        code_max = make_code(
            "auto max_val = std::ranges::max(numbers);", 18
        )
        code_max.to_edge(UP, buff=0.5)

        arr2 = make_array(NUMS)
        arr2.move_to(UP * 0.2)
        src_label2 = Text("numbers", font="monospace", color=GREY, font_size=16)
        src_label2.next_to(arr2, LEFT, buff=0.3)

        with self.voiceover(LINES["max_run"]) as tracker:
            self.play(FadeIn(code_max))
            self.play(FadeIn(src_label2),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr2], lag_ratio=0.05))

            scanner2 = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner2.next_to(arr2[0], UP, buff=0.15)
            self.play(FadeIn(scanner2), run_time=0.2)

            max_val = NUMS[0]
            max_idx = 0
            max_label = Text(f"max = {max_val}", font="monospace",
                             color=ORANGE, font_size=18)
            max_label.next_to(arr2, DOWN, buff=0.5)

            self.play(
                arr2[0][0].animate.set_stroke(ORANGE, width=3),
                FadeIn(max_label),
                run_time=0.3,
            )

            for i in range(1, len(NUMS)):
                self.play(scanner2.animate.next_to(arr2[i], UP, buff=0.15),
                          run_time=0.2)
                if NUMS[i] > max_val:
                    self.play(
                        arr2[max_idx][0].animate.set_stroke(GREY, width=2),
                        run_time=0.1,
                    )
                    max_val = NUMS[i]
                    max_idx = i
                    new_label = Text(f"max = {max_val}", font="monospace",
                                     color=ORANGE, font_size=18)
                    new_label.move_to(max_label)
                    self.play(
                        arr2[i][0].animate.set_stroke(ORANGE, width=3),
                        Transform(max_label, new_label),
                        run_time=0.25,
                    )
                else:
                    self.play(arr2[i].animate.set_opacity(0.4), run_time=0.1)

            self.play(FadeOut(scanner2))

            result_max = Text(f"max_val = {max_val}", font="monospace",
                              color=ORANGE, font_size=20)
            result_max.next_to(max_label, DOWN, buff=0.3)
            self.play(FadeIn(result_max))
            self.wait(max(0.2, tracker.duration - 5.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- minmax animation ----
        code_mm = make_code(
            "auto [min_elem, max_elem] =\n"
            "    std::ranges::minmax(numbers);", 18
        )
        code_mm.to_edge(UP, buff=0.5)

        arr3 = make_array(NUMS)
        arr3.move_to(UP * 0.2)
        src_label3 = Text("numbers", font="monospace", color=GREY, font_size=16)
        src_label3.next_to(arr3, LEFT, buff=0.3)

        with self.voiceover(LINES["minmax_run"]) as tracker:
            self.play(FadeIn(code_mm))
            self.play(FadeIn(src_label3),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr3], lag_ratio=0.05))

            scanner3 = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner3.next_to(arr3[0], UP, buff=0.15)
            self.play(FadeIn(scanner3), run_time=0.2)

            cur_min = NUMS[0]
            cur_max = NUMS[0]
            cur_min_idx = 0
            cur_max_idx = 0

            mm_label = Text(f"min = {cur_min}  max = {cur_max}",
                            font="monospace", color=GOLD, font_size=18)
            mm_label.next_to(arr3, DOWN, buff=0.5)

            self.play(
                arr3[0][0].animate.set_stroke(GOLD, width=3),
                FadeIn(mm_label),
                run_time=0.3,
            )

            for i in range(1, len(NUMS)):
                self.play(scanner3.animate.next_to(arr3[i], UP, buff=0.15),
                          run_time=0.2)

                updated = False
                if NUMS[i] < cur_min:
                    if cur_min_idx != cur_max_idx:
                        self.play(
                            arr3[cur_min_idx][0].animate.set_stroke(GREY, width=2),
                            run_time=0.1,
                        )
                    cur_min = NUMS[i]
                    cur_min_idx = i
                    self.play(
                        arr3[i][0].animate.set_stroke(GREEN, width=3),
                        run_time=0.15,
                    )
                    updated = True

                if NUMS[i] > cur_max:
                    if cur_max_idx != cur_min_idx:
                        self.play(
                            arr3[cur_max_idx][0].animate.set_stroke(GREY, width=2),
                            run_time=0.1,
                        )
                    cur_max = NUMS[i]
                    cur_max_idx = i
                    self.play(
                        arr3[i][0].animate.set_stroke(ORANGE, width=3),
                        run_time=0.15,
                    )
                    updated = True

                if updated:
                    new_mm = Text(f"min = {cur_min}  max = {cur_max}",
                                  font="monospace", color=GOLD, font_size=18)
                    new_mm.move_to(mm_label)
                    self.play(Transform(mm_label, new_mm), run_time=0.2)
                else:
                    self.play(arr3[i].animate.set_opacity(0.4), run_time=0.1)

            self.play(FadeOut(scanner3))

            result_mm = Text(
                f"minmax: [{cur_min}, {cur_max}]",
                font="monospace", color=GOLD, font_size=20,
            )
            result_mm.next_to(mm_label, DOWN, buff=0.3)
            self.play(FadeIn(result_mm))
            self.wait(max(0.2, tracker.duration - 6.0))

        # ---- summary ----
        with self.voiceover(LINES["minmax_summary"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("ranges::min(range)", "→ smallest value", GREEN),
                ("ranges::max(range)", "→ largest value", ORANGE),
                ("ranges::minmax(range)", "→ both in one pass", GOLD),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=18)
                row_r = Text(desc, font="monospace", color=GREY, font_size=18)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=1.0))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            note = Text("minmax is more efficient — single traversal ⚡",
                        font="monospace", color=TEAL, font_size=16)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.25))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesReverse(VoiceoverScene):
    """Scene 8: std::ranges::reverse demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Reverse a range")

        # ---- title ----
        title = Text("std::ranges::reverse", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["reverse_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- reverse animation ----
        code = make_code(
            "std::vector<int> to_reverse = numbers;\n"
            "std::ranges::reverse(to_reverse);", 18
        )
        code.to_edge(UP, buff=0.5)

        src_label = Text("to_reverse", font="monospace", color=GREY, font_size=16)
        arr = make_array(NUMS, cell_size=0.6)
        arr.move_to(UP * 0.1)
        src_label.next_to(arr, LEFT, buff=0.3)

        with self.voiceover(LINES["reverse_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))

            # Two pointers swapping from ends
            left_ptr = Triangle(color=GREEN, fill_opacity=1).scale(0.12)
            right_ptr = Triangle(color=ORANGE, fill_opacity=1).scale(0.12)

            left_ptr.next_to(arr[0], UP, buff=0.15)
            right_ptr.next_to(arr[-1], UP, buff=0.15)
            self.play(FadeIn(left_ptr), FadeIn(right_ptr), run_time=0.3)

            values = list(NUMS)
            left = 0
            right = len(values) - 1

            while left < right:
                # Highlight the pair
                self.play(
                    arr[left][0].animate.set_stroke(GREEN, width=3),
                    arr[right][0].animate.set_stroke(ORANGE, width=3),
                    run_time=0.2,
                )

                # Swap animation: move labels to each other's positions
                left_pos = arr[left][1].get_center()
                right_pos = arr[right][1].get_center()

                self.play(
                    arr[left][1].animate.move_to(right_pos),
                    arr[right][1].animate.move_to(left_pos),
                    run_time=0.4,
                    rate_func=smooth,
                )

                # Swap the actual VGroup label references
                arr[left][1], arr[right][1] = arr[right][1], arr[left][1]
                values[left], values[right] = values[right], values[left]

                # Reset stroke
                self.play(
                    arr[left][0].animate.set_stroke(GREY, width=2),
                    arr[right][0].animate.set_stroke(GREY, width=2),
                    run_time=0.1,
                )

                left += 1
                right -= 1

                if left < right:
                    self.play(
                        left_ptr.animate.next_to(arr[left], UP, buff=0.15),
                        right_ptr.animate.next_to(arr[right], UP, buff=0.15),
                        run_time=0.2,
                    )

            self.play(FadeOut(left_ptr), FadeOut(right_ptr))

            result = Text(
                f"reversed = {{{', '.join(str(x) for x in values)}}}",
                font="monospace", color=GREEN, font_size=18,
            )
            result.next_to(arr, DOWN, buff=0.5)
            self.play(FadeIn(result))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- views::reverse note ----
        with self.voiceover(LINES["reverse_note"]) as tracker:
            note_code = make_code(
                "// Non-mutating alternative:\n"
                "for (int x : numbers | std::views::reverse)\n"
                "    // lazy view, no copy", 16
            )
            note_code.next_to(result, DOWN, buff=0.4)
            self.play(FadeIn(note_code))
            self.wait(max(0.2, tracker.duration - 1.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
