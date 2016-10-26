from pyx import *
from pyxgradients import reverse_viridis
import numpy as np
from sys import argv

text.set(text.LatexRunner)

plot = np.load(argv[1])

g = graph.graphxy(
    width  = 8,
    height = 8,
    x = graph.axis.lin(title=r"$\alpha$", min=-0.5, max=0.5),
    y = graph.axis.lin(title=r"$\beta$", min=0, max=1.05)
)
coloraxis = graph.axis.log(title=r"max$(|\lambda_1|, |\lambda_2|)$")
g.plot(graph.data.points(plot, x=1, y=2, color=3), [graph.style.density(gradient=reverse_viridis, coloraxis=coloraxis)])

g.plot(graph.data.function("y(x)=sqrt(-2*x)", points=1000), [graph.style.line([style.linestyle.dashed])])
g.finish()
g.stroke(g.xgridpath(0),    [style.linestyle.dashed])
g.stroke(g.ygridpath(0.45), [style.linestyle.dashed])

g.writePDFfile("mathieu.pdf")
