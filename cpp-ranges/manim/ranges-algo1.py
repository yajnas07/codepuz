from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService


# manim render -pql ranges-algo1.py RangesSort
# manim render -pql ranges-algo1.py RangesFind
# manim render -pql ranges-algo1.py RangesCount
# manim render -pql ranges-algo1.py RangesTransform

# ---- colour palette (matching sample.py) ----
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
    lbl.to_corner(DL, buff=0.25)
    scene.add(lbl)
    return lbl

# ---- narration lines ----
LINES = {
    # Scene 1: ranges::sort
    "sort_intro": (
        "In C++ 20, ranges sort lets you sort an entire container "
        "without spelling out begin and end iterators. "
        "Just pass the vector directly."
    ),
    "sort_asc": (
        "Calling ranges sort with no comparator sorts in ascending order. "
        "Watch the elements rearrange themselves from smallest to largest."
    ),
    "sort_desc": (
        "To sort in descending order, pass std greater as the comparator. "
        "This is equivalent to a lambda that returns a greater than b."
    ),
    "sort_compare": (
        "Compare the old way, std sort with begin and end, "
        "versus the ranges way, which is cleaner and less error prone."
    ),

    # Scene 2: ranges::find / find_if
    "find_intro": (
        "Ranges find searches for an exact value in a container. "
        "It returns an iterator to the first match, or end if not found."
    ),
    "find_scan": (
        "Let's search for the value 7. The algorithm scans left to right, "
        "checking each element until it finds a match."
    ),
    "find_if_intro": (
        "Find if takes a predicate instead of a value. "
        "Here we look for the first element greater than 8."
    ),
    "find_if_scan": (
        "The scanner checks each element against the condition. "
        "It skips elements that don't match, and stops at 9, the first value greater than 8."
    ),

        # Scene 3: ranges::count / count_if
    "count_intro": (
        "Ranges count if counts how many elements satisfy a condition. "
        "Unlike find, it does not stop early. It scans the entire range and returns a number."
    ),
    "count_even": (
        "Let's count even numbers. The predicate checks if each value is divisible by 2. "
        "Watch as we tally the matches."
    ),
    "count_prime": (
        "Now let's count prime numbers using a more complex predicate. "
        "The lambda uses a nested is prime helper to test each element."
    ),
    "count_summary": (
        "Count returns an integer, not an iterator. "
        "Use count for exact values, and count if for conditions."
    ),

    # Scene 4: ranges::transform
    "transform_intro": (
        "Ranges transform applies a function to every element and writes the results "
        "into an output range. It maps input values to new values, one by one."
    ),
    "transform_run": (
        "Here we square each number. The lambda takes x and returns x times x. "
        "Each input element produces exactly one output element."
    ),
    "transform_note": (
        "Important: the output vector must be pre-sized. Transform writes into existing "
        "slots. It does not append or resize the destination."
    ),


}

# ---- data ----
NUMS = [5, 2, 8, 1, 9, 3, 7, 4, 6, 10]
SORTED_ASC = sorted(NUMS)
SORTED_DESC = sorted(NUMS, reverse=True)


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
    """Create a styled code block using Text (avoids Code file requirement)."""
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


