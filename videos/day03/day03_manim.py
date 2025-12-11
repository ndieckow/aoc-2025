from manim import *


def argmax(nums):
    maxv, maxi = 0, None
    for i, n in enumerate(nums):
        if n > maxv:
            maxv = n
            maxi = i
    return maxv, maxi


def solve(bank, k):
    nums = [int(x) for x in bank]
    N = len(nums)
    offset = 0
    ans = 0
    indices = []
    for j in range(k):
        subnums = nums[offset : N - (k - 1) + j]
        d, max_i = argmax(subnums)
        indices.append(offset + max_i)
        offset += max_i + 1
        ans += d * 10 ** (k - j - 1)
    return ans, indices


class BruteForce(Scene):

    def construct(self):
        data = open("../../03.test").read().splitlines()
        rows = [[int(x) for x in row] for row in data]
        indices = [solve(row, 2)[1] for row in rows]
        prev = MathTex(*rows[0]).scale(0.9)
        blocks = VGroup(prev)
        for row in rows[1:]:
            newblock = MathTex(*row).scale(0.9).next_to(prev, 2 * DOWN)
            prev = newblock
            blocks.add(newblock)
        blocks.center()
        self.play(Create(blocks))

        # MARK
        anims = []
        for row, ind in zip(blocks, indices):
            anims += [row[i].animate.set_color(RED) for i in ind]
        self.play(*anims)

        # MERGE
        anims = []
        ans = 0
        mobs_summands = VGroup()  # mobjects to be summed up in the end
        for i, row in enumerate(blocks):
            ind = indices[i]
            n = rows[i][ind[0]] * 10 + rows[i][ind[1]]
            ans += n
            anims.append(
                FadeOut(
                    *[row[i] for i in range(len(row)) if i not in ind], run_time=0.8
                )
            )
            if abs(ind[0] - ind[1]) == 1:
                anims.append(row[ind[0] : ind[1] + 1].animate.move_to(row))
                mobs_summands.add(row[ind[0] : ind[1] + 1])
            else:
                new_mob = MathTex(n, color=RED).scale(0.9).move_to(row)
                anims.append(
                    TransformMatchingShapes(
                        VGroup(row[ind[0]], row[ind[1]]),
                        new_mob,
                    )
                )
                mobs_summands.add(new_mob)
        self.play(*anims)

        # SUM
        mob_sum = MathTex(ans, color=GREEN).scale(1.5)
        self.play(Transform(mobs_summands, mob_sum))


K = 2


class GreedyAlgo(Scene):

    def construct(self):
        Animation.set_default(run_time=0.5)

        data = open("../../03.test").read().splitlines()

        for example in data:
            nums = [int(x) for x in example]
            n = len(nums)
            row = MathTex(*example).scale(0.9).shift(1 * UP)
            self.play(Create(row))

            # GRAY LAST K-1 DIGITS
            self.play(row[-(K - 1):].animate.set_color(GRAY_D))
            below_digits = VGroup()
            offset = 0
            prev_fade_idx = 0
            for i in range(K):
                # UNGRAY ONE DIGIT
                if i > 0:
                    self.play(row[n - K + i].animate.set_color(WHITE))

                # CHOOSE MAX
                _, max_idx = argmax(nums[offset : n - (K - 1 - i)])
                mob_max = row[offset + max_idx]
                self.play(mob_max.animate.set_color(RED))

                # MOVE IT DOWN, NEXT TO PREVIOUS (IF ANY) AND RE-CENTER
                anims = []
                anims += [
                    (
                        mob_max.animate.scale(1.5).move_to(DOWN)
                        if i == 0
                        else mob_max.animate.scale(1.5).next_to(below_digits.submobjects[-1], 0.25 * RIGHT)
                    ),
                    FadeOut(row[prev_fade_idx : offset + max_idx]),
                ]
                prev_fade_idx = offset + max_idx + 1

                if offset + max_idx + 1 < n:
                    anims.append(row[offset + max_idx + 1 :].animate.set_x(ORIGIN[0]))
                self.play(*anims)

                below_digits.add(mob_max)
                self.play(below_digits.animate.set_x(ORIGIN[0]))
                offset += max_idx + 1

                # CHOOSE MAX AND MOVE IT
                # _, max_idx2 = argmax(nums[max_idx + 1 :])
                # max_idx2 += max_idx + 1
                # self.play(row[max_idx2].animate.set_color(RED))
                # self.play(
                #    row[max_idx2].animate.scale(1.5).next_to(row[max_idx], 0.25 * RIGHT)
                # )
                # self.play(VGroup(row[max_idx], row[max_idx2]).animate.set_x(ORIGIN[0]))

            self.play(FadeOut(*self.mobjects))
