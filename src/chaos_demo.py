from manim import *
from chain_anim import Chain
from functools import reduce
from pend_anim import PendAnim


def add_text_anim(*lines):
  descripton_text_params = {
    "color": WHITE,
    "font_size": 14,
    "font": "Annapurna SIL",
    "line_spacing": 0.5
  }
  text = Paragraph(*lines, **descripton_text_params)
  text.to_edge(UP)
  return [
    Write(text, run_time=3),
    Wait(run_time=3),
    Uncreate(text, run_time=1)
  ]

def text_anims():
  anims = [
    add_text_anim(
      "Consider a pendulum starting",
      "moving from upward position."
    ),
    add_text_anim(
      "It may seem that conducting",
      "several experiments we will",
      "see the same behaviour.",
    ),
    add_text_anim(
      "But surprising fact is",
      "arbitrarily small variations",
      "in initial state will change",
      "shape of the motion",
      "beyound recognition.",
    ),
    add_text_anim(
      "The more time we watch,",
      "the more different",
      "trajectories will be.",
    ),
    add_text_anim(
      "It seems unbelievable,",
      "but after a while the",
      "pendulum will come close to",
      "the initial configuration."
    ),
    add_text_anim(
      "Such a behavior is called",
      "             CHAOS"
    )
  ]
  return sum(anims, [])

class ChaosDemo(Scene):
  def construct(self):
    self.camera.background_color = BLACK
    nlinks = 8
    animtime = 45
    q0 = np.zeros(nlinks)
    np.random.seed(0)
    dq0 = 1e-5 * np.random.normal(size=nlinks)
    pend1 = PendAnim(q0, dq0, speed=1)
    pend1.set_x(-0.5)
    pend1.set_y(1)
    pend1.scale(0.5)

    dq0 += 1e-12 * np.random.normal(size=dq0.shape)
    pend2 = PendAnim(q0, dq0, speed=1)
    pend2.set_x(0.5)
    pend2.set_y(1)
    pend2.scale(0.5)
    heading = Text("What is chaos?", color=WHITE, font_size=18)
    heading.to_edge(UP)
    self.play(
      AnimationGroup(
        Write(heading),
        Create(pend1),
        Create(pend2),
        lag_ratio=0.5,
        run_time=5
      )
    )
    self.play(
      Uncreate(heading)
    )
    a1 = pend1.animate(run_time=animtime)
    a2 = pend2.animate(run_time=animtime)
    anims = text_anims()
    self.play(
      Chain(*anims, Wait(run_time=5)), a1, a2,
    )


if __name__ == '__main__':
  with tempconfig({
    # "quality": "production_quality", 
    "quality": "medium_quality", 
    # "quality": "example_quality",
    # "format": "gif", 
    "pixel_width": 500,
    "pixel_height": 1000,
    "frame_height": 6,
    "frame_width": 3,
    "aspect": 0.5,
    "disable_caching": True
  }):
    np.random.seed(0)
    scene = ChaosDemo()
    scene.render()
