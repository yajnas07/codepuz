from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo8.py RangesNthElement
# manim render -pql ranges-algo8.py RangesWithStrings

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

# ---- narration lines ----
LINES = {
    # Scene 17: ranges::nth_element
    "nth_intro": (
        "Ranges nth element is a partial sort. "
        "It places the correct element at the nth position, "
        "with smaller elements to the left and larger to the right."
    ),
    "nth_run": (
        "We want the 5th smallest element, at index 4. "
        "The algorithm partitions around the target position. "
        "It doesn't fully sort, it only guarantees the nth element is correct."
    ),
    "nth_result": (
        "After nth element, index 4 holds the value 5, "
        "which is exactly what would be there in a fully sorted array. "
        "Everything to the left is less than or equal to 5, "
        "and everything to the right is greater than or equal to 5."
    ),
    "nth_summary": (
        "Nth element runs in O of n on average, much faster than a full sort. "
        "It's ideal for finding medians, k-th smallest values, or top-k problems."
    ),

    # Scene 18: Ranges with strings
    "str_intro": (
        "Range algorithms work with any type, not just integers. "
        "Here we use them with strings to sort names by length."
    ),
    "str_run": (
        "We sort a vector of names using a custom comparator "
        "that compares string lengths instead of lexicographic order. "
        "Shorter names move to the front."
    ),
    "str_note": (
        "The default sort would order names alphabetically. "
        "Custom comparators let you sort by any criteria, "
        "length, last character, or any computed property."
    ),
}

# ---- data ----
NTH_NUMS = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
NAMES = ["Alice", "Bob", "Charlie", "David", "Eve"]


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


def make_str_array(values, cell_color=GREY, text_color=OFFWHITE):
    """Create a row of boxes sized to string content."""
    grp = VGroup()
    for v in values:
        cell = RoundedRectangle(
            width=max(0.8, len(v) * 0.22 + 0.3), height=0.55, corner_radius=0.06,
            stroke_color=cell_color, stroke_width=2,
            fill_color=SURF, fill_opacity=1,
        )
        lbl = Text(v, font="monospace", color=text_color, font_size=16)
        lbl.move_to(cell)
        grp.add(VGroup(cell, lbl))
    grp.arrange(RIGHT, buff=0.12)
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


