import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,GLib

import numpy as np
from numpy import pi
from scipy.integrate import odeint


def parse_float(s):
    """Parse string and return float, also accept π and pi"""
    s = s.replace("π", "pi")
    return float(eval(s))


def derivs(y,t,l,m,g):
    """Derivatives for double pendulum"""
    theta1,theta2,p1,p2 = y 

    Delta = theta1-theta2
    cos_Delta = np.cos(Delta)
    sin_Delta = np.sin(Delta)

    denom = l**2*m*(1+sin_Delta**2)
    C = (p1*p2*sin_Delta-(p1**2+2*p2**2-2*p1*p2*cos_Delta)*sin_Delta*cos_Delta)/denom

    dtheta1 =   (p1-p2*cos_Delta)/denom
    dtheta2 = (2*p2-p1*cos_Delta)/denom
    dp1 = -2*m*g*l*np.sin(theta1)-C
    dp2 = -  m*g*l*np.sin(theta2)+C

    return np.array((dtheta1,dtheta2,dp1,dp2))


class DoublePendulum(Gtk.Window):
    def __init__(self):
        super(DoublePendulum, self).__init__()

        self.run = False
        self.timer = None

        self.set_title("Double pendulum")

        self.connect("destroy", Gtk.main_quit)

        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(hbox)

        self.darea = darea = Gtk.DrawingArea()
        darea.connect("draw", self.expose)
        darea.set_size_request(500, 500)
        hbox.pack_start(darea, True, True, 0)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        self.grid = grid = Gtk.Grid()
        vbox.pack_start(grid, True, True, 0)

        label = Gtk.Label()
        label.set_markup("<big>Parameter</big>")
        grid.attach(label, 0, 0, 2, 1)

        # length
        label_l = Gtk.Label()
        label_l.set_markup("<big>l:</big> ")
        self.entry_l = entry_l = Gtk.Entry()
        entry_l.set_text("1")
        grid.attach(label_l, 0, 1, 1, 1)
        grid.attach(entry_l, 1, 1, 1, 1)

        # mass
        label_m = Gtk.Label()
        label_m.set_markup("<big>m:</big> ")
        self.entry_m = entry_m = Gtk.Entry()
        entry_m.set_text("1")
        grid.attach(label_m, 0, 2, 1, 1)
        grid.attach(entry_m, 1, 2, 1, 1)

        # gravity
        label_g = Gtk.Label()
        label_g.set_markup("<big>g:</big> ")
        self.entry_g = entry_g = Gtk.Entry()
        entry_g.set_text("9.81")
        grid.attach(label_g, 0, 3, 1, 1)
        grid.attach(entry_g, 1, 3, 1, 1)

        # epsilon
        label_eps = Gtk.Label()
        label_eps.set_markup("<big>ε:</big> ")
        self.entry_eps = entry_eps = Gtk.Entry()
        entry_eps.set_text("0")
        grid.attach(label_eps, 0, 4, 1, 1)
        grid.attach(entry_eps, 1, 4, 1, 1)

        # omega
        label_omega = Gtk.Label()
        label_omega.set_markup("<big>ω:</big> ")
        self.entry_omega = entry_omega = Gtk.Entry()
        entry_omega.set_text("1")
        grid.attach(label_omega, 0, 5, 1, 1)
        grid.attach(entry_omega, 1, 5, 1, 1)

        label = Gtk.Label()
        label.set_markup("\n<big>Anfangsbedingungen</big>")
        grid.attach(label, 0, 6, 2, 1)

        # theta1
        label_theta1 = Gtk.Label()
        label_theta1.set_markup("<big>ϑ<sub>1</sub>:</big> ")
        self.entry_theta1 = entry_theta1 = Gtk.Entry()
        entry_theta1.set_text("π")
        grid.attach(label_theta1, 0, 7, 1, 1)
        grid.attach(entry_theta1, 1, 7, 1, 1)

        # theta2
        label_theta2 = Gtk.Label()
        label_theta2.set_markup("<big>ϑ<sub>2</sub>:</big> ")
        self.entry_theta2 = entry_theta2 = Gtk.Entry()
        entry_theta2.set_text("π")
        grid.attach(label_theta2, 0, 8, 1, 1)
        grid.attach(entry_theta2, 1, 8, 1, 1)

        # p1
        label_p1 = Gtk.Label()
        label_p1.set_markup("<big>p<sub>1</sub>:</big> ")
        self.entry_p1 = entry_p1 = Gtk.Entry()
        entry_p1.set_text("0")
        grid.attach(label_p1, 0, 9, 1, 1)
        grid.attach(entry_p1, 1, 9, 1, 1)

        # p2
        label_p2 = Gtk.Label()
        label_p2.set_markup("<big>p<sub>2</sub>:</big> ")
        self.entry_p2 = entry_p2 = Gtk.Entry()
        entry_p2.set_text("0")
        grid.attach(label_p2, 0, 10, 1, 1)
        grid.attach(entry_p2, 1, 10, 1, 1)

        label = Gtk.Label()
        label.set_markup("\n<big>Simulation</big>")
        grid.attach(label, 0, 11, 2, 1)

        # simulation time
        label_T = Gtk.Label()
        label_T.set_markup("<big>T:</big> ")
        self.entry_T = entry_T = Gtk.Entry()
        entry_T.set_text("60")
        grid.attach(label_T, 0, 12, 1, 1)
        grid.attach(entry_T, 1, 12, 1, 1)

        # FPS
        label_fps = Gtk.Label()
        label_fps.set_markup("<big>FPS:</big> ")
        self.spin_fps = spin_fps = Gtk.SpinButton()
        spin_fps.set_range(10,100)
        spin_fps.set_value(50)
        spin_fps.set_increments(1,5)
        grid.attach(label_fps,  0, 13, 1, 1)
        grid.attach(spin_fps,   1, 13, 1, 1)

        # start and stop buttons
        button_hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.button_start = button_start = Gtk.Button(stock=Gtk.STOCK_APPLY)
        self.button_stop  = button_stop  = Gtk.Button(stock=Gtk.STOCK_CANCEL)
        button_start.connect("clicked", self.start_cb)
        button_stop. connect("clicked", self.stop_cb)
        button_hbox.pack_start(button_start, True, True, 0)
        button_hbox.pack_start(button_stop,  True, True, 0)
        vbox.pack_start(button_hbox, False, True, 0)

        self.show_all()


    def start_cb(self, widget):
        # stop running simulations
        self.stop_cb(None)

        # get parameters
        l = parse_float(self.entry_m.get_text())
        m = parse_float(self.entry_m.get_text())
        g = parse_float(self.entry_g.get_text())
        eps = parse_float(self.entry_eps.get_text())
        omega = parse_float(self.entry_omega.get_text())

        # get initial conditions
        theta1 = parse_float(self.entry_theta1.get_text())
        theta2 = parse_float(self.entry_theta2.get_text())
        p1 = parse_float(self.entry_p1.get_text())
        p2 = parse_float(self.entry_p2.get_text())

        # get numerical parameters
        T = float(self.entry_T.get_text())
        fps = float(self.spin_fps.get_value())
        dt = int(1000/fps)

        # calculate solution
        v0 = [theta1,theta2,p1,p2]
        t = np.arange(0, T, dt/1000.)
        self.data = odeint(derivs,v0,t,args=(l,m,g))

        # start simulation
        self.i = 0
        self.run = True
        self.timer = GLib.timeout_add(dt, self.on_timer)


    def stop_cb(self,widget):
        if self.run:
            GLib.source_remove(self.timer)
            self.run = False


    def on_timer(self):
        if self.run:
            self.darea.queue_draw()

            self.i += 1
            if self.i >= len(self.data)-1:
                # simulation finished
                self.run = False
                return False

            return True
        else:
            self.run = False
            return False


    def draw(self, l1=1, l2=1):
        resolution = min(self.get_size())

        cr = self.cr
        cr.scale(resolution, resolution)

        # white background
        cr.rectangle(0, 0, 1, 1)
        cr.set_source_rgb(1, 1, 1)
        cr.fill()

        if self.run:
            index = self.i
            theta1,theta2 = self.data[index,0], self.data[index,1]
            deltal = 0.47/(l1+l2)

            point1 = l1*np.sin(theta1)*deltal+0.5, l1*np.cos(theta1)*deltal+0.5
            point2 = l2*np.sin(theta2)*deltal+point1[0], l2*np.cos(theta2)*deltal+point1[1]

            # rods
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(0.5, 0.5) # aufhaengepunkt
            cr.line_to(point1[0], point1[1])
            cr.line_to(point2[0], point2[1])
            cr.set_line_width(0.007)
            cr.stroke()

            # point for m1
            cr.set_source_rgb(1, 0, 0)
            cr.arc(point1[0], point1[1], 0.02, 0, 2*pi)
            cr.fill()
            cr.stroke()

            # point for m2
            cr.set_source_rgb(0, 1, 0)
            cr.arc(point2[0], point2[1], 0.02, 0, 2*pi)
            cr.fill()
            cr.stroke()

    
    def expose(self, widget, event):
        self.cr = widget.get_property("window").cairo_create()
        self.draw()


if __name__ == "__main__":
    DoublePendulum()
    Gtk.main()
