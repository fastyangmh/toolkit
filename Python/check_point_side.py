#import


#def
def check_point_side(line_start, line_end, point):
    v = (line_end[0] - line_start[0]) * (point[1] - line_start[1]) - (
        line_end[1] - line_start[1]) * (point[0] - line_start[0])
    if v > 0:
        return 'left or up'
    elif v < 0:
        return 'right or down'
    else:
        return 'online'


if __name__ == '__main__':
    #parameters
    line_start = (-5, 3)
    line_end = (5, 3)
    point = (3, 2)

    #run
    for point in [(3, 9), (3, 7), (3, 5), (3, 3), (3, 1)]:
        print(
            point,
            check_point_side(line_start=line_start,
                             line_end=line_end,
                             point=point))
