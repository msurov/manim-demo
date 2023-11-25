class CustomAnim(VGroup):
  def __init__(self, *objs, **kwargs) -> None:
    super().__init__(**kwargs)
    self.objs = objs
    self.anims = []
    for obj in objs:
      obj.set_opacity(0.0)
      self.add(obj)
      self.anims.append(Write(obj))
    self.time = 0
    self.cur_obj = 0
    self.add_updater(self._update)

  def animate(self, run_time=1):
    self.run_time = run_time
    return super().animate(run_time=run_time)
  
  def _update(self, _, dt, recursive=None):
    self.time += dt
    nobjs = len(self.objs)
    interval = self.run_time / nobjs
    cur_obj = int(self.time / interval)
    cur_obj = np.clip(cur_obj, 0, nobjs - 1)
    if cur_obj > self.cur_obj:
      self.objs[self.cur_obj].set_opacity(0.)
      self.cur_obj = cur_obj

    dt = self.time - cur_obj * interval
    alpha = dt / interval
    self.objs[cur_obj].set_opacity(alpha)
    self.anims[cur_obj].interpolate(alpha)
