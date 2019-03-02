import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

DEFAULT_GRID_SIZE = 10 # In kilometers

KILOMETERS = "Kilometers (km)"
METERS     = "Meters (m)"
MILES      = "Miles (mi)"

class map:
    def __init__(self,  window):
        # Define the window.
        self.window = window

        # Initialize object data/information
        self.waypoints     = []
        self.uav_data      = []
        self.units         = KILOMETERS
        self.size          = DEFAULT_GRID_SIZE  
        self.zero_offset_x = 0
        self.zero_offset_y = 0

        # Inialize the Tk-compatible Figure, the map, and the canvas
        self.fig    = self.init_fig()
        self.map    = self.init_map()
        self.canvas = self.init_canvas()        

        # Start listening for mouse-clicks
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)  
        self.set_range() # Set to default range of [-10,10] KM 

        # Add some test waypoints
        self.add_waypoint( 5, 5)
        self.add_waypoint(-5,-5)

        self.zoom_out()
        self.zoom_out()


        self.zoom_in()
        self.zoom_in()
        self.zoom_in()
        self.zoom_in()
    
        # Re-draw the canvas.
        self.draw_canvas()
        
        self.set_units(MILES)


    def zero_map(self, x=0, y=0):
        self.zero_offset_x = x
        self.zero_offset_y = y

    def on_click(self, event):
        prompt_window = Tk()
        prompt_window.title("New Waypoint");
        prompt_window.wm_attributes('-type', 'dialog')
        prompt_input  = Entry(prompt_window, bd=5)
        prompt_input.insert(0, 'My Waypoint') # Placeholder for input
        prompt_submit = Button(prompt_window, text="Save", command=lambda: self.add_waypoint(event.xdata, event.ydata, str(prompt_input.get()), prompt_window ))

        prompt_input.pack(side=LEFT)
        prompt_submit.pack(side=RIGHT)
        prompt_window.mainloop();

    def add_uav_data(self, x=10, y=10):
        self.uav_data.append([x,y])
        self.draw_uav_path()

    def draw_uav_path():
        #plot lines, etcc..
        return

    def draw_canvas(self):
        return self.canvas.draw()        

    def init_canvas(self):
        # Create a tkinter-usable component.
        canvas = FigureCanvasTkAgg(self.fig, master=self.window) 
        canvas.get_tk_widget().pack()
        return canvas

    def init_fig(self):
        fig = Figure(figsize=(20,20))
        return fig 

    def init_map(self):
        graph = self.fig.add_subplot(111)
        graph.grid(b=True, which='major', axis='both')
        
        graph.spines['left'].set_position('zero')

        # turn off the right spine/ticks
        graph.spines['right'].set_color('none')
        graph.yaxis.tick_left()

        # set the y-spine
        graph.spines['bottom'].set_position('zero')

        # turn off the top spine/ticks
        graph.spines['top'].set_color('none')
        graph.xaxis.tick_bottom()

        graph.set_facecolor('xkcd:cyan')
        return graph

    def add_waypoint(self, x=0, y=0, label="My Waypoint", prompt=0):

        if prompt: # If we are coming in from a user-prompt, destroy their window.
            prompt.destroy()
    
        print( "Adding waypoint " + label + " at position (" + str(x) + ", " + str(y) + ").\n"+
               " It's longitude is "+ str(x+self.zero_offset_x))

        self.waypoints.append( [x,y,label] )
        self.draw_waypoints()
        self.draw_canvas()
        return [x,y]

    def zoom_out(self):
        self.set_range(x=self.size*1.3, y=self.size*1.3)
        self.draw_canvas()

    def zoom_in(self):
        self.set_range(x=self.size/1.3, y=self.size/1.3)
        self.draw_canvas()

    def set_range(self, x=DEFAULT_GRID_SIZE, y=DEFAULT_GRID_SIZE):
        self.map.set_xlim([-x,x])
        self.map.set_ylim([-y,y])
        self.size = x
        self.draw_canvas()

    def set_units(self, unit=METERS):
        multiplier = 1

        # Convert KM -> M
        if unit == METERS and self.units == KILOMETERS:
            multiplier = 1000
        
        # Convert MI -> M
        if unit == METERS and self.units == MILES:
            multiplier = 1609.34

        # Convert KM -> MI
        if unit == MILES and self.units == KILOMETERS:
            multiplier = 0.621371
        
        # Convert M -> MI
        if unit == MILES and self.units == METERS:
            multiplier = 0.000621371

        # Convert MI -> KM
        if unit == KILOMETERS and self.units == MILES:
            multiplier = 1.60934
        
        # Convert M -> KM
        if unit == KILOMETERS and self.units == METERS:
            multiplier = 0.001
      

        # Apply conversion
        for waypoint in self.waypoints:
            waypoint[0] *= multiplier
            waypoint[1] *= multiplier

        self.size *= multiplier
        self.set_range(x=self.size, y=self.size)

        self.draw_waypoints()
        self.draw_canvas()

    def draw_waypoints(self):
        for waypoint in self.waypoints:
            self.map.plot(waypoint[0], waypoint[1], marker='o',markersize=5, color="red")
            self.map.annotate(xy=(waypoint[0], waypoint[1]), s=waypoint[2] + " ("+str(round(waypoint[0],3))+","+str(round(waypoint[1],3))+")" )

root = Tk()
start = map(root)
root.mainloop()
