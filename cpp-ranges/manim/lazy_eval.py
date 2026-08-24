from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

# ---- narration lines, one per animation beat ----
LINES = {
    "intro":  "A range pipeline does no work when it is written. It only builds a plan and waits.",
    "idle":   "The items rest on the belt. Nothing has been pulled yet, so nothing moves.",
    "pull":   "Ask for one value, and the demand travels back up the chain to fetch it.",
    "drop":   "An item that fails a filter is discarded on the spot. The belt never collects it.",
    "pass":   "A surviving value flows through the transform and out the far end, one at a time.",
    "close":  "Because nothing is ever gathered in between, no intermediate vector is ever allocated.",
}


INK      = "#1a1a18"
OFFWHITE = "#e8e6df"
TEAL     = "#00b4d8"
TEAL_DIM = "#007a94"
GOLD     = "#d4a017"
GREEN    = "#74b860"
RED      = "#c84b2f"
GREY     = "#7a7875"
SURF     = "#2a2a27"
MUTED    = GREY
PASS     = GREEN
DROP     = RED

ITEMS = [
    {"v": 0,  "bus": False, "win": False, "sig": "clk"},
    {"v": 42, "bus": True,  "win": False, "sig": "data_bus"},
    {"v": 47, "bus": True,  "win": True,  "sig": "data_bus"},
    {"v": 51, "bus": True,  "win": True,  "sig": "data_bus"},
    {"v": 58, "bus": True,  "win": True,  "sig": "data_bus"},
    {"v": 0,  "bus": False, "win": False, "sig": "clk"},
]


