import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,GLib

import numpy as np
from scipy.integrate import odeint

class DoublePendulum(Gtk.Window):
    def __init__(self, data, dt):
        super(DoublePendulum, self).__init__()

        self.data = data
        
        self.set_title("Double pendulum")
        self.set_size_request(350, 350)

        self.connect("destroy", Gtk.main_quit)

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.expose)
        self.add(self.darea)

        GLib.timeout_add(dt, self.on_timer)
        
        self.i = 0
        self.show_all()


    def on_timer(self):
        self.darea.queue_draw()

        self.i += 1
        if self.i >= len(self.data)-1:
            return False

        return True


    def draw(self, l1=1, l2=1):
        index = self.i
        theta1,theta2 = self.data[index,0], self.data[index,1]
        deltal = 0.47/(l1+l2)

        point1 = l1*np.sin(theta1)*deltal+0.5, l1*np.cos(theta1)*deltal+0.5
        point2 = l2*np.sin(theta2)*deltal+point1[0], l2*np.cos(theta2)*deltal+point1[1]

        resolution = min(self.get_size())

        cr = self.cr
        cr.scale(resolution, resolution)

        # hintergrund weiss
        cr.rectangle(0, 0, 1, 1)
        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        # stangen
        cr.set_source_rgb(0, 0, 0)
        cr.move_to(0.5, 0.5) # aufhaengepunkt
        cr.line_to(point1[0], point1[1])
        cr.line_to(point2[0], point2[1])
        cr.set_line_width(0.007)
        cr.stroke()

        # massenpunkt m1
        cr.set_source_rgb(1, 0, 0)
        cr.arc(point1[0], point1[1], 0.02, 0, 2*np.pi)
        cr.fill()
        cr.stroke()

        # massenpunkt m2
        cr.set_source_rgb(0, 1, 0)
        cr.arc(point2[0], point2[1], 0.02, 0, 2*np.pi)
        cr.fill()
        cr.stroke()

    
    def expose(self, widget, event):
        self.cr = widget.get_property("window").cairo_create()
        self.draw()


def derivs(y,t,L,m,g):
    theta1,theta2,p1,p2 = y 

    Delta = theta1-theta2
    cos_Delta = np.cos(Delta)
    sin_Delta = np.sin(Delta)

    denom = L**2*m*(1+sin_Delta**2)
    C = (p1*p2*sin_Delta-(p1**2+2*p2**2-2*p1*p2*cos_Delta)*sin_Delta*cos_Delta)/denom

    dtheta1 =   (p1-p2*cos_Delta)/denom
    dtheta2 = (2*p2-p1*cos_Delta)/denom
    dp1 = -2*m*g*L*np.sin(theta1)-C
    dp2 = -  m*g*L*np.sin(theta2)+C

    return np.array((dtheta1,dtheta2,dp1,dp2))


if __name__ == "__main__":
    t0 = 0
    tf = 30

    dt = 10 # in miliseconds
    t = np.arange(t0, tf, dt/1000.)

    L = 1
    m = 1
    g = 9.81

    data = odeint(derivs,[np.pi,np.pi,0,0],t,args=(1,1,9.81))

    DoublePendulum(data,dt)

Gtk.main()
