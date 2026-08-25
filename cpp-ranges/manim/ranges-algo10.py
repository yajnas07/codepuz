from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo10.py RangesViewsPipeline

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
PURPLE   = "#a87bdb"


def _scene_label(scene, text):
    """Add a persistent bottom-left scene label."""
    lbl = Text(text, font="monospace", font_size=24, color="#74b860")
    lbl.set_opacity(0.7).to_corner(DL, buff=0.25)
    scene.add(lbl)
    return lbl

# ---- narration lines ----
LINES = {
    "views_intro": (
        "Views, also called range adaptors, let you build lazy transformation pipelines "
        "using the pipe operator. No intermediate containers are created. "
        "This is the final and arguably most elegant feature of C++ 20 ranges."
    ),
    "views_code": (
        "We chain three views. Filter keeps only even numbers. "
        "Transform squares each value. Take limits the output to the first 3 results."
    ),
    "views_lazy": (
        "The key insight is that views are lazy. "
        "Nothing happens when you define the pipeline. "
        "Computation only occurs when you iterate, "
        "and each element flows through the entire chain one at a time."
    ),
    "views_flow": (
        "Let's trace the element-by-element flow. "
        "1 is odd, so filter skips it. "
        "2 is even, filter passes it, transform squares it to 4, and take emits it. "
        "3 is odd, skipped. "
        "4 passes filter, becomes 16, emitted. "
        "5 skipped. "
        "6 passes, becomes 36, emitted. "
        "Take has 3 results, so iteration stops. Elements 7 through 10 are never examined."
    ),
    "views_vs_algo": (
        "Views are lazy and non-mutating. Algorithms are eager and may mutate. "
        "Views compose with the pipe operator. Algorithms are called individually. "
        "Use views for read-only pipelines, and algorithms when you need to modify data."
    ),
    "views_common": (
        "Here are the most commonly used views. "
        "Filter, transform, and take are the workhorses. "
        "Drop, reverse, keys, values, split, and join cover most other needs."
    ),
    "views_closing": (
        "And that concludes our tour of C++ 20 range algorithms and views. "
        "From sort and find to projections and lazy pipelines, "
        "ranges make C++ code safer, cleaner, and more expressive."
    ),
}

# ---- data ----
DATA = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


