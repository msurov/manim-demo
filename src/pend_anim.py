from manim import *
from pendulum import PendSimulator, get_verts_coordinates


class PendView(VGroup):
  def __init__(self, q0):
    super().__init__()
    self.nlinks, = np.shape(q0)
    self.scale_factor = 1.
    axes = Axes(
      x_range = [-0.5, 0.5],
      y_range = [-0.5, 0.5],
      x_length = 1,
      y_length = 1,
      axis_config = {
        "stroke_width": 0,
      },
      tips=False
    )
    self.axes = axes
    self.q = np.copy(q0)
    self._create_links()
    self._create_verts()
    self.add(axes)

  def get_verts_positions(self):
    x, y = get_verts_coordinates(self.q)
    coords = np.array([x, y])
    points = self.axes.coords_to_point(coords.T)
    return points

  def _create_verts(self):
    pts = self.get_verts_positions()
    verts = []
    for i in range(self.nlinks + 1):
      vert = Dot(pts[i], color=DARK_BLUE, radius=0.2)
      verts.append(vert)

    self.verts = verts
    self.axes.add(*verts)

  def _create_links(self):
    pts = self.get_verts_positions()
    links = []
    for i in range(self.nlinks):
      link = Line(pts[i], pts[i+1])
      link.set(color=RED)
      link.set(stroke_width = 10 * self.scale_factor)
      links.append(link)

    self.links = links
    self.axes.add(*links)

  def _update(self):
    pts = self.get_verts_positions()
    self.verts[0].set_x(pts[0,0])
    self.verts[0].set_y(pts[0,1])
    for i in range(self.nlinks):
      self.verts[i + 1].set_x(pts[i + 1, 0])
      self.verts[i + 1].set_y(pts[i + 1, 1])
      self.links[i].put_start_and_end_on(pts[i], pts[i+1])

  def move(self, q):
    self.q = np.copy(q)
    self._update()

  def scale(self, factor):
    self.scale_factor = factor

    for link in self.links:
      link.set(stroke_width = 10 * self.scale_factor)

    self._update()
    super().scale(factor)

class PendAnim(VGroup):
  def __init__(self, q0, dq0, speed=1):
    super().__init__()
    model = PendSimulator(q0, dq0, max_step=1e-3, nsteps=200)
    view = PendView(q0)
    self.speed = speed
    self.model = model
    self.view = view
    self.time = 0
    self.add(view)

  def animate(self, *args, **kwargs):
    self.add_updater(self._update)
    return super().animate(*args, **kwargs)

  def _update(self, _, dt=0, recursive=None):
    self.time += dt * self.speed
    q,_ = self.model.update(self.time * self.speed)
    self.view.move(q)

  def scale(self, factor):
    self.view.scale(factor)
    super().scale(factor)

class PendDemo(Scene):
  def construct(self):
    self.camera.background_color = WHITE
    nlinks = 8
    animtime = 5
    q0 = np.zeros(nlinks)
    np.random.seed(0)
    dq0 = 1e-3 * np.random.normal(size=nlinks)
    pend1 = PendAnim(q0, dq0, speed=1)
    pend1.set_x(-0.5)
    pend1.set_y(1)
    pend1.scale(0.5)

    dq0 = 1e-3 * np.random.normal(size=nlinks)
    pend2 = PendAnim(q0, dq0, speed=1)
    pend2.set_x(0.5)
    pend2.set_y(1)
    pend2.scale(0.5)
    heading = Text("What is chaos?", color=BLACK, font_size=18)
    heading.to_edge(UP)
    self.play(AnimationGroup(Write(heading), Create(pend1), Create(pend2), lag_ratio=0.5))
    self.wait()
    description = Paragraph(
      "The pendulum behavior\n"
      "depends significantly\n"
      "on initial conditions.\n"
      "A small change in\n"
      "initial speed changes\n"
      "motion beyond the recognition.", 
      color=BLACK, font_size=18
    )
    description.to_edge(UP)
    self.play(
      FadeOut(heading),
      pend1.animate(run_time=animtime),
      pend2.animate(run_time=animtime),
      Write(description, run_time=10)
    )

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
    scene = PendDemo()
    scene.render()
