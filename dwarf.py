import json
import requests
import tkinter
import tkinter.messagebox
import customtkinter
from tkintermapview import TkinterMapView

customtkinter.set_appearance_mode('Dark')
customtkinter.set_default_color_theme('blue')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        #region Window
        
        ## Window creation
        self.title('dwarf.py')
        self.geometry(f'{1400}x{800}')

        ## Grid layout
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        #endregion

        #region Sidebar frame
        
        ## Frame creation & grid layout
        self.sidebar_frame = customtkinter.CTkFrame(self, width=150, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(3, weight=1)

        ## Logo
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text='dwarf', font=customtkinter.CTkFont(size=25, weight='bold'))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky='n')

        ## Address
        self.string_input_button = customtkinter.CTkButton(self.sidebar_frame, text='Search by address', command=self.search_by_address)
        self.string_input_button.grid(row=1, column=0, padx=20, pady=10, sticky='n')

        ## IP
        self.string_input_button = customtkinter.CTkButton(self.sidebar_frame, text='Search by IP', command=self.search_by_ip)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=10, sticky='n')

        ## Appearance
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['Light', 'Dark', 'System'], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=3, column=0, padx=20, pady=10, sticky='s')

        ## Scaling
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=['80%', '90%', '100%', '110%', '120%'], command=self.change_scaling)
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(10,20), sticky='s')

        #endregion

        #region Map frame
        
        ## Frame creation & grid layout
        self.map_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.map_frame.grid(row=0, column=1, rowspan=1, sticky='nsew')
        self.map_frame.grid_rowconfigure(0, weight=1)
        self.map_frame.grid_columnconfigure(0, weight=1)
        
        ## Map widget
        self.map_widget = TkinterMapView(self.map_frame, corner_radius=8)
        self.map_widget.grid(row=0, rowspan=1, column=0, columnspan=1, padx=(0,20), pady=20, sticky='nswe')
        
        #endregion

        #region Default values

        self.map_widget.set_address('Polska')
        self.appearance_mode_optionemenu.set('Dark')
        self.scaling_optionemenu.set('100%')

        #endregion
    
    def search_by_address(self):
        dialog = customtkinter.CTkInputDialog(text='Enter an address:', title='Search by address')
        self.map_widget.set_address(dialog.get_input())

    def search_by_ip(self):
        dialog = customtkinter.CTkInputDialog(text='Enter an IP address:', title='Search by IP')
        request_url = 'https://geolocation-db.com/jsonp/' + dialog.get_input()
        response = requests.get(request_url)
        output = response.content.decode()
        output = output.split('(')[1].strip(')')
        output  = json.loads(output)
        self.map_widget.set_position(output['latitude'], output['longitude']) # TODO: some IP aren't working, requests.exceptions.ConnectionError: ('Connection aborted.', OSError(0, 'Error'))
        self.map_widget.set_zoom(15)

    def change_appearance_mode(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace('%', '')) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

if __name__ == '__main__':
    App().mainloop()
