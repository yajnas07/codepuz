from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo4.py RangesUnique
# manim render -pql ranges-algo4.py RangesRemoveIf

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
    # Scene 9: ranges::unique
    "unique_intro": (
        "Ranges unique removes consecutive duplicate elements from a range. "
        "It shifts unique elements to the front and returns a subrange of leftover garbage."
    ),
    "unique_run": (
        "The algorithm compares each element with the previous one. "
        "When a duplicate is found, it is marked for removal. "
        "Only adjacent duplicates are removed, so the data should be sorted first if needed."
    ),
    "unique_erase": (
        "Unique does not resize the container. "
        "You must call erase on the returned subrange to actually shrink the vector. "
        "This is the ranges version of the classic erase-remove idiom."
    ),

    # Scene 10: ranges::remove_if
    "remove_intro": (
        "Ranges remove if moves elements that do not match a predicate to the front. "
        "Matching elements are left as garbage at the end."
    ),
    "remove_run": (
        "We remove all odd numbers using the predicate x mod 2 not equal to 0. "
        "Elements that don't match, the even numbers, are shifted forward."
    ),
    "remove_erase": (
        "Just like unique, remove if does not shrink the container. "
        "You call erase on the returned subrange to finish the job. "
        "This two-step pattern exists because algorithms work with iterators, not containers."
    ),
}

# ---- data ----
UNIQUE_NUMS = [1, 1, 2, 2, 2, 3, 3, 4, 5, 5]
REMOVE_NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


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


