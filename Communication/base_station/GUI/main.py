import datetime
import tkMessageBox
from Tkinter import *
from map import Map

TOP_FRAME_HEIGHT = 370
BOT_FRAME_HEIGHT = 200

# Test Constants
FONT = "Courier New"
HEADING_SIZE = 20
BUTTON_SIZE  = 11
STATUS_SIZE  = 12

# frame paddings
PADX = 5
PADY = 5

# button paddings
bPADX = 10
bPADY = 2.5

# button width and heigth (in text units) 
BUTTON_WIDTH = 17
BUTTON_HEIGHT = 2

class Main:
    def __init__(self, master):
        self.master = master
        self.master.title("Yonder Arctic OPS")

        self.top_frame = Frame(self.master, bd = 1) 
        self.top_frame.pack( fill = BOTH, side = TOP, padx = PADX, pady = PADY, expand = YES)

        self.bot_frame = Frame(self.master, bd = 1)
        self.bot_frame.pack( fill = BOTH, side = BOTTOM, padx = PADX, pady = PADY, expand = YES)
 
        self.init_function_frame()
        self.init_map_frame()
        self.init_status_frame()
        self.init_log_frame()
        self.init_calibrate_frame()
        self.init_config_frame()
        self.create_map(self.map_frame)
        self.create_function_buttons()

    def get_time(self, now):
        return now.strftime("%Y-%m-%d %H:%M:%S: ")

    # Create the frame for functions
    def init_function_frame(self):
        self.functions_frame = Frame(self.top_frame, height = TOP_FRAME_HEIGHT, width = 150, bd = 1, relief = SUNKEN)
        self.functions_frame.pack( padx = PADX, pady = PADY, side = LEFT, fill=Y, expand = NO)
        self.functions_frame.pack_propagate(0)

    # Create the frame for the x, y map
    def init_map_frame(self):
        self.map_frame = Frame(self.top_frame, height = TOP_FRAME_HEIGHT, width = TOP_FRAME_HEIGHT, bd = 1, relief = SUNKEN)
        self.map_frame.pack( fill = BOTH, padx = PADX, pady = PADY, side = LEFT, expand = YES)
        self.map_frame.pack_propagate(0)

    def init_status_frame(self):
        self.status_frame = Frame(self.top_frame, height = TOP_FRAME_HEIGHT, width = 350, bd = 1, relief = SUNKEN )
        self.status_frame.pack(fill = BOTH, padx = PADX, pady = PADY, side = LEFT, expand = NO)
        self.status_frame.pack_propagate(0)
        self.status_label = Label(self.status_frame, text = "Vehicle Stats", font = (FONT, HEADING_SIZE))
        self.status_label.pack() 
        self.status_label.place(relx = 0.22, rely = 0.02)
        
        self.position_label_string = StringVar()
        self.position_label = Label(self.status_frame, textvariable = self.position_label_string, font = (FONT, STATUS_SIZE), justify = LEFT)
        self.position_label.pack()
        self.position_label_string.set("Position \n \tX: \t Y: ")
        self.position_label.place(relx = 0.05, rely = 0.30, anchor = 'sw') 

        self.heading_label_string = StringVar()
        self.heading_label = Label(self.status_frame, textvariable = self.heading_label_string, font = (FONT, STATUS_SIZE), justify = LEFT)
        self.heading_label.pack()
        self.heading_label_string.set("Heading: ")
        self.heading_label.place(relx = 0.05, rely = 0.40, anchor = 'sw')

        self.battery_status_string = StringVar()
        self.battery_voltage = Label(self.status_frame, textvariable = self.battery_status_string, font = (FONT, STATUS_SIZE))
        self.battery_voltage.pack()
        self.battery_status_string.set("Battery Voltage: ")
        self.battery_voltage.place(relx = 0.05, rely = 0.50, anchor = 'sw')

        self.vehicle_status_string = StringVar()
        self.vehicle_status = Label(self.status_frame, textvariable = self.vehicle_status_string, font = (FONT, STATUS_SIZE))
        self.vehicle_status.pack()
        self.vehicle_status_string.set("Vehicle Status: Manual Control")
        self.vehicle_status.place(relx = 0.05, rely = 0.60, anchor = 'sw')

        self.comms_status_string = StringVar()
        self.comms_status = Label(self.status_frame, textvariable = self.comms_status_string, font = (FONT, STATUS_SIZE))
        self.comms_status.pack()
        self.comms_status_string.set("Comms Status: Not connected")
        self.comms_status.place(relx = 0.05, rely = 0.70, anchor = 'sw')

    def init_log_frame(self):
        self.log_frame = Frame(self.bot_frame, height = BOT_FRAME_HEIGHT, width = 100, bd = 1, relief = SUNKEN )
        self.log_frame.pack( fill = BOTH, padx = PADX, pady = PADY, side = LEFT, expand = YES)
        self.log_frame.pack_propagate(0)
        self.console = Text( self.log_frame, state = DISABLED ) 

        self.scrollbar = Scrollbar(self.log_frame)
        self.console.configure( yscrollcommand = self.scrollbar.set ) 
        self.scrollbar.pack(side = RIGHT, fill = Y) 
        self.console.pack()

    def log(self, time, string):
        self.console.config(state = NORMAL)
        self.console.insert(END, time + string + "\n")
        self.console.config(state = DISABLED)
        
    def init_calibrate_frame(self): 
        self.calibrate_frame = Frame(self.bot_frame, height = BOT_FRAME_HEIGHT, width = 600, bd = 1, relief = SUNKEN)
        self.calibrate_frame.pack( fill = NONE, padx = PADX, pady = PADY, side = LEFT, expand = NO)
        self.calibrate_frame.pack_propagate(0)
        self.left_calibrate_button = Button( self.calibrate_frame, text = "Calibrate LM", takefocus = False, width = 15, height = 3,
                                                padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None )
        self.left_calibrate_button.pack(side = LEFT) 

        self.right_calibrate_button = Button(self.calibrate_frame, text = "Calibrate RM", takefocus = False, width = 15, height = 3,
                                                padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None )
        self.right_calibrate_button.pack(side = RIGHT) 

        self.front_calibrate_button = Button( self.calibrate_frame, text = "Calibrate FM", takefocus = False, width = 15, height = 3,
                                                padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None )
        self.front_calibrate_button.pack(side = TOP)

        self.calibrate_all_button = Button(self.calibrate_frame, text = "Calibrate All", takefocus = False, width = 15, height = 3,
                                                padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None )
        self.calibrate_all_button.place(relx = 0.5, rely = 0.5, anchor = CENTER) 

        self.back_calibrate_button = Button( self.calibrate_frame, text = "Calibrate BM", takefocus = False, width = 15, height = 3,
                                                padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None )
        self.back_calibrate_button.pack(side = BOTTOM)

    def init_config_frame(self):
        self.config_frame = Frame(self.bot_frame, height = BOT_FRAME_HEIGHT, width = 100, bd = 1, relief = SUNKEN)
        self.config_frame.pack( fill = BOTH, padx = PADX, pady = PADY, side = LEFT, expand = YES)
        self.config_frame.pack_propagate(0)

    def abort_mission(self):
        ans = tkMessageBox.askquestion("Abort Mission", "Are you sure you want to abort the mission")
        time = self.get_time( datetime.datetime.now() )
        if ans == 'yes':
            message = "Mission aborted"
            self.log( time, message )
        else:
            message = "Clicked mission abort; continuing mission though"
            self.log( time, message )
        
    def create_function_buttons(self):
        self.origin_button           = Button(self.functions_frame, text = "Set Origin", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                              padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = self.map.new_waypoint_prompt )
        self.add_waypoint_button     = Button(self.functions_frame, text = "Add Waypoint", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT, 
                                              padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = self.map.new_waypoint_prompt)
        self.nav_to_waypoint_button  = Button(self.functions_frame, text = "Nav. to Waypoint", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                              padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None)
        self.ballast_button          = Button(self.functions_frame, text = "Start Ballast", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                              padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None)
        self.switch_to_manual_button = Button(self.functions_frame, text = "Switch to Manual", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                              padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None)
        self.stop_manual_button      = Button(self.functions_frame, text = "Stop Manual", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                              padx = bPADX, pady = bPADY, font = (FONT, BUTTON_SIZE), command = lambda: None)
        self.abort_button            = Button(self.functions_frame, text = "ABORT MISSION", takefocus = False, width = BUTTON_WIDTH, height = BUTTON_HEIGHT,
                                              padx = bPADX, pady = bPADY, bg = 'dark red', activebackground = "red", overrelief = "sunken", font = (FONT, BUTTON_SIZE), command = self.abort_mission)

        self.origin_button.pack(expand=YES, fill=BOTH, pady = 3)
        self.add_waypoint_button.pack(expand=YES, fill=BOTH, pady = 3)
        self.nav_to_waypoint_button.pack(expand=YES, fill=BOTH, pady = 3)
        self.ballast_button.pack(expand=YES, fill=BOTH, pady = 3)
        self.switch_to_manual_button.pack(expand=YES, fill=BOTH, pady = 3)
        self.stop_manual_button.pack(expand=YES, fill=BOTH, pady = 3)
        self.abort_button.pack(expand=YES, fill=BOTH, pady = 3)
        
    def create_map(self, frame):
        self.map = Map(frame)

    def on_closing(self):
        self.map.on_close()
        self.master.destroy()
        sys.exit()

# Define the window object.
root = Tk()
root.geometry("1200x600") 

# To fix HiDPI-scaling of fonts.
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
developed_res_x = 1920.0
developed_res_y = 1080.0
multiplier = screen_width / developed_res_x
HEADING_SIZE = int(HEADING_SIZE / multiplier)
BUTTON_SIZE  = int(BUTTON_SIZE  / multiplier)
STATUS_SIZE  = int(STATUS_SIZE  / multiplier)
# End fixing HiDPI-scaling of fonts.

# Create the main window.
Main = Main(root)

# Call function to properly end the program
root.protocol("WM_DELETE_WINDOW", Main.on_closing)

root.mainloop()