class LazyEvaluation(VoiceoverScene):
    def construct(self):
        self.camera.background_color = INK
        self.set_speech_service(
            # EdgeTTSService(voice="en-IN-PrabhatNeural")
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )
        watermark = Text(
            "© CodePuz",
            font="Arial",
            font_size=18,
            color="#ffffff",
            weight=NORMAL,
        )
        watermark.set_opacity(0.35)
        watermark.to_corner(DR, buff=0.25)
        self.add(watermark)

        stage_names = ["source", "filter: bus", "filter: window", "transform: value"]
        stage_x = [-5.2, -1.9, 1.4, 4.7]
        stages = VGroup()
        for name, x in zip(stage_names, stage_x):
            box = RoundedRectangle(
                width=2.6, height=0.7, corner_radius=0.1,
                stroke_color=TEAL, stroke_width=2, fill_color=SURF, fill_opacity=1,
            ).move_to([x, 2.6, 0])
            lbl = Text(name, font="monospace", color=OFFWHITE).scale(0.3).move_to(box)
            stages.add(VGroup(box, lbl))

        # ---- intro narration over the stage reveal ----
        with self.voiceover(LINES["intro"]) as tracker:
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in stages], lag_ratio=0.15))

            belt = Line([-6.4, -0.2, 0], [6.4, -0.2, 0], stroke_color=MUTED, stroke_width=2)
            belt_hint = Text("pull from this end \u2192", font="monospace", color=GREY).scale(0.28)
            belt_hint.next_to(belt.get_end() - RIGHT * 1.5, UP, buff=0.15)
            self.play(Create(belt), FadeIn(belt_hint))
            self.wait(max(0.2, tracker.duration - 2.2))

        item_mobs = VGroup()
        start_x = -5.6
        for i, it in enumerate(ITEMS):
            cell = Square(side_length=0.7, stroke_color=GREY, stroke_width=1.5,
                          fill_color=SURF, fill_opacity=1)
            val = Text(str(it["v"]), font="monospace", color=OFFWHITE).scale(0.32)
            grp = VGroup(cell, val).move_to([start_x + i * 0.85, -0.9, 0])
            item_mobs.add(grp)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in item_mobs], lag_ratio=0.08))

        # ---- idle beat ----
        with self.voiceover(LINES["idle"]) as tracker:
            idle = Text("belt is idle: no value has been pulled yet",
                        font="monospace", color=GREY).scale(0.3).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(idle))
            self.wait(tracker.duration - 0.8 if tracker.duration > 0.8 else 0.1)
        self.play(FadeOut(idle))

        tray_label = Text("values pulled", font="monospace", color=OFFWHITE).scale(0.3)
        tray_label.move_to([4.5, -1.85, 0])
        self.play(FadeIn(tray_label))

        surviving_x = 4.7
        pulled = VGroup()

        # narrate the first pull, the first drop, and the first pass once each,
        # so the concepts are spoken without repeating on every item
        narrated = {"pull": False, "drop": False, "pass": False}

        def maybe_voiceover(key):
            """Return a voiceover context for the first occurrence; None thereafter."""
            if not narrated[key]:
                narrated[key] = True
                return self.voiceover(LINES[key])
            return None

        def pull(idx, produced_slot):
            it = ITEMS[idx]
            mob = item_mobs[idx]

            vo_pull = maybe_voiceover("pull")
            ctx_pull = vo_pull.__enter__() if vo_pull else None
            pulse = Dot(color=TEAL, radius=0.08).move_to([6.2, -0.2, 0])
            self.play(pulse.animate.move_to(mob.get_center() + UP * 0.6),
                      run_time=0.6, rate_func=linear)
            self.play(FadeOut(pulse), run_time=0.2)
            # Move item from below belt to above belt, then to first stage
            self.play(mob.animate.move_to([mob.get_center()[0], 0.4, 0]), run_time=0.3)
            self.play(mob.animate.move_to([stage_x[0], 0.4, 0]), run_time=0.4)
            if vo_pull:
                vo_pull.__exit__(None, None, None)

            self.play(mob.animate.move_to([stage_x[1], 0.4, 0]), run_time=0.4)
            if not it["bus"]:
                vo_drop = maybe_voiceover("drop")
                if vo_drop:
                    with vo_drop:
                        x = Cross(mob, stroke_color=DROP, stroke_width=4).scale(0.4)
                        self.play(mob.animate.set_opacity(0.35), FadeIn(x), run_time=0.3)
                        self.play(FadeOut(mob), FadeOut(x), run_time=0.3)
                else:
                    x = Cross(mob, stroke_color=DROP, stroke_width=4).scale(0.4)
                    self.play(mob.animate.set_opacity(0.35), FadeIn(x), run_time=0.3)
                    self.play(FadeOut(mob), FadeOut(x), run_time=0.3)
                return None

            self.play(mob.animate.move_to([stage_x[2], 0.4, 0]), run_time=0.4)
            if not it["win"]:
                vo_drop = maybe_voiceover("drop")
                if vo_drop:
                    with vo_drop:
                        x = Cross(mob, stroke_color=DROP, stroke_width=4).scale(0.4)
                        self.play(mob.animate.set_opacity(0.35), FadeIn(x), run_time=0.3)
                        self.play(FadeOut(mob), FadeOut(x), run_time=0.3)
                else:
                    x = Cross(mob, stroke_color=DROP, stroke_width=4).scale(0.4)
                    self.play(mob.animate.set_opacity(0.35), FadeIn(x), run_time=0.3)
                    self.play(FadeOut(mob), FadeOut(x), run_time=0.3)
                return None

            vo_pass = maybe_voiceover("pass")
            if vo_pass:
                with vo_pass:
                    self.play(mob.animate.move_to([stage_x[3], 0.4, 0]), run_time=0.4)
                    self.play(mob[0].animate.set_stroke(PASS, width=2.5), run_time=0.25)
                    target = [surviving_x - 0.9 + produced_slot * 0.7, -2.5, 0]
                    self.play(mob.animate.scale(0.8).move_to(target), run_time=0.4)
            else:
                self.play(mob.animate.move_to([stage_x[3], 0.4, 0]), run_time=0.4)
                self.play(mob[0].animate.set_stroke(PASS, width=2.5), run_time=0.25)
                target = [surviving_x - 0.9 + produced_slot * 0.7, -2.5, 0]
                self.play(mob.animate.scale(0.8).move_to(target), run_time=0.4)
            return mob

        slot = 0
        for i in range(len(ITEMS)):
            result = pull(i, slot)
            if result is not None:
                pulled.add(result)
                slot += 1
            self.wait(0.2)

        # ---- closing beat ----
        with self.voiceover(LINES["close"]) as tracker:
            note = Text("no intermediate vector was ever allocated",
                        font="monospace", color=GREEN).scale(0.32).to_edge(DOWN, buff=0.7)
            self.play(Write(note))
            self.wait(tracker.duration - 1.0 if tracker.duration > 1.0 else 0.5)