class RangesSort(VoiceoverScene):
    """Scene 1: std::ranges::sort demonstration."""

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
        _scene_label(self, "Sort a container")

        # ---- title ----
        title = Text("std::ranges::sort", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["sort_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- show the code ----
        code_asc = make_code("std::ranges::sort(sorted_nums);")
        code_asc.to_edge(UP, buff=0.6)

        # ---- ascending sort animation ----
        arr_label = Text("sorted_nums", font="monospace",
                         color=GREY, font_size=18)
        arr_unsorted = make_array(NUMS)
        arr_unsorted.move_to(ORIGIN + UP * 0.3)
        arr_label.next_to(arr_unsorted, LEFT, buff=0.4)

        with self.voiceover(LINES["sort_asc"]) as tracker:
            self.play(FadeIn(code_asc), FadeIn(arr_label))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15)
                                    for m in arr_unsorted], lag_ratio=0.05))
            self.wait(0.5)

            # animate the sort: fade out unsorted, fade in sorted
            arr_sorted = make_array(SORTED_ASC, cell_color=GREEN)
            arr_sorted.move_to(arr_unsorted.get_center())

            # highlight each element moving to its sorted position
            self.play(
                *[arr_unsorted[i].animate.set_opacity(0.3) for i in range(len(NUMS))],
                run_time=0.4,
            )
            self.play(
                FadeOut(arr_unsorted),
                FadeIn(arr_sorted, shift=DOWN * 0.1),
                run_time=0.8,
            )
            result_lbl = Text("→ ascending", font="monospace",
                              color=GREEN, font_size=16)
            result_lbl.next_to(arr_sorted, RIGHT, buff=0.4)
            self.play(FadeIn(result_lbl))
            self.wait(max(0.2, tracker.duration - 3.5))

        # ---- descending sort ----
        code_desc = make_code("std::ranges::sort(sorted_nums, std::greater{});")
        code_desc.to_edge(UP, buff=0.6)

        with self.voiceover(LINES["sort_desc"]) as tracker:
            self.play(FadeOut(code_asc), FadeIn(code_desc))
            self.wait(0.3)

            arr_desc = make_array(SORTED_DESC, cell_color=ORANGE)
            arr_desc.move_to(arr_sorted.get_center() + DOWN * 1.2)
            desc_label = Text("sorted_nums", font="monospace",
                              color=GREY, font_size=18)
            desc_label.next_to(arr_desc, LEFT, buff=0.4)
            desc_result = Text("→ descending", font="monospace",
                               color=ORANGE, font_size=16)
            desc_result.next_to(arr_desc, RIGHT, buff=0.4)

            self.play(FadeIn(desc_label))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr_desc], lag_ratio=0.05))
            self.play(FadeIn(desc_result))
            self.wait(max(0.2, tracker.duration - 2.5))

        # ---- old vs new comparison ----
        with self.voiceover(LINES["sort_compare"]) as tracker:
            self.play(*[FadeOut(m) for m in [code_desc, arr_sorted, arr_label,
                                             result_lbl, arr_desc, desc_label,
                                             desc_result]])
            old_code = make_code("// old way\nstd::sort(vec.begin(), vec.end());", 18)
            new_code = make_code("// ranges way\nstd::ranges::sort(vec);", 18)
            old_code.move_to(LEFT * 3 + UP * 0.3)
            new_code.move_to(RIGHT * 3 + UP * 0.3)

            vs_text = Text("vs", font="monospace", color=GREY, font_size=24)
            vs_text.move_to(ORIGIN + RIGHT * 0.45 + UP * 0.3)

            cross = Cross(stroke_color=RED, stroke_width=4).scale(0.3)
            cross.next_to(old_code, DOWN, buff=0.3)
            old_lbl = Text("error-prone", font="monospace",
                           color=RED, font_size=14)
            old_lbl.next_to(cross, DOWN, buff=0.15)

            check = Text("✓", font="monospace", color=GREEN, font_size=36)
            check.next_to(new_code, DOWN, buff=0.3)
            new_lbl = Text("cleaner & safer", font="monospace",
                           color=GREEN, font_size=14)
            new_lbl.next_to(check, DOWN, buff=0.15)

            self.play(FadeIn(old_code, shift=RIGHT * 0.3),
                      FadeIn(new_code, shift=LEFT * 0.3),
                      FadeIn(vs_text))
            self.play(FadeIn(cross), FadeIn(old_lbl),
                      FadeIn(check), FadeIn(new_lbl))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesFind(VoiceoverScene):
    """Scene 2: std::ranges::find / find_if demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = Text("© CodePuz", font="Arial", font_size=18,
                         color="#ffffff", weight=NORMAL)
        watermark.set_opacity(0.35).to_corner(DR, buff=0.25)
        self.add(watermark)
        _scene_label(self, "Find an element")

        # ---- title ----
        title = Text("std::ranges::find / find_if", font="monospace",
                     color=TEAL, font_size=34)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["find_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- ranges::find(numbers, 7) ----
        code_find = make_code("auto it = std::ranges::find(numbers, 7);")
        code_find.to_edge(UP, buff=0.6)

        arr = make_array(NUMS)
        arr.move_to(ORIGIN + UP * 0.2)
        idx_labels = VGroup()
        for i, mob in enumerate(arr):
            idx = Text(str(i), font="monospace", color=GREY, font_size=12)
            idx.next_to(mob, DOWN, buff=0.15)
            idx_labels.add(idx)

        with self.voiceover(LINES["find_scan"]) as tracker:
            self.play(FadeIn(code_find))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(m) for m in idx_labels], lag_ratio=0.05))

            # scanning animation
            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            target_idx = NUMS.index(7)
            for i in range(len(NUMS)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.25)
                if NUMS[i] == 7:
                    # found it!
                    self.play(
                        arr[i][0].animate.set_stroke(GREEN, width=3),
                        arr[i][1].animate.set_color(GREEN),
                        run_time=0.3,
                    )
                    found_text = Text(f"Found 7 at position {target_idx}",
                                      font="monospace", color=GREEN, font_size=18)
                    found_text.next_to(arr, DOWN, buff=0.6)
                    self.play(FadeIn(found_text))
                    break
                else:
                    # dim non-matches
                    self.play(arr[i].animate.set_opacity(0.4), run_time=0.15)

            self.wait(max(0.2, tracker.duration - 4.0))

        # ---- transition to find_if ----
        self.play(FadeOut(scanner), FadeOut(found_text), FadeOut(code_find),
                  FadeOut(arr), FadeOut(idx_labels))

        # ---- ranges::find_if ----
        code_find_if = make_code(
            "auto it = std::ranges::find_if(numbers,\n"
            "    [](int x) { return x > 8; });"
        )
        code_find_if.to_edge(UP, buff=0.6)

        arr2 = make_array(NUMS)
        arr2.move_to(ORIGIN + UP * 0.2)
        idx_labels2 = VGroup()
        for i, mob in enumerate(arr2):
            idx = Text(str(i), font="monospace", color=GREY, font_size=12)
            idx.next_to(mob, DOWN, buff=0.15)
            idx_labels2.add(idx)

        # condition label
        cond_label = Text("condition: x > 8", font="monospace",
                          color=GOLD, font_size=16)
        cond_label.next_to(arr2, DOWN, buff=0.7)

        with self.voiceover(LINES["find_if_intro"]) as tracker:
            self.play(FadeIn(code_find_if))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr2], lag_ratio=0.05),
                      LaggedStart(*[FadeIn(m) for m in idx_labels2], lag_ratio=0.05))
            self.play(FadeIn(cond_label))
            self.wait(max(0.2, tracker.duration - 2.0))

        with self.voiceover(LINES["find_if_scan"]) as tracker:
            scanner2 = Triangle(color=GOLD, fill_opacity=1).scale(0.12)
            scanner2.next_to(arr2[0], UP, buff=0.15)
            self.play(FadeIn(scanner2), run_time=0.2)

            for i in range(len(NUMS)):
                self.play(scanner2.animate.next_to(arr2[i], UP, buff=0.15),
                          run_time=0.25)

                # show check result
                check_text = Text(
                    f"{NUMS[i]} > 8 ? {'✓' if NUMS[i] > 8 else '✗'}",
                    font="monospace",
                    color=GREEN if NUMS[i] > 8 else RED,
                    font_size=14,
                )
                check_text.next_to(arr2[i], UP, buff=0.45)

                if NUMS[i] > 8:
                    self.play(FadeIn(check_text), run_time=0.2)
                    self.play(
                        arr2[i][0].animate.set_stroke(GREEN, width=3),
                        arr2[i][1].animate.set_color(GREEN),
                        run_time=0.3,
                    )
                    found_text2 = Text(f"First element > 8: {NUMS[i]}",
                                       font="monospace", color=GREEN, font_size=18)
                    found_text2.next_to(cond_label, DOWN, buff=0.3)
                    self.play(FadeIn(found_text2))
                    break
                else:
                    self.play(FadeIn(check_text), run_time=0.15)
                    self.play(arr2[i].animate.set_opacity(0.4),
                              FadeOut(check_text), run_time=0.2)

            self.wait(max(0.2, tracker.duration - 4.0))

        # ---- summary table ----
        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

        table_title = Text("find vs find_if", font="monospace",
                           color=TEAL, font_size=28)
        table_title.to_edge(UP, buff=0.8)

        row1_l = Text("find(range, value)", font="monospace",
                       color=OFFWHITE, font_size=18)
        row1_r = Text("search by exact value", font="monospace",
                       color=GREY, font_size=18)
        row2_l = Text("find_if(range, pred)", font="monospace",
                       color=OFFWHITE, font_size=18)
        row2_r = Text("search by condition", font="monospace",
                       color=GREY, font_size=18)

        table = VGroup(
            VGroup(row1_l, row1_r).arrange(RIGHT, buff=1.5),
            VGroup(row2_l, row2_r).arrange(RIGHT, buff=1.5),
        ).arrange(DOWN, buff=0.5).move_to(ORIGIN)

        divider = Line(
            table[0].get_left() + LEFT * 0.3,
            table[0].get_right() + RIGHT * 0.3,
            stroke_color=GREY, stroke_width=1,
        ).move_to((table[0].get_bottom() + table[1].get_top()) / 2)

        self.play(FadeIn(table_title))
        self.play(FadeIn(table[0]), Create(divider))
        self.play(FadeIn(table[1]))
        self.wait(2)

        # self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        #clear screen
        self.clear()
        self.wait(1.0)
def is_prime(n):
    """Check if n is prime."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
    
