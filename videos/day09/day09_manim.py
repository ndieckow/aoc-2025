from manim import *


def area(p, q):
    return (abs(p[0] - q[0]) + 1) * (abs(p[1] - q[1]) + 1)


class PartOne(Scene):

    def scale_point(self, x, y):
        a = self.L + (x - self.min_x) / (self.max_x - self.min_x) * (self.R - self.L)
        b = self.U + (y - self.min_y) / (self.max_y - self.min_y) * (self.D - self.U)
        return a + b

    def get_rect_corners(self, p, q):
        return [
            self.scale_point(max(p[0], q[0]), min(p[1], q[1])),  # Top-right
            self.scale_point(min(p[0], q[0]), min(p[1], q[1])),  # Top-left
            self.scale_point(min(p[0], q[0]), max(p[1], q[1])),  # Bottom-left
            self.scale_point(max(p[0], q[0]), max(p[1], q[1])),  # Bottom-right
        ]

    def construct(self):
        data = open("../../09.test2").read().splitlines()
        points = [tuple(int(x) for x in p.split(",")) for p in data]
    
        #mob_coords = VGroup(MathTex("(" + x + ")") for x in data).arrange(DOWN)
        #self.play(Create(mob_coords))

        self.wait(0.5)

        self.min_x, self.max_x = min(p[0] for p in points), max(p[0] for p in points)
        self.min_y, self.max_y = min(p[1] for p in points), max(p[1] for p in points)

        self.L, self.R = 1.7 * LEFT, 1.7 * RIGHT
        self.U, self.D = 1.7 * UP, 1.7 * DOWN

        dots = VGroup()
        anims = []
        for (x, y), mob in zip(points, points):
            dot = Dot(self.scale_point(x, y), color=RED, radius=DEFAULT_DOT_RADIUS / 2)
            dots.add(dot)
            self.add(dot)
            #anims.append(ReplacementTransform(mob, dot))
        #self.play(*anims)

        self.wait(0.5)

        maxarea = ValueTracker(0)
        maxp, maxq, maxrect = None, None, None

        mob_maxarea = Integer(maxarea.get_value(), color=ORANGE).scale(1).next_to(dots, 4*DOWN)
        mob_maxarea.add_updater(lambda m: m.set_value(maxarea.get_value()))
        mob_label = Tex("max.\\\\area:", color=ORANGE).scale(0.4).next_to(mob_maxarea, LEFT)
        self.play(Create(mob_maxarea), Create(mob_label), VGroup(dots, mob_maxarea, mob_label).animate.center())

        for i, p in enumerate(points):
            for j, q in enumerate(points[i + 1 :]):
                sp, sq = self.scale_point(*p), self.scale_point(*q)
                if p[0] == q[0] or p[1] == q[1]:
                    rect = Line(
                        sp,
                        sq,
                        color=RED,
                        z_index=-1,
                        stroke_width=DEFAULT_STROKE_WIDTH / 2,
                    )
                else:
                    rect = Polygon(
                        *self.get_rect_corners(p, q),
                        color=RED,
                        fill_opacity=0.2,
                        z_index=-1,
                        stroke_width=DEFAULT_STROKE_WIDTH / 2
                    )

                self.add(rect)

                self.wait(0.1)

                a = area(p, q)
                if a > maxarea.get_value():
                    maxarea.set_value(a)
                    mob_maxarea.update()
                    maxp, maxq = p, q
                    if maxrect:
                        self.remove(maxrect)
                    maxrect = rect
                    rect.set_color(GOLD)
                else:
                    self.remove(rect)

        maxrect.set_color(GREEN)
        VGroup(mob_maxarea, mob_label).set_color(GREEN)
        self.wait(1)
