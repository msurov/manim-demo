from manim import *
from anim_graphs import PlotLines
from pend_anim import PendAnim

def svgobj_fix_pathes(obj):
  for i in range(len(obj)):
    obj[i].stroke_width = 0.5

class LogoAnim(Scene):
  def construct(self):
    self.camera.background_color = WHITE
    self.speedup = 5.

    animtime = 10
    self.anims = []
    pend = PendAnim(5, animtime)
    self.add(pend)
    a = Create(pend)
    self.play(a)
    # self.add_phase_portrait()
    # self.add_sing_cond()
    # self.add_fundamental()
    # self.add_formals()
    # self.add_trans_basis()
    # self.add_cart_chain()
    # if self.anims:
    #   self.play(*self.anims)

  def add_fundamental(self):
    obj = ImageMobject('fig/fundemental-match.png')
    obj.set(height=2)
    obj.set_x(2.5)
    obj.set_y(-2)
    anim = FadeIn(obj)
    self.anims.append(anim)

  def add_phase_portrait(self):
    obj = SVGMobject('fig/full_phase-2.svg')
    svgobj_fix_pathes(obj)
    obj.set(height=1.5)
    obj.set_x(-4)
    obj.set_y(1.5)
    anim = Create(obj)
    self.anims.append(anim)

  def add_sing_cond(self):
    obj = SVGMobject('fig/singularity_condition_2.svg')
    svgobj_fix_pathes(obj)
    obj.set(height=1.5)
    obj.set_x(4)
    obj.set_y(2.5)
    anim = Create(obj)
    self.anims.append(anim)

  def add_formals(self):
    text = MathTex(
      R"\frac{\partial\phi}{\partial p_{k}}\left[\frac{1}{2}\frac{\partial m^{ij}}{\partial q^{k}}p_{i}p_{j}-\frac{\partial U}{\partial q^{k}}\right]+\frac{\partial\phi}{\partial p_{k}}f_{k}+\frac{\partial\phi}{\partial q^{k}}m^{kj}p_{j}"
    )
    text.set(height=0.5)
    text.set_x(-3)
    text.set_y(0)
    text.set(color=BLACK)
    anim = Write(text)
    self.anims.append(anim)

    text = MathTex(
      R"\dot{\xi}\approx\underbrace{\frac{dE_{\tau}^{T}}{d\tau}E_{\tau}\xi}_{1}+\underbrace{E_{\tau}^{T}\frac{h_{x_{\star}}^{T}Ph_{x_{\star}}\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}-h_{x_{\star}}h_{x_{\star}}^{T}P\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}-h_{x_{\star}}h_{x_{\star}}^{T}\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}^{T}P}{h_{x_{\star}}^{T}Ph_{x_{\star}}}E_{\tau}\xi}_{2}+\underbrace{E_{\tau}^{T}g_{x_{\star}}v}_{3}-\underbrace{E_{\tau}^{T}h_{x_{\star}}\frac{h_{x_{\star}}^{T}Pg_{x_{\star}}}{h_{x_{\star}}^{T}Ph_{x_{\star}}}v}_{5}"
    )
    text.set(height=0.5)
    text.set_x(-3)
    text.set_y(-3)
    text.set(color=BLACK)
    anim = Write(text)
    self.anims.append(anim)

    text = MathTex(
      R"A=\left(E_{\tau}^{T}\frac{h_{x_{\star}}^{T}Ph_{x_{\star}}\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}-h_{x_{\star}}h_{x_{\star}}^{T}P\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}-h_{x_{\star}}h_{x_{\star}}^{T}\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}^{T}P}{h_{x_{\star}}^{T}Ph_{x_{\star}}}+\frac{dE_{\tau}^{T}}{d\tau}\right)E_{\tau}",
    )
    text.set(height=0.5)
    text.set_x(2)
    text.set_y(-0.5)
    text.set(color=BLACK)
    anim = Write(text)
    self.anims.append(anim)

    text = MathTex(
      R"\dot{\tau} \approx 1+\frac{h_{x_{\star}}^{T}\left[P\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}+\left(\frac{\partial h}{\partial x}\right)_{x_{\star}}^{T}P\right]E}{h_{x_{\star}}^{T}Ph_{x_{\star}}}\cdot\xi+\frac{h_{x_{\star}}^{T}Pg_{x_{\star}}}{h_{x_{\star}}^{T}Ph_{x_{\star}}}\cdot v",
    )
    text.set(height=0.5)
    text.set_x(-4)
    text.set_y(3)
    text.set(color=BLACK)
    anim = Write(text)
    self.anims.append(anim)

  def add_trans_basis(self):
    obj = ImageMobject('fig/transverse_basis.png')
    obj.set(height=2)
    obj.set_x(1)
    obj.set_y(1)
    anim = FadeIn(obj)
    self.anims.append(anim)

  def add_cart_chain(self):
    obj = ImageMobject('fig/free_motion_anim.gif')
    obj.set(height=2)
    obj.set_x(1)
    obj.set_y(3)
    anim = Animation(obj)
    self.anims.append(anim)

with tempconfig({"quality": "medium_quality", "speedup": 2}):
  scene = LogoAnim()
  scene.render()

