from typing import NamedTuple

class Point2D(NamedTuple):
    x: float
    y: float

class Line2D:
    def __init__(self, p1: Point2D, p2: Point2D) -> None:
        self.p1 = p1
        self.p2 = p2

class Point3D(NamedTuple):
    x: float
    y: float
    z: float

class Line3D:
    def __init__(self, p1: Point3D, p2: Point3D) -> None:
        self.p1 = p1
        self.p2 = p2


from typing import NamedTuple, Optional

class Point2D(NamedTuple):
    x: float
    y: float

class Line2D:
    def __init__(self, p1: Point2D, p2: Point2D) -> None:
        self.p1 = p1
        self.p2 = p2

def intersect_lines(line1: Line2D, line2: Line2D) -> Optional[Point2D]:
    # Calculating the slopes and intercepts of the lines
    dx1 = line1.p2.x - line1.p1.x
    dy1 = line1.p2.y - line1.p1.y
    dx2 = line2.p2.x - line2.p1.x
    dy2 = line2.p2.y - line2.p1.y

    # Prevent division by zero for vertical lines
    if dx1 == 0 and dx2 == 0:
        return None  # Lines are parallel and vertical

    if dx1 == 0:  # Line1 is vertical
        # Calculate x from line1 and y using line2's equation
        x = line1.p1.x
        m2 = dy2 / dx2
        c2 = line2.p1.y - m2 * line2.p1.x
        y = m2 * x + c2
        return Point2D(x, y)

    if dx2 == 0:  # Line2 is vertical
        # Calculate x from line2 and y using line1's equation
        x = line2.p1.x
        m1 = dy1 / dx1
        c1 = line1.p1.y - m1 * line1.p1.x
        y = m1 * x + c1
        return Point2D(x, y)

    # Calculate slopes
    m1 = dy1 / dx1
    m2 = dy2 / dx2

    # If slopes are equal, lines are parallel
    if m1 == m2:
        return None

    # Calculate intercepts
    c1 = line1.p1.y - m1 * line1.p1.x
    c2 = line2.p1.y - m2 * line2.p1.x

    # Calculate intersection point
    x = (c2 - c1) / (m1 - m2)
    y = m1 * x + c1

    return Point2D(x, y)




def _test_intersect_lines():
    # Test for intersecting lines
    line1 = Line2D(Point2D(0, 0), Point2D(1, 1))
    line2 = Line2D(Point2D(0, 1), Point2D(1, 0))
    assert intersect_lines(line1, line2) == Point2D(0.5, 0.5), "Test failed for intersecting lines"

    # Test for parallel lines
    line1 = Line2D(Point2D(0, 0), Point2D(1, 1))
    line2 = Line2D(Point2D(0, 1), Point2D(1, 2))
    assert intersect_lines(line1, line2) is None, "Test failed for parallel lines"

    # Test for overlapping lines (assuming intersect_lines returns None)
    line1 = Line2D(Point2D(0, 0), Point2D(1, 1))
    line2 = Line2D(Point2D(2, 2), Point2D(3, 3))
    assert intersect_lines(line1, line2) is None, "Test failed for overlapping lines"

    # Test for perpendicular lines
    line1 = Line2D(Point2D(0, 0), Point2D(1, 0))
    line2 = Line2D(Point2D(0, 0), Point2D(0, 1))
    assert intersect_lines(line1, line2) == Point2D(0, 0), "Test failed for perpendicular lines"

    # Test for lines intersecting at origin
    line1 = Line2D(Point2D(-1, -1), Point2D(1, 1))
    line2 = Line2D(Point2D(-1, 1), Point2D(1, -1))
    assert intersect_lines(line1, line2) == Point2D(0, 0), "Test failed for lines intersecting at origin"

    # Test for vertical and horizontal lines
    line1 = Line2D(Point2D(0, 0), Point2D(0, 1))  # Vertical
    line2 = Line2D(Point2D(-1, 0.5), Point2D(1, 0.5))  # Horizontal
    assert intersect_lines(line1, line2) == Point2D(0, 0.5), "Test failed for vertical and horizontal lines"

    print("All tests passed!")


if __name__ == '__main__':
    _test_intersect_lines()