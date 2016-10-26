import numpy as np
from scipy.integrate import odeint

# integrate differential equation
def derivs(v, t, alpha, beta):
    """Integrate differential equation
    d²/dt² X + (α+βcos(t))X = 0
    as system of 1st order:
    d/dt X = Y
    d/dt Y = -(α+βcos(t))X
    """
    X,Y = v
    dX = Y
    dY = -(alpha+beta*np.cos(t))*X
    return np.array([dX,dY])


def eigenvalues(alpha,beta,npts=500):
    T = 2*np.pi
    times = np.linspace(0,T,npts)

    v1 = np.array([1,0])
    v2 = np.array([0,1])

    sol1 = odeint(derivs, v1, times, args=(alpha,beta))[-1]
    sol2 = odeint(derivs, v2, times, args=(alpha,beta))[-1]

    M = np.array([sol1,sol2]).T

    return np.linalg.eigvals(M)



npts = 500
plot = []
alpha_min, alpha_max = -0.5, 0.5
beta_min, beta_max   = 0, 1.05
for i,alpha in enumerate(np.linspace(alpha_min, alpha_max, npts)):
    for beta in np.linspace(beta_min, beta_max, npts):
        lambda1,lambda2 = eigenvalues(alpha,beta)
        maxreal = max(abs(lambda1), abs(lambda2))
        if maxreal > 1.000001:
            plot.append((alpha,beta,maxreal))

    print("%.1f%%" % (100*(i+1)/npts))

np.save("data.npy", plot)
