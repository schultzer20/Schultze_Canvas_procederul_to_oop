import math


class Canvas(list[str, ...]):
    def __init__(self, width, height):  # Canvas itself with 2 parameters
        self.width = width
        self.height = height
        super().__init__([" " * self.width for _ in range(self.height)])

    def create_row_headers(self, length):
        return "".join([str(i % 10) for i in range(length)])

    def print(self):  # canvas: list[str, ...]):  # Print the canvas to see the result
        header = " " + self.create_row_headers(len(self[0]))
        print(header)
        for idx, row in enumerate(self):
            print(idx % 10, row, idx % 10, sep="")
        print(header)

    def replace_at_index(self, s: str, r: str, idx: int):
        return s[:idx] + r + s[idx + len(r):]

    def draw_line_segment(self, start: tuple[int, int], end: tuple[int, int], line_char: str = "*"):
        x1, y1 = start
        x2, y2 = end

        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        error = dx - dy

        while x1 != x2 or y1 != y2:
            self[y1] = self.replace_at_index(self[y1], line_char, x1)

            double_error = error * 2
            if double_error > -dy:
                error -= dy
                x1 += sx

            if double_error < dx:
                error += dx
                y1 += sy

        self[y2] = self.replace_at_index(self[y2], line_char, x2)

    def draw_polygon(self, *points: tuple[int, int], closed: bool = True, line_char: str = "*"):
        # Determine the start and end points of the open polygon
        start_points = points[:-1]
        end_points = points[1:]
        # If closed, add the start and end points of the line segment that connects the last and the first point
        if closed:
            start_points += (points[-1],)
            end_points += (points[0],)

        # Draw each segment in turn. zip is used to build tuples each consisting of a start and an end point
        for start_point, end_point in zip(start_points, end_points):
            self.draw_line_segment(start_point, end_point, line_char)

    def draw_line(self, start: tuple[int, int], end: tuple[int, int], line_char: str = "*"):
        canvas.draw_polygon(start, end, closed=False, line_char=line_char)

    def draw_rectangle(self, upper_left: tuple[int, int], lower_right: tuple[int, int], line_char: str = "*"):
        x1, y1 = upper_left
        x2, y2 = lower_right

        self.draw_polygon(upper_left, (x2, y1), lower_right, (x1, y2), line_char=line_char)

    def draw_n_gon(self, center: tuple[int, int], radius: int, number_of_points: int, rotation: int = 0, line_char="*"):
        angles = range(rotation, 360 + rotation, 360 // number_of_points)
        points = []
        for angle in angles:
            # Convert the angle of the point to radians
            angle_in_radians = math.radians(angle)
            # Calculate the x and y positions of the point
            x = center[0] + radius * math.cos(angle_in_radians)
            y = center[1] + radius * math.sin(angle_in_radians)
            # Add the point to the list of points as a tuple
            points.append((round(x), round(y)))

        # Use the draw_polygon function to draw all the lines of the n-gon
        self.draw_polygon(*points, line_char=line_char)


canvas = Canvas(100, 40)
canvas.draw_polygon((7, 12), (24, 29), (42, 15), (37, 32), (15, 35))
canvas.draw_line((10, 4), (92, 19), "+")
canvas.draw_rectangle((45, 2), (80, 27), line_char='#')
canvas.draw_n_gon((72, 25), 12, 20, 80, "-")
canvas.print()


class Point:
    def __init__(self, x_coordinate: float, y_coordinate: float):
        self.x_coordinate = str(x_coordinate)
        # create a Point class that can represent itself, i.e., it can format itself as a string. --> so I cast it
        self.y_coordinate = str(y_coordinate)

    def __repr__(self):
        return f"({self.x_coordinate}/{self.y_coordinate})"

    def __str__(self):  # is called whenever we want a representation
        return self.__repr__()

    def __getitem__(self, item):
        return item

    def distance_from_origin(self) -> float:
        distance = math.sqrt(float(self.x_coordinate)**2 + float(self.y_coordinate)**2)
        return distance


p1 = Point(2.3, 43.14)
p2 = Point(5.53, 2.5)
p3 = Point(12.2, 28.7)
print(p1)
print(p1, p2, p3)  # This calls __str__() --> as defined there
print([p1, p2, p3])  # This calls __repr__() --> print as a list


class Shape(list[Point, ...]):  # child class of list class --> Shape is a list of Points
    def __init__(self, *points):
        super().__init__(points)
        self.points = [point if isinstance(point, Point) else Point(*point) for point in points]
        # self.points = Point(x, y) for x, y in points  # --> TypeError cannot unpack non-iterable Point object

    def __repr__(self):
        return f"({super().__repr__()})"  # self.points

    def __str__(self):
        return f"({super().__str__()})"

    def centroid(self) -> Point:
        x_coordinate = [float(p.x_coordinate) for p in self]
        #  bc we cast it as a string before
        #  I cast it as a float and not an integer in case it has decimals
        y_coordinate = [float(p.y_coordinate) for p in self]
        amount = len(self)
        centroid_x = sum(x_coordinate)/amount
        centroid_y = sum(y_coordinate)/amount
        return Point(centroid_x, centroid_y)

    def __eq__(self, other):
        return self.centroid().distance_from_origin() == other.centroid().distance_from_origin()
        # if isinstance(other, Shape):
            # if self.centroid() == other.centroid():
                # return True #self.centroid == other.centroid  #and self.centroid_y == other.centroid_y

    def __lt__(self, other):
        distance_1 = self.centroid().distance_from_origin()
        distance_2 = other.centroid().distance_from_origin()
        return distance_1 < distance_2


s1 = Shape(p1, p2, p3)
s2 = Shape(p2)
s3 = Shape()
print(f"Shape of s1: {s1}")
print(f"Shape of s2: {s2}")
print(f"Shape of s3: {s3}")

s1 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
s2 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))
s3 = Shape(Point(0.25, 0.25), Point(0.25, 0.75), Point(0.75, 0.75), Point(0.75, 0.25))
print(f"Centroid of s1: {s1.centroid()}")
print(f"Centroid of s2: {s2.centroid()}")
print(f"Centroid of s3: {s3.centroid()}")

p4 = Point(1, 1)
p5 = Point(5, 5)
p6 = Point(10, 10)

print(p4.distance_from_origin())
print(p5.distance_from_origin())
print(p6.distance_from_origin())

s1 = Shape(Point(0, 0), Point(0, 1), Point(1, 1), Point(1, 0))
s2 = Shape(Point(0, 0.5), Point(0.5, 1), Point(1, 0.5), Point(0.5, 0))
print(s1 == s2)  # Equal because the two have the same centroid

s2 = Shape(Point(5, 5), Point(5, 6), Point(6, 6), Point(6, 5))
print(s1 < s2)  # s1 is smaller than s2 because its centroid is closer to the origin

s3 = Shape(Point(10, 10), Point(10, 11), Point(11, 11), Point(11, 10))
shapes = [s3, s1, s2]
print(shapes)
print(sorted(shapes))  # sorted by their distance from the origin
