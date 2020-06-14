"""
Project Euler 102
Ethan Wright
"""


class Coordinate(object):

    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)

    def __repr__(self):
        return "({}, {})".format(self.x, self.y)

class Triangle(object):

    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def does_triangle_contain_origin(self):
        ai = AxisIntersections()

        # TODO Line Class?
        # for line in self.lines:
        #    ai.apply_line(line)

        # Compare every permutation of coordinates, or each line
        ai.apply_line(self.A, self.B)
        ai.apply_line(self.A, self.C)
        ai.apply_line(self.B, self.C)

        return ai.contains_origin()

    def __repr__(self):
        return "{}, {}, {}".format(self.A, self.B, self.C)

class AxisIntersections(object):

    RIGHT_OF_AXIS = 'right'
    LEFT_OF_AXIS = 'left'
    ABOVE_AXIS = 'above'
    BELOW_AXIS = 'below'

    def __init__(self):
        self.above = 0
        self.below = 0
        self.left = 0
        self.right = 0

    def apply_line(self, coordinate1, coordinate2):
        """
        # If the x axis changes from - to +, then it crossed the x axis. Same for y axis.
        # If it crosses both, then I need to do more work to determine if the intersection was above or below
        """
        print("Checking Line: {}, {}".format(coordinate1, coordinate2))
        y_switched_signs = False
        x_switched_signs = False

        if (coordinate1.y < 0 and coordinate2.y > 0) or (coordinate1.y > 0 and coordinate2.y < 0) or (coordinate1.y == 0 or coordinate2.y == 0):
            if coordinate1.y != 0 and coordinate2.y != 0:
                y_switched_signs = True

            if coordinate1.x <= 0 and coordinate2.x <= 0:
                self.increment_found_intersection(self.LEFT_OF_AXIS)

            elif coordinate1.x >= 0 and coordinate2.x >= 0:
                self.increment_found_intersection(self.RIGHT_OF_AXIS)

        if (coordinate1.x < 0 and coordinate2.x > 0) or (coordinate1.x > 0 and coordinate2.x < 0) or (coordinate1.x == 0 or coordinate2.x == 0):
            if coordinate1.x != 0 and coordinate2.x != 0:
                x_switched_signs = True

            if coordinate1.y <= 0 and coordinate2.y <= 0:
                self.increment_found_intersection(self.BELOW_AXIS)

            elif coordinate1.y >= 0 and coordinate2.y >= 0:
                self.increment_found_intersection(self.ABOVE_AXIS)

        if x_switched_signs and y_switched_signs:
            print("Both x and y changed signs. Calculating line equations")
            self.calculate_double_intersection(coordinate1, coordinate2)

    def calculate_double_intersection(self, coordinate1, coordinate2):
        """
        Find formula for each line via rise over run, then find where they cross the axes.
        """
        rise = coordinate2.y - coordinate1.y
        run = coordinate2.x - coordinate1.x
        slope = float(rise) / float(run)
        print("Slope: {}".format(slope))

        # Find where they cross the axes
        # y = slope * x + b
        # b = y - (slope * x)
        # Plug in one of the coordinates and find b

        offset1 = float(coordinate1.y) - (slope * float(coordinate1.x))
        offset2 = float(coordinate2.y) - (slope * float(coordinate2.x))
        #print("Offset 1: {} Offset 2: {}".format(offset1, offset2))
        print("{} = {} * {} + {}".format(coordinate1.y, slope,  coordinate1.x, offset1))
        print("{} = {} * {} + {}".format(coordinate2.y, slope,  coordinate2.x, offset2))
        offset = offset1

        # x_intersection -> 0 = slope * x + b -> x = -b / slope
        # y_intersection -> y = slope * 0 + b -> b

        x_intersection = -1.0 * (offset / slope)
        y_intersection = offset

        if x_intersection > 0:
            self.increment_found_intersection(self.RIGHT_OF_AXIS)
        elif x_intersection < 0:
            self.increment_found_intersection(self.LEFT_OF_AXIS)

        if y_intersection > 0:
            self.increment_found_intersection(self.ABOVE_AXIS)
        elif y_intersection < 0:
            self.increment_found_intersection(self.BELOW_AXIS)

        if x_intersection == 0 or y_intersection == 0:
            exit("TODO Should going through the origin count as an auto Contains the Origin?")

    def contains_origin(self):
        """
        There should be one intersection above, below, to the right, and to the left of the origin.
        """
        print("Axis Breakdown: Above: {}, Below: {}, Left: {}, Right: {}".format(self.above, self.below, self.left, self.right))
        return self.above == 1 and self.below == 1 and self.left == 1 and self.right == 1

    def increment_found_intersection(self, direction):
        print("Incrementing Axis {}".format(direction))
        if direction == self.ABOVE_AXIS:
            self.above += 1
        elif direction == self.BELOW_AXIS:
            self.below += 1
        elif direction == self.LEFT_OF_AXIS:
            self.left += 1
        elif direction == self.RIGHT_OF_AXIS:
            self.right += 1

class PuzzleSolver(object):

    def run(self):
        total = 0
        contains_origin = 0
        file_name = 'data/project_euler_102_data.txt'

        with open(file_name) as triangle_file:
            line = triangle_file.readline().rstrip()
            while line:

                data = line.split(',')
                #print(data)
                coordinate1 = Coordinate(data[0], data[1])
                coordinate2 = Coordinate(data[2], data[3])
                coordinate3 = Coordinate(data[4], data[5])
                triangle = Triangle(coordinate1, coordinate2, coordinate3)
                print("Checking Triangle {}".format(triangle))
                result = triangle.does_triangle_contain_origin()

                if result:
                    contains_origin += 1
                    print("I contain the Origin")
                else:
                    print("I DO NOT contain the Origin")
                total += 1

                line = triangle_file.readline().rstrip()
                print('-' * 50)

        print("{} Total Triangles, {} contain the origin".format(total, contains_origin))
        return contains_origin


if __name__ == "__main__":
    puzzle = PuzzleSolver()
    puzzle.run()
