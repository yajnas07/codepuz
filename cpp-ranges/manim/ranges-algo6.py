from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo6.py RangesReplaceIf
# manim render -pql ranges-algo6.py RangesPartition

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
    # Scene 13: ranges::replace_if
    "replace_intro": (
        "Ranges replace if overwrites elements that match a condition with a new value. "
        "Unlike remove if, it does not eliminate elements. The container size stays the same."
    ),
    "replace_run": (
        "We replace all even numbers with zero. "
        "The predicate checks divisibility by 2. "
        "Matching elements are overwritten in place."
    ),
    "replace_note": (
        "Replace if modifies in place without changing the container size. "
        "Remove if eliminates matching elements. "
        "Choose based on whether you want to keep or discard matches."
    ),

    # Scene 14: ranges::partition
    "part_intro": (
        "Ranges partition rearranges elements so that all elements satisfying a condition "
        "come before those that don't. It returns the partition point."
    ),
    "part_run": (
        "We partition numbers into two groups: elements less than or equal to 5 go left, "
        "and elements greater than 5 go right. "
        "The relative order within each group is not preserved."
    ),
    "part_result": (
        "The returned subrange starts at the partition point. "
        "Everything before it satisfies the predicate. Everything after does not."
    ),
    "part_summary": (
        "Partition is useful for quicksort pivots, separating data into two groups, "
        "and filtering in place without allocating a second container. "
        "Use stable partition if you need to preserve relative order."
    ),
}

# ---- data ----
REPLACE_NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
PART_NUMS = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]


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


