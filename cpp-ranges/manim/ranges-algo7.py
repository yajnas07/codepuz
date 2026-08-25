from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo7.py RangesIsSorted
# manim render -pql ranges-algo7.py RangesBinarySearch

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
    # Scene 15: ranges::is_sorted
    "sorted_intro": (
        "Ranges is sorted checks whether a range is sorted in non-descending order. "
        "It returns a simple boolean, true or false."
    ),
    "sorted_yes": (
        "We check the sequence 1, 2, 3, 4, 5. "
        "Each element is less than or equal to the next, so the result is true."
    ),
    "sorted_no": (
        "Now we check 3, 1, 4, 1, 5. "
        "The algorithm short circuits as soon as it finds 3 followed by 1, "
        "which violates the ordering. The result is false."
    ),
    "sorted_note": (
        "Is sorted until is a related algorithm. "
        "Instead of a boolean, it returns an iterator to the first out-of-order element. "
        "Both are useful as pre-condition checks before binary search or merge."
    ),

    # Scene 16: ranges::binary_search
    "bsearch_intro": (
        "Ranges binary search performs an efficient O log n lookup on sorted data. "
        "It returns true if the value exists, false otherwise."
    ),
    "bsearch_found": (
        "We search for 5 in the sorted range 1 through 10. "
        "The algorithm repeatedly halves the search space, "
        "comparing the middle element until it finds 5."
    ),
    "bsearch_not_found": (
        "Now we search for 11, which is not in the range. "
        "The search space shrinks to empty, so the result is false."
    ),
    "bsearch_note": (
        "Binary search only returns a boolean. "
        "If you need the position, use lower bound or equal range instead. "
        "The range must be sorted, otherwise the result is undefined."
    ),
}

# ---- data ----
SORTED_YES = [1, 2, 3, 4, 5]
SORTED_NO  = [3, 1, 4, 1, 5]
BSEARCH_NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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


