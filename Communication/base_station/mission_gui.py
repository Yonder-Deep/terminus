from Tkinter import *
class Base_Station_GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Yonder Arctic OPS")

        self.top_frame = Frame(self.master, bd = 1) 
        self.top_frame.pack( fill = BOTH, side = TOP, padx = 5, pady = 5, expand = YES)
#        self.top_label = Label(self.top_frame, text = "in top frame").pack()

        self.bot_frame = Frame(self.master, bd = 1)
        self.bot_frame.pack( fill = BOTH, side = BOTTOM, padx = 5, pady = 5, expand = YES)
 #       self.bot_label = Label(self.bot_frame, text = "in bot frame").pack()
 
        self.functions_frame = Frame(self.top_frame, height = 100, width = 100, bd = 1, relief = SUNKEN)
        self.functions_frame.pack( fill = BOTH, padx = 5, pady = 5, side = LEFT, expand = YES)
        self.functions_frame.pack_propagate(0)
        self.function_label = Label(self.functions_frame, text = "in functions frame").pack() 

        self.map_frame = Frame(self.top_frame, height = 100, width = 200, bd = 1, relief = SUNKEN)
        self.map_frame.pack( fill = BOTH, padx = 5, pady = 5, side = LEFT, expand = YES)
        self.map_frame.pack_propagate(0)
        self.map_label = Label(self.map_frame, text = "in map label").pack()

        self.status_frame = Frame(self.top_frame, height = 100, width = 100, bd = 1, relief = SUNKEN )
        self.status_frame.pack(fill = BOTH, padx = 5, pady = 5, side = LEFT, expand = YES)
        self.status_frame.pack_propagate(0)
        self.status_label = Label(self.status_frame, text = "in status label").pack()

        self.log_frame = Frame(self.bot_frame, height = 100, width = 100, bd = 1, relief = SUNKEN )
        self.log_frame.pack( fill = BOTH, padx = 5, pady = 5, side = LEFT, expand = YES)
        self.log_frame.pack_propagate(0)
        self.log_label = Label(self.log_frame, text = "in log frame").pack()
    
        self.legend_frame = Frame(self.bot_frame, height = 100, width = 100, bd = 1, relief = SUNKEN)
        self.legend_frame.pack( fill = BOTH, padx = 5, pady = 5, side = LEFT, expand = YES)
        self.legend_frame.pack_propagate(0)
        self.legend_label = Label(self.legend_frame, text = "in legend frame").pack()

        self.config_frame = Frame(self.bot_frame, height = 100, width = 100, bd = 1, relief = SUNKEN)
        self.config_frame.pack( fill = BOTH, padx = 5, pady = 5, side = LEFT, expand = YES)
        self.config_frame.pack_propagate(0)
        self.config_label = Label(self.config_frame, text = "in config frame").pack() 
        
        
root = Tk()
root.geometry("1200x600") 
Base_Station_GUI = Base_Station_GUI(root)
root.mainloop()