class RangesNthElement(VoiceoverScene):
    """Scene 17: std::ranges::nth_element demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)

        # ---- title ----
        title = Text("std::ranges::nth_element", font="monospace",
                     color=TEAL, font_size=34)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["nth_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- nth_element animation ----
        code = make_code(
            "std::ranges::nth_element(\n"
            "    for_nth, for_nth.begin() + 4);", 18
        )
        code.to_edge(UP, buff=0.5)

        arr = make_array(NTH_NUMS, cell_size=0.6)
        arr.move_to(UP * 0.1)

        src_label = Text("for_nth", font="monospace", color=GREY, font_size=16)
        src_label.next_to(arr, LEFT, buff=0.3)

        # Index labels
        idx_grp = VGroup()
        for i in range(len(NTH_NUMS)):
            idx = Text(str(i), font="monospace", color=GREY, font_size=11)
            idx.next_to(arr[i], DOWN, buff=0.12)
            idx_grp.add(idx)

        nth_label = Text("nth = index 4  (5th smallest)",
                         font="monospace", color=GOLD, font_size=16)
        nth_label.next_to(idx_grp, DOWN, buff=0.3)

        with self.voiceover(LINES["nth_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))
            self.play(FadeIn(idx_grp), FadeIn(nth_label))

            # Highlight the target position
            nth_marker = Triangle(color=GOLD, fill_opacity=1).scale(0.12)
            nth_marker.next_to(arr[4], UP, buff=0.15)
            self.play(FadeIn(nth_marker), run_time=0.3)

            # Show the sorting happening — simulate the result
            # The sorted array is [1,2,3,4,5,6,7,8,9,10], so index 4 = 5
            # A possible nth_element result: [3,2,4,1,5,9,7,8,6,10]
            nth_result = [3, 2, 4, 1, 5, 9, 7, 8, 6, 10]

            # Animate a "shuffle" effect — flash all elements
            self.play(
                *[arr[i][0].animate.set_stroke(TEAL, width=2.5)
                  for i in range(len(NTH_NUMS))],
                run_time=0.3,
            )

            # Replace all labels with result values
            for i in range(len(NTH_NUMS)):
                new_lbl = Text(str(nth_result[i]), font="monospace",
                               color=OFFWHITE).scale(0.35)
                new_lbl.move_to(arr[i][1].get_center())
                arr[i].remove(arr[i][1])
                arr[i].add(new_lbl)

            self.play(
                *[arr[i][0].animate.set_stroke(GREY, width=2)
                  for i in range(len(NTH_NUMS))],
                run_time=0.3,
            )

            self.wait(max(0.2, tracker.duration - 3.0))

        # ---- show the guarantees ----
        with self.voiceover(LINES["nth_result"]) as tracker:
            # Highlight nth element
            self.play(
                arr[4][0].animate.set_stroke(GOLD, width=4),
                arr[4][1].animate.set_color(GOLD),
                run_time=0.3,
            )

            # Color left partition green, right partition orange
            for i in range(4):
                self.play(
                    arr[i][0].animate.set_stroke(GREEN, width=3),
                    arr[i][1].animate.set_color(GREEN),
                    run_time=0.12,
                )
            for i in range(5, len(nth_result)):
                self.play(
                    arr[i][0].animate.set_stroke(ORANGE, width=3),
                    arr[i][1].animate.set_color(ORANGE),
                    run_time=0.12,
                )

            # Labels for partitions
            left_lbl = Text("all ≤ 5", font="monospace", color=GREEN, font_size=15)
            nth_lbl = Text("= 5", font="monospace", color=GOLD, font_size=15)
            right_lbl = Text("all ≥ 5", font="monospace", color=ORANGE, font_size=15)

            left_lbl.next_to(arr[1], DOWN, buff=0.55)
            nth_lbl.next_to(arr[4], DOWN, buff=0.55)
            right_lbl.next_to(arr[7], DOWN, buff=0.55)

            self.play(FadeIn(left_lbl), FadeIn(nth_lbl), FadeIn(right_lbl))

            # Show what full sort would look like
            sorted_label = Text(
                "fully sorted: {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}",
                font="monospace", color=GREY, font_size=14,
            )
            sorted_label.next_to(nth_label, DOWN, buff=0.8)
            confirm = Text("index 4 → 5  ✓  correct!",
                           font="monospace", color=GOLD, font_size=16)
            confirm.next_to(sorted_label, DOWN, buff=0.2)

            self.play(FadeIn(sorted_label), FadeIn(confirm))
            self.wait(max(0.2, tracker.duration - 3.0))

        # ---- summary ----
        with self.voiceover(LINES["nth_summary"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("nth_element(range, nth)", "O(n) avg — only nth correct", GOLD),
                ("partial_sort(range, mid)", "O(n log k) — first k sorted", TEAL),
                ("sort(range)", "O(n log n) — fully sorted", GREEN),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=17)
                row_r = Text(desc, font="monospace", color=GREY, font_size=17)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=0.8))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            note = Text("ideal for medians & top-k problems ⚡",
                        font="monospace", color=ORANGE, font_size=15)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.25))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesWithStrings(VoiceoverScene):
    """Scene 18: Ranges with strings demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)

        # ---- title ----
        title = Text("Ranges with Strings", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["str_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- sort strings by length ----
        code = make_code(
            "std::ranges::sort(names,\n"
            "    [](const auto& a, const auto& b) {\n"
            "        return a.length() < b.length();\n"
            "    });", 17
        )
        code.to_edge(UP, buff=0.4)

        src_label = Text("names", font="monospace", color=GREY, font_size=16)
        arr = make_str_array(NAMES)
        arr.move_to(UP * 0.0)
        src_label.next_to(arr, LEFT, buff=0.3)

        # Length labels below each name
        len_grp = VGroup()
        for i, name in enumerate(NAMES):
            ll = Text(f"len={len(name)}", font="monospace",
                      color=GREY, font_size=11)
            ll.next_to(arr[i], DOWN, buff=0.12)
            len_grp.add(ll)

        with self.voiceover(LINES["str_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.06))
            self.play(FadeIn(len_grp))

            # Show comparisons — highlight by length
            # Sorted by length: Bob(3), Eve(3), Alice(5), David(5), Charlie(7)
            sorted_names = sorted(NAMES, key=len)

            # Animate the sort as a shuffle
            self.play(
                *[arr[i][0].animate.set_stroke(TEAL, width=2.5)
                  for i in range(len(NAMES))],
                run_time=0.4,
            )

            # Build sorted array
            sorted_arr = make_str_array(sorted_names)
            sorted_arr.move_to(DOWN * 1.5)

            sorted_label = Text("sorted by length:", font="monospace",
                                color=GREEN, font_size=16)
            sorted_label.next_to(sorted_arr, LEFT, buff=0.3)

            # Length labels for sorted
            sorted_len_grp = VGroup()
            for i, name in enumerate(sorted_names):
                ll = Text(f"len={len(name)}", font="monospace",
                          color=GREEN, font_size=11)
                ll.next_to(sorted_arr[i], DOWN, buff=0.12)
                sorted_len_grp.add(ll)

            # Animate each name flying to its sorted position
            for i, name in enumerate(sorted_names):
                orig_idx = NAMES.index(name)
                # Mark used to avoid duplicate "Bob"/"Eve" issue
                if i > 0 and name == sorted_names[i - 1]:
                    # Find the second occurrence
                    for j in range(len(NAMES)):
                        if NAMES[j] == name and j != NAMES.index(sorted_names[i - 1]):
                            orig_idx = j
                            break

                self.play(
                    arr[orig_idx][0].animate.set_stroke(GREEN, width=3),
                    run_time=0.15,
                )

            self.play(
                FadeIn(sorted_label),
                LaggedStart(*[FadeIn(m, shift=UP * 0.15)
                              for m in sorted_arr], lag_ratio=0.08),
                FadeIn(sorted_len_grp),
            )

            # Reset source
            self.play(
                *[arr[i][0].animate.set_stroke(GREY, width=2)
                  for i in range(len(NAMES))],
                run_time=0.2,
            )

            self.wait(max(0.2, tracker.duration - 4.0))

        # ---- note ----
        with self.voiceover(LINES["str_note"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            rows = [
                ("sort(names)", "alphabetical (default)", GREY),
                ("sort(names, by_length)", "by string length", GREEN),
                ("sort(names, by_last_char)", "by any custom criteria", TEAL),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=18)
                row_r = Text(desc, font="monospace", color=GREY, font_size=18)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=0.8))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            note = Text("all range algorithms work with any type ✓",
                        font="monospace", color=ORANGE, font_size=15)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.25))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
