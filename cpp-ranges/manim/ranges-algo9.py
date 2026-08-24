from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# manim render -pql ranges-algo9.py RangesProjections

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

# ---- narration lines ----
LINES = {
    "proj_intro": (
        "Projections are one of the most powerful features unique to C++ 20 range algorithms. "
        "They let you tell an algorithm which part of each element to look at, "
        "without writing a full comparator."
    ),
    "proj_concept": (
        "Think of a projection as a lens. "
        "Instead of comparing entire objects, the algorithm first passes each element "
        "through the projection, then compares the results. "
        "This cleanly separates what to compare from how to compare."
    ),
    "proj_sort": (
        "Here we sort a vector of Person structs by age. "
        "The second argument is the comparator, left as default ascending. "
        "The third argument is the projection, a pointer to the age member. "
        "The algorithm extracts each person's age before comparing."
    ),
    "proj_sort_anim": (
        "Watch how the projection works. "
        "For each comparison, the algorithm projects onto the age field, "
        "then sorts by those projected values."
    ),
    "proj_find": (
        "Projections also work with find. "
        "Here we search for the name Charlie. "
        "The projection extracts the name member, "
        "so find compares Charlie against each person's name, not the whole struct."
    ),
    "proj_vs_lambda": (
        "Without projections, you would need a verbose lambda for the comparator. "
        "Projections make the same code shorter and more readable. "
        "The projection separates the concern of what field to access "
        "from the algorithm's logic."
    ),
    "proj_more": (
        "Projections work with almost every range algorithm. "
        "You can use them with min, count if, all of, and many more. "
        "They can be pointers to members, lambdas, or any callable."
    ),
    "proj_summary": (
        "Projections are unique to ranges. Classic STL algorithms don't have them. "
        "They make code cleaner, more composable, and less error prone."
    ),
}

# ---- data ----
PEOPLE = [
    ("Alice", 30),
    ("Bob", 25),
    ("Charlie", 35),
    ("David", 28),
]

PEOPLE_SORTED = sorted(PEOPLE, key=lambda p: p[1])  # by age


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


def make_person_row(name, age, name_color=OFFWHITE, age_color=OFFWHITE,
                    cell_color=GREY):
    """Create a visual row: [ name | age ]."""
    name_cell = RoundedRectangle(
        width=1.4, height=0.5, corner_radius=0.06,
        stroke_color=cell_color, stroke_width=2,
        fill_color=SURF, fill_opacity=1,
    )
    name_lbl = Text(name, font="monospace", color=name_color, font_size=16)
    name_lbl.move_to(name_cell)
    name_grp = VGroup(name_cell, name_lbl)

    age_cell = RoundedRectangle(
        width=0.7, height=0.5, corner_radius=0.06,
        stroke_color=cell_color, stroke_width=2,
        fill_color=SURF, fill_opacity=1,
    )
    age_lbl = Text(str(age), font="monospace", color=age_color, font_size=16)
    age_lbl.move_to(age_cell)
    age_grp = VGroup(age_cell, age_lbl)

    # Arrange the two groups (name and age) horizontally
    row = VGroup(name_grp, age_grp).arrange(RIGHT, buff=0.3)
    return row


def make_person_table(people, name_color=OFFWHITE, age_color=OFFWHITE,
                      cell_color=GREY):
    """Create a vertical table of person rows with aligned columns."""
    rows = VGroup()
    for name, age in people:
        rows.add(make_person_row(name, age, name_color, age_color, cell_color))
    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    return rows


