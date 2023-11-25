from manim import *
from manim.mobject.mobject import _AnimationBuilder
from manim.mobject.opengl.opengl_compatibility import ConvertToOpenGL


class PolyLine(VMobject, metaclass=ConvertToOpenGL):
  def __init__(self, axes : Axes, color: ParsableManimColor = BLUE, **kwargs) -> None:
    self.axes = axes
    super().__init__(color = color, **kwargs)

  def generate_points(self) -> None:
    self.start_new_path([0, 0, 0])

  def append_value(self, t, x):
    points = self.axes.coords_to_point([[t, x]])
    if len(self.points) <= 1:
      self.start_new_path(points)
    else:
      self.add_points_as_corners([points])

  init_points = generate_points

class PlotView(VGroup):
  def __init__(self, xrange, yrange, width=1, height=1, **axes_args):
    super().__init__()
    ax = Axes(
      x_range = xrange,
      y_range = yrange,
      x_length = width,
      y_length = height,
      **axes_args
    )
    self.ax = ax
    self.add(ax)
    self.curves = []

  def add_curve(self, color, stroke_width=1, **kwargs) -> PolyLine:
    p = PolyLine(self.ax, color=color, stroke_width=stroke_width, **kwargs)
    self.ax.add(p)
    self.curves.append(p)
    return p

class PlotAnim(VGroup):
  def __init__(self):
    super().__init__()
    self.plot = PlotView(
      [0, 5],
      [-2, 2],
      5, 6,
      axis_config={"color": DARK_BLUE},
      tips=False,
    )
    self.plot.scale(0.3)
    self.c1 = self.plot.add_curve(YELLOW)
    self.c2 = self.plot.add_curve(GREEN)
    self.c3 = self.plot.add_curve(RED)
    self.time = 0
    self.add(self.plot)

  def animate(self, **kwargs) -> _AnimationBuilder:
    self.time = 0
    self.add_updater(self._update, call_updater=True)
    return super().animate(**kwargs)
  
  def _update(self, _, dt, recursive=None):
    self.time += dt
    self.c1.append_value(self.time, np.sin(2 * self.time))
    self.c2.append_value(self.time, np.sin(3 * self.time))
    self.c3.append_value(self.time, np.sin(4 * self.time))

class Demo(Scene):
  def construct(self):
    self.camera.background_color = BLACK
    p = PlotAnim()
    self.play(Create(p))
    self.play(p.animate(run_time=5))

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
