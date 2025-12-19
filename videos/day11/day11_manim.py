from collections import defaultdict

from manim import *


class Exposition(Scene):

    def construct(self):
        data_raw = open("../../11.test").read()
        data = data_raw.splitlines()
        adj = defaultdict(list)
        for line in data:
            a, b = line.split(":")
            adj[a] += b.split()

        # SHOW THE INPUT
        """
        mob_input = Text(data_raw, font="Source Code Pro", font_size=25)
        cols = [RED, GREEN, BLUE]
        self.add(mob_input)
        """

        vertices = sorted(set(adj.keys()) | set().union(*adj.values()))
        edges = []
        for k, v in adj.items():
            edges += [(k, vv) for vv in v]
        graph = DiGraph(
            vertices,
            edges,
            layout={
                "aaa": 2*UP,
                "you": 2*UP + LEFT,
                "hhh": UP,
                "bbb": UP + 2*LEFT,
                "ccc": UP + LEFT,
                "ddd": LEFT,
                "eee": 2*LEFT,
                "fff": ORIGIN,
                "ggg": DOWN + 0.5*LEFT,
                "iii": RIGHT,
                "out": 2*DOWN,
            },
            edge_config={
                "tip_config": {"tip_length": 0.1, "tip_width": 0.1},
                "stroke_width": 1.5,
            },
            # vertex_mobjects={v: create_labeled_vertex(v) for v in vertices},
            vertex_config={
                "radius": 0.2,
                "stroke_width": 1.5,
                "color": WHITE,  # Boundary color (stroke)
                "fill_color": WHITE,  # Fill color
                "fill_opacity": 0.05,
            },
            # layout_scale=5,
            labels={v: Text(v, font="Source Code Pro", font_size=15).scale(0.65) for v in vertices},
        ).shift(0.5*RIGHT + 0.7*UP).scale(1.1)
        self.add(graph)

        # MARK YOU AND OUT
        self.play(graph.vertices[v].animate.set_color(RED_B) for v in ['you', 'out'])

        s = {('you', 'out'): 1}
        mob_eq = MathTex("f(\\texttt{you}, \\texttt{out})", font_size=25).move_to(2.5*DOWN)
        self.play(Create(mob_eq))
        
        def build_string(s):
            ret = []
            n = len(s)
            for i,((u,w),b) in enumerate(s):
                if b > 1:
                    ret.append(str(b))
                ret.append(f"f(\\texttt{{{u}}}, \\texttt{{{w}}})")
                if n > 3 and (i-1) % 3 == 0:
                    ret.append("\\\\")
                ret.append("+")
            return ret[:-1]

        strings = []
        while s:
            t = []
            td = defaultdict(int)
            flag = False
            for (v,w),b in s.items():
                for u in adj[v]:
                    if u != 'out':
                        flag = True
                    t.append(((u,w),b))
                    td[u,w] += b
                if v == 'out':
                    t.append((('out',w),b))
                    td['out',w] += b
            #strings.append(MathTex(build_string(t), font_size=25).move_to(2.5*DOWN))
            strings.append(MathTex(*build_string(td.items()), font_size=25).move_to(2.5*DOWN))

            if flag:
                s = td
            else:
                break
        
        for s in strings:
            self.play(ReplacementTransform(mob_eq, s))
            self.wait(0.3)
            mob_eq = s
        
        #mob_brace = Brace(s[1:], DOWN)
        mob_brace = BraceLabel(s[1:], "1", DOWN, stroke_width=0.5)
        #mob_brace_txt = Integer(1).next_to(mob_brace, DOWN)
        self.play(DrawBorderThenFill(mob_brace))

        # f(you, out) = f(bbb, out) + f(ccc, out)
        # f(you, out) = (f(eee, out) + f(ddd, out)) + f(ccc, out)
        # f(you, out) = (f(eee, out) + f(ddd, out)) + (f(eee, out) + f(ddd, out), f(fff, out))
        # f(you, out) = 2 f(eee, out) + 2 f(ddd, out) + f(fff, out)
        # f(you, out) = 2 f(out, out) + 2 f(ggg, out) + f(out, out)
        # f(you, out) = 3 f(out, out) + 2 f(out, out)
        # f(you, out) = 5 f(out, out)
        # f(you, out) = 5