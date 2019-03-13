import matplotlib
import matplotlib.axes
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.pyplot import scatter
from Tkinter import *

# Object & Map Constants
DEFAULT_FIGURE_SIZE =  30 # Window Size
DEFAULT_GRID_SIZE   = 1000 # Grid Size in Meters

# String Constants
KILOMETERS = "Kilometers (km)"
METERS     = "Meters (m)"
MILES      = "Miles (mi)"

# Color Constants
BACKGROUND_COLOR = 'darkturquoise'
AUV_PATH_COLOR   = 'red'
WAYPOINT_COLOR   = 'red'
MINOR_TICK_COLOR = 'black'

# Conversion Multiplier Constants
KM_TO_M  = 1000.000000000
MI_TO_M  = 1609.340000000
KM_TO_MI = 0000.621371000
M_TO_MI  = 0000.000621371
MI_TO_KM = 0001.609340000
M_TO_KM  = 0000.001000000

# Other Debug Constants
ZOOM_SCALAR  = 1.05
CLOSE_ENOUGH = 0.25

class Map:
    def __init__(self,  window):
        # Define the window.
        self.window = window

        # Initialize object data/information
        self.waypoints      = list()
        self.units          = METERS
        self.size           = DEFAULT_GRID_SIZE  
        self.zero_offset_x  = 0
        self.zero_offset_y  = 0
        self.old_position   = 0     # Used to move the map whenever the boat moves.
        self.press_position = [0,0]
        self.mouse_pressing = False
        self.legend_obj     = None
        self.auv_path_obj   = None
        self.auv_data       = [list(), list()]
        
        # Inialize the Tk-compatible Figure, the map, and the canvas
        self.fig    = self.init_fig()
        self.map    = self.init_map()
        self.canvas = self.init_canvas()        

        # Start listening for mouse-clicks
        self.fig.canvas.mpl_connect('button_press_event',   self.on_press)  
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event',  self.on_move)
        self.fig.canvas.mpl_connect('scroll_event',         self.on_map_scroll)  
    
        # Assign default values.
        self.set_range() # Set to default range

        # Re-draw the canvas.
        self.draw_canvas()
    
        # Add random data to test line/path functionality.
        self.add_auv_data(100,100)
        self.add_auv_data(110,105)
        self.add_auv_data(130, 109)
        self.add_auv_data(200,225)
        self.add_auv_data(240,250)
        self.add_auv_data(350, 330)
        self.add_auv_data(360, 200)
        self.add_auv_data(370, 260)
        self.add_auv_data(360, 230)
        self.add_auv_data(350, 200)
        #self.clear()
        self.draw_canvas()


    def clear(self):
        self.clear_waypoints()
        self.clear_auv_path()
        self.draw_canvas()

    def clear_auv_path(self):
        self.auv_path_obj.pop(0).remove()

    def undraw_waypoints(self):
        for waypoint in self.waypoints:
            # Remove waypoint from map.
            if waypoint[3] != None and type(waypoint[3]) != tuple:
                waypoint[3].pop(0).remove() 
                waypoint[3] = None
            
            if waypoint[4] != None:
                waypoint[4].remove()
                waypoint[4] = None

    def clear_waypoints(self):
        self.undraw_waypoints()
        del self.waypoints[:] 
    
    def zero_map(self, x=0, y=0):
        self.zero_offset_x = x
        self.zero_offset_y = y

    def on_move(self, mouse):
        if self.mouse_pressing == True and mouse.xdata != None and mouse.ydata != None:
            x_delta = (self.press_position[0] - mouse.xdata) / 6
            y_delta = (self.press_position[1] - mouse.ydata) / 6
            lim     = [self.map.get_xlim(), self.map.get_ylim()]

            self.map.set_xlim( lim[0][0] + x_delta, lim[0][1] + x_delta )
            self.map.set_ylim( lim[1][0] + y_delta, lim[1][1] + y_delta )
            
            self.draw_canvas()

    def redraw_waypoints(self):
        self.undraw_waypoints()
        for waypoint in self.waypoints:
            # Draw waypoint again.
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
        if mouse.button == 1: # 1 => Left mouse click
            self.new_waypoint_prompt(mouse.xdata, mouse.ydata)
        if mouse.button == 3: # 3 => Right mouse click
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
        prompt_window = Toplevel(self.window)
        prompt_window.title("Remove Waypoint \""+ str(waypoint[2]) + "\"?");
        prompt_window.wm_attributes('-type', 'dialog')
        prompt_submit = Button(prompt_window, text="Yes, I want to remove waypoint \""+str(waypoint[2])+"\"",
                               command=lambda:
                               [
                                self.confirm_remove_waypoint(waypoint),
                                prompt_window.destroy()
                               ])

        prompt_submit.pack(padx=5, pady=5)
        prompt_window.mainloop()

    def confirm_remove_waypoint(self, waypoint):
        self.waypoints.remove(waypoint)
        waypoint[3].pop(0).remove() 
        waypoint[4].remove();
        self.draw_canvas()
        print ("Waypoint \"" + waypoint[2] + "\" removed!")
        return;

    def new_waypoint_prompt(self, x = 0, y = 0):
        print("Opening new-waypoint prompt.")
        prompt_window = Toplevel(self.window)
        prompt_window.title("New Waypoint");
        prompt_window.wm_attributes('-type', 'dialog')
        Label(prompt_window, text = "Name").grid(row = 0)
        Label(prompt_window, text = "X").grid(row = 1)
        Label(prompt_window, text = "Y").grid(row = 2)
        prompt_input_name = Entry(prompt_window, bd = 5)
        prompt_input_name.grid(row = 0, column = 1)
        prompt_input_x = Entry(prompt_window, bd=5)
        prompt_input_x.grid(row = 1, column = 1)
        prompt_input_y = Entry(prompt_window, bd = 5)
        prompt_input_y.grid(row = 2, column = 1)
        
        prompt_input_name.insert(0, "My waypoint") # Placeholder for input
        prompt_input_x.insert(0, x) 
        prompt_input_y.insert(0, y)
        prompt_submit = Button(prompt_window, text="Save", 
                               command=lambda: # Runs multiple functions.
                               [
                                self.add_waypoint(float(prompt_input_x.get()), 
                                                  float(prompt_input_y.get()),
                                                  str(prompt_input_name.get())),
                                prompt_window.destroy()
                               ])
        
        prompt_submit.grid(row = 3, column = 0, padx=5, pady=5)
        prompt_window.mainloop();

    def add_auv_data(self, x=0, y=0):
        print("Adding AUV data at: ("+str(x)+", "+str(y)+").")
        self.auv_data[0].append(x)
        self.auv_data[1].append(y)
        self.draw_auv_path()

    def draw_auv_path(self):
        print("Drawing AUV path.")

        # Completely delete the previous line, if it exists.
        if self.auv_path_obj != None:
            self.auv_path_obj.pop(0).remove()

        # Re-draw the entire line using the newly updated x-values (auv_data[0]) and y-values (auv_data[1])
        self.auv_path_obj = self.map.plot(self.auv_data[0], self.auv_data[1], label="AUV Path", color=AUV_PATH_COLOR)
        
        # Re-draw the canvas.
        self.draw_canvas()
    
    def draw_canvas(self):
        return self.canvas.draw()        

    def init_canvas(self):
        print("Initializing the canvas.")

        # Remove excess borders around figure.
        self.fig.subplots_adjust( left = 0, bottom = 0, right = 1, top = 1, wspace = 0, hspace = 0 )
        
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

        graph.set_facecolor(BACKGROUND_COLOR)

        # Setup the Legend
        legend_elements = [Line2D([0], [0], color=AUV_PATH_COLOR, lw=2, label='AUV Path'),
                           scatter([0], [0], marker='o', color=WAYPOINT_COLOR, label='Waypoint')]
        
        graph.legend(handles=legend_elements, loc='lower right', title="Legend")

        # Change color of minor axis.
        graph.tick_params(axis='x', colors=MINOR_TICK_COLOR)
        graph.tick_params(axis='y', colors=MINOR_TICK_COLOR)
        
        return graph

    def add_waypoint(self, x=0, y=0, label="My Waypoint"):
        print("Added waypoint \"" + label + "\" at map-position (" + str(x) + ", " + str(y) + ").")
        print("Its earth-coordinates are (" + str(float(x)+self.zero_offset_x) + ", " + str(float(y)+self.zero_offset_y) + ").")

        # The code below should never fail (that would be a big problem).
        self.waypoints.append( [
                                x,y,
                                label,
                                self.map.plot(x, y, marker='o',markersize=5, color=WAYPOINT_COLOR, label=label),
                                self.map.annotate(xy=(x, y), s=label + " ("+str(round(float(x)+self.zero_offset_x,5))+","+str(round(float(y)+self.zero_offset_y,5))+")" )
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

    def on_close(self):
        self.map.cla()
        self.fig.clf()
        self.window.destroy()
