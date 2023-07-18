import math
import solid as scad

import naca4

class Catamaran:

    @classmethod
    def hullSlice(cls, width, height, bottom_height, segments = 20):
        base_height = height - bottom_height
        base = scad.translate([-width / 2, 0]).add(scad.square([width, base_height]))
        bottom = scad.resize([width, bottom_height]).add(scad.circle(segments = 2 * segments))
        bottom = scad.translate([0, base_height]).add(bottom)
        return base + bottom
    
    @classmethod
    def hullSolid(cls, length, width, height, segments = 20):
        hull = scad.hull()
        for i in range(1, segments + 1):
            r = i / segments
            if r < 0.382:
                k = math.sin(r / 0.382 * math.pi / 2)
            elif r < 0.618:
                k = 1
            else:
                k = math.sin(((1 - r) / 0.382 + 1) * math.pi / 4)
            (uh, bh) = (0.4 + 0.218 * k, 0.382 * k)
            slice = cls.hullSlice(k, uh + bh, bh, segments)
            if i == 1:
                slice = scad.linear_extrude(height = 1, scale = [0, 1]).add(slice)
                slice = scad.mirror([0, 0, 1]).add(slice)
                slice = scad.translate([0, 0, 1]).add(slice)
            else:
                slice = scad.linear_extrude(height = 0.001).add(slice)
                slice = scad.translate([0, 0, i]).add(slice)
            hull.add(slice)
        hull = scad.resize([width, height, length]).add(hull)
        hull = scad.rotate([-90,0, -90]).add(hull)
        return hull

    @classmethod
    def hull(cls, length, width, height, thickness, segments = 20):
        hull_solid = cls.hullSolid(length, width, height, segments)
        hull = scad.minkowski().add(hull_solid).add(
            scad.sphere(r = thickness, segments = segments))
        servo = scad.cube([24, 12.5, thickness * 2 + 1], center = True)
        servo1 = scad.translate([length * 0.3, 0, 0]).add(servo)
        servo2 = scad.translate([length - 30, 0, 0]).add(servo)
        (door_l, door_w) = (length * 0.3, width * 0.6)
        door_pos = length * 0.6
        door_diff = scad.cube([door_l, door_w, thickness * 2 + 1], center = True)
        door_diff = scad.translate([door_pos, 0, 0]).add(door_diff)
        hull = hull - hull_solid - servo1 - servo2 - door_diff
        wall_height = 10
        wall = scad.square([door_l, door_w], center = True)
        wall = scad.offset(r = thickness, segments = segments).add(wall) - wall
        wall = scad.linear_extrude(height = wall_height).add(wall)
        wall = scad.translate([door_pos, 0, 0]).add(wall)
        lid_diff = scad.square([door_l + 2 * thickness + 1, door_w + 2 * thickness + 1],
            center = True)
        lid = scad.offset(r = thickness, segments = segments).add(lid_diff)
        lid_diff = scad.linear_extrude(height = wall_height).add(lid_diff)
        lid = scad.linear_extrude(height = wall_height + thickness).add(lid)
        lid -= lid_diff
        lid = scad.translate([door_pos, 0, 0]).add(lid)
        return (hull, wall, lid)

    @classmethod
    def rotorSet(cls, size, height, shaft_diameter, motor_diameter, motor_length, thickness,
        segments = 20):
        rotor_set = scad.cylinder(d1 = size, d2 = shaft_diameter + thickness * 2, h = height,
            segments = segments)
        shaft_diff = scad.cylinder(d = shaft_diameter, h = height + 1, segments = segments)
        rotor_set -= shaft_diff
        motor_set = scad.cylinder(d = motor_diameter + 2 * thickness, h = motor_length,
            center = True, segments = segments)
        motor_set = scad.rotate([0, 90, 0]).add(motor_set)
        motor_set = scad.translate([0, 0, height]).add(motor_set)
        motor_diff = scad.cylinder(d = motor_diameter, h = motor_length + 1,
            center = True, segments = segments)
        motor_diff = scad.rotate([0, 90, 0]).add(motor_diff)
        motor_diff = scad.translate([0, 0, height]).add(motor_diff)
        shaft_set = scad.cylinder(d = shaft_diameter + 2 * thickness, h = height,
            segments = segments)
        shaft_diff = scad.cylinder(d = shaft_diameter, h = height, segments = segments)
        motor_set = motor_set + shaft_set - motor_diff - shaft_diff
        return (rotor_set, motor_set)

    @classmethod
    def rudder(cls, length, height, shaft_diameter, bush_height, bush_thickness, segments = 20):
        airfoil = scad.polygon(zip(*naca4.naca4("0014", segments = segments)))
        airfoil = scad.translate([-0.4, 0]).add(airfoil)
        airfoil = scad.resize([length, 0], auto = True).add(airfoil)
        rudder = scad.linear_extrude(height = height, scale = 0.618).add(airfoil)
        rudder = scad.mirror([0, 0, 1]).add(rudder)
        bush = scad.cylinder(d = shaft_diameter + 2 * bush_thickness, h = bush_height,
            segments = segments)
        shaft_diff = scad.cylinder(d = shaft_diameter, h = height / 3 + 1, segments = segments)
        shaft_diff = scad.translate([0, 0, bush_height - height / 3]).add(shaft_diff)
        rudder = rudder + bush - shaft_diff
        return rudder

    @classmethod
    def rudderTiller(cls, length, height, shaft_diameter, srew_diameter, thickness, segments = 20):
        shaft = scad.circle(d = shaft_diameter + 2 * thickness, segments = segments)
        srew = scad.circle(d = srew_diameter + 2 * thickness, segments = segments)
        srew = scad.translate([0, length]).add(srew)
        srew_diff = scad.circle(d = srew_diameter, segments = segments)
        srew_diff = scad.translate([0, length]).add(srew_diff)
        tiller = scad.hull().add(shaft).add(srew) - srew_diff
        tiller = scad.linear_extrude(height = thickness).add(tiller)
        shaft_set = scad.cylinder(d = shaft_diameter + 2 * thickness, h = height,
            segments = segments)
        shaft_diff = scad.cylinder(d = shaft_diameter, h = height, segments = segments)
        tiller = tiller + shaft_set - shaft_diff
        return tiller

    @classmethod
    def rudderSet(cls, diameter, height, thickness, segments = 20):
        r = diameter / 2 + thickness
        circle = scad.circle(r = r, segments = segments)
        circle = scad.translate([r, 0]).add(circle)
        line = scad.square([0.001,  2 * r])
        line = scad.translate([0, -r]).add(line)
        diff = scad.circle(r = diameter / 2, segments = segments)
        diff = scad.translate([r, 0]).add(diff)
        slice = scad.hull().add(circle).add(line) - diff
        rudder_set = scad.linear_extrude(height = height).add(slice)
        return rudder_set

    @classmethod
    def bush(cls, height, diameter, thickness, segments = 20):
        bush = scad.cylinder(d = diameter + 2 * thickness, h = height, segments = segments)
        diff = scad.cylinder(d = diameter, h = height, segments = segments)
        bush -= diff
        return bush

    @classmethod
    def frame(cls, width, jib_length, sail_length, thickness_h, thickness_v,
        mast_set_size, mast_set_height, mast_diameter, segments = 20):
        total_len = jib_length + sail_length
        bar = scad.square([thickness_h, width], center = True)
        end = scad.circle(d = thickness_h, segments = segments)
        end1 = scad.translate([0, -width / 2]).add(end)
        end2 = scad.translate([0, width / 2]).add(end)
        beam_h = end1 + bar + end2
        beam_h1 = scad.translate([jib_length, 0]).add(beam_h)
        beam_h2 = scad.translate([total_len, 0]).add(beam_h)
        bar = scad.square([total_len, thickness_h])
        bar = scad.translate([0, -thickness_h / 2]).add(bar)
        beam_v = bar + end
        beams = beam_h1 + beam_h2 + beam_v
        beams = scad.linear_extrude(height = thickness_v).add(beams)
        bar = scad.square([thickness_h, mast_set_size], center = True)
        foot_h = scad.linear_extrude(height = mast_set_height,
            scale = [1, thickness_h / mast_set_size]).add(bar)
        foot_v = scad.rotate([0, 0, 90]).add(foot_h)
        mast_diff = scad.cylinder(d = mast_diameter, h = mast_set_height + 1, segments = segments)
        mast_set = foot_h + foot_v - mast_diff
        mast_set = scad.translate([jib_length, 0, thickness_v]).add(mast_set)
        return beams + mast_set

    @classmethod
    def mastBeam(cls, length, width, height, angle, set_height, mast_diameter, thickness,
        segments = 20):
        beam = scad.cube([length, width, height])
        beam = scad.translate([0, -width / 2, 0]).add(beam)
        end = scad.cylinder(d = width, h = height, segments = segments)
        end = scad.translate([length, 0, 0]).add(end)
        beam += end
        beam = scad.rotate([0, angle, 0]).add(beam)
        beam = scad.translate([0, 0,
            (mast_diameter / 2 + thickness) * math.tan(math.radians(angle))]).add(beam)
        set = scad.cylinder(d = mast_diameter + 2 * thickness, h = set_height, segments = segments)
        diff = scad.cylinder(d = mast_diameter, h = set_height + 2, segments = segments)
        diff = scad.translate([0, 0, -1]).add(diff)
        beam = beam + set - diff
        beam = scad.mirror([0, 0, 1]).add(beam)
        return beam
    
    @classmethod
    def jibBeam(cls, length, width, height, segments = 20):
        beam = scad.cube([length, width, height])
        beam = scad.translate([0, -width / 2, 0]).add(beam)
        end1 = scad.cylinder(d = width, h = height, segments = segments)
        end2 = scad.translate([length, 0, 0]).add(end1)
        beam += end1 + end2
        return beam
