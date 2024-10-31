# %%
from foundation import Part, Sketch, Point, Rectangle, Extrusion, show, Hole, Chamfer


class YCorner(Part):
    LENGTH = 18
    WIDTH = 47
    EXTRUDE_HEIGHT = 22
    HOLE_DIAMETER = 8.4
    LARGE_HOLE_DIAMETER = 10.6
    WASHER_HOLE_DIAMETER = 22
    WASHER_POCKET = 2
    HOLE_DISTANCE = 20
    HOLE_OFFSET = 10
    XY_HOLE_Y_OFFSET = 45
    XY_LARGE_HOLE_Y_OFFSET = 20
    RECT_POCKET_OFFSET = 40
    RECT_POCKET_WIDTH = 3.5
    RECT_POCKET_HEIGHT = 2
    AXIS_POCKET_OFFSET = 2
    CHAMFER = 2

    def __init__(self):
        super().__init__()
        self.create_rectangle()
        self.create_holes_yz()
        self.create_hole_xy()
        self.create_large_hole()
        self.create_rect_pocket()

    def create_rectangle(self):
        sketch = Sketch(self.xy())
        center = Point(sketch, 0, 0)
        rectangle = Rectangle.from_center_and_sides(center, self.LENGTH, self.WIDTH)
        extrusion = Extrusion(
            rectangle, self.EXTRUDE_HEIGHT / 2, -self.EXTRUDE_HEIGHT / 2
        )
        f = Chamfer(extrusion, self.CHAMFER)
        self.add_operation(f)

    def create_holes_yz(self):
        # Create holes on the side of the extrusion
        side_plane = Plane.get_parallel_plane(self.yz(), -self.LENGTH / 2, "sideyx")
        sketch = Sketch(side_plane)
        hole_z = -self.EXTRUDE_HEIGHT / 2 + self.HOLE_OFFSET
        hole1_y = -self.WIDTH / 2 + self.HOLE_OFFSET
        hole2_y = hole1_y + self.HOLE_DISTANCE

        hole1_center = Point(sketch, hole1_y, hole_z)
        hole2_center = Point(sketch, hole2_y, hole_z)

        hole1 = Hole(hole1_center, self.HOLE_DIAMETER / 2, self.LENGTH)
        hole2 = Hole(hole2_center, self.HOLE_DIAMETER / 2, self.LENGTH)

        self.add_operation(hole1)
        self.add_operation(hole2)

    def create_hole_xy(self):
        # Create hole on XY plane
        bottom_plane = Plane.get_parallel_plane(
            self.xy(), -self.EXTRUDE_HEIGHT / 2 + self.AXIS_POCKET_OFFSET, "bottomxy"
        )
        sketch = Sketch(bottom_plane)
        hole_center = Point(sketch, 0, self.XY_HOLE_Y_OFFSET - self.WIDTH / 2)
        hole = Hole(hole_center, self.HOLE_DIAMETER / 2, self.EXTRUDE_HEIGHT)
        self.add_operation(hole)

    def create_large_hole(self):
        # Create large hole on XY plane
        bottom_plane = Plane.get_parallel_plane(
            self.xy(), -self.EXTRUDE_HEIGHT / 2, "bottomxy"
        )
        sketch = Sketch(bottom_plane)
        hole_center = Point(sketch, 0, self.XY_LARGE_HOLE_Y_OFFSET - self.WIDTH / 2)
        hole2 = Hole(hole_center, self.LARGE_HOLE_DIAMETER / 2, self.EXTRUDE_HEIGHT)
        self.add_operation(hole2)

        whasher_hole = Hole(
            hole_center, self.WASHER_HOLE_DIAMETER / 2, self.WASHER_POCKET
        )
        self.add_operation(whasher_hole)

    def create_rect_pocket(self):
        sketch = Sketch(self.yz())
        center = Point(sketch, self.RECT_POCKET_OFFSET - self.WIDTH / 2, 0)
        rect_pocket = Rectangle.from_center_and_sides(
            center, self.RECT_POCKET_HEIGHT, self.RECT_POCKET_WIDTH
        )
        extrusion = Extrusion(
            rect_pocket, self.EXTRUDE_HEIGHT / 2, -self.EXTRUDE_HEIGHT / 2, cut=True
        )
        self.add_operation(extrusion)


if __name__ == "__main__":
    show(YCorner())  # %%

# %%