class RangesIsSorted(VoiceoverScene):
    """Scene 15: std::ranges::is_sorted demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Check if sorted")

        # ---- title ----
        title = Text("std::ranges::is_sorted", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["sorted_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- sorted case: {1,2,3,4,5} ----
        code1 = make_code(
            "std::ranges::is_sorted({1, 2, 3, 4, 5})", 18
        )
        code1.to_edge(UP, buff=0.5)

        arr1 = make_array(SORTED_YES, cell_size=0.7)
        arr1.move_to(UP * 0.1)

        with self.voiceover(LINES["sorted_yes"]) as tracker:
            self.play(FadeIn(code1))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr1], lag_ratio=0.06))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr1[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            # Check pairs
            for i in range(len(SORTED_YES) - 1):
                self.play(scanner.animate.next_to(arr1[i], UP, buff=0.15),
                          run_time=0.2)

                # Highlight the pair being compared
                comp_label = Text(
                    f"{SORTED_YES[i]} ≤ {SORTED_YES[i+1]} ✓",
                    font="monospace", color=GREEN, font_size=14,
                )
                comp_label.next_to(arr1[i], DOWN, buff=0.3)

                self.play(
                    arr1[i][0].animate.set_stroke(GREEN, width=3),
                    arr1[i+1][0].animate.set_stroke(GREEN, width=3),
                    FadeIn(comp_label),
                    run_time=0.25,
                )
                self.play(
                    arr1[i][0].animate.set_stroke(GREY, width=2),
                    arr1[i+1][0].animate.set_stroke(GREY, width=2),
                    FadeOut(comp_label),
                    run_time=0.15,
                )

            self.play(FadeOut(scanner))

            result1 = Text("→ true", font="monospace", color=GREEN, font_size=22)
            result1.next_to(arr1, DOWN, buff=0.5)
            self.play(FadeIn(result1))
            self.wait(max(0.2, tracker.duration - 4.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- unsorted case: {3,1,4,1,5} ----
        code2 = make_code(
            "std::ranges::is_sorted({3, 1, 4, 1, 5})", 18
        )
        code2.to_edge(UP, buff=0.5)

        arr2 = make_array(SORTED_NO, cell_size=0.7)
        arr2.move_to(UP * 0.1)

        with self.voiceover(LINES["sorted_no"]) as tracker:
            self.play(FadeIn(code2))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr2], lag_ratio=0.06))

            scanner2 = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner2.next_to(arr2[0], UP, buff=0.15)
            self.play(FadeIn(scanner2), run_time=0.2)

            # First pair: 3 > 1 — fails!
            self.play(scanner2.animate.next_to(arr2[0], UP, buff=0.15),
                      run_time=0.2)

            comp_fail = Text(
                f"3 > 1 ✗  short-circuit!",
                font="monospace", color=RED, font_size=14,
            )
            comp_fail.next_to(arr2[0], DOWN, buff=0.3)

            self.play(
                arr2[0][0].animate.set_stroke(RED, width=3),
                arr2[1][0].animate.set_stroke(RED, width=3),
                FadeIn(comp_fail),
                run_time=0.3,
            )

            # Dim remaining elements (never examined)
            for i in range(2, len(SORTED_NO)):
                arr2[i].set_opacity(0.35)

            self.play(FadeOut(scanner2))

            result2 = Text("→ false", font="monospace", color=RED, font_size=22)
            result2.next_to(arr2, DOWN, buff=0.7)
            self.play(FadeIn(result2))
            self.wait(max(0.2, tracker.duration - 3.0))

        # ---- is_sorted_until note ----
        with self.voiceover(LINES["sorted_note"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("is_sorted(range)", "→ bool (true / false)", GREEN),
                ("is_sorted_until(range)", "→ iterator to first violation", GOLD),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=18)
                row_r = Text(desc, font="monospace", color=GREY, font_size=18)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=0.8))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            note = Text("useful as pre-condition for binary_search, merge",
                        font="monospace", color=ORANGE, font_size=15)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.3))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesBinarySearch(VoiceoverScene):
    """Scene 16: std::ranges::binary_search demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Binary search")

        # ---- title ----
        title = Text("std::ranges::binary_search", font="monospace",
                     color=TEAL, font_size=34)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["bsearch_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- binary search for 5 (found) ----
        code1 = make_code(
            "std::ranges::binary_search(\n"
            "    {1,2,3,4,5,6,7,8,9,10}, 5);", 18
        )
        code1.to_edge(UP, buff=0.5)

        arr = make_array(BSEARCH_NUMS, cell_size=0.55)
        arr.move_to(UP * 0.0)

        target_label = Text("target: 5", font="monospace",
                            color=GOLD, font_size=16)
        target_label.next_to(arr, RIGHT, buff=0.5)

        with self.voiceover(LINES["bsearch_found"]) as tracker:
            self.play(FadeIn(code1))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.04))
            self.play(FadeIn(target_label))

            # Binary search animation
            lo, hi = 0, len(BSEARCH_NUMS) - 1
            target = 5

            # Bracket indicators
            lo_marker = Text("lo", font="monospace", color=GREEN, font_size=12)
            hi_marker = Text("hi", font="monospace", color=ORANGE, font_size=12)
            mid_marker = Triangle(color=TEAL, fill_opacity=1).scale(0.12)

            lo_marker.next_to(arr[lo], DOWN, buff=0.15)
            hi_marker.next_to(arr[hi], DOWN, buff=0.15)

            self.play(FadeIn(lo_marker), FadeIn(hi_marker), run_time=0.3)

            while lo <= hi:
                mid = (lo + hi) // 2

                mid_marker.next_to(arr[mid], UP, buff=0.15)
                mid_label = Text(f"mid={BSEARCH_NUMS[mid]}", font="monospace",
                                 color=TEAL, font_size=13)
                mid_label.next_to(mid_marker, UP, buff=0.08)

                self.play(
                    FadeIn(mid_marker), FadeIn(mid_label),
                    arr[mid][0].animate.set_stroke(TEAL, width=3),
                    run_time=0.3,
                )

                if BSEARCH_NUMS[mid] == target:
                    # Found!
                    self.play(
                        arr[mid][0].animate.set_stroke(GREEN, width=4),
                        arr[mid][1].animate.set_color(GREEN),
                        run_time=0.3,
                    )
                    self.play(FadeOut(mid_label))
                    break
                elif BSEARCH_NUMS[mid] < target:
                    # Dim left half
                    for j in range(lo, mid + 1):
                        arr[j].set_opacity(0.3)
                    lo = mid + 1
                    self.play(
                        lo_marker.animate.next_to(arr[lo], DOWN, buff=0.15),
                        FadeOut(mid_label),
                        run_time=0.25,
                    )
                else:
                    # Dim right half
                    for j in range(mid, hi + 1):
                        arr[j].set_opacity(0.3)
                    hi = mid - 1
                    self.play(
                        hi_marker.animate.next_to(arr[hi], DOWN, buff=0.15),
                        FadeOut(mid_label),
                        run_time=0.25,
                    )

                self.play(FadeOut(mid_marker), run_time=0.1)

            result1 = Text("→ true  (found!)", font="monospace",
                           color=GREEN, font_size=20)
            result1.next_to(arr, DOWN, buff=0.7)
            self.play(FadeIn(result1),
                      FadeOut(lo_marker), FadeOut(hi_marker), FadeOut(mid_marker))
            self.wait(max(0.2, tracker.duration - 5.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- binary search for 11 (not found) ----
        code2 = make_code(
            "std::ranges::binary_search(\n"
            "    {1,2,3,4,5,6,7,8,9,10}, 11);", 18
        )
        code2.to_edge(UP, buff=0.5)

        arr2 = make_array(BSEARCH_NUMS, cell_size=0.55)
        arr2.move_to(UP * 0.0)

        target_label2 = Text("target: 11", font="monospace",
                             color=GOLD, font_size=16)
        target_label2.next_to(arr2, RIGHT, buff=0.5)

        with self.voiceover(LINES["bsearch_not_found"]) as tracker:
            self.play(FadeIn(code2))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr2], lag_ratio=0.04))
            self.play(FadeIn(target_label2))

            lo, hi = 0, len(BSEARCH_NUMS) - 1
            target = 11

            lo_marker2 = Text("lo", font="monospace", color=GREEN, font_size=12)
            hi_marker2 = Text("hi", font="monospace", color=ORANGE, font_size=12)
            mid_marker2 = Triangle(color=TEAL, fill_opacity=1).scale(0.12)

            lo_marker2.next_to(arr2[lo], DOWN, buff=0.15)
            hi_marker2.next_to(arr2[hi], DOWN, buff=0.15)

            self.play(FadeIn(lo_marker2), FadeIn(hi_marker2), run_time=0.3)

            while lo <= hi:
                mid = (lo + hi) // 2

                mid_marker2.next_to(arr2[mid], UP, buff=0.15)
                mid_label2 = Text(f"mid={BSEARCH_NUMS[mid]}", font="monospace",
                                  color=TEAL, font_size=13)
                mid_label2.next_to(mid_marker2, UP, buff=0.08)

                self.play(
                    FadeIn(mid_marker2), FadeIn(mid_label2),
                    arr2[mid][0].animate.set_stroke(TEAL, width=3),
                    run_time=0.3,
                )

                if BSEARCH_NUMS[mid] < target:
                    for j in range(lo, mid + 1):
                        arr2[j].set_opacity(0.3)
                    lo = mid + 1
                    if lo <= hi:
                        self.play(
                            lo_marker2.animate.next_to(arr2[lo], DOWN, buff=0.15),
                            FadeOut(mid_label2),
                            run_time=0.25,
                        )
                    else:
                        self.play(FadeOut(mid_label2), run_time=0.15)
                else:
                    for j in range(mid, hi + 1):
                        arr2[j].set_opacity(0.3)
                    hi = mid - 1
                    if lo <= hi:
                        self.play(
                            hi_marker2.animate.next_to(arr2[hi], DOWN, buff=0.15),
                            FadeOut(mid_label2),
                            run_time=0.25,
                        )
                    else:
                        self.play(FadeOut(mid_label2), run_time=0.15)

                self.play(FadeOut(mid_marker2), run_time=0.1)

            empty_label = Text("search space empty!", font="monospace",
                               color=RED, font_size=16)
            empty_label.next_to(arr2, DOWN, buff=0.5)
            self.play(FadeIn(empty_label))

            result2 = Text("→ false  (not found)", font="monospace",
                           color=RED, font_size=20)
            result2.next_to(empty_label, DOWN, buff=0.3)
            self.play(FadeIn(result2),
                      FadeOut(lo_marker2), FadeOut(hi_marker2))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- note ----
        with self.voiceover(LINES["bsearch_note"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("binary_search(range, val)", "→ bool", GREEN),
                ("lower_bound(range, val)", "→ iterator (first ≥ val)", TEAL),
                ("upper_bound(range, val)", "→ iterator (first > val)", BLUE),
                ("equal_range(range, val)", "→ subrange (all == val)", GOLD),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=16)
                row_r = Text(desc, font="monospace", color=GREY, font_size=16)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=0.6))
            table.arrange(DOWN, buff=0.4).move_to(ORIGIN)

            note = Text("* range must be sorted — O(log n)",
                        font="monospace", color=ORANGE, font_size=15)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.2))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
