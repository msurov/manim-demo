import casadi as ca
import numpy as np
from scipy.integrate import solve_ivp, ode


class Pendulum:
  def __init__(self, nlinks):
    self.nlinks = nlinks
    q = ca.SX.sym('q', nlinks)
    x = ca.cumsum(ca.sin(q))
    y = ca.cumsum(ca.cos(q))
    r = ca.horzcat(x, y)
    M = 0
    for i in range(nlinks):
      Ji = ca.jacobian(r[i,:], q)
      M += Ji.T @ Ji
    dq = ca.SX.sym('dq', nlinks)
    D = ca.jacobian(M @ dq, q)
    C = D - D.T / 2
    U = ca.sum1(y)
    G = ca.jacobian(U, q).T
    C = D - D.T / 2
    ddq = ca.pinv(M) @ (-C @ dq - G)
    rhs = ca.vertcat(dq, ddq)
    self.dynamics = ca.Function('dynamics', [q, dq], [rhs])
    E = dq.T @ M @ dq / 2 + U
    self.energy = ca.Function('energy', [q, dq], [E])

class PendSimulator:
  def __init__(self, q0, dq0, **integrator_params):
    nlinks, = np.shape(q0)
    self.nlinks = nlinks
    self.pend = Pendulum(nlinks)
    self.integrator = ode(self.rhs)
    self.integrator.set_integrator('dopri5', **integrator_params)
    self.q = np.copy(q0)
    self.dq = np.copy(dq0)
    st0 = np.concatenate([q0, dq0], axis=0)
    self.integrator.set_initial_value(st0, 0)
  
  def rhs(self, _, st):
    q = st[:self.nlinks]
    dq = st[self.nlinks:]
    dst = self.pend.dynamics(q, dq)
    return np.reshape(dst, (2*self.nlinks,))

  def update(self, t):
    self.integrator.integrate(t)
    assert self.integrator.successful(), self.integrator.get_return_code()
    self.q = self.integrator.y[0:self.nlinks].copy()
    self.dq = self.integrator.y[self.nlinks:].copy()
    return self.q, self.dq
  
  def get_state(self):
    return self.q, self.dq

def get_verts_coordinates(q : np.ndarray):
  match np.shape(q):
    case nt,nlinks:
      x = np.zeros((nt, nlinks + 1))
      y = np.zeros((nt, nlinks + 1))
      x[:,1:] = np.cumsum(np.sin(q), axis=1)
      y[:,1:] = np.cumsum(np.cos(q), axis=1)
    case nlinks,:
      x = np.zeros(nlinks + 1)
      y = np.zeros(nlinks + 1)
      x[1:] = np.cumsum(np.sin(q))
      y[1:] = np.cumsum(np.cos(q))
  return x, y


def pend_simulate(pend : Pendulum, q0 : np.ndarray, dq0 : np.ndarray, interval : float):
  def rhs(_, st):
    q = st[:pend.nlinks]
    dq = st[pend.nlinks:]
    dst = pend.dynamics(q, dq)
    dst = np.array(dst).reshape(-1)
    return dst

  st0 = np.concatenate([q0, dq0], axis=0)
  sol = solve_ivp(rhs, [0, interval], st0, max_step=1e-3)
  return sol.t, sol.y[0:pend.nlinks,:].T, sol.y[pend.nlinks:,:].T

def demo1():
  import matplotlib.pyplot as plt

  pend = Pendulum(5)
  t, q, dq = pend_simulate(pend, np.zeros(5), 1e-3*np.random.normal(size=5), 10)
  E = [float(pend.energy(a, b)) for a, b in zip(q, dq)]
  plt.subplot(211)
  plt.plot(t, q)
  plt.subplot(212)
  plt.plot(t, E)
  plt.show()

def demo2():
  import matplotlib.pyplot as plt
  q0 = np.zeros(6)
  dq0 = 1e-3*np.random.normal(size=q0.shape)
  pend = PendSimulator(q0, dq0)
  t = np.linspace(0, 100, 1000)
  x, y = get_verts_coordinates(q0)
  plt.axis('equal')
  plt.ylim([-6, 6])
  line, = plt.plot(x, y, 'o-')
  for ti in t:
    q,_ = pend.update(ti)
    x, y = get_verts_coordinates(q)
    line.set_data(x, y)
    plt.draw()
    plt.pause(0.01)

if __name__ == '__main__':
  # demo1()
  demo2()