def make_array(values, cell_color=GREY, text_color=OFFWHITE, cell_size=0.6):
    """Create a row of boxes with values inside."""
    grp = VGroup()
    for v in values:
        cell = RoundedRectangle(
            width=cell_size, height=cell_size, corner_radius=0.06,
            stroke_color=cell_color, stroke_width=2,
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


def make_stage_box(label, color):
    """Create a pipeline stage box."""
    box = RoundedRectangle(
        width=2.0, height=0.55, corner_radius=0.08,
        stroke_color=color, stroke_width=2,
        fill_color=SURF, fill_opacity=1,
    )
    lbl = Text(label, font="monospace", color=color, font_size=14)
    lbl.move_to(box)
    return VGroup(box, lbl)


class RangesViewsPipeline(VoiceoverScene):
    """Scene 20: Combining algorithms with views (range adaptors)."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)
        _scene_label(self, "Lazy range adaptors")

        # ---- title ----
        title = Text("Views & Pipe Operator", font="monospace",
                     color=TEAL, font_size=38)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["views_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- show the code ----
        code = make_code(
            "auto result = data\n"
            "    | std::views::filter([](int x) { return x % 2 == 0; })\n"
            "    | std::views::transform([](int x) { return x * x; })\n"
            "    | std::views::take(3);", 15
        )
        code.to_edge(UP, buff=0.4)

        with self.voiceover(LINES["views_code"]) as tracker:
            self.play(FadeIn(code))

            # Show pipeline stages visually
            stage_data = make_stage_box("data", GREY)
            pipe1 = Text("|", font="monospace", color=TEAL, font_size=20)
            stage_filter = make_stage_box("filter(even?)", GREEN)
            pipe2 = Text("|", font="monospace", color=TEAL, font_size=20)
            stage_transform = make_stage_box("transform(x²)", BLUE)
            pipe3 = Text("|", font="monospace", color=TEAL, font_size=20)
            stage_take = make_stage_box("take(3)", GOLD)

            pipeline = VGroup(
                stage_data, pipe1, stage_filter, pipe2,
                stage_transform, pipe3, stage_take,
            ).arrange(RIGHT, buff=0.15).move_to(DOWN * 0.3)

            self.play(
                LaggedStart(
                    FadeIn(stage_data),
                    FadeIn(pipe1),
                    FadeIn(stage_filter),
                    FadeIn(pipe2),
                    FadeIn(stage_transform),
                    FadeIn(pipe3),
                    FadeIn(stage_take),
                    lag_ratio=0.12,
                ),
            )
            self.wait(max(0.2, tracker.duration - 2.5))

        # ---- lazy evaluation concept ----
        with self.voiceover(LINES["views_lazy"]) as tracker:
            lazy_note = Text(
                "⚡ LAZY — no work until iteration",
                font="monospace", color=ORANGE, font_size=16,
            )
            lazy_note.next_to(pipeline, DOWN, buff=0.5)

            no_copy = Text(
                "no intermediate vectors created",
                font="monospace", color=GREY, font_size=14,
            )
            no_copy.next_to(lazy_note, DOWN, buff=0.2)

            self.play(FadeIn(lazy_note), FadeIn(no_copy))
            self.wait(max(0.2, tracker.duration - 1.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- element-by-element flow animation ----
        with self.voiceover(LINES["views_flow"]) as tracker:
            # Rebuild pipeline stages as column headers
            hdr_data = Text("data", font="monospace", color=GREY, font_size=16)
            hdr_filter = Text("filter\n(even?)", font="monospace", color=GREEN, font_size=14)
            hdr_transform = Text("transform\n(x²)", font="monospace", color=BLUE, font_size=14)
            hdr_take = Text("take(3)", font="monospace", color=GOLD, font_size=14)

            headers = VGroup(hdr_data, hdr_filter, hdr_transform, hdr_take)
            headers.arrange(RIGHT, buff=1.2).to_edge(UP, buff=0.5)

            # Arrows between headers
            arrows = VGroup()
            for i in range(3):
                a = Arrow(
                    headers[i].get_right(), headers[i + 1].get_left(),
                    color=TEAL, stroke_width=1.5, buff=0.1,
                    max_tip_length_to_length_ratio=0.15,
                )
                arrows.add(a)

            self.play(FadeIn(headers), *[GrowArrow(a) for a in arrows])

            # Trace each element
            output_vals = []
            take_count = 0
            row_y_start = headers.get_bottom()[1] - 0.5

            for i, val in enumerate(DATA):
                if take_count >= 3:
                    break

                y_pos = row_y_start - i * 0.45

                # Data column
                val_mob = Text(str(val), font="monospace", color=OFFWHITE, font_size=16)
                val_mob.move_to([hdr_data.get_center()[0], y_pos, 0])
                self.play(FadeIn(val_mob), run_time=0.15)

                is_even = val % 2 == 0

                # Filter column
                if is_even:
                    filter_mob = Text(f"{val} ✓", font="monospace",
                                     color=GREEN, font_size=14)
                else:
                    filter_mob = Text("skip", font="monospace",
                                     color=RED, font_size=14)

                filter_mob.move_to([hdr_filter.get_center()[0], y_pos, 0])

                if not is_even:
                    self.play(
                        FadeIn(filter_mob),
                        val_mob.animate.set_color(RED).set_opacity(0.4),
                        run_time=0.2,
                    )
                    continue

                # Even — passes filter
                squared = val * val
                transform_mob = Text(str(squared), font="monospace",
                                     color=BLUE, font_size=16)
                transform_mob.move_to([hdr_transform.get_center()[0], y_pos, 0])

                take_count += 1
                take_mob = Text(f"emit ({take_count}/3)", font="monospace",
                                color=GOLD, font_size=13)
                take_mob.move_to([hdr_take.get_center()[0], y_pos, 0])
                output_vals.append(squared)

                self.play(FadeIn(filter_mob), run_time=0.15)
                self.play(FadeIn(transform_mob), run_time=0.15)
                self.play(FadeIn(take_mob), run_time=0.15)

            # Show STOP
            if take_count >= 3:
                stop_label = Text("STOP — take(3) satisfied",
                                  font="monospace", color=ORANGE, font_size=15)
                stop_y = row_y_start - (6) * 0.45
                stop_label.move_to([0, stop_y, 0])

                remaining = Text("elements 7–10 never examined ⚡",
                                 font="monospace", color=GREY, font_size=13)
                remaining.next_to(stop_label, DOWN, buff=0.15)

                self.play(FadeIn(stop_label), FadeIn(remaining))

            # Show final output
            result_text = Text(
                f"output: {{{', '.join(str(v) for v in output_vals)}}}",
                font="monospace", color=GOLD, font_size=18,
            )
            result_text.next_to(remaining, DOWN, buff=0.3)
            self.play(FadeIn(result_text))
            self.wait(max(0.2, tracker.duration - 8.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- views vs algorithms comparison ----
        with self.voiceover(LINES["views_vs_algo"]) as tracker:
            # Define fixed column x-positions
            col_x = [-2.5, 0.0, 2.5]

            headers_tbl = VGroup(
                Text("", font="monospace", font_size=1).move_to([col_x[0], 0, 0]),
                Text("Views", font="monospace", color=TEAL, font_size=17).move_to([col_x[1], 0, 0]),
                Text("Algorithms", font="monospace", color=GREEN, font_size=17).move_to([col_x[2], 0, 0]),
            )
            headers_tbl.to_edge(UP, buff=0.8)

            comparisons = [
                ("Execution", "lazy", "eager"),
                ("Memory", "no copies", "may copy"),
                ("Compose", "pipe |", "individual calls"),
                ("Mutation", "read-only", "some mutate"),
            ]

            rows_grp = VGroup()
            for i, (label, view_val, algo_val) in enumerate(comparisons):
                l = Text(label, font="monospace", color=GREY, font_size=15)
                v = Text(view_val, font="monospace", color=TEAL, font_size=15)
                a = Text(algo_val, font="monospace", color=GREEN, font_size=15)
                # Position each element at fixed column x
                y_pos = headers_tbl.get_bottom()[1] - 0.5 - i * 0.45
                l.move_to([col_x[0], y_pos, 0])
                v.move_to([col_x[1], y_pos, 0])
                a.move_to([col_x[2], y_pos, 0])
                rows_grp.add(VGroup(l, v, a))

            self.play(FadeIn(headers_tbl))
            self.play(LaggedStart(*[FadeIn(r) for r in rows_grp], lag_ratio=0.15))
            self.wait(max(0.2, tracker.duration - 2.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- common views reference ----
        with self.voiceover(LINES["views_common"]) as tracker:
            views_list = [
                ("filter(pred)", "keep matching elements", GREEN),
                ("transform(fn)", "apply function to each", BLUE),
                ("take(n)", "first n elements", GOLD),
                ("drop(n)", "skip first n elements", ORANGE),
                ("reverse", "reverse order", TEAL),
                ("keys / values", "for map-like ranges", PURPLE),
                ("split(delim)", "split by delimiter", GREY),
                ("join", "flatten nested ranges", GREY),
            ]

            # Fixed column x-positions for alignment
            name_x = -1.8
            desc_x = 1.2
            start_y = 2.0
            row_spacing = 0.4

            views_grp = VGroup()
            for i, (name, desc, clr) in enumerate(views_list):
                n = Text(name, font="monospace", color=clr, font_size=15)
                d = Text(desc, font="monospace", color=GREY, font_size=14)
                y_pos = start_y - i * row_spacing
                n.move_to([name_x, y_pos, 0])
                d.move_to([desc_x, y_pos, 0])
                views_grp.add(VGroup(n, d))

            self.play(LaggedStart(*[FadeIn(v) for v in views_grp], lag_ratio=0.1))
            self.wait(max(0.2, tracker.duration - 2.5))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- closing ----
        with self.voiceover(LINES["views_closing"]) as tracker:
            closing_title = Text("C++20 Range Algorithms", font="monospace",
                                 color=TEAL, font_size=34)
            closing_sub = Text("Complete Tour ✓", font="monospace",
                               color=GREEN, font_size=24)
            closing_sub.next_to(closing_title, DOWN, buff=0.3)

            topics = VGroup(
                Text("sort · find · count · transform · copy_if", font="monospace",
                     color=GREY, font_size=14),
                Text("all_of · min/max · reverse · unique · remove_if", font="monospace",
                     color=GREY, font_size=14),
                Text("fill · generate · replace_if · partition", font="monospace",
                     color=GREY, font_size=14),
                Text("is_sorted · binary_search · nth_element", font="monospace",
                     color=GREY, font_size=14),
                Text("strings · projections · views & pipes", font="monospace",
                     color=GREY, font_size=14),
            ).arrange(DOWN, buff=0.2)
            topics.next_to(closing_sub, DOWN, buff=0.5)

            self.play(Write(closing_title), FadeIn(closing_sub, shift=UP * 0.2))
            self.play(LaggedStart(*[FadeIn(t) for t in topics], lag_ratio=0.15))
            self.wait(max(0.2, tracker.duration - 3.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
