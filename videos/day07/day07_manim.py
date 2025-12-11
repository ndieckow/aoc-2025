from dataclasses import dataclass

from manim import *

t2c = {".": GRAY_E, "^": RED, "|": GREEN, "S": GREEN} | {
    str(d): GOLD for d in range(10)
}


def read_data(ending = "test"):
    return open("../../07." + ending).read()


@dataclass(frozen=True)
class Vec2:
    r: int
    c: int

    def __add__(self, o):
        return Vec2(self.r + o.r, self.c + o.c)

    def __sub__(self, o):
        return Vec2(self.r - o.r, self.c - o.c)


class Grid(Text):

    def __init__(self, grid_string, t2c=None, font_size=30):
        self.grid_string = grid_string

        self.grid = [list(x) for x in self.grid_string.splitlines()]
        self.R = len(self.grid)
        self.C = len(self.grid[0])
        self.t2c = t2c | {"©": BLACK}

        super().__init__(
            self._join_grid(), font="Source Code Pro", font_size=font_size, t2c=self.t2c
        )

    def reset(self):
        self.grid = [list(x) for x in self.grid_string.splitlines()]
        self._render()

    def _join_grid(self):
        return (
            "©\n"
            + "\n".join(["".join(row) for row in self.grid])
            + "\n"
            + " " * (self.C - 1)
            + "©"
        )

    def _render(self):
        pos = self.get_center()
        self.become(
            Text(
                self._join_grid(),
                font="Source Code Pro",
                font_size=self.font_size,
                t2c=self.t2c,
            )
        ).move_to(pos)

    def in_bounds(self, p: Vec2):
        return 0 <= p.r < self.R and 0 <= p.c < self.C

    def at(self, p: Vec2):
        return self.grid[p.r][p.c]

    def mob_at(self, r, c):
        return self[r * self.C + c + 1]

    def set(self, p: Vec2, v: str):
        self.grid[p.r][p.c] = v
        self._render()

    def set_all(self, assignments: dict[Vec2, str]):
        for p, v in assignments.items():
            self.grid[p.r][p.c] = v
        self._render()

class Exposition(Scene):

    def construct(self):
        grid_string = read_data()

        mob_grid = Grid(grid_string, t2c=t2c, font_size=24).shift(0.75 * UP)
        self.play(Create(mob_grid))

        lines = grid_string.splitlines()
        R, C = len(lines), len(lines[0])
        beams = set()
        for c in range(C):
            if lines[0][c] == "S":
                beams.add(c)
                break

        # ans = 0
        ans = ValueTracker(0)
        mob_ans = Integer(ans.get_value(), color=GREEN).next_to(mob_grid, DOWN)
        mob_ans.add_updater(lambda m: m.set_value(ans.get_value()))
        self.play(Create(mob_ans))

        for r in range(R):
            new_beams = set()
            for c in beams:
                if lines[r][c] != "^":
                    new_beams.add(c)
                else:
                    ans.increment_value(1)
                    new_beams.update([c - 1, c + 1])

            beams = new_beams
            self.play(
                mob_grid.animate.set_all(
                    {Vec2(r, c): "|" for c in new_beams if lines[r][c] != "^"}
                ),
                run_time=0.0166667,
            )
            self.wait(0.2)


