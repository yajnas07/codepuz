# animation2_barycenter.py
# CodePuz — Animation 2: The Barycenter Sweep (~35s)
#
#   pip install manim manim-voiceover gtts
#   manim -pqm animation2_barycenter.py BarycenterSweep
#
# Uses the same graph as Widget 1 (crossing counter): the reader has already
# dragged this one by hand; now they watch the barycenter method solve it.
# Font: Montserrat (must be installed on the system, or Manim will fall back).

from manim import *
from manim_voiceover import VoiceoverScene
from edge_service import EdgeTTSService

CPZ_BG    = "#0A1220"
CPZ_TEAL  = "#43E6C8"
CPZ_GOLD  = "#D8A44E"
CPZ_CORAL = "#E8735A"
CPZ_TEXT  = "#E8EDF5"
CPZ_MUTED = "#8896B0"

FONT = "Montserrat"
NODE_R = 0.32


class BarycenterSweep(VoiceoverScene):
    def construct(self):
        self.camera.background_color = CPZ_BG
        self.set_speech_service(EdgeTTSService(voice="en-US-AvaMultilingualNeural"))
        watermark = Text("© CodePuz",  font="Montserrat", font_size=18,  color="#ffffff",     weight=BOLD,   )     
        watermark.set_opacity(0.45)
        watermark.to_corner(DR, buff=0.25)
        self.add(watermark)
        
        # Same structure as Widget 1.
        top = ["A", "B"]
        mid_init = ["1", "2", "3", "4"]
        bot = ["C", "D"]
        edges_tm = [("A", "1"), ("A", "2"), ("A", "4"),
                    ("B", "1"), ("B", "3"), ("B", "4")]
        edges_mb = [("1", "D"), ("2", "C"), ("3", "D"), ("4", "C")]
        all_edges = edges_tm + edges_mb

        # Column x-positions and per-layer y-slots.
        X_TOP, X_MID, X_BOT = -4.5, 0.0, 4.5
        top_y = {"A": 1.4, "B": -1.4}
        bot_y = {"C": 1.4, "D": -1.4}
        mid_slots = [2.4, 0.8, -0.8, -2.4]

        state = {"mid": mid_init[:]}

        def mid_y(node):
            return mid_slots[state["mid"].index(node)]

        def pos(node):
            if node in top_y:
                return np.array([X_TOP, top_y[node], 0])
            if node in bot_y:
                return np.array([X_BOT, bot_y[node], 0])
            return np.array([X_MID, mid_y(node), 0])

        node_m = {}

        def build_node(lab, is_mid):
            circ = Circle(radius=NODE_R, color=(CPZ_GOLD if is_mid else CPZ_TEAL),
                          fill_color=CPZ_BG, fill_opacity=1, stroke_width=2)
            txt = Text(lab, font=FONT, color=CPZ_TEXT).scale(0.42)
            return VGroup(circ, txt).move_to(pos(lab))

        for lab in top:
            node_m[lab] = build_node(lab, False)
        for lab in mid_init:
            node_m[lab] = build_node(lab, True)
        for lab in bot:
            node_m[lab] = build_node(lab, False)

        def trimmed(a, b):
            pa, pb = pos(a), pos(b)
            d = pb - pa
            L = np.linalg.norm(d)
            if L < 1e-6:
                return pa, pb
            u = d / L
            return pa + u * NODE_R, pb - u * NODE_R

        def make_edges(color_fn):
            arr = {}
            for a, b in all_edges:
                s, e = trimmed(a, b)
                arr[(a, b)] = Line(s, e, color=color_fn(a, b), stroke_width=2.5)
            return arr

        # def make_edges(color_fn):
        #     arr = {}
        #     for a, b in all_edges:
        #         arr[(a, b)] = Line(pos(a), pos(b), color=color_fn(a, b),
        #                            stroke_width=2.5)
        #     return arr

        def seg_int(p1, p2, p3, p4):
            def ccw(a, b, c):
                return (c[1]-a[1])*(b[0]-a[0]) > (b[1]-a[1])*(c[0]-a[0])
            return (ccw(p1, p3, p4) != ccw(p2, p3, p4) and
                    ccw(p1, p2, p3) != ccw(p1, p2, p4))

        def count_crossings():
            n = 0
            for i in range(len(all_edges)):
                for j in range(i + 1, len(all_edges)):
                    a1, b1 = all_edges[i]; a2, b2 = all_edges[j]
                    if len({a1, b1, a2, b2}) < 4:
                        continue
                    if seg_int(pos(a1), pos(b1), pos(a2), pos(b2)):
                        n += 1
            return n

        def edge_color(a, b):
            return CPZ_TEAL if count_crossings() == 0 else CPZ_CORAL

        edge_m = make_edges(edge_color)

        def redraw_edges():
            clean = count_crossings() == 0
            anims = []
            for (a, b), ln in edge_m.items():
                s, e = trimmed(a, b)
                anims.append(ln.animate.put_start_and_end_on(s, e)
                             .set_color(CPZ_TEAL if clean else CPZ_CORAL))
            return anims

        # def redraw_edges():
        #     clean = count_crossings() == 0
        #     anims = []
        #     for (a, b), ln in edge_m.items():
        #         anims.append(ln.animate.put_start_and_end_on(pos(a), pos(b))
        #                      .set_color(CPZ_TEAL if clean else CPZ_CORAL))
        #     return anims

        def count_label():
            return Text(f"Crossings: {count_crossings()}", font=FONT,
                        color=CPZ_GOLD).scale(0.5).to_corner(UR, buff=0.6)

        # ---- Scene 1: initial messy state ----
        # On-screen definition of barycenter.
        bary_def = Text(
            "Barycenter = average position of a node's neighbors",
            font=FONT, color=CPZ_MUTED).scale(0.36).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bary_def), run_time=0.6)

        clabel = count_label()
        with self.voiceover(
            text="After layer assignment, the nodes within each layer are in "
                 "an arbitrary order. The result is a tangle of crossings."):
            self.play(*[FadeIn(node_m[n]) for n in node_m], run_time=1.0)
            self.play(*[Create(edge_m[k]) for k in edge_m], run_time=1.2)
            self.play(FadeIn(clabel), run_time=0.5)

        # ---- Scene 2: barycenter computation ----
        # ---- Scene 2: barycenter computation (one worked example) ----
        top_pos_idx = {"A": 0, "B": 1}
        bary = {}
        for node in state["mid"]:
            nb = [top_pos_idx[a] for (a, b) in edges_tm if b == node]
            bary[node] = sum(nb) / len(nb) if nb else mid_slots[state["mid"].index(node)]

        with self.voiceover(
            text="Take node 1 in the middle layer. It connects to A and B "
                 "in the left layer. A sits at position 0, B at position 1. "
                 "The barycenter is their average: zero plus one, over two, "
                 "equals nought point five."):

            # Position-index labels on the top-layer nodes.
            posA = Text("pos 0", font=FONT, color=CPZ_MUTED).scale(0.34)
            posA.next_to(node_m["A"], UP, buff=0.2)
            posB = Text("pos 1", font=FONT, color=CPZ_MUTED).scale(0.34)
            posB.next_to(node_m["B"], DOWN, buff=0.2)
            self.play(FadeIn(posA), FadeIn(posB), run_time=0.6)

            # Highlight node 1 and its two upward edges.
            def hi(a, b):
                for (x, y), ln in edge_m.items():
                    if (x, y) == (a, b):
                        return ln
                return None
            e_a1, e_b1 = hi("A", "1"), hi("B", "1")
            node1_ring = Circle(radius=NODE_R + 0.08, color=CPZ_GOLD,
                                stroke_width=3).move_to(pos("1"))
            self.play(
                Create(node1_ring),
                e_a1.animate.set_color(CPZ_GOLD).set_stroke(width=4),
                e_b1.animate.set_color(CPZ_GOLD).set_stroke(width=4),
                run_time=0.8,
            )

            # The arithmetic, shown step by step near node 1.
            calc = Text("(0 + 1) / 2 = 0.5", font=FONT, color=CPZ_GOLD).scale(0.42)
            calc.next_to(node_m["1"], LEFT, buff=0.45)
            self.play(Write(calc), run_time=1.0)
            self.wait(0.6)

            # Settle node 1's result into a compact label, restore edges.
            b1_label = Text("1: 0.5", font=FONT, color=CPZ_GOLD).scale(0.4)
            b1_label.next_to(node_m["1"], LEFT, buff=0.35)
            self.play(
                Transform(calc, b1_label),
                e_a1.animate.set_color(CPZ_CORAL).set_stroke(width=2.5),
                e_b1.animate.set_color(CPZ_CORAL).set_stroke(width=2.5),
                FadeOut(node1_ring),
                FadeOut(posA), FadeOut(posB),
                run_time=0.8,
            )

        with self.voiceover(
            text="The other three nodes in the middle layer work the same way. "
                 "Each one computes the average position of its neighbors "
                 "in the left layer."):
            # `calc` was Transform-ed into b1_label; tracking `calc` keeps the
            # on-screen mobject reference so FadeOut later removes it too.
            eqs = VGroup(calc)
            for node in state["mid"]:
                if node == "1":
                    continue
                eq = Text(f"{node}: {bary[node]:.1f}", font=FONT,
                          color=CPZ_GOLD).scale(0.4)
                eq.next_to(node_m[node], LEFT, buff=0.35)
                eqs.add(eq)
                self.play(FadeIn(eq), run_time=0.45)
            self.wait(0.5)

        # ---- Scene 3: reorder by barycenter (down-sweep) ----
        new_order = sorted(state["mid"], key=lambda n: (bary[n],
                            mid_init.index(n)))

        # Build a dict mapping each mid node to its on-screen label mobject.
        # eqs contains calc (which is the on-screen ref for node "1") plus
        # the other three labels added in order.
        eq_map = {}
        eq_idx = 0
        for node in state["mid"]:
            if node == "1":
                eq_map["1"] = eqs[0]  # calc (transformed into b1_label)
            else:
                eq_idx += 1
                eq_map[node] = eqs[eq_idx]

        with self.voiceover(
            text="We then sort the middle layer nodes by their barycenters. "
                 "Nodes with smaller values move up; nodes with larger values "
                 "move down. Like being pulled by springs."):
            # Sweep direction indicator.
            sweep_label_d = Text("→ Sweep from left layer", font=FONT,
                                 color=CPZ_MUTED).scale(0.38).to_corner(UL, buff=0.5)
            self.play(FadeIn(sweep_label_d), run_time=0.4)
            state["mid"] = new_order
            # Move nodes AND their barycenter labels together.
            move = []
            for n in state["mid"]:
                target = pos(n)
                move.append(node_m[n].animate.move_to(target))
                label_target = target + LEFT * (NODE_R + 0.35)
                move.append(eq_map[n].animate.move_to(label_target))
            self.play(*move, run_time=1.5)
            self.play(*redraw_edges(), run_time=0.8)
            nl = count_label()
            self.play(Transform(clabel, nl), run_time=0.5)
            self.wait(1.0)
            # Fade out labels and sweep indicator before the reverse sweep.
            self.play(FadeOut(eqs), FadeOut(sweep_label_d), run_time=0.5)

        # ---- Scene 4: reverse sweep from the bottom layer ----


        with self.voiceover(
            text="Now we sweep in the opposite direction. This time, each "
                 "middle layer node looks at its neighbors in the right layer. "
                 "C sits at position zero, D at position one. A new "
                 "barycenter is computed from these positions."):
            # Sweep direction indicator.
            sweep_label = Text("← Sweep from right layer", font=FONT,
                               color=CPZ_MUTED).scale(0.38).to_corner(UL, buff=0.5)
            self.play(FadeIn(sweep_label), run_time=0.4)

            bot_pos_idx = {"C": 0, "D": 1}
            bary2 = {}
            for node in state["mid"]:
                nb = [bot_pos_idx[b] for (a, b) in edges_mb if a == node]
                bary2[node] = sum(nb) / len(nb) if nb else 0
            order2 = sorted(state["mid"], key=lambda n: (bary2[n],
                            state["mid"].index(n)))

            # Position-index labels on the bottom-layer nodes.
            posC = Text("pos 0", font=FONT, color=CPZ_MUTED).scale(0.34)
            posC.next_to(node_m["C"], UP, buff=0.2)
            posD = Text("pos 1", font=FONT, color=CPZ_MUTED).scale(0.34)
            posD.next_to(node_m["D"], DOWN, buff=0.2)
            self.play(FadeIn(posC), FadeIn(posD), run_time=0.5)

            # Show bottom-layer barycenters (different direction, label with ↑).
            eqs2 = VGroup()
            eq2_map = {}
            for node in state["mid"]:
                eq = Text(f"{node}↑{bary2[node]:.1f}", font=FONT,
                          color=CPZ_GOLD).scale(0.4)
                eq.next_to(node_m[node], LEFT, buff=0.35)
                eqs2.add(eq)
                eq2_map[node] = eq
            self.play(*[FadeIn(e) for e in eqs2], run_time=0.6)
            self.wait(2)
            

            # Only apply reorder if it actually reduces crossings.
            old_crossings = count_crossings()
            if order2 != state["mid"]:
                old_order = state["mid"][:]
                state["mid"] = order2
                new_crossings = count_crossings()
                if new_crossings <= old_crossings:
                    move2 = []
                    for n in state["mid"]:
                        target = pos(n)
                        move2.append(node_m[n].animate.move_to(target))
                        label_target = target + LEFT * (NODE_R + 0.35)
                        move2.append(eq2_map[n].animate.move_to(label_target))
                    self.play(*move2, run_time=1.3)
                else:
                    state["mid"] = old_order  # revert

            self.play(*redraw_edges(), run_time=0.8)
            fl = count_label()
            self.play(Transform(clabel, fl), run_time=0.5)
            self.wait(8.0)
            self.play(FadeOut(posC), FadeOut(posD), run_time=0.4)
            self.play(FadeOut(eqs2), FadeOut(sweep_label), run_time=0.5)

        # ---- Scene 5: additional sweeps until convergence ----
        max_iters = 4
        for iteration in range(max_iters):
            # Down sweep (from top layer)
            bary_down = {}
            for node in state["mid"]:
                nb = [top_pos_idx[a] for (a, b) in edges_tm if b == node]
                bary_down[node] = sum(nb) / len(nb) if nb else 0
            order_down = sorted(state["mid"], key=lambda n: (bary_down[n],
                                state["mid"].index(n)))
            old_c = count_crossings()
            changed = False
            if order_down != state["mid"]:
                old_order = state["mid"][:]
                state["mid"] = order_down
                if count_crossings() < old_c:
                    changed = True
                else:
                    state["mid"] = old_order

            if not changed:
                # Up sweep
                bary_up = {}
                for node in state["mid"]:
                    nb = [bot_pos_idx[b] for (a, b) in edges_mb if a == node]
                    bary_up[node] = sum(nb) / len(nb) if nb else 0
                order_up = sorted(state["mid"], key=lambda n: (bary_up[n],
                                  state["mid"].index(n)))
                if order_up != state["mid"]:
                    old_order = state["mid"][:]
                    state["mid"] = order_up
                    if count_crossings() < old_c:
                        changed = True
                    else:
                        state["mid"] = old_order

            if not changed:
                break  # converged

            self.play(*[node_m[n].animate.move_to(pos(n))
                        for n in state["mid"]], run_time=1.0)
            self.play(*redraw_edges(), run_time=0.6)
            il = count_label()
            self.play(Transform(clabel, il), run_time=0.4)

        self.play(FadeOut(bary_def), run_time=0.6)
        # ---- Closing: convergence message ----
        final_msg = Text(
            f"Converged at {count_crossings()} crossing — no better arrangement exists.",
            font=FONT, color=CPZ_TEXT).scale(0.42).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            text="No further sweep improves the layout. The algorithm has "
                 "converged. This is the best arrangement the barycenter "
                 "heuristic can find."):
            self.play(FadeIn(final_msg), run_time=1.5)
            self.wait(2.0)