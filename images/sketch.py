from pyx import *
from numpy import linspace
from math import *

c = canvas.canvas()
#c.stroke(path.line(1, 0, 5.2, 0), [style.linewidth.THICK])

c.stroke(path.line(3, 0, 4.5, 0),  [deco.earrow([deco.stroked()])])
c.text(4.6, 0, r"$x$")

c.stroke(path.line(3, 0, 3, 1.5), [deco.earrow([deco.stroked()])])
c.text(3, 1.65, r"$y$")

c.fill(path.circle(3, 0, .12))
c.text(2.6, 0.1, r"$O$")


l = 2.5
ldashed = 1.7
radius = 0.2
theta1 = 0.25
theta2 = 0.5
xoffset = 0.2
yoffset = +0.2

x0 = 3
y0 = 0
x1 = 3 + l*sin(theta1)
y1 = -l*cos(theta1)
x2 = x1 + l*sin(theta2)
y2 = y1 - l*cos(theta2)

c.stroke(path.line(x0, y0, x1, y1), [style.linewidth.thick])
c.text((x0+x1)/2+0.1, (y0+y1)/2, r"$L$")

c.stroke(path.line(x0, y0, x0, y0-ldashed), [style.linestyle.dashed])
c.text((x1+x2)/2+0.1, (y1+y2)/2, r"$L$")

c.stroke(path.line(x1, y1, x2, y2), [style.linewidth.thick])
c.stroke(path.line(x1, y1, x1, y1-ldashed), [style.linestyle.dashed])

c.fill(path.circle(x1, y1, radius), [color.cmyk.NavyBlue])
c.text(x1+xoffset, y1+yoffset, r"$m$")
c.fill(path.circle(x2, y2, radius), [color.cmyk.NavyBlue])
c.text(x2+xoffset, y2+yoffset, r"$m$")

ldashed2 = 1.5
c.stroke( path.path(path.arc(x0,y0,ldashed2,-90, -90+degrees(theta1))), [style.linewidth.thin, deco.earrow.small, deco.barrow.small] )
c.stroke( path.path(path.arc(x1,y1,ldashed2,-90, -90+degrees(theta2))), [style.linewidth.thin, deco.earrow.small, deco.barrow.small] )

c.text((x0+x1)/2-0.8, y0-ldashed+0.5, r"$\theta_1$")
c.stroke(path.line((x0+x1)/2-0.5, y0-ldashed+0.55, (x0+x1)/2-0.1, y0-ldashed+0.3), [style.linewidth.thin])

c.text((x1+x2)/2-0.45, y1-ldashed+0.4, r"$\theta_2$")

#c.stroke(path.line(0, 0, 0, -2))
#c.stroke(
#    path.curve(0, 0, 0, 4, 2, 4, 3, 3),
#         [style.linewidth.THICK, style.linestyle.dashed, color.rgb.blue,
#          deco.earrow([deco.stroked([color.rgb.red, style.linejoin.round]),
#                       deco.filled([color.rgb.green])], size=1)]
#)

c.writePDFfile()
