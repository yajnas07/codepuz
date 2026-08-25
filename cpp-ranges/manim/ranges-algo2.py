from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo2.py RangesCopyIf
# manim render -pql ranges-algo2.py RangesBoolPredicates

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
    # Scene 5: ranges::copy_if
    "copy_intro": (
        "Ranges copy if copies elements that satisfy a condition into a new container. "
        "Unlike transform, it only copies, it does not modify the values."
    ),
    "copy_run": (
        "We copy only even numbers. The predicate checks divisibility by 2. "
        "Matching elements are appended to the output via back inserter."
    ),
    "copy_note": (
        "Back inserter lets the destination grow dynamically. "
        "You don't need to pre-size the output vector."
    ),

    # Scene 6: ranges::all_of / any_of / none_of
    "bool_intro": (
        "All of, any of, and none of are boolean predicates. "
        "They test a condition across the entire range and return true or false."
    ),
    "all_of_run": (
        "All of returns true only if every element satisfies the condition. "
        "Here we check: are all numbers positive?"
    ),
    "any_of_run": (
        "Any of returns true if at least one element matches. "
        "We check: is any number greater than 5?"
    ),
    "none_of_run": (
        "None of returns true if zero elements match. "
        "We check: are there no negative numbers?"
    ),
    "bool_summary": (
        "All three short circuit for efficiency. "
        "They stop scanning as soon as the result is determined."
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


class RangesCopyIf(VoiceoverScene):
    """Scene 5: std::ranges::copy_if demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Copy matching elements")

        # ---- title ----
        title = Text("std::ranges::copy_if", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["copy_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- copy_if animation ----
        code = make_code(
            "std::ranges::copy_if(numbers,\n"
            "    std::back_inserter(evens),\n"
            "    [](int x) { return x % 2 == 0; });", 18
        )
        code.to_edge(UP, buff=0.5)

        # source array
        src_label = Text("numbers", font="monospace", color=GREY, font_size=16)
        arr_src = make_array(NUMS)
        arr_src.move_to(UP * 0.2)
        src_label.next_to(arr_src, LEFT, buff=0.3)

        # destination (starts empty)
        dst_label = Text("evens", font="monospace", color=GREY, font_size=16)
        dst_label.move_to(LEFT * 4.5 + DOWN * 1.8)

        cond_label = Text("condition: x % 2 == 0", font="monospace",
                          color=GOLD, font_size=16)
        cond_label.next_to(arr_src, RIGHT, buff=0.5)

        with self.voiceover(LINES["copy_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr_src], lag_ratio=0.05))
            self.play(FadeIn(dst_label), FadeIn(cond_label))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr_src[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            copied = VGroup()
            copy_slot = 0
            evens_collected = []

            for i in range(len(NUMS)):
                self.play(scanner.animate.next_to(arr_src[i], UP, buff=0.15),
                          run_time=0.2)

                if NUMS[i] % 2 == 0:
                    # highlight as match
                    self.play(
                        arr_src[i][0].animate.set_stroke(GREEN, width=3),
                        arr_src[i][1].animate.set_color(GREEN),
                        run_time=0.2,
                    )
                    # create a copy that flies down
                    copy_cell = make_array([NUMS[i]], cell_color=GREEN, text_color=GREEN)
                    copy_cell.move_to(arr_src[i].get_center())

                    target_x = dst_label.get_right()[0] + 0.5 + copy_slot * 0.7
                    target_pos = [target_x, DOWN[1] * 1.8, 0]

                    self.play(
                        copy_cell.animate.move_to(target_pos),
                        run_time=0.4,
                        rate_func=smooth,
                    )
                    copied.add(copy_cell)
                    evens_collected.append(NUMS[i])
                    copy_slot += 1

                    # reset source highlight
                    self.play(
                        arr_src[i][0].animate.set_stroke(GREY, width=2),
                        arr_src[i][1].animate.set_color(OFFWHITE),
                        run_time=0.1,
                    )
                else:
                    # dim non-match
                    self.play(arr_src[i].animate.set_opacity(0.4), run_time=0.12)

            self.play(FadeOut(scanner))
            result = Text(
                f"evens = {{{', '.join(str(x) for x in evens_collected)}}}",
                font="monospace", color=GREEN, font_size=18,
            )
            result.next_to(copied, DOWN, buff=0.4)
            self.play(FadeIn(result))
            self.wait(max(0.2, tracker.duration - 6.0))

        # ---- back_inserter note ----
        with self.voiceover(LINES["copy_note"]) as tracker:
            note = Text("back_inserter → no pre-sizing needed",
                        font="monospace", color=ORANGE, font_size=18)
            note.next_to(result, DOWN, buff=0.4)
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 1.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesBoolPredicates(VoiceoverScene):
    """Scene 6: std::ranges::all_of / any_of / none_of demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Boolean predicates")

        # ---- title ----
        title = Text("all_of / any_of / none_of", font="monospace",
                     color=TEAL, font_size=34)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["bool_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- helper to run one predicate animation ----
        def animate_predicate(code_text, condition_text, pred_fn, narration_key,
                              short_circuit_on_fail=False, short_circuit_on_pass=False):
            """Animate scanning with a predicate, showing pass/fail per element."""
            code = make_code(code_text, 17)
            code.to_edge(UP, buff=0.5)

            arr = make_array(NUMS, cell_size=0.55)
            arr.move_to(ORIGIN + UP * 0.1)

            cond = Text(condition_text, font="monospace", color=GOLD, font_size=16)
            cond.next_to(arr, DOWN, buff=0.5)

            result_holder = [None]

            with self.voiceover(LINES[narration_key]) as tracker:
                self.play(FadeIn(code))
                self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                        for m in arr], lag_ratio=0.04))
                self.play(FadeIn(cond))

                scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.1)
                scanner.next_to(arr[0], UP, buff=0.12)
                self.play(FadeIn(scanner), run_time=0.15)

                final_result = True
                stopped_early = False

                for i in range(len(NUMS)):
                    self.play(scanner.animate.next_to(arr[i], UP, buff=0.12),
                              run_time=0.18)

                    passes = pred_fn(NUMS[i])
                    mark = Text(
                        "✓" if passes else "✗",
                        font="monospace",
                        color=GREEN if passes else RED,
                        font_size=16,
                    )
                    mark.next_to(arr[i], UP, buff=0.4)

                    if passes:
                        self.play(
                            FadeIn(mark),
                            arr[i][0].animate.set_stroke(GREEN, width=2.5),
                            run_time=0.18,
                        )
                    else:
                        self.play(
                            FadeIn(mark),
                            arr[i][0].animate.set_stroke(RED, width=2.5),
                            run_time=0.18,
                        )

                    # short-circuit logic
                    if short_circuit_on_fail and not passes:
                        final_result = False
                        sc_text = Text("short-circuit → false", font="monospace",
                                       color=RED, font_size=16)
                        sc_text.next_to(cond, DOWN, buff=0.3)
                        self.play(FadeIn(sc_text))
                        stopped_early = True
                        break
                    if short_circuit_on_pass and passes:
                        final_result = True
                        sc_text = Text("short-circuit → true", font="monospace",
                                       color=GREEN, font_size=16)
                        sc_text.next_to(cond, DOWN, buff=0.3)
                        self.play(FadeIn(sc_text))
                        stopped_early = True
                        break

                if not stopped_early:
                    res_color = GREEN if final_result else RED
                    res_text = Text(
                        f"→ {'true' if final_result else 'false'}",
                        font="monospace", color=res_color, font_size=20,
                    )
                    res_text.next_to(cond, DOWN, buff=0.3)
                    self.play(FadeIn(res_text))

                self.play(FadeOut(scanner))
                self.wait(max(0.2, tracker.duration - 4.5))

            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
            self.wait(0.3)

        # ---- all_of: all positive? ----
        animate_predicate(
            "std::ranges::all_of(numbers,\n"
            "    [](int x) { return x > 0; });",
            "condition: x > 0",
            lambda x: x > 0,
            "all_of_run",
            short_circuit_on_fail=True,
        )

        # ---- any_of: any > 5? ----
        animate_predicate(
            "std::ranges::any_of(numbers,\n"
            "    [](int x) { return x > 5; });",
            "condition: x > 5",
            lambda x: x > 5,
            "any_of_run",
            short_circuit_on_pass=True,
        )

        # ---- none_of: none negative? ----
        animate_predicate(
            "std::ranges::none_of(numbers,\n"
            "    [](int x) { return x < 0; });",
            "condition: x < 0",
            lambda x: x < 0,
            "none_of_run",
            short_circuit_on_pass=True,
        )

        # ---- summary ----
        with self.voiceover(LINES["bool_summary"]) as tracker:
            rows = [
                ("all_of(range, pred)", "true if ALL match", GREEN),
                ("any_of(range, pred)", "true if ANY matches", TEAL),
                ("none_of(range, pred)", "true if NONE match", GOLD),
            ]
            table = VGroup()
            for name, desc, clr in rows:
                row_l = Text(name, font="monospace", color=clr, font_size=18)
                row_r = Text(desc, font="monospace", color=GREY, font_size=18)
                table.add(VGroup(row_l, row_r).arrange(RIGHT, buff=1.2))
            table.arrange(DOWN, buff=0.5).move_to(ORIGIN)

            note = Text("all three short-circuit ⚡", font="monospace",
                        color=ORANGE, font_size=16)
            note.next_to(table, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.25))
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
