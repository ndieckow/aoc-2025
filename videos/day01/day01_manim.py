from manim import *


class Exposition(Scene):

    def make_dial(self):
        outer_circ = Circle(1, color=GREEN_B, fill_opacity=1)
        inner_circ = Circle(0.5, color=GREEN_E, fill_opacity=1)
        mobs_num = []
        mobs_ticks = []
        for num in range(0, 100):
            tick = (
                Dot(inner_circ.get_center(), radius=0.009, color=BLACK)
                .shift(0.98 * UP)
                .rotate_about_origin(-num * 2 * np.pi / 100)
            )
            mobs_ticks.append(tick)
            if num % 10 == 0:
                tex = (
                    MathTex(num, font_size=15, color=BLACK)
                    .shift(0.85 * UP)
                    .rotate_about_origin(-num * 2 * np.pi / 100)
                )
                tick.scale(2)
                mobs_num.append(tex)

        dial = VGroup(outer_circ, inner_circ, *mobs_num, *mobs_ticks)
        dial.rotate(np.pi)  # should start at 50
        dial.scale(1.2)
        return dial

    def rotate_clicks(self, dial, clicks):
        self.play(Rotate(dial, clicks / 100 * 2 * np.pi))

    def construct(self):
        input_txt = open("test.txt").read()
        lines = input_txt.splitlines()

        text_config = {
            "font": "Source Code Pro",
            "color": GRAY_B,
            "t2c": {"L": RED, "R": BLUE},
        }
        line_config = {"stroke_opacity": 0}
        rot_table = Table(
            [
                [
                    lines[i],
                    lines[5 + i],
                ]
                for i in range(5)
            ],
            element_to_mobject=Text,
            element_to_mobject_config=text_config,
            line_config=line_config,
            v_buff=0.2,
            h_buff=1.2,
            arrange_in_grid_config={"cell_alignment": LEFT}
        ).scale(0.9)
        self.play(FadeIn(rot_table))
        self.play(rot_table.animate.scale(0.56).shift(2.7 * UP))

        """
        mob_lines1 = Text(
            "\n".join(lines[:5]),
            font="Source Code Pro",
            color=GRAY_B,
            t2c={"L": RED, "R": BLUE},
        )
        mob_lines2 = Text(
            "\n".join(lines[5:]),
            font="Source Code Pro",
            color=GRAY_B,
            t2c={"L": RED, "R": BLUE},
        ).next_to(mob_lines1, 4 * RIGHT)
        mobs_lines = VGroup(mob_lines1, mob_lines2).center()
        self.play(FadeIn(mobs_lines))
        self.play(mobs_lines.animate.scale(0.5).shift(2.7 * UP))
        """

        dial = self.make_dial()
        triangle = (
            Triangle(color=RED, fill_opacity=1)
            .rotate(np.pi)
            .scale(0.1)
            .next_to(dial, 0.5 * UP)
        )
        safe = VGroup(triangle, dial)

        self.play(
            FadeIn(safe)
        )

        self.wait(0.5)
        self.rotate_clicks(dial, -50)
        self.wait(0.5)
        self.rotate_clicks(dial, -1)
        self.wait(0.5)
        self.rotate_clicks(dial, 51)
        self.wait(0.5)

        zero_count = 0
        mob_counter = MathTex(0, color=GREEN).scale(1.5).shift(2.2 * DOWN)
        self.play(Create(mob_counter))
        # mob_counter.add_updater(lambda x: x.become(MathTex(zero_count, color=GREEN).shift(DOWN)))

        rect_config = {"color": WHITE, "fill_opacity": 0.2, "stroke_opacity": 0, "corner_radius": 0.1}
        table_entries = rot_table.get_entries()
        dial_num = 50
        for i,line in enumerate(lines):
            if i == 0:
                rect = SurroundingRectangle(table_entries[(i % 5) * 2 + i // 5], z_index=-10, **rect_config)
                self.play(FadeIn(rect), run_time=0.5)
            else:
                self.play(Transform(rect, SurroundingRectangle(table_entries[(i % 5) * 2 + i // 5], z_index=-10, **rect_config)), run_time=0.5)
            d, amt = line[0], int(line[1:])
            if d == "L":
                amt *= -1
            dial_num = (dial_num + amt) % 100
            self.rotate_clicks(dial, amt)
            if dial_num == 0:
                zero_count += 1
                # mob_counter.update()
                self.play(
                    Transform(
                        mob_counter,
                        MathTex(zero_count, color=GREEN)
                        .scale(1.5)
                        .move_to(mob_counter),
                    ),
                    run_time=0.5,
                )
        self.wait(0.5)
        self.next_section("Part 2")

        # PART 2
        # RESET
        self.remove(rect)
        self.remove(dial)
        self.remove(mob_counter)
        zero_count = 0
        dial_num = 50
        dial = self.make_dial()
        self.add(dial)

        mob_counter = MathTex(0, color=GREEN).scale(1.5).shift(2.2 * DOWN)
        self.add(mob_counter)

        # Some trackers
        angle_tracker = ValueTracker(0)
        previous_angle_tracker = ValueTracker(0)
        dial_pos_tracker = ValueTracker(50)
        prev_pos_tracker = ValueTracker(50)
        zero_crossing_tracker = ValueTracker(0)
        flag = ValueTracker(0)
        flag2 = ValueTracker(0)

        def update_dial_pos(mobject):
            # Calculate dial pos based on angle
            current_signed_angle = (angle_tracker.get_value() + PI) % (2*PI)
            total_turn_frac = current_signed_angle / (2 * PI)
            dial_num = round(total_turn_frac * 100) % 100
            #if abs(dial_num) < 1e-6:
            #    dial_num = 0.0
            mobject.set_value(dial_num)

        def update_zero_crossing(mobject):
            current_pos = dial_pos_tracker.get_value()
            prev_pos = prev_pos_tracker.get_value()
            current_count = zero_crossing_tracker.get_value()

            crossed_cw = prev_pos > 97 and current_pos < 3
            crossed_ccw = prev_pos < 3 and current_pos > 97
            #landed_on_boundary = (abs(current_pos - 100) < 1e-6 or abs(current_pos) < 1e-6)
            landed_on_boundary = (current_pos == prev_pos == 0)

            if 3 < current_pos < 97:
                flag.set_value(0)
                flag2.set_value(0)

            # increasing angle (CW)
            #print(prev_pos, current_pos, current_angle, previous_angle)
            if flag.get_value() == 0 and (crossed_ccw or crossed_cw):
                current_count += 1
                flag.set_value(1)
            
            if flag.get_value() == 0 and flag2.get_value() == 0 and landed_on_boundary:
                current_count += 1
                flag.set_value(1)
                flag2.set_value(1)

            #total_turns = angle_tracker.get_value() / (2*PI)
            #full_cycles = int(abs(total_turns - 0.5))
            mobject.set_value(current_count)
            prev_pos_tracker.set_value(current_pos)

        dial_pos_tracker.add_updater(update_dial_pos)
        zero_crossing_tracker.add_updater(update_zero_crossing)

        def update_pointer_rotation(mobject):
            current_target_angle = angle_tracker.get_value()
            previous_angle = previous_angle_tracker.get_value()
            
            # 1. Calculate the rotation delta
            delta_angle = current_target_angle - previous_angle
            
            # 2. Apply the delta rotation to the mobject
            mobject.rotate(delta_angle, about_point=mobject.get_center())
            
            # 3. Update the auxiliary tracker for the next frame's calculation
            previous_angle_tracker.set_value(current_target_angle)

        dial.add_updater(update_pointer_rotation)
        mob_counter.add_updater(lambda m: m.become(
            MathTex(
                str(int(zero_crossing_tracker.get_value())), 
                color=GREEN
            ).scale(1.5).move_to(m)
        ))

        self.add(angle_tracker, previous_angle_tracker, zero_crossing_tracker, dial_pos_tracker, prev_pos_tracker)

        for i,line in enumerate(lines):
            d, amt = line[0], int(line[1:])

            if i == 0:
                rect = SurroundingRectangle(table_entries[(i % 5) * 2 + i // 5], z_index=-10, **rect_config)
                self.play(FadeIn(rect), run_time=0.5)
            else:
                self.play(Transform(rect, SurroundingRectangle(table_entries[(i % 5) * 2 + i // 5], z_index=-10, **rect_config)), run_time=0.5)

            if d == "L":
                angle_change = -(amt / 100) * 2 * PI
            else:
                angle_change = (amt / 100) * 2 * PI
            
            #flag.set_value(0)

            self.play(angle_tracker.animate.increment_value(angle_change))

            dial_num = (dial_num + amt) % 100
            #if dial_num == 0:
            #    zero_crossing_tracker.increment_value(1)