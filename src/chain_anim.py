from manim import *


class Chain(Succession):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

  def make_all_invisible(self):
    allobjs = [anim.mobject for anim in self.animations]
    allobjs = remove_list_redundancies(allobjs)
    for obj in allobjs:
      obj.set_opacity(0.)

  def update_active_animation(self, index: int):
    super().update_active_animation(index)
    self.make_all_invisible()
    if self.active_animation is not None:
      objs = self.active_animation.get_all_mobjects()
      objs = remove_list_redundancies(objs)
      for obj in objs:
        obj.set_opacity(1.)

  def interpolate(self, alpha: float) -> None:
    return super().interpolate(alpha)


class Demo(Scene):
  def construct(self):
    t1 = Text("The pendulums motion\n seems equavalent", font_size=10)
    t2 = Text("but after a while their\n configurations", font_size=10)
    t3 = Text("are becoming more\n and more different", font_size=10)
    anim = Chain(
      Write(t1),
      Uncreate(t1),
      Write(t2),
      Uncreate(t2),
      Write(t3),
      Uncreate(t3),
    )
    self.play(anim)

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
