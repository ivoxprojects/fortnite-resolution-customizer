# IVOX 2023 (github.com/ivoxprojects)
# Open-Source free for distribution

import customtkinter
from customtkinter import filedialog
from configparser import ConfigParser
import os
import ctypes
import sys

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('FRC')
        self.geometry('300x150')
        self.resizable(False, False)
        self.iconbitmap('icon.ico')
        self.eval('tk::PlaceWindow . center')

        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1, 3), weight=1)

        self.font = customtkinter.CTkFont('Bahnschrift', 15)

        # Width Height Fps
        self.label_width = customtkinter.CTkLabel(self, text='Width X', font=self.font) # Label
        self.entry_width = customtkinter.CTkEntry(self, height=40, justify='center')
        self.label_height = customtkinter.CTkLabel(self, text='Height Y', font=self.font) # label
        self.entry_height = customtkinter.CTkEntry(self, height=40, justify='center')
        self.label_fpslock = customtkinter.CTkLabel(self, text='FPS Lock', font=self.font) # Label
        self.entry_fpslock = customtkinter.CTkEntry(self, height=40, justify='center')

        self.label_width.grid(row=0, column=0, sticky='s') # label
        self.entry_width.grid(row=1, column=0, padx=10, sticky='n')
        self.label_height.grid(row=0, column=1, sticky='s') # Label
        self.entry_height.grid(row=1, column=1, padx=10, sticky='n')
        self.label_fpslock.grid(row=0, column=2, sticky='s') # Label
        self.entry_fpslock.grid(row=1, column=2, padx=10, sticky='n')

        # Apply
        self.button_apply = customtkinter.CTkButton(self, text='APPLY', font=self.font, fg_color='white', text_color='black', hover_color='lightgreen', command=self.apply)
        self.button_apply.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=10)

    def find_config(self):
        self.default = os.path.expanduser('~' + '\AppData\Local\FortniteGame\Saved\Config\WindowsClient\GameUserSettings.ini')
        
        try:
            with open('path.txt', 'r') as file:
                return file.read()
        except:
            if not os.path.exists(self.default):
                ctypes.windll.user32.MessageBoxW(0, 'Fortnite game config could not be found, please click OK and manually select your game config', 'Error', 0)
                self.manual_path = filedialog.askopenfilename(filetypes=[('Configuration settings files', '*.ini')])

                if self.manual_path:
                    with open('path.txt', 'w') as file:
                        file.write(self.manual_path)
            else:
                with open('path.txt', 'w') as file:
                    file.write(self.default)

        # Confirm Existance
        with open('path.txt', 'r') as file:
                return file.read()

    def apply(self):

        parser = ConfigParser()
        parser.read(config)

        try:
            width = int(self.entry_width.get())
            height = int(self.entry_height.get())
            fpslock = '{:.6f}'.format(int(self.entry_fpslock.get()))

            parser.set('/Script/FortniteGame.FortGameUserSettings', 'ResolutionSizeX', str(width)) # X
            parser.set('/Script/FortniteGame.FortGameUserSettings', 'lastuserconfirmedresolutionsizex', str(width))
            parser.set('/Script/FortniteGame.FortGameUserSettings', 'ResolutionSizeY', str(height)) # Y
            parser.set('/Script/FortniteGame.FortGameUserSettings', 'lastuserconfirmedresolutionsizey', str(height)) 
            parser.set('/Script/FortniteGame.FortGameUserSettings', 'FrameRateLimit', str(fpslock)) # FPSLOCK

            with open(config, 'w') as file:
                parser.write(file)

            ctypes.windll.user32.MessageBoxW(0, 'Config changed successfully', 'Message', 0)
        except:
            ctypes.windll.user32.MessageBoxW(0, 'One or more entries are empty', 'Error', 0)

if __name__ == '__main__':
    app = App()

    config = app.find_config()
    print(f'config found successfully at > {config}')

    try:
        parser = ConfigParser()
        parser.read(config)

        width = parser.get('/Script/FortniteGame.FortGameUserSettings', 'ResolutionSizeX')
        height = parser.get('/Script/FortniteGame.FortGameUserSettings', 'ResolutionSizeY')
        fpslock = int(float(parser.get('/Script/FortniteGame.FortGameUserSettings', 'FrameRateLimit')))

        app.entry_width.configure(placeholder_text = width)
        app.entry_height.configure(placeholder_text = height)
        app.entry_fpslock.configure(placeholder_text = fpslock)
    except:
        ctypes.windll.user32.MessageBoxW(0, 'Fortnite game config could not be found, please click OK and manually select your game config', 'Error', 0)
        config = filedialog.askopenfilename(filetypes=[('Configuration settings files', '*.ini')])
        
        with open('path.txt', 'w') as file:
            file.write(config)

        python = sys.executable
        os.execl(python, python, * sys.argv)

    app.mainloop()
