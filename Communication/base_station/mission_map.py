import matplotlib
import matplotlib.axes
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from Tkinter import *

# Object & Map Constants
DEFAULT_FIGURE_SIZE =  30 # Window Size
DEFAULT_GRID_SIZE   = 1000 # Grid Size in Meters

# String Constants
KILOMETERS = "Kilometers (km)"
METERS     = "Meters (m)"
MILES      = "Miles (mi)"

# Conversion Multiplier Constants
KM_TO_M  = 1000.000000000
MI_TO_M  = 1609.340000000
KM_TO_MI = 0000.621371000
M_TO_MI  = 0000.000621371
MI_TO_KM = 0001.609340000
M_TO_KM  = 0000.001000000

# Other Debug Constants
ZOOM_SCALAR  = 1.15
CLOSE_ENOUGH = 0.25


class map:
    def __init__(self,  window):
        # Define the window.
        self.window = window

        # Initialize object data/information
        self.waypoints     = list()
        self.auv_data      = []
        self.units         = METERS
        self.size          = DEFAULT_GRID_SIZE  
        self.zero_offset_x = 0
        self.zero_offset_y = 0
        self.old_position  = 0 # Used to move the map whenever the boat moves.
                               # => Not necessarily needed right now, but nice to have.
        self.press_position = [0,0]
        self.mouse_pressing = False
        # Inialize the Tk-compatible Figure, the map, and the canvas
        self.fig    = self.init_fig()
        self.map    = self.init_map()
        self.canvas = self.init_canvas()        

        # Start listening for mouse-clicks
        self.fig.canvas.mpl_connect('button_press_event', self.on_press)  
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.fig.canvas.mpl_connect('scroll_event', self.on_map_scroll)  
    
        # Assign default values.
        self.set_range() # Set to default range

        self.fig.subplots_adjust( left = 0, bottom = 0, right = 1, top = 1, wspace = 0, hspace = 0 )
        # Re-draw the canvas.
        self.draw_canvas()

        print(type(self.map.plot(0,0)))

    def zero_map(self, x=0, y=0):
        self.zero_offset_x = x
        self.zero_offset_y = y

    def on_move(self, mouse):
        if self.mouse_pressing == True and mouse.xdata != None and mouse.ydata != None:
            x_delta = (self.press_position[0] - mouse.xdata)/6
            y_delta = (self.press_position[1] - mouse.ydata)/6

            self.map.set_xlim( self.map.get_xlim()[0] + x_delta, self.map.get_xlim()[1] + x_delta )
            self.map.set_ylim( self.map.get_ylim()[0] + y_delta, self.map.get_ylim()[1] + y_delta )
            
            self.draw_canvas()

    def redraw_waypoints(self):
        for waypoint in self.waypoints:
            # Remove old point.
            if waypoint[3] != None and type(waypoint[3]) != tuple:
                waypoint[3].pop(0).remove() #.set_visible(False)#remove()
                waypoint[3] = None
            
            if waypoint[4] != None:
                waypoint[4].remove()
                waypoint[4] = None
            
            # Redraw new point.
            waypoint[3] = self.map.plot(waypoint[0], waypoint[1], marker='o',markersize=5, color="red"),
            waypoint[4] = self.map.annotate(xy=(waypoint[0], waypoint[1]), 
                          s=waypoint[2] + " ("+str(round(waypoint[0]+self.zero_offset_x,5))+","+str(round(waypoint[1]+self.zero_offset_y,5))+")" )
            
            # Redraw canvas.
            self.draw_canvas()

        print("Waypoints Redrawn!")

   
    def on_press(self, mouse):
        self.press_position = [mouse.xdata, mouse.ydata]
        self.mouse_pressing = True
    
    def on_release(self, mouse):
        self.mouse_pressing = False
        if mouse.xdata != None and mouse.xdata - self.press_position[0] == 0: # Same x as the press.
            if mouse.ydata != None and mouse.ydata - self.press_position[1] == 0: # Same y as the press.
                self.on_map_click(mouse)
    
    def on_map_scroll(self, mouse):
        if mouse.button == 'down': # down => Scroll down
            self.zoom_out()
        if mouse.button == 'up':   # up   =>  Scroll up
            self.zoom_in()
 
    def on_map_click(self, mouse):
        if mouse.button == 3: # 3 => Right mouse click
            self.new_waypoint_prompt(mouse.xdata, mouse.ydata)
        if mouse.button == 1: # 1 => Left mouse click
            self.try_remove_waypoint(mouse.xdata, mouse.ydata)

    def update_boat_position(self, x = 0, y = 0):
        return

    def try_remove_waypoint(self, x = 0, y = 0):
        close = CLOSE_ENOUGH * (self.size / DEFAULT_GRID_SIZE)

        if self.units == METERS:
            close += 100
        
        for waypoint in self.waypoints:
            if x - close < waypoint[0] and x + close  > waypoint[0]: # Close enough on x-axis.
                if y - close < waypoint[1] and y + close > waypoint[1]: # Close enough on y-axis.
                    self.remove_waypoint_prompt(waypoint)
                    return
    
    def remove_waypoint_prompt(self, waypoint):
        print("Opening remove-waypoint prompt.")
        prompt_window = Tk()
        prompt_window.title("Remove Waypoint "+ str(waypoint[2]) + "?");
        prompt_window.wm_attributes('-type', 'dialog')
        prompt_submit = Button(prompt_window, text="Yes, I want to remove waypoint "+str(waypoint[2]), command=lambda: self.confirm_remove_waypoint(waypoint, prompt_window ))
        prompt_submit.pack(padx=5, pady=5)
        prompt_window.mainloop()

    def confirm_remove_waypoint(self, waypoint, prompt_window):
        if prompt_window:
            prompt_window.destroy()

        self.waypoints.remove(waypoint)
        waypoint[3].pop(0).remove() 
        waypoint[4].remove();
        self.draw_canvas()
        print ("Waypoint removed!")
        return;

    def new_waypoint_prompt(self, x = 0, y = 0):
        print("Opening new-waypoint prompt.")
        prompt_window = Tk()
        prompt_window.title("New Waypoint");
        prompt_window.wm_attributes('-type', 'dialog')
        prompt_input  = Entry(prompt_window, bd=5)
        prompt_input.insert(0, 'My Waypoint') # Placeholder for input
        prompt_submit = Button(prompt_window, text="Save", command=lambda: self.add_waypoint(x, y, str(prompt_input.get()), prompt_window ))

        prompt_input.pack(side=LEFT)
        prompt_submit.pack(side=RIGHT)
        prompt_window.mainloop();

    def add_auv_data(self, x=10, y=10):
        print("Adding UAV data at: ("+x+", "+y+").")
        self.auv_data.append([x,y])
        self.draw_auv_path()

    def draw_auv_path():
        print("Drawing UAV path.")
        
        for point in self.auv_data:
            rel_to_map = [point[0] - self.zero_offset_x,
                          point[1] - self.zero_offset_y ] 
            # self.map.plot(

        #plot lines, etcc..
        return

    def draw_canvas(self):
        return self.canvas.draw()        

    def init_canvas(self):
        print("Initializing the canvas.")
        # Create a tkinter-usable component.
        canvas = FigureCanvasTkAgg(self.fig, master=self.window) 
        canvas.get_tk_widget().pack()
        return canvas

    def init_fig(self):
        print ("Initializing figure...")
        fig = Figure(figsize=(DEFAULT_FIGURE_SIZE, DEFAULT_FIGURE_SIZE))
        return fig 

    def init_map(self):
        print("Initializing map...")
        graph = self.fig.add_subplot(111, xmargin = -0.49, ymargin = -0.49)
        graph.grid(b=True, which='major', axis='both')
        
        graph.spines['left'].set_position(('data', 0))

        # turn off the right spine/ticks
        graph.spines['right'].set_color('none')
        graph.yaxis.tick_left()

        # set the y-spine
        graph.spines['bottom'].set_position(('data', 0))

        # turn off the top spine/ticks
        graph.spines['top'].set_color('none')
        graph.xaxis.tick_bottom()

        graph.set_facecolor('xkcd:cyan')
        graph.legend(loc = 'lower right', title = "Waypoint legend")
        
        return graph

    def add_waypoint(self, x=0, y=0, label="My Waypoint", prompt_window=0):
        if prompt_window: # If we are coming in from a user-prompt, destroy their window.
            prompt_window.destroy()
    
        print( "Adding waypoint " + label + " at position (" + str(x) + ", " + str(y) + ").\n"+
               " It's longitude is "+ str(x+self.zero_offset_x))

        self.waypoints.append( [
                                x,y,
                                label,
                                self.map.plot(x, y, marker='o',markersize=5, color="red"),
                                self.map.annotate(xy=(x, y), s=label + " ("+str(round(x+self.zero_offset_x,5))+","+str(round(y+self.zero_offset_y,5))+")" )
                                ] )
        
        self.draw_canvas()
        return [x,y]

    def zoom_out(self):
        print("Zooming out.")
        xlim = self.map.get_xlim()
        ylim = self.map.get_ylim()
        self.size *= ZOOM_SCALAR
        self.set_range(x=[xlim[0]*ZOOM_SCALAR, xlim[1]*ZOOM_SCALAR],
                       y=[ylim[0]*ZOOM_SCALAR, ylim[1]*ZOOM_SCALAR])

    def zoom_in(self):
        print("Zooming in.")
        xlim = self.map.get_xlim()
        ylim = self.map.get_ylim()
        self.size /= ZOOM_SCALAR
        self.set_range(x=[xlim[0]/ZOOM_SCALAR, xlim[1]/ZOOM_SCALAR], 
                       y=[ylim[0]/ZOOM_SCALAR, ylim[1]/ZOOM_SCALAR])

    def set_range(self, x=[-DEFAULT_GRID_SIZE, DEFAULT_GRID_SIZE], y=[-DEFAULT_GRID_SIZE, DEFAULT_GRID_SIZE]):
        print("Changing grid size to x="+str(x)+", and y="+str(y)+".") 
        self.map.set_xlim(x)
        self.map.set_ylim(y)
        self.draw_canvas()

    def set_units(self, unit=METERS):
        print("Changing units from " + self.units + " to "  + unit)
        multiplier = 1

        # Convert KM -> M
        if unit == METERS and self.units == KILOMETERS:
            multiplier = KM_TO_M
        
        # Convert MI -> M
        if unit == METERS and self.units == MILES:
            multiplier = MI_TO_M

        # Convert KM -> MI
        if unit == MILES and self.units == KILOMETERS:
            multiplier = KM_TO_MI
        
        # Convert M -> MI
        if unit == MILES and self.units == METERS:
            multiplier = M_TO_MI

        # Convert MI -> KM
        if unit == KILOMETERS and self.units == MILES:
            multiplier = MI_TO_KM
        
        # Convert M -> KM
        if unit == KILOMETERS and self.units == METERS:
            multiplier = M_TO_KM
      

        # Apply conversion
        for waypoint in self.waypoints:
            waypoint[0] *= multiplier
            waypoint[1] *= multiplier

        self.size *= multiplier
        self.units = unit
        self.set_range(x=self.size, y=self.size)

        self.draw_canvas()

    def draw_waypoints(self):
        for waypoint in self.waypoints:
            waypoint[2] = (self.map.plot(waypoint[0], waypoint[1], marker='o',markersize=5, color="red")) # Adds to waypoint
            waypoint[3] = (self.map.annotate(xy=(waypoint[0], waypoint[1]), s=waypoint[2] + " ("+str(round(waypoint[0],3))+","+str(round(waypoint[1],3))+")" ))