def all_paths(lines):
    R, C = len(lines), len(lines[0])

    def dfs(r, c):
        if r == R - 1:
            return [[(r, c)]]
        if lines[r][c] == "^":
            return dfs(r, c - 1) + dfs(r, c + 1)
        else:
            return [[(r, c)] + ls for ls in dfs(r + 1, c)]

    return dfs(0, C // 2)


class AllPaths(Scene):

    def construct(self):
        grid_string = read_data()

        mob_grid = Grid(grid_string, t2c=t2c, font_size=24).shift(0.75 * UP)
        self.play(Create(mob_grid))

        lines = grid_string.splitlines()
        R, C = len(lines), len(lines[0])

        paths = all_paths(lines)

        count = ValueTracker(0)
        mob_count = Integer(0, color=GREEN).next_to(mob_grid, DOWN)
        mob_count.add_updater(lambda m: m.set_value(count.get_value()))
        self.play(Create(mob_count))

        for i, path in enumerate(paths):
            count.increment_value(1)
            self.play(
                mob_grid.animate.set_all(
                    {
                        Vec2(r, c): ("|" if (r, c) in path else lines[r][c])
                        for r in range(R)
                        for c in range(C)
                    }
                ),
                run_time=0.0166667,
            )
            self.wait(0.05)


class GaltonBoard(Scene):

    def construct(self):
        grid_string = read_data()
        mob_grid = Grid(grid_string, t2c=t2c, font_size=24).shift(0.75 * UP)
        self.add(mob_grid)
        self.wait(1)
        ls = [(8, 8), (10, 7), (12, 4), (12, 8), (12, 10), (14, 11)]
        self.play(mob_grid.animate.set_all({Vec2(*p): "^" for p in ls}))
        self.wait(1)
        self.play(mob_grid.animate.set_all({Vec2(*p): "." for p in ls}))
        self.wait(1)


from collections import defaultdict


class PartTwoDP(Scene):

    def construct(self):
        grid_string = read_data()
        mob_grid = Grid(grid_string, t2c=t2c, font_size=24).shift(0.75 * UP)
        self.play(Create(mob_grid))
        self.wait(1)

        # SOLVE
        lines = grid_string.splitlines()
        R, C = len(lines), len(lines[0])
        sc = C // 2

        ways = defaultdict(int)
        ways[2, sc] = 1
        ans2 = 0
        parents = defaultdict(set)
        for r in range(1, R):
            for c in range(C):
                if lines[r][c] != "^":
                    continue
                for cc in [-1, 1]:
                    for rr in range(1, R - r):
                        if lines[r + rr][c + cc] == "^":
                            ways[r + rr, c + cc] += ways[r, c]
                            parents[r + rr, c + cc].add((r, c))
                            break
                ans2 += ways[r, c]
        
        mobs_for_sum = VGroup()
        for r in range(R):
            for c in range(C):
                if lines[r][c] != "^":
                    continue
                mob_cell = mob_grid.mob_at(r, c)
                if parents[r, c]:
                    mob_lines = VGroup(
                        Line(
                            start=mob_grid.mob_at(rr, cc),
                            end=mob_cell,
                            color=GOLD,
                        )
                        for (rr, cc) in parents[r, c]
                    )
                    self.play(
                        #*[
                        #    Indicate(mob_grid.mob_at(rr, cc))
                        #    for (rr, cc) in parents[r, c]
                        #],
                        Indicate(mob_cell, color=GOLD),
                        ShowPassingFlash(mob_lines, time_width=0.2)
                    )
                self.play(mob_grid.animate.set(Vec2(r, c), str(ways[r, c])), run_time=0.5)
                mobs_for_sum.add(mob_cell)
        
        # SUM UP
        mob_ans = Integer(ans2, color=GREEN).scale(1.5)
        self.play(ReplacementTransform(mobs_for_sum, mob_ans), FadeOut(*[mob for mob in mob_grid.submobjects if mob not in mobs_for_sum]))
        self.wait(0.5)
        self.play(mob_ans.animate.set_value(ans2 + 1))
        self.wait(0.5)


class Complexity(Scene):

    def construct(self):
        complexity = Tex("\\underline{Complexity}")
        part1 = Tex("Part 1: $\\mathcal O(n)$").next_to(complexity, 2*DOWN)
        part2 = Tex("Part 2: $\\mathcal O(n R)$").next_to(part1, 0.5*DOWN)

        comments = (
            Tex(
                "\\\\".join(
                    [
                        "$\\star$ $n=$ no.~of splitters",
                        "$\\star$ $R=$ no.~of rows",
                    ]
                ),
                tex_environment="flushleft",
            )
            .scale(0.5)
            .next_to(part2, 2 * DOWN)
        )

        self.add(VGroup(complexity, part1, part2, comments).center())