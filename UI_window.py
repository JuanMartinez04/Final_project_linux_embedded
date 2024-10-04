import tkinter as tk
import useful_func 
import colors
import server_commands
#from tkinter import filedialog
from tkinter import ttk
#from PIL import ImageTk, Image


class Router_UI(tk.Tk):


    def __init__(self):
        super().__init__()
        self.op_icon = useful_func.open_img("./images/op_icon.png", (20,20) )
        self.status_icon = useful_func.open_img("./images/status_icon.png", (30,30) )
        self.settings_icon = useful_func.open_img("./images/settings_icon.png", (50,30) )
        self.devices_icon = useful_func.open_img("./images/devices_icon.png", (30,30) )
        self.un_logo=useful_func.open_img("./images/un_logo.png", (80,80) )
        self.channels_list= server_commands.channels()
        self.status_v='Activado'
        self.conf_windows()
        self.confpanels()
        self.tf_controls()
        self.sf_controls()

    def conf_windows(self):
        self.title("BeaglePlay router status")
        w, h = 1024, 600        
        useful_func.centerw(self, w, h)   

    def confpanels(self):
        self.toppanel= tk.Frame(self, bg=colors.TF_color, height=100)
        self.toppanel.pack(side=tk.TOP,fill='both')

        self.sidepanel= tk.Frame(self, bg=colors.LF_color, width=160)
        self.sidepanel.pack(side=tk.LEFT,fill='both',expand=False)

        self.principal = tk.Frame(self, bg=colors.PF_color)
        self.principal.pack(side=tk.RIGHT,fill='both',expand=True)

    def tf_controls(self):

        self.open_op = tk.Button(self.toppanel, bd=0, image=self.op_icon
                                  , bg=colors.TF_color, padx=15, command=self.toggle_panel)
        self.open_op.pack(side=tk.LEFT)

        self.welcome= tk.Label(self.toppanel, text="WELCOME USER")
        self.welcome.config(fg="#fff",bg=colors.TF_color, pady=10, font=("Times", 12))
        self.welcome.pack(side=tk.LEFT)

        self.stem_info = tk.Label(self.toppanel,text="Juan-Sergio",fg="#fff",bg=colors.TF_color, 
                                   pady=10, font=("Times", 10))
        self.stem_info.pack(side= tk.RIGHT)
    

    def sf_controls(self):
        self.un= tk.Label(self.sidepanel,image=self.un_logo,bg=colors.LF_color)
        self.un.pack(side=tk.BOTTOM,fill='both')
        self.status = tk.Button(self.sidepanel, bd=0, text='Status', font=("Times",14), image=self.status_icon,compound="left",
                                relief="raised", borderwidth=1, bg=colors.LF_color, fg="#C8CACB",pady=15, padx=10, 
                                command=self.status_panel)
        self.status.pack(side=tk.TOP,expand=False,fill='both')

        self.Devices = tk.Button(self.sidepanel, bd=0, text='Devices', font=("Times",14),image=self.devices_icon,compound="left",
                                relief="raised", borderwidth=1, bg=colors.LF_color, fg="#C8CACB",pady=15,padx=10,
                                  command=self.devices_panel)
        self.Devices.pack(side=tk.TOP,expand=False,fill= 'both')

        self.Settings = tk.Button(self.sidepanel, bd=0, text='Settings', font=("Times",14), image=self.settings_icon,compound="left",
                                relief="raised", borderwidth=1, bg=colors.LF_color, fg="#C8CACB",pady=15, padx=10, 
                                command=self.settings_panel)
        self.Settings.pack(side=tk.TOP,expand=False, fill='both')

    
    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.sidepanel.winfo_ismapped():
            self.sidepanel.pack_forget()
        else:
            self.sidepanel.pack(side=tk.LEFT, fill='y')


    def devices_panel(self):
        useful_func.clear_frame(self.principal)

        self.headers=tk.Frame(self.principal, height=60)
        self.headers.pack(side=tk.TOP, fill='both')

        self.name= tk.Label(self.headers, text='Nombre del dispositivo', font=('Times',14), height=6,width=20,
                            relief="raised", borderwidth=2)
        self.name.pack(side=tk.LEFT, expand=True, fill='both')
        self.ip= tk.Label(self.headers, text='IP del dispositivo',font=('Times',14), height=6,width=20,
                          relief="raised", borderwidth=1)
        self.ip.pack(side=tk.LEFT, expand=True,fill='both')
        self.MAC= tk.Label(self.headers, text='MAC del dispositivo',font=('Times',14), height=6,width=20,
                           relief="raised", borderwidth=1)
        self.MAC.pack(side=tk.LEFT, expand=True,fill='both')


        I,M,N = server_commands.devices()
        n=len(N)
        for i in range(0,n):
            
            self.devices_info=tk.Frame(self.principal)
            self.devices_info.pack(side=tk.TOP, fill='both', expand=True)

            self.name= tk.Label(self.devices_info, text=N[i], font=('Times',14),relief="raised", borderwidth=1,width=20)
            self.name.pack(side=tk.LEFT, expand=True, fill='both')
            self.ip= tk.Label(self.devices_info, text=I[i],font=('Times',14),relief="raised", borderwidth=1,width=20)
            self.ip.pack(side=tk.LEFT, expand=True,fill='both')
            self.MAC= tk.Label(self.devices_info, text=M[i],font=('Times',14),relief="raised", borderwidth=1,width=20)
            self.MAC.pack(side=tk.LEFT, expand=True,fill='both')
            

 

    def settings_panel(self):
        useful_func.clear_frame(self.principal)

        self.settings_range=tk.Frame(self.principal)
        self.settings_range.pack(side=tk.TOP,expand=True,fill='both')

        self.settings_channels=tk.Frame(self.principal)
        self.settings_channels.pack(side=tk.TOP,expand=True,fill='both')

        self.settings_save=tk.Frame(self.principal)
        self.settings_save.pack(side=tk.TOP,expand=True,fill= 'both')

        self.l_range=tk.Label(self.settings_range, text='Seleccione un rango de ip', font=('Times',18),
                              padx=15,width=20)
        self.l_range.pack(side=tk.LEFT, fill='both',expand=True)
        self.range= ttk.Combobox(self.settings_range,values=['10.0.0.10 10.0.0.100'])
        self.range.pack(side=tk.LEFT, fill='x',expand=True,padx=20)
        self.l_channel=tk.Label(self.settings_channels, text='Seleccione un canal disponible', font=('Times',18),
                                padx=15,width=20)
        self.l_channel.pack(side=tk.LEFT,fill='both',expand=True)

        self.channels= ttk.Combobox(self.settings_channels, values=self.channels_list)
        self.channels.pack(side=tk.LEFT,fill='x',expand=True,padx=20)

        self.l_save= tk.Label(self.settings_save, text='Desea guardar la nueva configuración',font=('Times',18),
                              width=20,padx=15)
        self.l_save.pack(side=tk.LEFT,fill='both',expand=True)
        self.save_conf= tk.Button(self.settings_save,text='SAVE',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command=self.save_config)
        self.save_conf.pack(side=tk.LEFT,fill='x',expand=True,padx=20)


    def save_config(self):
        canal= self.channels.get()
        rango=self.range.get()
        server_commands.configure_hostapd(canal)



    def status_panel(self):
        useful_func.clear_frame(self.principal)

        self.status=tk.Frame(self.principal)
        self.status.pack(side=tk.TOP,expand=True,fill='both')

        self.start=tk.Frame(self.principal)
        self.start.pack(side=tk.TOP,expand=True,fill='both')

        self.restart=tk.Frame(self.principal)
        self.restart.pack(side=tk.TOP,expand=True,fill= 'both')

        self.stop=tk.Frame(self.principal)
        self.stop.pack(side=tk.TOP,expand=True,fill= 'both')


        
        self.l_status=tk.Label(self.status, text=f'El servidor está {self.status_v}', font=('Times',18),
                              padx=15,width=20)
        self.l_status.pack(side=tk.LEFT, fill='both')
      

        self.l_start=tk.Label(self.start, text='Activar la red', font=('Times',18),
                                padx=15,width=20)
        self.l_start.pack(side=tk.LEFT,fill='both',expand=True)

        self.start_b= tk.Button(self.start,text='START',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command= self.start_net )
        self.start_b.pack(side=tk.LEFT,fill='x',expand=True,padx=20)



        self.l_restart=tk.Label(self.restart, text='Reiniciar la red', font=('Times',18),
                                padx=15,width=20)
        self.l_restart.pack(side=tk.LEFT,fill='both',expand=True)
        self.restart_b= tk.Button(self.restart,text='RESTART',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command=self.restart_net )
        self.restart_b.pack(side=tk.LEFT,fill='x',expand=True,padx=20)


        self.l_stop=tk.Label(self.stop, text='Desactivar la red', font=('Times',18),
                                padx=15,width=20)
        self.l_stop.pack(side=tk.LEFT,fill='both',expand=True)
        self.stop_b= tk.Button(self.stop,text='STOP',font=('Times',14),relief='raised',borderwidth=2,
                                  bg=colors.LB_color, command=self.stop_net )
        self.stop_b.pack(side=tk.LEFT,fill='x',expand=True,padx=20)


    def start_net(self):
        server_commands.start_server()
        self.status_v= 'Activo'
        self.status_panel()

    def restart_net(self):
        self.status_v= 'Reiniciando'
        server_commands.restart_server()
        self.status_v='Activo'
        self.status_panel()

    def stop_net(self):
        server_commands.stop_server()
        self.status_v='Apagado'
        self.status_panel()
    