class RangesProjections(VoiceoverScene):
    """Scene 19: Projections — a key C++20 ranges feature."""

    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )

        watermark = make_watermark()
        self.add(watermark)

        # ---- title ----
        title = Text("Projections", font="monospace",
                     color=TEAL, font_size=40)
        subtitle = Text("C++20 Range Algorithms", font="monospace",
                        color=GREY, font_size=22)
        subtitle.next_to(title, DOWN, buff=0.3)
        with self.voiceover(LINES["proj_intro"]) as tracker:
            self.play(Write(title), FadeIn(subtitle, shift=UP * 0.2))
            self.wait(max(0.2, tracker.duration - 1.5))
        self.play(FadeOut(title), FadeOut(subtitle))

        # ---- concept: projection as a lens ----
        with self.voiceover(LINES["proj_concept"]) as tracker:
            # Show the signature
            sig = make_code(
                "sort(range, comparator, projection)\n"
                "              ↑              ↑\n"
                "      how to compare   what to extract", 16
            )
            sig.move_to(UP * 1.5)

            # Diagram: element → [projection] → value → [comparator] → order
            elem_box = RoundedRectangle(
                width=1.6, height=0.5, corner_radius=0.06,
                stroke_color=GREY, stroke_width=2,
                fill_color=SURF, fill_opacity=1,
            )
            elem_lbl = Text("Person", font="monospace", color=OFFWHITE, font_size=16)
            elem_lbl.move_to(elem_box)
            elem_grp = VGroup(elem_box, elem_lbl)

            arrow1 = Arrow(ORIGIN, RIGHT * 1.2, color=TEAL, stroke_width=2,
                           max_tip_length_to_length_ratio=0.15)

            proj_box = RoundedRectangle(
                width=1.8, height=0.5, corner_radius=0.06,
                stroke_color=PURPLE, stroke_width=2,
                fill_color=SURF, fill_opacity=1,
            )
            proj_lbl = Text("&Person::age", font="monospace", color=PURPLE, font_size=14)
            proj_lbl.move_to(proj_box)
            proj_grp = VGroup(proj_box, proj_lbl)

            arrow2 = Arrow(ORIGIN, RIGHT * 1.2, color=TEAL, stroke_width=2,
                           max_tip_length_to_length_ratio=0.15)

            val_box = RoundedRectangle(
                width=0.8, height=0.5, corner_radius=0.06,
                stroke_color=GOLD, stroke_width=2,
                fill_color=SURF, fill_opacity=1,
            )
            val_lbl = Text("30", font="monospace", color=GOLD, font_size=16)
            val_lbl.move_to(val_box)
            val_grp = VGroup(val_box, val_lbl)

            flow = VGroup(elem_grp, arrow1, proj_grp, arrow2, val_grp)
            flow.arrange(RIGHT, buff=0.15).move_to(DOWN * 0.5)

            proj_title = Text("projection = lens 🔍", font="monospace",
                              color=PURPLE, font_size=18)
            proj_title.next_to(flow, DOWN, buff=0.5)

            self.play(FadeIn(sig))
            self.play(
                LaggedStart(
                    FadeIn(elem_grp),
                    GrowArrow(arrow1),
                    FadeIn(proj_grp),
                    GrowArrow(arrow2),
                    FadeIn(val_grp),
                    lag_ratio=0.15,
                ),
            )
            self.play(FadeIn(proj_title))
            self.wait(max(0.2, tracker.duration - 3.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- sort by age with projection ----
        code_sort = make_code(
            "std::ranges::sort(people, {}, &Person::age);", 17
        )
        code_sort.to_edge(UP, buff=0.5)

        # Header
        hdr_name = Text("name", font="monospace", color=GREY, font_size=14)
        hdr_age = Text("age", font="monospace", color=GREY, font_size=14)
        hdr = VGroup(hdr_name, hdr_age).arrange(RIGHT, buff=1.5)
        hdr.move_to(UP * 1.5 + LEFT * 2.5)

        table = make_person_table(PEOPLE)
        table.next_to(hdr, DOWN, buff=0.2)
        table.align_to(hdr, LEFT)

        with self.voiceover(LINES["proj_sort"]) as tracker:
            self.play(FadeIn(code_sort))
            self.play(FadeIn(hdr))
            self.play(LaggedStart(*[FadeIn(r) for r in table], lag_ratio=0.12))

            # Highlight the projection parameter in the code
            proj_highlight = SurroundingRectangle(
                code_sort, color=PURPLE, stroke_width=2, buff=0.08
            )

            # Show which part is comparator, which is projection
            comp_lbl = Text("{} = default (ascending)",
                            font="monospace", color=GREY, font_size=13)
            proj_lbl2 = Text("&Person::age = projection",
                             font="monospace", color=PURPLE, font_size=13)
            comp_lbl.next_to(code_sort, DOWN, buff=0.2)
            proj_lbl2.next_to(comp_lbl, DOWN, buff=0.1)

            self.play(FadeIn(comp_lbl), FadeIn(proj_lbl2))
            self.wait(max(0.2, tracker.duration - 3.0))

        # ---- animate the sort ----
        with self.voiceover(LINES["proj_sort_anim"]) as tracker:
            self.play(FadeOut(comp_lbl), FadeOut(proj_lbl2))

            # Highlight age column with projection lens
            for row in table:
                age_cell = row[1]  # (age_cell, age_lbl)
                self.play(
                    age_cell[0].animate.set_stroke(PURPLE, width=3),
                    age_cell[1].animate.set_color(PURPLE),
                    run_time=0.15,
                )

            proj_note = Text("projection extracts age →",
                             font="monospace", color=PURPLE, font_size=14)
            proj_note.next_to(table, RIGHT, buff=0.4)

            # Show extracted ages
            ages_extracted = VGroup()
            for i, (_, age) in enumerate(PEOPLE):
                a = Text(str(age), font="monospace", color=PURPLE, font_size=16)
                a.next_to(table[i], RIGHT, buff=3.0)
                ages_extracted.add(a)

            self.play(FadeIn(proj_note))
            self.play(LaggedStart(*[FadeIn(a) for a in ages_extracted],
                                  lag_ratio=0.1))
            self.wait(0.5)

            # Now show sorted result
            self.play(
                FadeOut(table), FadeOut(hdr), FadeOut(proj_note),
                FadeOut(ages_extracted),
            )

            sorted_table = make_person_table(PEOPLE_SORTED,
                                             age_color=GREEN, cell_color=GREEN)
            sorted_table.move_to(DOWN * 0.3)

            sorted_hdr = Text("sorted by age (ascending):",
                              font="monospace", color=GREEN, font_size=16)
            sorted_hdr.next_to(sorted_table, UP, buff=0.3)

            self.play(FadeIn(sorted_hdr))
            self.play(LaggedStart(*[FadeIn(r) for r in sorted_table],
                                  lag_ratio=0.12))
            self.wait(max(0.2, tracker.duration - 4.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- find with projection ----
        code_find = make_code(
            'auto it = std::ranges::find(\n'
            '    people, "Charlie", &Person::name);', 17
        )
        code_find.to_edge(UP, buff=0.5)

        table2 = make_person_table(PEOPLE_SORTED)
        table2.move_to(UP * 0.0 + LEFT * 2.0)

        with self.voiceover(LINES["proj_find"]) as tracker:
            self.play(FadeIn(code_find))
            self.play(LaggedStart(*[FadeIn(r) for r in table2], lag_ratio=0.1))

            target_lbl = Text('target: "Charlie"', font="monospace",
                              color=GOLD, font_size=16)
            target_lbl.next_to(table2, RIGHT, buff=0.8)
            proj_lbl3 = Text("projection: &Person::name",
                             font="monospace", color=PURPLE, font_size=14)
            proj_lbl3.next_to(target_lbl, DOWN, buff=0.2)
            self.play(FadeIn(target_lbl), FadeIn(proj_lbl3))

            scanner = Triangle(color=TEAL, fill_opacity=1).scale(0.1)
            self.wait(0.5)
            self.play(FadeOut(target_lbl), FadeOut(proj_lbl3))

            # Scan each row
            for i, (name, age) in enumerate(PEOPLE_SORTED):
                scanner.next_to(table2[i], LEFT, buff=0.15)
                self.play(FadeIn(scanner) if i == 0 else
                          scanner.animate.next_to(table2[i], LEFT, buff=0.15),
                          run_time=0.2)

                # Highlight name cell (projection)
                name_cell = table2[i][0]
                self.play(
                    name_cell[0].animate.set_stroke(PURPLE, width=3),
                    run_time=0.15,
                )

                comp_text = f'"{name}" == "Charlie"?'
                match = (name == "Charlie")
                comp = Text(
                    comp_text + (" ✓" if match else " ✗"),
                    font="monospace",
                    color=GREEN if match else RED,
                    font_size=13,
                )
                comp.next_to(table2[i], RIGHT, buff=2.5)

                self.play(FadeIn(comp), run_time=0.2)

                if match:
                    self.play(
                        table2[i][0][0].animate.set_stroke(GREEN, width=4),
                        table2[i][1][0].animate.set_stroke(GREEN, width=4),
                        table2[i][0][1].animate.set_color(GREEN),
                        table2[i][1][1].animate.set_color(GREEN),
                        run_time=0.3,
                    )
                    result_find = Text(
                        f"Found Charlie, age: {age}",
                        font="monospace", color=GREEN, font_size=18,
                    )
                    result_find.next_to(table2, DOWN, buff=0.6)
                    self.play(FadeIn(result_find), FadeOut(scanner))
                    break
                else:
                    self.play(
                        name_cell[0].animate.set_stroke(GREY, width=2),
                        table2[i].animate.set_opacity(0.4),
                        run_time=0.12,
                    )

            self.wait(max(0.2, tracker.duration - 5.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- projection vs lambda comparison ----
        with self.voiceover(LINES["proj_vs_lambda"]) as tracker:
            lbl_with = Text("With projection:", font="monospace",
                            color=GREEN, font_size=16)
            code_with = make_code(
                "std::ranges::sort(people, {}, &Person::age);", 16
            )
            lbl_without = Text("Without projection:", font="monospace",
                               color=RED, font_size=16)
            code_without = make_code(
                "std::ranges::sort(people,\n"
                "    [](const Person& a, const Person& b) {\n"
                "        return a.age < b.age;\n"
                "    });", 16
            )

            comparison = VGroup(
                VGroup(lbl_with, code_with).arrange(DOWN, buff=0.15),
                VGroup(lbl_without, code_without).arrange(DOWN, buff=0.15),
            ).arrange(DOWN, buff=0.6).move_to(ORIGIN)

            self.play(
                FadeIn(lbl_with), FadeIn(code_with),
            )
            self.wait(0.8)
            self.play(
                FadeIn(lbl_without), FadeIn(code_without),
            )

            verdict = Text("projection = cleaner & separates concerns",
                           font="monospace", color=PURPLE, font_size=15)
            verdict.next_to(comparison, DOWN, buff=0.5)
            self.play(FadeIn(verdict))
            self.wait(max(0.2, tracker.duration - 3.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.3)

        # ---- more examples ----
        with self.voiceover(LINES["proj_more"]) as tracker:
            examples = [
                ("ranges::min(people, {}, &Person::age)", "youngest person", GREEN),
                ("ranges::count_if(people, pred, &Person::age)", "count by age", TEAL),
                ("ranges::all_of(people, pred, &Person::age)", "check all ages", BLUE),
                ("ranges::find(people, val, &Person::name)", "find by name", GOLD),
            ]
            ex_grp = VGroup()
            for code_str, desc, clr in examples:
                c = Text(code_str, font="monospace", color=clr, font_size=15)
                d = Text(f"  // {desc}", font="monospace", color=GREY, font_size=14)
                ex_grp.add(VGroup(c, d).arrange(RIGHT, buff=0.3))
            ex_grp.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(ORIGIN)

            proj_types = Text(
                "projection can be: &member | lambda | any callable",
                font="monospace", color=PURPLE, font_size=14,
            )
            proj_types.next_to(ex_grp, DOWN, buff=0.6)

            self.play(LaggedStart(*[FadeIn(e) for e in ex_grp], lag_ratio=0.2))
            self.play(FadeIn(proj_types))
            self.wait(max(0.2, tracker.duration - 3.0))

        # ---- final summary ----
        with self.voiceover(LINES["proj_summary"]) as tracker:
            self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])

            summary_items = [
                "✓  Unique to C++20 ranges",
                "✓  Separates what from how",
                "✓  Cleaner than lambda comparators",
                "✓  Works with almost every algorithm",
            ]
            summary = VGroup()
            for item in summary_items:
                t = Text(item, font="monospace", color=PURPLE, font_size=18)
                summary.add(t)
            summary.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(ORIGIN)

            self.play(LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2)
                                    for s in summary], lag_ratio=0.25))
            self.wait(max(0.2, tracker.duration - 2.0))

        self.play(*[FadeOut(m) for m in self.mobjects if m != watermark])
        self.wait(0.5)
