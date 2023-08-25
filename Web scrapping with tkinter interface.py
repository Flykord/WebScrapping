# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 12:02:44 2023

@author: danie
"""

import requests
from bs4 import BeautifulSoup
import customtkinter
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import urllib.request
from PIL import Image
from io import BytesIO

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Scrapping")
        self.geometry(f"{1100}x{580}")
        self.image = []
        self.photoImages = []
        self.modifiedPhoto = []
        self.paths =[]
        self.modifiedImages = []
        self.filesMetadata=[]
        self.imageLabels = []
        self.imageTextbox = []
        self.imageButtons = []
        self.imagesToButtons=[]
        self.imageMessages=[]
        self.writtedImages=[]
        self.modifiedPath = "/dicom-tempModified/"
   
        #path ="C:/Users/danie/Downloads/10 Semestre/new1.png"
        #label['image']=img # Show Image  
        #self.imBase = PhotoImage(file=path)
        # configure grid layout
        #https://www.pythontutorial.net/tkinter/tkinter-grid/
        self.grid_columnconfigure((0,4), weight=1)
        self.grid_columnconfigure((1,2), weight=4)        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure((1, 2, 3,4), weight=4)

        
        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Scrapping", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 2))

        self.logo_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="E-commerce", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label1.grid(row=1, column=0, padx=20, pady=(0, 2))

        self.logo_label1 = customtkinter.CTkLabel(self.sidebar_frame, text="pages", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label1.grid(row=2, column=0, padx=20, pady=(0, 10))

        self.apply_button = customtkinter.CTkButton(self.sidebar_frame, text="Acerca de",
                                                           command=self.open_input_dialog_event)
        self.apply_button.grid(row=5, column=0, padx=20, pady=(10, 10))                            

        
        

        # create tabview
        self.tabview = customtkinter.CTkTabview(self)
        self.tabview.grid(row=1, column=1, columnspan=2, rowspan=5, padx=(10, 0), pady=(0, 0), sticky="nsew")
        self.tabview.add("Images")       
        self.tabview.tab("Images").grid_columnconfigure(0, weight=3)  # configure grid of individual tabs
        self.imagesSpace=customtkinter.CTkScrollableFrame(master=self.tabview.tab("Images"))
        self.imagesScroll = customtkinter.CTkScrollbar(master=self.tabview.tab("Images"))
        self.imagesScroll.grid(row=0,column=0,sticky="ns")
        # create radiobutton frame
        self.options_frame = customtkinter.CTkFrame(self)
        self.options_frame.grid(row=0, column=3, rowspan=2, padx=(20, 20), pady=(20, 0), sticky="nsew")              
        self.opciones_title = customtkinter.CTkLabel(master=self.options_frame, text="Image Manipulation:")
        self.opciones_title.grid(row=0, column=0, columnspan=1, padx=10, pady=10, sticky="")

        self.filters_menu = customtkinter.CTkOptionMenu(self.options_frame, dynamic_resizing=False,
                                                        values=["Open Image", "Draw points"])
        self.filters_menu.grid(row=1, column=0, padx=20, pady=(20, 10))   
                
        # create slider and progressbar frame
        self.navbar_frame = customtkinter.CTkFrame(self)
        self.navbar_frame.grid(row=0, column=1, rowspan=1, columnspan=2, padx=(20, 20), pady=(20, 0), sticky="n")
        self.navbar_frame.grid_columnconfigure(1, weight=4)
        self.navbar_frame.grid_columnconfigure((0,2,3), weight=0)
        self.navbar_frame.grid_rowconfigure(0, weight=0)

        self.cutOffFreq2 = customtkinter.CTkLabel(self.navbar_frame, text="0.500", font=customtkinter.CTkFont(size=10, weight="bold"))
        
        self.labelDesc = customtkinter.CTkLabel(master=self.navbar_frame,text="Producto : ", anchor="w")
        self.labelDesc.grid(row=1, column=0, padx=(0, 0), pady=(20, 20))
        self.producTextbox = customtkinter.CTkTextbox(master=self.navbar_frame,width=200,height=20)
        self.producTextbox.grid(row=1,column=2,padx=(2,2),pady=(1,1),sticky="nsew")
        self.openFile_button = customtkinter.CTkButton(master=self.navbar_frame, width=10, height=10, text="Enviar", fg_color="#1561F0", text_color=("gray10", "#DCE4EE"),command=self.scrapData)        
        self.openFile_button.grid(row=1, column=3, padx=(10, 0), pady=(20, 20), sticky="nsew")        
   
        # create checkbox and switch frame
        self.theme_frame = customtkinter.CTkFrame(self)
        self.theme_frame.grid(row=2, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.appearance_mode_label = customtkinter.CTkLabel(self.theme_frame, text="Apariencia de la aplicación:", anchor="w")
        self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.theme_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.theme_frame, text="Escala:", anchor="w")
        self.scaling_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.theme_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=4, column=0, padx=20, pady=(10, 20))
        self.scaling_label = customtkinter.CTkLabel(self.theme_frame, text="Generar PDF:", anchor="w")
        self.scaling_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.genPdf_button = customtkinter.CTkButton(master=self.theme_frame, width=10, height=10, text="PDF", fg_color="#1561F0", text_color=("gray10", "#FAFAFA"))        
        self.genPdf_button.grid(row=6, column=0, padx=(0, 0), pady=(20, 20), sticky="nsew")        
        
        # set default values              
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")        
        self.filters_menu.set("Tools")
        self.appearance_mode_optionemenu.set("Tema")
        self.recording = False
        self.currentFilter = ""   
        
    def open_input_dialog_event(self):              
            CTkMessagebox(title="Image Info", message="\nFacultad de Ingeniería, UASLP\nDesarrollado por:\nVázquez Garcia Daniel Alejandro\n")        
       
    def change_appearance_mode_event(self, new_appearance_mode: str):
            customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
            new_scaling_float = int(new_scaling.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)
            
    def scrapData(self):
        product = self.producTextbox.get("0.0", "end")
        print(product)
        self.producTextbox.delete("0.0","end")
        url_base="https://www.mercadolibre.com.mx/"
        #url_with_search = "https://listado.mercadolibre.com.mx/sworks#D[A:sworks]"
        #r=requests.get(url_with_search)
        #content = r.content
        url_consult="https://listado.mercadolibre.com.mx/{}#D[A:{}]".format(product.replace(' ','-'),product)
        r=requests.get(url_consult)
        print(r)
        content = r.content
        print(content)
        print(url_consult)
        soup = BeautifulSoup(content,'html.parser')
        #print(soup)
        
        #Extraer objetos
        all_divs=soup.find_all('div',{'class':'andes-card'})
        products = []
        
        for item in all_divs:
            data={}
            data_images={}
            data_price={}
            data['nombre articulo']=item.find('h2',{'class':'ui-search-item__title'}).text
            
            #data['imagen']=item.find('img',{'class':'ui-search-result-image__element'}).text
            imagen = item.find('img',{'class':'ui-search-result-image__element'})
            
            if imagen.has_attr('data-src'):
                data['imagen']=imagen['data-src']
            data['price']=item.find('span',{'class':'andes-money-amount__fraction'}).text
            products.append(data)
            #print(im_src)
        
        self.muestraProductos(products)
            
            
    def muestraProductos(self,data):
        col=0
        row=0
        for prod in data:
            print(prod)
            if col==10:
                row+=1
                col=0
            self.createView(prod,row,col)
            col+=1
            
    def createView(self,prod,row,col):
        
        im = self.getImage(prod['imagen'])
        #print(prod['imagen'])
        your_image = customtkinter.CTkImage(light_image=im, size=(130 ,100))
        self.productName = customtkinter.CTkLabel(master=self.tabview.tab("Images"),text="", image=your_image)
        self.productName.grid(row=row, column=col, padx=(4,4), pady=(4, 4),sticky="nsew")
    
    def getImage(self,link):
        print(link)
        response = requests.get(link)

        # Verifica si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Lee los datos de la imagen en formato binario
            image_data = BytesIO(response.content)

            # Abre la imagen con Pillow
            imagen = Image.open(image_data)

     
        else:
            print("No se pudo obtener la imagen desde el enlace.")
        return imagen
if __name__ == "__main__":
    app = App()
    app.mainloop()