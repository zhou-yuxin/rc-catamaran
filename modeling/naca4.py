import math

def naca4(digits, segments, half_cosine_spacing = True, finite_trailing_edge = False):
    m = float(digits[0]) / 100
    p = float(digits[1]) / 10
    t = float(digits[2:]) / 100
    linespace = lambda a, b, n: (a + (b - a) * i / (n - 1) for i in range(n))
    if half_cosine_spacing:
        x = [0.5 * (1 - math.cos(i)) for i in linespace(0, math.pi, segments + 1)]
    else:
        x = list(linespace(0, 1, segments + 1))
    (a0, a1, a2, a3) = (+0.2969, -0.1260, -0.3516, +0.2843)
    a4 = -0.1015 if finite_trailing_edge else -0.1036
    yt = [5 * t * (a0 * math.sqrt(i) + a1 * i + a2 * math.pow(i, 2) + a3 * math.pow(i, 3)   \
        + a4 * math.pow(i, 4)) for i in x]
    if p == 0:
        (xu, xl) = (x, x)
        yu = yt
        yl = [-i for i in yt]
    else:
        xc1 = [i for i in x if i <= p]
        xc2 = [i for i in x if i > p]
        yc1 = [m / math.pow(p, 2) * i * (2 * p - i) for i in xc1]
        yc2 = [m / math.pow(1 - p, 2) * (1 - 2 * p + i) * (1 - i) for i in xc2]
        zc = yc1 + yc2
        dyc1_dx = [m / math.pow(p, 2) * (2 * p - 2 * i) for i in xc1]
        dyc2_dx = [m / math.pow(1 - p, 2) * (2 * p - 2 * i) for i in xc2]
        dyc_dx = dyc1_dx + dyc2_dx
        theta = [math.atan(i) for i in dyc_dx]
        xu = [i - j * math.sin(k) for (i, j, k) in zip(x, yt, theta)]
        yu = [i + j * math.cos(k) for (i, j, k) in zip(zc, yt, theta)]
        xl = [i + j * math.sin(k) for (i, j, k) in zip(x, yt, theta)]
        yl = [i - j * math.cos(k) for (i, j, k) in zip(zc, yt, theta)]
    x = xu[::-1] + xl[1:]
    y = yu[::-1] + yl[1:]
    return (x, y)
