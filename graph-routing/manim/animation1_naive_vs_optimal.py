# animation1_naive_vs_optimal.py
# CodePuz — Animation 1: The Naive Layout vs The Optimal Layout (teaser, ~25s)
#
#   pip install manim manim-voiceover gtts
#   manim -pqm animation1_naive_vs_optimal.py NaiveVsOptimal
#
# Font: uses "DejaVu Sans Mono", which ships with Manim's matplotlib dependency
# and is present on effectively all systems. Change MONO below if you prefer.

from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

CPZ_BG    = "#0A1220"
CPZ_TEAL  = "#43E6C8"
CPZ_GOLD  = "#D8A44E"
CPZ_CORAL = "#E8735A"
CPZ_TEXT  = "#E8EDF5"
CPZ_MUTED = "#8896B0"

MONO = "Montserrat"
NODE_R = 0.35


class NaiveVsOptimal(VoiceoverScene):
    def construct(self):
        self.camera.background_color = CPZ_BG
        self.set_speech_service(
            EdgeTTSService(voice="en-US-AvaMultilingualNeural")
        )
        watermark = Text("© CodePuz",  font="Montserrat", font_size=18,  color="#ffffff",     weight=BOLD,   )     
        watermark.set_opacity(0.45)
        watermark.to_corner(DR, buff=0.25)
        self.add(watermark)

        labels = ["A", "B", "C", "D", "E", "F"]
        edges = [("A", "C"), ("A", "D"), ("B", "C"), ("B", "E"),
                 ("C", "F"), ("D", "F"), ("E", "F")]

        # Naive layout: deliberately interleaved so several edges tangle.
        # Verify the live counter reads 4 on render; nudge if needed.
        naive_pos = {
            "A": LEFT * 4.5 + UP * 2.0,
            "B": LEFT * 4.5 + DOWN * 2.0,
            "C": RIGHT * 3.5 + DOWN * 2.0,
            "D": LEFT * 1.5 + UP * 3.0,
            "E": RIGHT * 2.2 + UP * 3.0,
            "F": LEFT * 0.5 + DOWN * 1.3,
        }
        layered_pos_1 = {   # one crossing remaining (C above D)
            "A": LEFT * 4.2 + UP * 1.2,
            "B": LEFT * 4.2 + DOWN * 1.2,
            "C": ORIGIN + UP * 2.2,
            "D": ORIGIN,
            "E": ORIGIN + DOWN * 2.2,
            "F": RIGHT * 4.2,
        }
        layered_pos_0 = dict(layered_pos_1)   # zero crossings: swap C and D
        layered_pos_0["C"], layered_pos_0["D"] = layered_pos_1["D"], layered_pos_1["C"]

        def make_nodes(posmap):
            g = {}
            for lab in labels:
                circ = Circle(radius=NODE_R, color=CPZ_TEAL,
                              fill_color=CPZ_BG, fill_opacity=1, stroke_width=2)
                txt = Text(lab, font=MONO, color=CPZ_TEXT).scale(0.5)
                g[lab] = VGroup(circ, txt).move_to(posmap[lab])
            return g

        def make_edges(nodes, color):
            arrows = {}
            for a, b in edges:
                arrows[(a, b)] = Arrow(
                    nodes[a].get_center(), nodes[b].get_center(),
                    buff=NODE_R, color=color, stroke_width=3,
                    tip_length=0.2, max_tip_length_to_length_ratio=0.15)
            return arrows

        def seg_intersect(p1, p2, p3, p4):
            def ccw(a, b, c):
                return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
            return (ccw(p1, p3, p4) != ccw(p2, p3, p4) and
                    ccw(p1, p2, p3) != ccw(p1, p2, p4))

        def crossing_points(nodes):
            pts, ek = [], list(edges)
            for i in range(len(ek)):
                for j in range(i + 1, len(ek)):
                    a1, b1 = ek[i]; a2, b2 = ek[j]
                    if len({a1, b1, a2, b2}) < 4:
                        continue
                    p1, p2 = nodes[a1].get_center(), nodes[b1].get_center()
                    p3, p4 = nodes[a2].get_center(), nodes[b2].get_center()
                    if seg_intersect(p1, p2, p3, p4):
                        d = ((p1[0]-p2[0])*(p3[1]-p4[1]) -
                             (p1[1]-p2[1])*(p3[0]-p4[0]))
                        if abs(d) < 1e-6:
                            continue
                        px = ((p1[0]*p2[1]-p1[1]*p2[0])*(p3[0]-p4[0]) -
                              (p1[0]-p2[0])*(p3[0]*p4[1]-p3[1]*p4[0])) / d
                        py = ((p1[0]*p2[1]-p1[1]*p2[0])*(p3[1]-p4[1]) -
                              (p1[1]-p2[1])*(p3[0]*p4[1]-p3[1]*p4[0])) / d
                        pts.append(np.array([px, py, 0]))
            return pts

        def crossing_dots(nodes):
            return VGroup(*[Dot(pt, radius=0.12, color=CPZ_GOLD,
                                fill_opacity=0.85)
                            for pt in crossing_points(nodes)])

        def count_label(n):
            return Text(f"Crossings: {n}", font=MONO,
                        color=CPZ_GOLD).scale(0.5).to_corner(UR, buff=1.6)

        # ---- Scene 1: naive layout ----
        nodes = make_nodes(naive_pos)
        arrows = make_edges(nodes, CPZ_CORAL)
        with self.voiceover(
            text="Here is a simple six node graph. Seven connections. "
                 "When we lay it out naively, we get four crossings. "
                 "Every crossing makes the diagram harder to read."):
            self.play(*[FadeIn(nodes[l]) for l in labels], run_time=1.2)
            for a, b in edges:
                self.play(GrowArrow(arrows[(a, b)]), run_time=0.3)
            dots = crossing_dots(nodes)
            clabel = count_label(len(dots))
            self.play(FadeIn(dots), FadeIn(clabel), run_time=0.6)
            self.play(dots.animate.scale(1.4), rate_func=there_and_back,
                      run_time=0.8)

        # ---- Scene 2: transform to layered (one crossing) ----
        with self.voiceover(
            text="If we organize nodes into layers, based on the direction "
                 "of flow, things improve. But we still have one crossing."):
            self.play(*[nodes[l].animate.move_to(layered_pos_1[l])
                        for l in labels], run_time=2.0)
            na = make_edges(nodes, CPZ_CORAL)
            self.play(*[Transform(arrows[k], na[k]) for k in arrows],
                      run_time=0.8)
            nd = crossing_dots(nodes)
            nl = count_label(len(nd))
            self.play(Transform(dots, nd), Transform(clabel, nl), run_time=0.8)

        # ---- Scene 3: reorder within layer to zero ----
        with self.voiceover(
            text="A small reordering within one layer eliminates the last "
                 "crossing. For this tiny graph, we could try every "
                 "arrangement by hand. But what happens when the graph has "
                 "fifty nodes? Or five thousand?"):
            self.play(nodes["C"].animate.move_to(layered_pos_0["C"]),
                      nodes["D"].animate.move_to(layered_pos_0["D"]),
                      run_time=1.5)
            ca = make_edges(nodes, CPZ_TEAL)
            self.play(*[Transform(arrows[k], ca[k]) for k in arrows],
                      run_time=0.8)
            zd = crossing_dots(nodes)
            zl = count_label(len(zd))
            self.play(Transform(dots, zd), Transform(clabel, zl), run_time=0.6)
            self.wait(1.0)

        # ---- Closing question ----
        question = Text("How do we find this arrangement automatically?",
                        font=MONO, color=CPZ_TEXT).scale(0.6)
        with self.voiceover(text="How can we find this arrangement automatically?"):
            self.play(*[FadeOut(nodes[l]) for l in labels],
                      *[FadeOut(arrows[k]) for k in arrows],
                      FadeOut(dots), FadeOut(clabel), run_time=0.8)
            self.play(Write(question), run_time=1.0)
        self.wait(2.5)