class RangesUnique(VoiceoverScene):
    """Scene 9: std::ranges::unique demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)

        # ---- title ----
        title = Text("std::ranges::unique", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["unique_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- unique animation ----
        code = make_code(
            "auto [first, last] =\n"
            "    std::ranges::unique(with_dups);\n"
            "with_dups.erase(first, last);", 17
        )
        code.to_edge(UP, buff=0.5)

        src_label = Text("with_dups", font="monospace", color=GREY, font_size=16)
        arr = make_array(UNIQUE_NUMS, cell_size=0.55)
        arr.move_to(UP * 0.1)
        src_label.next_to(arr, LEFT, buff=0.3)

        with self.voiceover(LINES["unique_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            # First element is always kept
            self.play(
                arr[0][0].animate.set_stroke(GREEN, width=3),
                run_time=0.2,
            )

            kept_indices = [0]
            dup_indices = []

            for i in range(1, len(UNIQUE_NUMS)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.2)

                if UNIQUE_NUMS[i] == UNIQUE_NUMS[i - 1]:
                    # Duplicate — mark red
                    mark = Text("dup", font="monospace", color=RED, font_size=12)
                    mark.next_to(arr[i], DOWN, buff=0.15)
                    self.play(
                        arr[i][0].animate.set_stroke(RED, width=2.5),
                        arr[i][1].animate.set_color(RED),
                        FadeIn(mark),
                        run_time=0.2,
                    )
                    dup_indices.append(i)
                else:
                    # Unique — mark green
                    self.play(
                        arr[i][0].animate.set_stroke(GREEN, width=3),
                        run_time=0.2,
                    )
                    kept_indices.append(i)

            self.play(FadeOut(scanner))
            self.wait(max(0.2, tracker.duration - 4.0))

        # ---- erase step ----
        with self.voiceover(LINES["unique_erase"]) as tracker:
            # Show the garbage subrange bracket
            if dup_indices:
                garbage_label = Text("← garbage (erase this) →",
                                     font="monospace", color=RED, font_size=14)
                garbage_label.next_to(arr, DOWN, buff=0.6)
                self.play(FadeIn(garbage_label))
                self.wait(0.5)

                # Fade out duplicates
                fade_anims = []
                for idx in dup_indices:
                    fade_anims.append(FadeOut(arr[idx], shift=DOWN * 0.3))
                self.play(*fade_anims, FadeOut(garbage_label), run_time=0.5)

            # Show final result
            unique_vals = []
            seen = set()
            for v in UNIQUE_NUMS:
                if v not in seen:
                    unique_vals.append(v)
                    seen.add(v)

            result_arr = make_array(unique_vals, cell_color=GREEN, text_color=GREEN,
                                    cell_size=0.55)
            result_arr.move_to(DOWN * 1.2)

            result_label = Text(
                f"after erase: {{{', '.join(str(x) for x in unique_vals)}}}",
                font="monospace", color=GREEN, font_size=18,
            )
            result_label.next_to(result_arr, DOWN, buff=0.3)

            self.play(
                LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in result_arr],
                            lag_ratio=0.06),
                FadeIn(result_label),
            )
            self.wait(max(0.2, tracker.duration - 2.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)


class RangesRemoveIf(VoiceoverScene):
    """Scene 10: std::ranges::remove_if demonstration."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)

        # ---- title ----
        title = Text("std::ranges::remove_if", font="monospace",
                     color=TEAL, font_size=36)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["remove_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- remove_if animation ----
        code = make_code(
            "auto [rem_first, rem_last] =\n"
            "    std::ranges::remove_if(to_remove,\n"
            "        [](int x) { return x % 2 != 0; });\n"
            "to_remove.erase(rem_first, rem_last);", 16
        )
        code.to_edge(UP, buff=0.4)

        src_label = Text("to_remove", font="monospace", color=GREY, font_size=16)
        arr = make_array(REMOVE_NUMS, cell_size=0.55)
        arr.move_to(UP * 0.0)
        src_label.next_to(arr, LEFT, buff=0.3)

        cond_label = Text("predicate: x % 2 != 0  (odd numbers)",
                          font="monospace", color=GOLD, font_size=15)
        cond_label.next_to(arr, DOWN, buff=0.4)

        with self.voiceover(LINES["remove_run"]) as tracker:
            self.play(FadeIn(code))
            self.play(FadeIn(src_label),
                      LaggedStart(*[FadeIn(m, shift=UP * 0.1)
                                    for m in arr], lag_ratio=0.05))
            self.play(FadeIn(cond_label))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.12)
            scanner.next_to(arr[0], UP, buff=0.15)
            self.play(FadeIn(scanner), run_time=0.2)

            keep_indices = []
            remove_indices = []

            for i in range(len(REMOVE_NUMS)):
                self.play(scanner.animate.next_to(arr[i], UP, buff=0.15),
                          run_time=0.2)

                is_odd = REMOVE_NUMS[i] % 2 != 0
                if is_odd:
                    # Matches predicate → will be removed
                    mark = Text("✗", font="monospace", color=RED, font_size=16)
                    mark.next_to(arr[i], UP, buff=0.4)
                    self.play(
                        FadeIn(mark),
                        arr[i][0].animate.set_stroke(RED, width=2.5),
                        arr[i][1].animate.set_color(RED),
                        run_time=0.2,
                    )
                    remove_indices.append(i)
                else:
                    # Does not match → kept
                    mark = Text("✓", font="monospace", color=GREEN, font_size=16)
                    mark.next_to(arr[i], UP, buff=0.4)
                    self.play(
                        FadeIn(mark),
                        arr[i][0].animate.set_stroke(GREEN, width=3),
                        run_time=0.2,
                    )
                    keep_indices.append(i)

            self.play(FadeOut(scanner))
            self.wait(max(0.2, tracker.duration - 5.0))

        # ---- erase step ----
        with self.voiceover(LINES["remove_erase"]) as tracker:
            # Show kept elements shifting forward
            kept_vals = [REMOVE_NUMS[i] for i in keep_indices]

            # Build the "after" state: kept values + garbage
            after_label = Text("after remove_if (before erase):",
                               font="monospace", color=GREY, font_size=14)
            after_label.next_to(cond_label, DOWN, buff=0.5)

            kept_arr = make_array(kept_vals, cell_color=GREEN, text_color=GREEN,
                                  cell_size=0.55)

            garbage_vals = [REMOVE_NUMS[i] for i in remove_indices]
            garbage_arr = make_array(garbage_vals, cell_color=RED, text_color=RED,
                                     cell_size=0.55)
            for cell_grp in garbage_arr:
                cell_grp.set_opacity(0.35)

            combined = VGroup(kept_arr, garbage_arr).arrange(RIGHT, buff=0.1)
            combined.next_to(after_label, DOWN, buff=0.3)

            # Divider line between kept and garbage
            divider = Line(UP * 0.35, DOWN * 0.35, color=GOLD, stroke_width=2)
            divider.move_to(
                (kept_arr.get_right() + garbage_arr.get_left()) / 2
            )

            div_label = Text("← kept | garbage →", font="monospace",
                             color=GOLD, font_size=12)
            div_label.next_to(divider, DOWN, buff=0.15)

            self.play(FadeIn(after_label))
            self.play(
                LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in kept_arr],
                            lag_ratio=0.05),
                LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in garbage_arr],
                            lag_ratio=0.05),
            )
            self.play(Create(divider), FadeIn(div_label))
            self.wait(0.5)

            # Erase garbage
            self.play(
                FadeOut(garbage_arr, shift=DOWN * 0.3),
                FadeOut(divider), FadeOut(div_label),
                run_time=0.5,
            )

            result_label = Text(
                f"after erase: {{{', '.join(str(x) for x in kept_vals)}}}",
                font="monospace", color=GREEN, font_size=18,
            )
            result_label.next_to(kept_arr, DOWN, buff=0.4)
            self.play(FadeIn(result_label))

            # Explain the two-step pattern
            note = Text("algorithms move → .erase() shrinks",
                        font="monospace", color=ORANGE, font_size=16)
            note.next_to(result_label, DOWN, buff=0.4)
            self.play(FadeIn(note))
            self.wait(max(0.2, tracker.duration - 3.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
