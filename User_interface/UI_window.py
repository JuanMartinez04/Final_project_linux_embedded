#Import tkinter for the ui
import tkinter as tk
from tkinter import ttk
#import the functionalities
import useful_func 
import colors
import server_commands



#Making the ui main class
class Router_UI(tk.Tk):


    def __init__(self):
        super().__init__()
        #defining variables and loading icons for the ui
        self.op_icon = useful_func.open_img("./Images/op_icon.png", (20,20) )
        self.status_icon = useful_func.open_img("./Images/status_icon.png", (30,30) )
        self.settings_icon = useful_func.open_img("./Images/settings_icon.png", (50,30) )
        self.devices_icon = useful_func.open_img("./Images/devices_icon.png", (30,30) )
        self.un_logo=useful_func.open_img("./Images/un_logo.png", (80,80) )
        self.channels_list= server_commands.Channels()
        self.status_v='Online'
        #initialization of graphic functions
        self.conf_windows()
        self.confpanels()
        self.tf_controls()
        self.sf_controls()

    def conf_windows(self):
        """
        Configuration function
        self: window to be configured
        """
        self.title("BeaglePlay router") #app title
        w, h = 1024, 600        #initial size
        useful_func.centerw(self, w, h)    #resizing and centering

    def confpanels(self):
        """
        Panels creation function
        self: window to place the panels
        """
        self.toppanel= tk.Frame(self, bg=colors.TF_color, height=100)
        self.toppanel.pack(side=tk.TOP,fill='both')

        self.sidepanel= tk.Frame(self, bg=colors.LF_color, width=160)
        self.sidepanel.pack(side=tk.LEFT,fill='both',expand=False)

        self.principal = tk.Frame(self, bg=colors.PF_color)
        self.principal.pack(side=tk.RIGHT,fill='both',expand=True)

    def tf_controls(self):
        """
        Top panel features
        """

        #Options buttom for hide or show the side panel
        self.open_op = tk.Button(self.toppanel, bd=0, image=self.op_icon
                                  , bg=colors.TF_color, padx=15, command=self.toggle_panel)
        self.open_op.pack(side=tk.LEFT)
        #welcome message
        self.welcome= tk.Label(self.toppanel, text="WELCOME USER")
        self.welcome.config(fg="#fff",bg=colors.TF_color, pady=10, font=("Times", 12))
        self.welcome.pack(side=tk.LEFT)
        #autors names
        self.stem_info = tk.Label(self.toppanel,text="Juan D. Martinez-Sergio A. Cuadrado",fg="#fff",bg=colors.TF_color, 
                                   pady=10, font=("Times", 10))
        self.stem_info.pack(side= tk.RIGHT)
    

    def sf_controls(self):
        """
        Left side panel features
        """
        #UN icon
        self.un= tk.Label(self.sidepanel,image=self.un_logo,bg=colors.LF_color)
        self.un.pack(side=tk.BOTTOM,fill='both')

        #Button to open the status panel
        self.status = tk.Button(self.sidepanel, bd=0, text='Status', font=("Times",14), image=self.status_icon,compound="left",
                                relief="raised", borderwidth=1, bg=colors.LF_color, fg="#C8CACB",pady=15, padx=10, 
                                command=self.status_panel)
        self.status.pack(side=tk.TOP,expand=False,fill='both')
        #Button to open the Devices panel
        self.Devices = tk.Button(self.sidepanel, bd=0, text='Devices', font=("Times",14),image=self.devices_icon,compound="left",
                                relief="raised", borderwidth=1, bg=colors.LF_color, fg="#C8CACB",pady=15,padx=10,
                                  command=self.devices_panel)
        self.Devices.pack(side=tk.TOP,expand=False,fill= 'both')
        #Button to open the Settings panel
        self.Settings = tk.Button(self.sidepanel, bd=0, text='Settings', font=("Times",14), image=self.settings_icon,compound="left",
                                relief="raised", borderwidth=1, bg=colors.LF_color, fg="#C8CACB",pady=15, padx=10, 
                                command=self.settings_panel)
        self.Settings.pack(side=tk.TOP,expand=False, fill='both')

    
    def toggle_panel(self):
        """
        Function to hide or show the side panel
        """
        if self.sidepanel.winfo_ismapped():
            self.sidepanel.pack_forget()
        else:
            self.sidepanel.pack(side=tk.LEFT, fill='y')


    def devices_panel(self):

        """
        Devices tab construction function
        """
        #clear the principal panel
        useful_func.clear_frame(self.principal)
        #create the headers panel
        self.headers=tk.Frame(self.principal, height=60)
        self.headers.pack(side=tk.TOP, fill='both')
        #set the name tag
        self.name= tk.Label(self.headers, text='Device name', font=('Times',14), height=6,width=20,
                            relief="raised", borderwidth=2)
        self.name.pack(side=tk.LEFT, expand=True, fill='both')
        #set the IP tag
        self.ip= tk.Label(self.headers, text='Device IP',font=('Times',14), height=6,width=20,
                          relief="raised", borderwidth=1)
        self.ip.pack(side=tk.LEFT, expand=True,fill='both')
        #set the MAC tag
        self.MAC= tk.Label(self.headers, text='Device MAC',font=('Times',14), height=6,width=20,
                           relief="raised", borderwidth=1)
        self.MAC.pack(side=tk.LEFT, expand=True,fill='both')


        n,N,I,M = server_commands.devices() #get the info of each connected device
        
        for i in range(0,n): #iterate between devices
            #create a device panel to set the information for each device
            self.devices_info=tk.Frame(self.principal)
            self.devices_info.pack(side=tk.TOP, fill='both', expand=True)
            #set the device name
            self.name= tk.Label(self.devices_info, text=N[i], font=('Times',14),relief="raised", borderwidth=1,width=20)
            self.name.pack(side=tk.LEFT, expand=True, fill='both')
            #set the device IP
            self.ip= tk.Label(self.devices_info, text=I[i],font=('Times',14),relief="raised", borderwidth=1,width=20)
            self.ip.pack(side=tk.LEFT, expand=True,fill='both')
            #set the device MAC
            self.MAC= tk.Label(self.devices_info, text=M[i],font=('Times',14),relief="raised", borderwidth=1,width=20)
            self.MAC.pack(side=tk.LEFT, expand=True,fill='both')
            

 

    def settings_panel(self):

        """
        Settings tab construction function
        """
        #clear the principal panel
        useful_func.clear_frame(self.principal)
        #create the ip range panel
        self.settings_range=tk.Frame(self.principal)
        self.settings_range.pack(side=tk.TOP,expand=True,fill='both')
        #create the channel panel
        self.settings_channels=tk.Frame(self.principal)
        self.settings_channels.pack(side=tk.TOP,expand=True,fill='both')
        #create the ip save panel
        self.settings_save=tk.Frame(self.principal)
        self.settings_save.pack(side=tk.TOP,expand=True,fill= 'both')

        self.l_range=tk.Label(self.settings_range, text='Select an ip range', font=('Times',18),
                              padx=15,width=20)
        self.l_range.pack(side=tk.LEFT, fill='both',expand=True)
        #create a list selector to choose from the available ip ranges
        self.range= ttk.Combobox(self.settings_range,values=['10.0.0.10 10.0.0.100'])
        self.range.pack(side=tk.LEFT, fill='x',expand=True,padx=20)
        self.l_channel=tk.Label(self.settings_channels, text='Select an available channel', font=('Times',18),
                                padx=15,width=20)
        self.l_channel.pack(side=tk.LEFT,fill='both',expand=True)
        #create a list selector to choose from the available channels
        self.channels= ttk.Combobox(self.settings_channels, values=self.channels_list)
        self.channels.pack(side=tk.LEFT,fill='x',expand=True,padx=20)

        self.l_save= tk.Label(self.settings_save, text='Save the configuration',font=('Times',18),
                              width=20,padx=15)
        self.l_save.pack(side=tk.LEFT,fill='both',expand=True)
        #button to save the configuration
        self.save_conf= tk.Button(self.settings_save,text='SAVE',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command=self.save_config) #call the save function
        self.save_conf.pack(side=tk.LEFT,fill='x',expand=True,padx=20)


    def save_config(self):
        """
        Function to save the server configuration
        """
        #get the configurations values
        canal= self.channels.get()
        rango=self.range.get()
        server_commands.configure_hostapd(canal) #set the configurations



    def status_panel(self):

        
        """
        Status tab construction function
        """
        #cleat the pirncipal panel
        useful_func.clear_frame(self.principal)


        #server status frame
        self.status=tk.Frame(self.principal)
        self.status.pack(side=tk.TOP,expand=True,fill='both')
        #start  server frame
        self.start=tk.Frame(self.principal)
        self.start.pack(side=tk.TOP,expand=True,fill='both')
        #restard server frame
        self.restart=tk.Frame(self.principal)
        self.restart.pack(side=tk.TOP,expand=True,fill= 'both')
        #stop server frame
        self.stop=tk.Frame(self.principal)
        self.stop.pack(side=tk.TOP,expand=True,fill= 'both')


        #Status tag
        self.l_status=tk.Label(self.status, text=f'The server is {self.status_v}', font=('Times',18),
                              padx=15,width=20)
        self.l_status.pack(side=tk.LEFT, fill='both')
      

        self.l_start=tk.Label(self.start, text='Activate the network', font=('Times',18),
                                padx=15,width=20)
        self.l_start.pack(side=tk.LEFT,fill='both',expand=True)
        #button to start the server
        self.start_b= tk.Button(self.start,text='START',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command= self.start_net ) #calls the start function
        self.start_b.pack(side=tk.LEFT,fill='x',expand=True,padx=20)



        self.l_restart=tk.Label(self.restart, text='Restart the network', font=('Times',18),
                                padx=15,width=20)
        self.l_restart.pack(side=tk.LEFT,fill='both',expand=True)
        #buttom to restart the server
        self.restart_b= tk.Button(self.restart,text='RESTART',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command=self.restart_net ) #calls the restart function
        self.restart_b.pack(side=tk.LEFT,fill='x',expand=True,padx=20)


        self.l_stop=tk.Label(self.stop, text='Deactivate the network', font=('Times',18),
                                padx=15,width=20)
        self.l_stop.pack(side=tk.LEFT,fill='both',expand=True)
        #buttom to stop the server
        self.stop_b= tk.Button(self.stop,text='STOP',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command=self.stop_net )#calls the stop function
        self.stop_b.pack(side=tk.LEFT,fill='x',expand=True,padx=20)


    def start_net(self):
        """
        Function to start the accespoint 
        """

        server_commands.start_server() #calls the server startup function
        self.status_v= 'Online' #sets the server status to "online"
        self.status_panel() #update the status panel

    def restart_net(self):
        """
        Function to restart the accespoint 
        """
        self.status_v= 'Restarting' #sets the server status to "restarting"
        self.status_panel()#update the status panel
        server_commands.restart_server() #calls the server restart function
        self.status_v='Online'#sets the server status to "online"
        self.status_panel()#update the status panel

    def stop_net(self):
        """
        Function to stop the accespoint 
        """
        server_commands.stop_server()#calls the server shutdown function
        self.status_v='Offline'#sets the server status to "offlines"
        self.status_panel()#update the status panel
    




