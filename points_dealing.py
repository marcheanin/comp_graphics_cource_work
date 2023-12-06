import math


def find_closest_point(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    # cos_theta = (r1 ** 2 + distance ** 2 - r2 ** 2) / (2 * r1 * distance)
    # sin_theta = math.sqrt(1 - cos_theta ** 2)
    # closest_point1_x = x1 + r1 * (x2 - x1) / distance * cos_theta - r1 * (y2 - y1) / distance * sin_theta
    # closest_point1_y = y1 + r1 * (x2 - x1) / distance * sin_theta + r1 * (y2 - y1) / distance * cos_theta
    # closest_point2_x = x1 + r1 * (x2 - x1) / distance * cos_theta + r1 * (y2 - y1) / distance * sin_theta
    # closest_point2_y = y1 - r1 * (x2 - x1) / distance * sin_theta + r1 * (y2 - y1) / distance * cos_theta

    proportion1 = r1 / distance
    closest_point1_x = x2 + (x1 - x2) * proportion1
    closest_point1_y = y2 + (y1 - y2) * proportion1

    proportion2 = r2 / distance
    closest_point2_x = x1 + (x2 - x1) * proportion2
    closest_point2_y = y1 + (y2 - y1) * proportion2

    return round((closest_point1_x + closest_point2_x) / 2, 2), round((closest_point1_y + closest_point2_y) / 2, 2)


def find_closest_point2(x1, y1, r1, x2, y2, r2):
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    angle = math.atan2(y2 - y1, x2 - x1)

    x_res_1 = x1 + r1 * math.cos(angle)
    y_res_1 = y1 + r1 * math.sin(angle)

    angle2 = math.atan2(y1 - y2, x1 - x2)

    x_res_2 = x2 + r2 * math.cos(angle2)
    y_res_2 = y2 + r2 * math.sin(angle2)

    return round((x_res_1 + x_res_2) / 2, 2), round((y_res_1 + y_res_2) / 2, 2)


def get_intersections(x0, y0, r0, x1, y1, r1):
    # circle 1: (x0, y0), radius r0
    # circle 2: (x1, y1), radius r1

    d = math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

    # non intersecting
    if d > r0 + r1:
        return ()
    # One circle within other
    if d < abs(r0 - r1):
        return ()
    # coincident circles
    if d == 0 and r0 == r1:
        return ()
    else:
        a = (r0 ** 2 - r1 ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(r0 ** 2 - a ** 2)
        x2 = x0 + a * (x1 - x0) / d
        y2 = y0 + a * (y1 - y0) / d
        x3 = x2 + h * (y1 - y0) / d
        y3 = y2 - h * (x1 - x0) / d

        x4 = x2 - h * (y1 - y0) / d
        y4 = y2 + h * (x1 - x0) / d

        return (round(x3, 2), round(y3, 2)), (round(x4, 2), round(y4, 2))


def count_dist(p1, p2):
    # return math.hypot(p1[0] - p2[0], p1[1] - p2[1])
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_three_nearest_points(points: list):
    dist = 999999
    res_points = (points[0], points[1], points[2])
    for p1 in points:
        for p2 in points:
            for p3 in points:
                if p1 != p2 and p1 != p3 and p2 != p3:
                    dist1 = count_dist(p1, p2)
                    dist2 = count_dist(p1, p3)
                    dist3 = count_dist(p2, p3)
                    if dist1 + dist2 + dist3 < dist:
                        dist = dist1 + dist2 + dist3
                        res_points = (p1, p2, p3)
    return res_points


def get_trig_center(points):
    x, y = (points[0][0] + points[1][0] + points[2][0]) / 3, (points[0][1] + points[1][1] + points[2][1]) / 3
    error = (count_dist((x, y), points[0]) + count_dist((x, y), points[1]) + count_dist((x, y), points[2])) / 3
    return round((points[0][0] + points[1][0] + points[2][0]) / 3, 2), round((points[0][1] + points[1][1] + points[2][1]) / 3, 2), error


def count_point_from_3_dists(x1, y1, d1, x2, y2, d2, x3, y3, d3):
    intersections1 = get_intersections(x1, y1, d1, x2, y2, d2)
    intersections2 = get_intersections(x1, y1, d1, x3, y3, d3)
    intersections3 = get_intersections(x2, y2, d2, x3, y3, d3)

    #print(intersections1, intersections2, intersections3, sep='\n')
    #print()

    if intersections1 == ():
        intersections1 = (find_closest_point2(x1, y1, d1, x2, y2, d2),)

    if intersections2 == ():
        intersections2 = (find_closest_point2(x1, y1, d1, x3, y3, d3),)

    if intersections3 == ():
        intersections3 = (find_closest_point2(x2, y2, d2, x3, y3, d3),)

    #print(intersections1, intersections2, intersections3, sep='\n')

    points = list(intersections1) + list(intersections2) + list(intersections3)

    #print(points, len(points))
    if len(points) < 3:
        res = get_trig_center([(x1, y1), (x2, y2), (x3, y3)])
        return res

    near_points = get_three_nearest_points(points)
    #print(near_points)
    return get_trig_center(near_points)


#print(count_point_from_3_dists(1, 2, math.sqrt(1), 4, 6, math.sqrt(1), 1, 6, math.sqrt(1)))