class RangesCount(VoiceoverScene):
    """Scene 3: std::ranges::count_if demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = Text("© CodePuz", font="Arial", font_size=18,
                         color="#ffffff", weight=NORMAL)
        watermark.set_opacity(0.35).to_corner(DR, buff=0.25)
        self.add(watermark)
        _scene_label(self, "Count matching elements")

        # ---- title ----
        title = Text("std::ranges::count_if", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["count_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- count even numbers ----
        code_even = make_code(
            "auto n = std::ranges::count_if(numbers,\n"
            "    [](int x) { return x % 2 == 0; });", 18
        )
        code_even.to_edge(UP, buff=0.5)

        arr = make_array(NUMS)
        arr.move_to(ORIGIN + UP * 0.3)

        tally_label = Text("count: 0", font="monospace",
                           color=GOLD, font_size=22)
        tally_label.next_to(arr, DOWN, buff=0.8)

        with self.voiceover(LINES["count_even"]) as tracker:
            self.play(FadeIn(code_even))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))
            self.play(FadeIn(tally_label))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            count = 0
            for i in range(len(NUMS)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.2)
                if NUMS[i] % 2 == 0:
                    count += 1
                    self.play(
                        arr[i][0].animate.set_stroke(GREEN, width=3),
                        arr[i][1].animate.set_color(GREEN),
                        run_time=0.2,
                    )
                    new_tally = Text(f"count: {count}", font="monospace",
                                     color=GOLD, font_size=22)
                    new_tally.move_to(tally_label)
                    self.play(FadeOut(tally_label), FadeIn(new_tally), run_time=0.2)
                    tally_label = new_tally
                else:
                    self.play(arr[i].animate.set_opacity(0.4), run_time=0.12)

            result = Text(f"Even numbers found: {count}", font="monospace",
                          color=GREEN, font_size=18)
            result.next_to(tally_label, DOWN, buff=0.4)
            self.play(FadeOut(scanner), FadeIn(result))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- count prime numbers ----
        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

        code_prime = make_code(
            "auto n = std::ranges::count_if(numbers,\n"
            "    [](int x) { return is_prime(x); });", 18
        )
        code_prime.to_edge(UP, buff=0.5)

        arr2 = make_array(NUMS)
        arr2.move_to(ORIGIN + UP * 0.3)

        tally2 = Text("count: 0", font="monospace", color=GOLD, font_size=22)
        tally2.next_to(arr2, DOWN, buff=0.8)

        with self.voiceover(LINES["count_prime"]) as tracker:
            self.play(FadeIn(code_prime))
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr2], lag_ratio=0.05))
            self.play(FadeIn(tally2))

            scanner2 = Triangle(color=GOLD, fill_opacity=1).scale(0.12)
            scanner2.next_to(arr2[0], UP, buff=0.15)
            self.play(FadeIn(scanner2), run_time=0.2)

            pcount = 0
            for i in range(len(NUMS)):
                self.play(scanner2.animate.next_to(arr2[i], UP, buff=0.15),
                          run_time=0.2)

                prime_check = Text(
                    f"{NUMS[i]} {'prime ✓' if is_prime(NUMS[i]) else 'not prime ✗'}",
                    font="monospace",
                    color=GREEN if is_prime(NUMS[i]) else RED,
                    font_size=13,
                )
                prime_check.next_to(arr2[i], UP, buff=0.45)

                if is_prime(NUMS[i]):
                    pcount += 1
                    self.play(FadeIn(prime_check), run_time=0.15)
                    self.play(
                        arr2[i][0].animate.set_stroke(GREEN, width=3),
                        arr2[i][1].animate.set_color(GREEN),
                        run_time=0.2,
                    )
                    new_tally2 = Text(f"count: {pcount}", font="monospace",
                                      color=GOLD, font_size=22)
                    new_tally2.move_to(tally2)
                    self.play(FadeOut(tally2), FadeIn(new_tally2),
                              FadeOut(prime_check), run_time=0.2)
                    tally2 = new_tally2
                else:
                    self.play(FadeIn(prime_check), run_time=0.12)
                    self.play(arr2[i].animate.set_opacity(0.4),
                              FadeOut(prime_check), run_time=0.15)

            prime_result = Text(f"Prime numbers found: {pcount}",
                                font="monospace", color=GREEN, font_size=18)
            prime_result.next_to(tally2, DOWN, buff=0.4)
            self.play(FadeOut(scanner2), FadeIn(prime_result))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- summary ----
        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

        with self.voiceover(LINES["count_summary"]) as tracker:
            row1_l = Text("count(range, value)", font="monospace",
                           color=OFFWHITE, font_size=18)
            row1_r = Text("how many equal value?", font="monospace",
                           color=GREY, font_size=18)
            row2_l = Text("count_if(range, pred)", font="monospace",
                           color=OFFWHITE, font_size=18)
            row2_r = Text("how many match condition?", font="monospace",
                           color=GREY, font_size=18)
            row3_l = Text("returns:", font="monospace",
                           color=OFFWHITE, font_size=18)
            row3_r = Text("integer (not iterator)", font="monospace",
                           color=GOLD, font_size=18)

            table = VGroup(
                VGroup(row1_l, row1_r).arrange(RIGHT, buff=1.2),
                VGroup(row2_l, row2_r).arrange(RIGHT, buff=1.2),
                VGroup(row3_l, row3_r).arrange(RIGHT, buff=1.2),
            ).arrange(DOWN, buff=0.45).move_to(ORIGIN)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.3))
            self.wait(max(0.2, tracker.duration - 1.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesTransform(VoiceoverScene):
    """Scene 4: std::ranges::transform demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = Text("© CodePuz", font="Arial", font_size=18,
                         color="#ffffff", weight=NORMAL)
        watermark.set_opacity(0.35).to_corner(DR, buff=0.25)
        self.add(watermark)
        _scene_label(self, "Transform elements")

        # ---- title ----
        title = Text("std::ranges::transform", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["transform_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- transform: square each element ----
        code = make_code(
            "std::ranges::transform(numbers,\n"
            "    squared.begin(),\n"
            "    [](int x) { return x * x; });", 18
        )
        code.to_edge(UP, buff=0.5)

        # input array
        input_label = Text("numbers", font="monospace", color=GREY, font_size=16)
        arr_in = make_array(NUMS)
        arr_in.move_to(LEFT * 0.5 + UP * 0.2)
        input_label.next_to(arr_in, LEFT, buff=0.3)

        # output array (empty initially with "?" placeholders)
        output_label = Text("squared", font="monospace", color=GREY, font_size=16)
        squared_vals = [v * v for v in NUMS]
        arr_out_vals = ["?"] * len(NUMS)
        arr_out = make_array(arr_out_vals, cell_color=GREY, text_color=GREY)
        arr_out.move_to(LEFT * 0.5 + DOWN * 1.5)
        output_label.next_to(arr_out, LEFT, buff=0.3)

        # lambda label
        fn_label = Text("x → x²", font="monospace", color=GOLD, font_size=20)
        fn_label.move_to(ORIGIN + DOWN * 0.6)

        with self.voiceover(LINES["transform_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(input_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr_in], lag_ratio=0.05))
            self.play(FadeIn(output_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr_out], lag_ratio=0.05))
            self.play(FadeIn(fn_label))
            self.wait(0.3)

            for i in range(len(NUMS)):
                # highlight input element
                self.play(
                    arr_in[i][0].animate.set_stroke(TEAL, width=3),
                    arr_in[i][1].animate.set_color(TEAL),
                    run_time=0.2,
                )

                # draw arrow from input to output
                arrow = Arrow(
                    arr_in[i].get_bottom() + DOWN * 0.05,
                    arr_out[i].get_top() + UP * 0.05,
                    color=GOLD, stroke_width=2, buff=0.1,
                    max_tip_length_to_length_ratio=0.3,
                )
                self.play(Create(arrow), run_time=0.2)

                # fill in the output cell
                new_val = Text(str(squared_vals[i]), font="monospace",
                               color=GREEN).scale(0.35)
                new_val.move_to(arr_out[i][1])
                self.play(
                    FadeOut(arr_out[i][1]),
                    FadeIn(new_val),
                    arr_out[i][0].animate.set_stroke(GREEN, width=2),
                    run_time=0.25,
                )
                # replace the label mob in the group
                arr_out[i].remove(arr_out[i][1])
                arr_out[i].add(new_val)

                # reset input highlight & remove arrow
                self.play(
                    arr_in[i][0].animate.set_stroke(GREY, width=2),
                    arr_in[i][1].animate.set_color(OFFWHITE),
                    FadeOut(arrow),
                    run_time=0.15,
                )

            self.wait(max(0.2, tracker.duration - 6.0))

        # ---- important note ----
        with self.voiceover(LINES["transform_note"]) as tracker:
            note = Text("* output must be pre-sized", font="monospace",
                        color=ORANGE, font_size=18)
            note.next_to(arr_out, DOWN, buff=0.2)

            old_code = make_code(
                "// old way\n"
                "std::transform(in.begin(),\n"
                "  in.end(), out.begin(), fn);", 16
            )
            new_code = make_code(
                "// ranges way\n"
                "std::ranges::transform(\n"
                "  in, out.begin(), fn);", 16
            )
            old_code.move_to(LEFT * 3 + DOWN * 3)
            new_code.move_to(RIGHT * 3 + DOWN * 3)

            self.play(FadeIn(note))
            self.play(FadeIn(old_code, shift=RIGHT * 0.2),
                      FadeIn(new_code, shift=LEFT * 0.2))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
