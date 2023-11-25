from typing import Callable
from PIL.Image import Image
from manim import *
from manim.animation.animation import Animation
from manim.constants import DEFAULT_STROKE_WIDTH, UL, LineJointType
from manim.mobject.mobject import _AnimationBuilder, Group, Mobject
from manim.mobject.opengl.opengl_vectorized_mobject import OpenGLVMobject
from manim.mobject.types.vectorized_mobject import VGroup, VMobject
from manim.utils.iterables import remove_list_redundancies
from manim.scene.scene import Scene
from manim.typing import PathFuncType, Vector3
from manim.utils.color import BLACK, ParsableManimColor
from manim.utils.paths import straight_path
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



