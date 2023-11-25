from manim import *
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL

class PolyLine(VMobject, metaclass=ConvertToOpenGL):
  def __init__(self, axes : Axes, color: ParsableManimColor = BLUE, **kwargs) -> None:
    self.axes = axes
    super().__init__(color = color, **kwargs)

  def generate_points(self) -> None:
    pass

  def append_point(self, t, x):
    points = self.axes.coords_to_point([[t, x]])
    if len(self.points) == 0:
      self.start_new_path(points)
    else:
      self.add_points_as_corners([points])

  init_points = generate_points

class PlotView(VGroup):
  def __init__(self):
    super().__init__()
    ax = Axes(
      x_range = [-1, 1],
      y_range = [-1, 1],
      x_length = 2,
      y_length = 2
    )
    self.ax = ax
    p = PolyLine(ax, stroke_width=1)
    for t in np.arange(0, 1, 0.01):
      p.append_point(t, np.sin(5*t))
    self.add(p)

class Demo(Scene):
  def construct(self):
    self.camera.background_color = BLACK
    p = PlotView()
    self.add(p)

if __name__ == '__main__':
  with tempconfig({
    "quality": "medium_quality", 
    "format": "gif", 
    "pixel_width": 1000,
    "pixel_height": 2000,
    "frame_height": 6,
    "frame_width": 3,
    "aspect": 0.5,
  }):
    scene = Demo()
    scene.render()
