import solid as scad

from catamaran import Catamaran

segments = 50

(hull, wall, lid) = Catamaran.hull(600, 50, 60, 1.2, segments)
lid = scad.translate([0, 0, 50]).add(lid)

(rotor_set, motor_set) = Catamaran.rotorSet(20, 15, 3.5, 7.5, 10, 2, segments)
rotor_set = scad.translate([520, 0, 2]).add(rotor_set)
motor_set = scad.translate([520, 0, 50]).add(motor_set)

motor_bush = Catamaran.bush(10, 3.3, 2, segments)
motor_bush = scad.translate([520, 0, 35]).add(motor_bush)

rudder_set = Catamaran.rudderSet(3.5, 45, 2, segments)
rudder_set = scad.translate([601.2, 0, -45]).add(rudder_set)

rudder = Catamaran.rudder(50, 80, 3.3, 15, 1.6, segments)
rudder = scad.translate([605, 0, -65]).add(rudder)

rudder_tiller = Catamaran.rudderTiller(20, 15, 3.3, 1, 2, segments)
rudder_tiller = scad.rotate([180, 0, 180]).add(rudder_tiller)
rudder_tiller = scad.translate([605, 0, 20]).add(rudder_tiller)

body = hull + wall + lid + rotor_set + motor_set + motor_bush + rudder_set + rudder + rudder_tiller

left = scad.translate([0, -180, 0]).add(body)
right = scad.mirror([0, 1, 0]).add(left)

frame = Catamaran.frame(380, 200, 250, 12, 10, 60, 30, 5.5, segments)
frame = scad.translate([35, 0, 0]).add(frame)

mast_beam = Catamaran.mastBeam(300, 5, 5, 0, 20, 5.7, 2, segments)
mast_beam = scad.rotate([0, 0, 30]).add(mast_beam)
mast_beam = scad.translate([235, 0, 70]).add(mast_beam)

jib_beam = Catamaran.jibBeam(250, 5, 5)
jib_beam = scad.translate([-90, 0, 60]).add(jib_beam)
jib_beam = scad.rotate([0, 0, 30]).add(jib_beam)
jib_beam = scad.translate([40, 0, 0]).add(jib_beam)

mast_bush = Catamaran.bush(10, 3.3, 0.85, segments)
mast_bush = scad.translate([235, 0, 300]).add(mast_bush)

all = left + right + frame + mast_beam + jib_beam + mast_bush

scad.scad_render_to_file(all, "all.scad")
