from manim import *


def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)


def get_data():
    data = open("../../05.test").read()
    ranstr, numbers = data.split("\n\n")
    ranges = [tuple(int(x) for x in ran.split("-")) for ran in ranstr.split("\n")]
    numbers = [int(x) for x in numbers.split("\n")]
    return ranstr, ranges, numbers


def make_tick_line(start, end, y_pos, tick_height, n_ticks):
        line = Line(start, end, color=WHITE, stroke_width=3).set_y(y_pos)
        dx = (end - start)[0] / (n_ticks - 1)
        ticks = VGroup()
        for i in range(n_ticks):
            tick_start = start + i * dx * RIGHT + y_pos * UP
            tick_end = start + i * dx * RIGHT + y_pos * UP

            outer = i in [0, n_ticks - 1]
            tick_len = (1 + outer / 2) * tick_height

            ticks.add(
                Line(
                    tick_start + tick_len * UP,
                    tick_end + tick_len * DOWN,
                    stroke_width=2,
                )
            )
        return VGroup(line, ticks)


def line2rect(line: Line, vert=False):
    if vert:
        return Rectangle(
            width=line.stroke_width / 100,
            height=(line.end - line.start)[1],
            fill_opacity=1,
            stroke_width=0,
        ).move_to(line)
    else:
        return Rectangle(
            width=(line.end - line.start)[0],
            height=line.stroke_width / 100,
            fill_opacity=1,
            stroke_width=0,
        ).move_to(line)


class Exposition(Scene):

    def construct(self):
        ranstr, ranges, numbers = get_data()

        # SHOW
        mob_ranges = VGroup(
            MathTex(ran, color=WHITE) for ran in ranstr.splitlines()
        ).arrange(DOWN)
        mob_numbers = (
            VGroup(MathTex(num, color=RED_E) for num in numbers)
            .arrange(DOWN)
            .next_to(mob_ranges, 2 * DOWN)
        )

        VGroup(mob_ranges, mob_numbers).center()
        self.play(Create(mob_ranges))
        self.wait(0.5)
        self.play(Create(mob_numbers))

        min_n, max_n = min(numbers), max(numbers)
        L, U = 1.7 * LEFT, 1.7 * RIGHT

        # TURN RANGES IN TO LINES
        mob_range_lines = VGroup()
        anims = []
        for (a, b), mob in zip(ranges, mob_ranges):
            start, end = L + (a - min_n) / (max_n - min_n) * (U - L), L + (
                b - min_n
            ) / (max_n - min_n) * (U - L)
            line = Line(start, end, color=WHITE, stroke_width=3).set_y(
                mob.get_center()[1]
            )
            #line = make_tick_line(start, end, mob.get_center()[1], 0.05, b - a + 1)
            mob_range_lines.add(line)
            anims.append(ReplacementTransform(mob, line))
        self.play(LaggedStart(*anims))

        # TURN NUMBERS INTO DOTS
        mob_dots = VGroup()
        anims = []
        for n, mob in zip(numbers, mob_numbers):
            xpos = L + (n - min_n) / (max_n - min_n) * (U - L)
            dot = Dot(xpos, radius=0.75 * DEFAULT_DOT_RADIUS, color=RED_E).set_y(
                mob.get_center()[1]
            )
            mob_dots.add(dot)
            anims.append(ReplacementTransform(mob, dot))
        self.play(LaggedStart(*anims))

        # MOVE ALL TO Y = 0
        anims = []
        for line in mob_range_lines:
            anims.append(line.animate.set_y(ORIGIN[1]))
        for dot in mob_dots:
            anims.append(dot.animate.set_y(ORIGIN[1]))
        self.play(*anims)

        # REMOVE POINTS NOT IN ANY RANGE
        anims = []
        for n, mob in zip(numbers, mob_dots):
            if not any([l <= n <= u for l, u in ranges]):
                anims.append(ShrinkToCenter(mob))
                mob_dots.remove(mob)
        self.play(*anims)

        # COMBINE TO NUMBER
        mob_sum = Integer(len(mob_dots), color=GREEN).scale(1.5).shift(DOWN)
        self.play(ReplacementTransform(mob_dots, mob_sum), FadeOut(mob_range_lines))


