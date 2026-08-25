from manim import *

# ---- colour palette ----
INK      = "#1a1a18"
OFFWHITE = "#e8e6df"
TEAL     = "#00b4d8"
GREY     = "#7a7875"
SURF     = "#2a2a27"

# ---- Title card data: (ClassName, algorithm_name, description) ----
CARDS = {
    "TitleSort":          ("ranges::sort",        "Sort a container"),
    "TitleFind":          ("ranges::find",        "Find an element"),
    "TitleCount":         ("ranges::count_if",    "Count matching elements"),
    "TitleTransform":     ("ranges::transform",   "Transform elements"),
    "TitleCopyIf":        ("ranges::copy_if",     "Copy matching elements"),
    "TitleBoolPred":      ("ranges::all_of / any_of / none_of", "Boolean predicates"),
    "TitleMinMax":        ("ranges::min / max",   "Find extremes"),
    "TitleReverse":       ("ranges::reverse",     "Reverse a range"),
    "TitleUnique":        ("ranges::unique",      "Remove consecutive duplicates"),
    "TitleRemoveIf":      ("ranges::remove_if",   "Remove matching elements"),
    "TitleFill":          ("ranges::fill",        "Fill with a value"),
    "TitleGenerate":      ("ranges::generate",    "Generate values"),
    "TitleReplaceIf":     ("ranges::replace_if",  "Replace matching elements"),
    "TitlePartition":     ("ranges::partition",   "Partition a range"),
    "TitleIsSorted":      ("ranges::is_sorted",   "Check if sorted"),
    "TitleBinarySearch":  ("ranges::binary_search", "Binary search"),
    "TitleNthElement":    ("ranges::nth_element", "Partial sort"),
    "TitleWithStrings":   ("ranges + strings",    "Algorithms with strings"),
    "TitleProjections":   ("Projections",         "Sort by a member"),
    "TitleViewsPipeline": ("Views | Pipeline",    "Lazy range adaptors"),
}


def _make_card_scene(class_name, algo_name, description):
    """Dynamically create a Scene subclass for a title card."""

    class CardScene(Scene):
        def construct(self):
            self.camera.background_color = INK

            # Main algorithm name
            title = Text(algo_name, font="monospace", color=TEAL, font_size=42)

            # Short description
            desc = Text(description, font="monospace", color=GREY, font_size=24)
            desc.next_to(title, DOWN, buff=0.35)

            # Subtle decorative line
            line = Line(LEFT * 2, RIGHT * 2, stroke_color=TEAL, stroke_width=1.5)
            line.set_opacity(0.5)
            line.next_to(desc, DOWN, buff=0.3)

            group = VGroup(title, desc, line).move_to(ORIGIN)

            # Subtle animation: scale up + fade in
            self.play(
                FadeIn(title, shift=UP * 0.2, scale=0.9),
                run_time=1.0,
            )
            self.play(
                FadeIn(desc, shift=UP * 0.15),
                GrowFromCenter(line),
                run_time=1.0,
            )
            self.wait(0.7)
            self.play(FadeOut(group, shift=UP * 0.2), run_time=1.0)

    CardScene.__name__ = class_name
    CardScene.__qualname__ = class_name
    return CardScene


# Dynamically create all scene classes and inject into module globals
for _name, (_algo, _desc) in CARDS.items():
    globals()[_name] = _make_card_scene(_name, _algo, _desc)
