from manim import *
from manim.mobject.mobject import _AnimationBuilder


class Anim(VGroup):
  def __init__(self, *vmobjects, **kwargs):
    super().__init__(*vmobjects, **kwargs)
    self.dot = Dot()
    self.add(self.dot)
    self.time = 0

  def hide(self):
    self.dot.set_opacity(0)

  @override_animate(hide)
  def _hide_animation(self, after=0, run_time=1, anim_args=None, **kw_args):
    self.hide_after = after
    self.hide_time = run_time

  def launch(self):
    self.time = 0

  @override_animate(launch)
  def _run_animation(self, after=0, anim_args=None, run_time=1):
    self.run_time = run_time
    self.run_after = after

  def update(self, dt, recursive=None):
    self.time += dt
    if hasattr(self, 'run_after'):
      if self.time >= self.run_after:
        self.dot.set_x(np.sin(2 * np.pi * self.time / self.run_time))
        self.dot.set_y(np.cos(2 * np.pi * self.time / self.run_time))

    if hasattr(self, 'hide_after'):
      alpha = np.clip((self.time - self.hide_after) / self.hide_time, 0, 1)
      self.dot.set_opacity(1 - alpha)

class Demo(MovingCameraScene):
  
  def construct(self):
    d = Anim()
    self.play(d.animate(run_time=3).launch().hide(after=2))

if __name__ == '__main__':
  with tempconfig({
    "quality": "medium_quality", 
    # "format": "gif", 
    "pixel_width": 1000,
    "pixel_height": 2000,
    "frame_height": 6,
    "frame_width": 3,
    "aspect": 0.5,
    "disable_caching": True
  }):
    np.random.seed(0)
    scene = Demo()
    scene.render()
