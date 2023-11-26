from manim import *
from functools import reduce


def concat(listoflists : list[list]) -> list:
  def joiner(a, b):
    return list(a) + list(b)
  return reduce(joiner, listoflists, [])

class Chain(Succession):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

  def begin(self):
    return super().begin()

  def _construct_visibility_table(self):
    allobjs = [anim.mobject for anim in self.animations]
    allobjs = remove_list_redundancies(allobjs)
    nanims = len(self.animations)
    nobjs = len(allobjs)
    table = np.zeros((nobjs, nanims), dtype=np.bool_)

    for i in range(nanims):
      anim = self.animations[i]
      obj = anim.mobject
      j = allobjs.index(obj)
      if anim.is_introducer():
        table[j,i:] = True
      elif anim.is_remover():
        if table[j,i] is False:
          table[j,:i+1] = True
        table[j,i+1:] = False
      else:
        table[j,i] = True
    
    self.vis_table = table
    self.mobjs = allobjs

  def update_active_animation(self, index: int):
    super().update_active_animation(index)

    if not hasattr(self, 'vis_table'):
      self._construct_visibility_table()

    if self.active_animation is not None:
      objs = self.active_animation.get_all_mobjects()
      for obj in objs:
        obj.set_opacity(1)

      for j in range(len(self.mobjs)):
        opacity = 1.0 * self.vis_table[j,index]
        self.mobjs[j].set_opacity(opacity)
    else:
      # set all invisible?
      pass

  def interpolate(self, alpha: float) -> None:
    return super().interpolate(alpha)

def rate_fun(x : float):
  return np.clip(5 * x, 0, 1)

class Demo(Scene):
  def construct(self):
    t1 = Text("The pendulums motion\n seems equavalent", font_size=10)
    t2 = Text("but after a while their\n configurations", font_size=10)
    t3 = Text("are becoming more\n and more different", font_size=10)
    anim = Chain(
      Write(t1, run_time=3, rate_func=rate_fun),
      Wait(run_time=2),
      Uncreate(t1),
      Write(t2, run_time=3, rate_func=rate_fun),
      Wait(run_time=2),
      Uncreate(t2),
      Write(t3, run_time=3, rate_func=rate_fun),
      Wait(run_time=2),
      Uncreate(t3)
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
