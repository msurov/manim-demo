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
  def __init__(self, q0, dq0, speed=1, animtime=1):
    super().__init__()
    model = PendSimulator(q0, dq0, 
                          max_step=1e-3, atol=1e-10, 
                          rtol=1e-10, nsteps=1000)
    view = PendView(q0)
    self.speed = speed
    self.animtime = animtime
    self.model = model
    self.view = view
    self.time = 0.
    self.add(view)

  def get_time(self):
    return self.time
  
  def get_model_state(self):
    return self.model.get_state()

  def animate(self, run_time=1, *args, **kwargs):
    self.run_time = run_time
    self.add_updater(self._update)
    return super().animate(run_time=run_time, *args, **kwargs)

  def _update(self, _, dt=0, recursive=None):
    self.time += dt
    q,_ = self.model.update(self.time * self.speed)
    self.view.move(q)
    alpha = np.clip(self.run_time - self.time, 0, 1)
    self.view.set_opacity(alpha)

  def scale(self, factor):
    self.view.scale(factor)
    super().scale(factor)