class RangesReplaceIf(VoiceoverScene):
    """Scene 13: std::ranges::replace_if demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Replace matching elements")

        # ---- title ----
        title = Text("std::ranges::replace_if", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["replace_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- replace_if animation ----
        code = make_code(
            "std::ranges::replace_if(to_replace,\n"
            "    [](int x) { return x % 2 == 0; }, 0);", 18
        )
        code.to_edge(UP, buff=0.5)

        src_label = Text("to_replace", font="monospace", color=GREY, font_size=16)
        arr = make_array(REPLACE_NUMS, cell_size=0.6)
        arr.move_to(UP * 0.1)
        src_label.next_to(arr, LEFT, buff=0.3)

        cond_label = Text("predicate: x % 2 == 0  →  replace with 0",
                          font="monospace", color=GOLD, font_size=15)
        cond_label.next_to(arr, DOWN, buff=0.5)

        with self.voiceover(LINES["replace_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))
            self.play(FadeIn(cond_label))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            result_vals = list(REPLACE_NUMS)

            for i in range(len(REPLACE_NUMS)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.2)

                is_even = REPLACE_NUMS[i] % 2 == 0
                if is_even:
                    # Highlight as match
                    self.play(
                        arr[i][0].animate.set_stroke(ORANGE, width=3),
                        run_time=0.15,
                    )

                    # Replace the label with 0
                    new_lbl = Text("0", font="monospace", color=ORANGE).scale(0.35)
                    new_lbl.move_to(arr[i][1].get_center())
                    self.play(
                        FadeOut(arr[i][1]),
                        FadeIn(new_lbl),
                        run_time=0.3,
                    )
                    arr[i].remove(arr[i][1])
                    arr[i].add(new_lbl)
                    result_vals[i] = 0

                    # Reset stroke
                    self.play(
                        arr[i][0].animate.set_stroke(GREY, width=2),
                        run_time=0.1,
                    )
                else:
                    # Not a match — brief green flash
                    self.play(
                        arr[i][0].animate.set_stroke(GREEN, width=3),
                        run_time=0.12,
                    )
                    self.play(
                        arr[i][0].animate.set_stroke(GREY, width=2),
                        run_time=0.08,
                    )

            self.play(FadeOut(scanner))

            result = Text(
                f"result = {{{', '.join(str(x) for x in result_vals)}}}",
                font="monospace", color=ORANGE, font_size=18,
            )
            result.next_to(cond_label, DOWN, buff=0.4)
            self.play(FadeIn(result))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- comparison note ----
        with self.voiceover(LINES["replace_note"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("replace_if(range, pred, val)", "overwrite matches → same size", ORANGE),
                ("remove_if(range, pred)", "eliminate matches → smaller size", RED),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=17)
                row_r = Text(desc, font="monospace", color=GREY, font_size=17)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=0.8))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.3))
            self.wait(max(0.2, tracker.duration - 1.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesPartition(VoiceoverScene):
    """Scene 14: std::ranges::partition demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Partition a range")

        # ---- title ----
        title = Text("std::ranges::partition", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["part_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- partition animation ----
        code = make_code(
            "auto pivot = std::ranges::partition(\n"
            "    to_partition,\n"
            "    [](int x) { return x <= 5; });", 17
        )
        code.to_edge(UP, buff=0.5)

        src_label = Text("to_partition", font="monospace", color=GREY, font_size=16)
        arr = make_array(PART_NUMS, cell_size=0.6)
        arr.move_to(UP * 0.0)
        src_label.next_to(arr, LEFT, buff=0.3)

        cond_label = Text("predicate: x <= 5",
                          font="monospace", color=GOLD, font_size=16)
        cond_label.next_to(arr, DOWN, buff=0.5)

        with self.voiceover(LINES["part_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))
            self.play(FadeIn(cond_label))

            # Two-pointer partition animation
            left_ptr = Triangle(color=GREEN, fill_opacity=1).scale(0.12)
            right_ptr = Triangle(color=ORANGE, fill_opacity=1).scale(0.12)

            values = list(PART_NUMS)
            left = 0
            right = len(values) - 1

            left_ptr.next_to(arr[left], UP, buff=0.15)
            right_ptr.next_to(arr[right], UP, buff=0.15)

            lbl_left = Text("L", font="monospace", color=GREEN, font_size=14)
            lbl_right = Text("R", font="monospace", color=ORANGE, font_size=14)
            lbl_left.next_to(left_ptr, UP, buff=0.05)
            lbl_right.next_to(right_ptr, UP, buff=0.05)

            self.play(FadeIn(left_ptr), FadeIn(right_ptr),
                      FadeIn(lbl_left), FadeIn(lbl_right), run_time=0.3)

            # Simulate partition with two pointers
            while left < right:
                # Advance left while it satisfies predicate
                while left < right and values[left] <= 5:
                    self.play(
                        arr[left][0].animate.set_stroke(GREEN, width=3),
                        run_time=0.15,
                    )
                    left += 1
                    if left < right:
                        self.play(
                            left_ptr.animate.next_to(arr[left], UP, buff=0.15),
                            lbl_left.animate.next_to(arr[left], UP, buff=0.35),
                            run_time=0.15,
                        )

                # Advance right while it doesn't satisfy predicate
                while left < right and values[right] > 5:
                    self.play(
                        arr[right][0].animate.set_stroke(ORANGE, width=3),
                        run_time=0.15,
                    )
                    right -= 1
                    if left < right:
                        self.play(
                            right_ptr.animate.next_to(arr[right], UP, buff=0.15),
                            lbl_right.animate.next_to(arr[right], UP, buff=0.35),
                            run_time=0.15,
                        )

                if left < right:
                    # Swap animation
                    self.play(
                        arr[left][0].animate.set_stroke(TEAL, width=3),
                        arr[right][0].animate.set_stroke(TEAL, width=3),
                        run_time=0.2,
                    )

                    left_pos = arr[left][1].get_center()
                    right_pos = arr[right][1].get_center()

                    self.play(
                        arr[left][1].animate.move_to(right_pos),
                        arr[right][1].animate.move_to(left_pos),
                        run_time=0.4,
                        rate_func=smooth,
                    )

                    # Swap references and values
                    arr[left][1], arr[right][1] = arr[right][1], arr[left][1]
                    values[left], values[right] = values[right], values[left]

                    # Color according to partition
                    self.play(
                        arr[left][0].animate.set_stroke(GREEN, width=3),
                        arr[right][0].animate.set_stroke(ORANGE, width=3),
                        run_time=0.15,
                    )

                    left += 1
                    right -= 1

                    if left <= right:
                        self.play(
                            left_ptr.animate.next_to(arr[left], UP, buff=0.15),
                            lbl_left.animate.next_to(arr[left], UP, buff=0.35),
                            right_ptr.animate.next_to(arr[right], UP, buff=0.15),
                            lbl_right.animate.next_to(arr[right], UP, buff=0.35),
                            run_time=0.15,
                        )

            # Color any remaining elements
            for i in range(len(values)):
                clr = GREEN if values[i] <= 5 else ORANGE
                arr[i][0].set_stroke(clr, width=3)

            self.play(FadeOut(left_ptr), FadeOut(right_ptr),
                      FadeOut(lbl_left), FadeOut(lbl_right))
            self.wait(max(0.2, tracker.duration - 6.0))

        # ---- show partition point ----
        with self.voiceover(LINES["part_result"]) as tracker:
            # Find partition point
            part_idx = sum(1 for v in values if v <= 5)

            divider = Line(UP * 0.4, DOWN * 0.4, color=GOLD, stroke_width=3)
            divider.move_to(
                (arr[part_idx - 1].get_right() + arr[part_idx].get_left()) / 2
            )

            part_label = Text(f"partition point at index {part_idx}",
                              font="monospace", color=GOLD, font_size=16)
            part_label.next_to(cond_label, DOWN, buff=0.4)

            left_grp = Text("≤ 5", font="monospace", color=GREEN, font_size=16)
            right_grp = Text("> 5", font="monospace", color=ORANGE, font_size=16)
            left_grp.next_to(divider, LEFT, buff=0.8)
            left_grp.shift(DOWN * 0.7)
            right_grp.next_to(divider, RIGHT, buff=0.8)
            right_grp.shift(DOWN * 0.7)

            self.play(Create(divider), FadeIn(part_label))
            self.play(FadeIn(left_grp), FadeIn(right_grp))
            self.wait(max(0.2, tracker.duration - 2.0))

        # ---- summary ----
        with self.voiceover(LINES["part_summary"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("partition(range, pred)", "unstable — order not preserved", TEAL),
                ("stable_partition(range, pred)", "stable — order preserved", GREEN),
                ("is_partitioned(range, pred)", "check if already partitioned", GOLD),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=17)
                row_r = Text(desc, font="monospace", color=GREY, font_size=17)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=0.8))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            note = Text("O(n) time, O(1) space — two-pointer swap ⚡",
                        font="monospace", color=ORANGE, font_size=15)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.25))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