class PartTwo(Scene):

    def scale_x(self, x):
        return self.L + (x - self.min_n) / (self.max_n - self.min_n) * (self.U - self.L)

    def construct(self):
        Animation.set_default(run_time=0.75)

        _, ranges, _ = get_data()
        ranges.append((13, 16))

        mob_ranges = VGroup(
            MathTex(str(a) + "-" + str(b), color=WHITE) for a, b in ranges
        ).arrange(DOWN)
        self.play(Create(mob_ranges))
        self.wait(0.5)

        self.min_n, self.max_n = min(a for a, b in ranges), max(b for a, b in ranges)
        self.L, self.U = 1.7 * LEFT, 1.7 * RIGHT

        # TURN TO LINES
        mob_range_lines = VGroup()
        anims = []
        for (a, b), mob in zip(ranges, mob_ranges):
            start, end = self.scale_x(a), self.scale_x(b)
            line = make_tick_line(start, end, mob.get_center()[1], 0.05, b - a + 1)
            mob_range_lines.add(line)
            anims.append(ReplacementTransform(mob, line))
        self.play(LaggedStart(*anims))

        # SORT 'EM
        sorted_ranges, sort_idx = sorted(ranges), argsort(ranges)
        mob_sorted_lines = VGroup()
        anims = []
        for i, k in enumerate(sort_idx):
            anims.append(
                mob_range_lines[k].animate.set_y(mob_range_lines[i].get_center()[1])
            )
            mob_sorted_lines.add(mob_range_lines[k])
        self.play(*anims)

        # DRAW ANSWER VARIABLE
        mob_ans = Integer(0, color=GREEN).scale(1.5).next_to(mob_sorted_lines, 2 * DOWN)
        self.play(
            VGroup(mob_sorted_lines, mob_ans).animate.center(),
            DrawBorderThenFill(mob_ans),
        )

        tiny_linies = []
        for x in mob_sorted_lines:
            tiny_linies.append(line2rect(x[0]))
            for y in x[1]:
                tiny_linies.append(line2rect(y, vert=True))

        # COUNT 'EM
        ans = 0

        max_u = ValueTracker(0)

        def mob_max_u_updater(m):
            m.set_x(self.scale_x(max_u.get_value())[0])

        mob_max_u = DashedLine(
            start=self.scale_x(-1) + 2.5 * UP,
            end=self.scale_x(-1) + 1.5 * DOWN,
            color=RED,
        )
        mob_max_u.add_updater(mob_max_u_updater)
        self.add(mob_max_u)
        self.play(max_u.animate.set_value(1))

        inters = always_redraw(
            lambda: VGroup(*[Intersection(
                line,
                Rectangle(
                    height=(mob_max_u.start - mob_max_u.end)[1],
                    width=10,
                    fill_opacity=1,
                    stroke_opacity=0,
                )
                .move_to(mob_max_u)
                .align_to(mob_max_u, RIGHT),
                fill_opacity=1,
                stroke_opacity=0,
                color=RED,
            ) for line in tiny_linies])
        )
        self.add(inters)

        for (l, u), mob in zip(sorted_ranges, mob_sorted_lines):
            self.play(mob.animate.set_color(GREEN))
            if l > max_u.get_value():
                ans += u - l + 1
            elif u > max_u.get_value():
                ans += u - max_u.get_value()
            self.play(
                Transform(
                    mob_ans, Integer(ans, color=GREEN).scale(1.5).move_to(mob_ans)
                )
            )
            old_max_u = max_u.get_value()
            self.play(max_u.animate.set_value(max(old_max_u, u)))
        self.wait(0.5)
        self.play(max_u.animate.increment_value(5))


class Complexity(Scene):

    def construct(self):
        complexity = Tex("\\underline{Complexity}")
        part1 = Tex("Part 1: $\\mathcal O(n \\cdot r)$").next_to(complexity, 2*DOWN)
        part2 = Tex("Part 2: $\\mathcal O(r \\log r)$").next_to(part1, 0.5*DOWN)

        comments = (
            Tex(
                "\\\\".join(
                    [
                        "$\\star$ $n=$ no.~of numbers",
                        "$\\star$ $r=$ no.~of ranges",
                    ]
                ),
                tex_environment="flushleft",
            )
            .scale(0.5)
            .next_to(part2, 2 * DOWN)
        )

        self.add(VGroup(complexity, part1, part2, comments).center())