from typing import Callable
from manim import *
from manim.animation.animation import Animation
from manim.mobject.mobject import Group
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
from manim.scene.scene import Scene
from pendulum import get_verts_coordinates


class Anim(VGroup):
  def __init__(self):
    super().__init__()
    self.time = 0
    p1, p2 = self.get_positions()
    self.p1 = Dot(p1)
    self.p2 = Dot(p2)
    self.add(self.p1)
    self.add(self.p2)

  def set_anim(self, turnon=True):
    if turnon:
      self.time = 0
      self.add_updater(self._update)
    else:
      self.remove_updater(self._update)

  def get_positions(self):
    x1 = 0.5 + 0.2 * np.sin(2*np.pi*self.time)
    y1 = 0.2 * np.cos(2*np.pi*self.time)
    x2 = -0.5 - 0.2 * np.sin(2*np.pi*self.time)
    y2 = 0.2 * np.cos(2*np.pi*self.time)
    return np.array([x1, y1, 0]), np.array([x2, y2, 0])

  def _update(self, _, dt, recursive=None, *args, **kwargs):
    self.time += dt
    p1, p2 = self.get_positions()
    self.p1.set_x(p1[0])
    self.p1.set_y(p1[1])
    self.p2.set_x(p2[0])
    self.p2.set_y(p2[1])

class Uncreate2(Uncreate):
  def __init__(self, mobject: VMobject | OpenGLVMobject, reverse_rate_function: bool = True, remover: bool = True, **kwargs) -> None:
    super().__init__(mobject, reverse_rate_function, remover, **kwargs)

  def _setup_scene(self, scene: Scene) -> None:
    print('_setup_scene')
    return super()._setup_scene(scene)

class Demo(Scene):
  def construct(self):

    heading = Text("What is chaos?", color=BLUE, font_size=18)
    # heading.to_edge(UP)
    description = Paragraph(
      "The pendulum behavior depends\n",
      "significantly on initial conditions.\n",
      "Even a small change in initial speed\n",
      "changes its future position\n",
      "beyond recognition.", 
      color=BLUE, font_size=14, font="Annapurna SIL", alignment="center", line_spacing=-0.3
    )
    self.play(Write(heading))
    self.play(
      Uncreate(heading, run_time=1),
      Succession(Wait(run_time=1), Write(description, run_time=3)),
      Succession(Wait(run_time=4), Uncreate2(description, run_time=1)),
    )
    # description.to_edge(UP)
    # self.play(
    #   Succession(
    #     Write(heading),
    #     FadeOut(heading),
    #     Create(description, run_time=2),
    #     FadeOut(description, run_time=1)
    #   )
    # )
  
    # self.add(description)

    # a = Anim()
    # self.play(Create(a))
    # a.set_anim()
    # self.play(a.animate(run_time=5))

if __name__ == '__main__':
  with tempconfig({
    "quality": "medium_quality", 
    "format": "gif", 
    "pixel_width": 1000,
    "pixel_height": 2000,
    "frame_height": 6,
    "frame_width": 3,
    "aspect": 0.5,
    "disable_caching": True
  }):
    scene = Demo()
    scene.render()
