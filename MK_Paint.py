

from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
import PIL.ImageGrab as ImageGrab
from tkinter import filedialog
import math
from turtle import ScrolledCanvas, width
from PIL import ImageGrab
from PIL import ImageTk

class MkPaint:
    def __init__(self, width, height, title):
        self.screen = Tk()
        self.screen.title(title)
        self.screen.geometry(str(width) + 'x' + str(height))

        self.last_x, self.last_y = None, None
        self.shape_id = None
        self.shape_id1=None
        self.end_x=None
        self.end_y= None
        self.center_x=None
        self.center_y=None
        self.undo=[]
        self.redo=[]

        #Buttons_Area
        self.button_area = Frame(self.screen, width = width, height = 100, bg = "pink")
        self.button_area.grid(row=0, column=0, sticky = NW)

        #Canvas
        self.canvas = Canvas(self.screen, width = width, height = height, bg = "white")
        self.canvas.grid(row=1, column=0)

#---------------------------File--------------------------------------------
        self.save = Frame(self.button_area, width=70, height=100, bg="light pink",
                                 relief= RAISED, borderwidth=4)
        self.save.grid(row= 0, column= 0)
#new image
        
        self.new_button = Button(self.save, text="NEW", width=7, bg="bisque",
                                     command= self.create_new)
        self.new_button.grid(row=0, column=0)

#load canvas

        self.load_button = Button(self.save, text = "LOAD", width=7, bg="bisque",
                                   command = self.load_canvas)
        self.load_button.grid(row= 1, column=0)

#save image

        self.save_button = Button(self.save, text="SAVE", width=7, bg="bisque",
                                     command= self.save_opt)
        self.save_button.grid(row=0, column=1)
      
#clear canvas
      
        self.clear_button = Button(self.save, text = "CLEAR", width=7
                                   ,bg="bisque", command = self.clear_canvas)
        self.clear_button.grid(row= 1, column=1)
        

        self.file_label = Label(self.save, text=" File ", width=7,bg="light pink")
        self.file_label.grid(row=2)

#------------------------selection Tool-----------------------------------
        
        self.image = Frame(self.button_area, width =80, height =100,bg="light pink",
                           relief= RAISED, borderwidth=4)
        self.image.grid(row=0, column =1)

        self.rect = None
        self.selected_region = None
        self.drag_data = None
        self.painting_items = []

        self.selection_button = Button(self.image, text = "Select", width= 9,bg="bisque",
                                    command = self.on_selectionButton)
        self.selection_button.grid(row = 1, column = 0)
     
        self.color_button = Button(self.image, text = "Edit Color",bg="bisque",
                                  width= 9, command = self.select_color)
        self.color_button.grid(row=0, column=0)

        self.image_label = Label(self.image, text=" Image ", width=9, bg="light pink")
        self.image_label.grid(row=2)

#---------------------Tools---------------------------

        self.tools = Frame(self.button_area, width = 70, height = 70,bg="light pink",
                           relief= RAISED, borderwidth=4)
        self.tools.grid(row = 0, column = 2);
        #brush
        self.brush_button = Button(self.tools, text = "BRUSH", width= 7,bg="bisque",
                                    command = self.on_BrushButton)
        self.brush_button.grid(row = 0, column = 0)
       
        self.brush_color = 'blue'
        self.fillcolor=None
         
        #eraser
        self.eraser_button = Button(self.tools, text = "Eraser", width= 7,bg="bisque",
                                    command = self.on_EraserButton)
        self.eraser_button.grid(row = 1, column = 0)
        self.eraser_color = 'white'

        #bucket
        self.bucket_button = Button(self.tools, text = "Bucket", width= 7,bg="bisque",
                                    command = self.on_FillButton)
        self.bucket_button.grid(row = 0, column = 1)

        #color picker
        self.picker_button = Button(self.tools, text = "Picker", width= 7,bg="bisque",
                                    command = self.on_picker_button)
        self.picker_button.grid(row = 1, column = 1)

        #magnifier
        self.zoom_in_button = Button(self.tools, text = "zoom in", width= 7,bg="bisque",
                                    command = self.on_zoomInButton)
        self.zoom_in_button.grid(row = 0, column = 2)
        self.zoom_out_button = Button(self.tools, text = "zoom out", width= 7,bg="bisque",
                                    command = self.on_zoomOutButton)
        self.zoom_out_button.grid(row = 1, column = 2)
        self.canvas_width = 1360
        self.canvas_height = 700
        self.current_zoom = 1.0


        self.tools_label = Label(self.tools, text="Tools", width=7, bg="light pink" )
        self.tools_label.grid(row = 3, column = 1)

        #color
        self.stroke_clr_b = StringVar()
        self.stroke_clr_b.set("black")
        self.stroke_clr_e = StringVar()
        self.stroke_clr_e.set("white")
        
 #--------------------------size----------------------------------
        self.size = Frame(self.button_area, width = 50, height = 70,
                          bg="light pink", relief=RAISED, borderwidth=4)
        self.size.grid(row = 0, column = 3 );
        
        self.stroke_size = IntVar()
        self.stroke_size.set(1)

        self.default_button = Button(self.size, text="Default", bg="bisque", width=7, 
                                     command= self.on_defBrushButton)
        self.default_button.pack()
        self.options = [2,5,8,11,14,17]

        self.size_list = OptionMenu(self.size, self.stroke_size, *self.options )
        self.size_list.config(bg="bisque")
        self.size_list.pack()

        self.size_label = Label(self.size, text="Size", width=7, bg="light pink")
        self.size_label.pack()

#----------------------shapes----------------------------------------------

        self.shapes = Frame(self.button_area, width=70, height=70,bg="light pink", relief=RAISED, borderwidth=4)
        self.shapes.grid(row= 0, column= 4)

        #circle button
        self.circle_button = Button(self.shapes, text = "Circle", width=5,bg="bisque",
                                  command = self.on_circleButton_pressed)
        self.circle_button.grid(row=0, column=0)

        #oval button
        self.oval_button = Button(self.shapes, text = "Oval", width=5,bg="bisque",
                                  command = self.on_ovalButton_pressed)
        self.oval_button.grid(row=1, column=0)

        #Rectangle button
        self.rectangle_button = Button(self.shapes, text = "Rect", width=5,bg="bisque",
                                  command = self.on_rectangleButton_pressed)
        self.rectangle_button.grid(row=0, column=1)

        #cube button
        self.cube_button = Button(self.shapes, text = "Cube", width=5,bg="bisque",
                                  command = self.on_cubeButton_pressed)
        self.cube_button.grid(row=1, column=1)

        #equi triangle button
        self.equitriangle_button = Button(self.shapes, text = "Tri1", width=5,bg="bisque",
                                  command = self.on_equitriangleButton_pressed)
        self.equitriangle_button.grid(row=0, column=2)

       
        #right triangle button
        self.rightTriangle_button = Button(self.shapes, text = "Tri2", width=5,bg="bisque",
                                  command = self.on_rightTriangleButton_pressed)
        self.rightTriangle_button.grid(row=1, column=2)

        #pentagon button
        self.pentagon_button = Button(self.shapes, text = "Penta", width=5,bg="bisque",
                                  command = self.on_pentagonButton_pressed)
        self.pentagon_button.grid(row=0, column=3)

        #hexagon button
        self.hexagon_button = Button(self.shapes, text = "Hexa", width=5,bg="bisque",
                                  command = self.on_hexagonButton_pressed)
        self.hexagon_button.grid(row=1, column=3)

        #star button
        self.star_button = Button(self.shapes, text = "Star", width=5,bg="bisque",
                                  command = self.on_starButton_pressed)
        self.star_button.grid(row=0, column=4)
       
        #polygon button
        self.polygon_button = Button(self.shapes, text="Polygon", bg="bisque", width=6, 
                                     command= self.on_polygonButton_pressed)
        self.polygon_button.grid(row=0, column=6)
        
        self.polygon_list = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  
        self.current_polygon = StringVar(value=3)
        self.polygon_menu = OptionMenu(self.shapes, self.current_polygon, *self.polygon_list)#, command=self.set_polygon)
       
        self.polygon_menu.config(bg="bisque")
        self.polygon_menu.grid(row=1, column=6)

        #line button
        self.line_button = Button(self.shapes, text="Line", bg="bisque", width=5, 
                                     command= self.on_lineButton_pressed)
        self.line_button.grid(row=1, column=4)

        #heart button
        self.heart_button = Button(self.shapes, text="Heart", bg="bisque", width=5, 
                                     command= self.on_heartButton_pressed)
        self.heart_button.grid(row=0, column=5)

        #curve button
        self.curve_button = Button(self.shapes, text="curve", bg="bisque", width=5,  
                                     command= self.on_curveButton_pressed)
        self.curve_button.grid(row=1, column=5)

        self.shape_label = Label(self.shapes, text="Shape", width=5, bg="light pink")
        self.shape_label.grid(row=2, column =3)

#---------------------------colors-------------------------------------
        
        #primary colors
        self.pri_colors = Frame(self.button_area, width=70, height=70,bg="light pink",
                                 relief=RAISED, borderwidth=4)
        self.pri_colors.grid(row=0, column=5)

        self.black_clr_button = Button(self.pri_colors, bg="black",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("black"), self.stroke_clr_e.set("black")))
        self.black_clr_button.grid(row=0, column=0)

        self.white_clr_button = Button(self.pri_colors, bg="white",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("white"), self.stroke_clr_e.set("white")))
        self.white_clr_button.grid(row=1, column=0)

        self.grey_clr_button = Button(self.pri_colors, bg="grey30",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("grey30"), self.stroke_clr_e.set("grey30")))
        self.grey_clr_button.grid(row=0, column=1)

        self.lgrey_clr_button = Button(self.pri_colors, bg="grey62",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("grey62"), self.stroke_clr_e.set("grey62")))
        self.lgrey_clr_button.grid(row=1, column=1)

        self.brown_clr_button = Button(self.pri_colors,bg="brown",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("brown"), self.stroke_clr_e.set("brown")))
        self.brown_clr_button.grid(row=0, column=2)

        self.yellow_clr_button = Button(self.pri_colors, bg="yellow",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("yellow"), self.stroke_clr_e.set("yellow")))
        self.yellow_clr_button.grid(row=1, column=2)

        self.red_clr_button = Button(self.pri_colors, bg="red",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("red"), self.stroke_clr_e.set("red")))
        self.red_clr_button.grid(row=0, column=3)

        self.pink_clr_button = Button(self.pri_colors, bg="pink",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("pink"), self.stroke_clr_e.set("pink")))
        self.pink_clr_button.grid(row=1, column=3)

        self.orange_clr_button = Button(self.pri_colors, bg="orange",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("orange"), self.stroke_clr_e.set("orange")))
        self.orange_clr_button.grid(row=0, column=4)

        self.gold_clr_button = Button(self.pri_colors, bg="gold",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("gold"), self.stroke_clr_e.set("gold")))
        self.gold_clr_button.grid(row=1, column=4)

        self.green_clr_button = Button(self.pri_colors, bg="green",width=3,
                                     command= lambda: (self.stroke_clr_b.set("green"), self.stroke_clr_e.set("green")))
        self.green_clr_button.grid(row=0, column=5)

        self.green2_clr_button = Button(self.pri_colors, bg="green2",width=3,
                                     command= lambda: (self.stroke_clr_b.set("green2"), self.stroke_clr_e.set("green2")))
        self.green2_clr_button.grid(row=1, column=5)

        self.blue_clr_button = Button(self.pri_colors, bg="blue",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("blue"), self.stroke_clr_e.set("blue")))
        self.blue_clr_button.grid(row=0, column=6)

        self.blue2_clr_button = Button(self.pri_colors, bg="cyan2",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("cyan2"), self.stroke_clr_e.set("cyan2")))
        self.blue2_clr_button.grid(row=1, column=6)

        self.purple_clr_button = Button(self.pri_colors, bg="purple",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("purple"), self.stroke_clr_e.set("purple")))
        self.purple_clr_button.grid(row=0, column=7)

        self.purple2_clr_button = Button(self.pri_colors, bg="MediumPurple2",width=3,  
                                     command= lambda: (self.stroke_clr_b.set("MediumPurple2"), self.stroke_clr_e.set("MediumPurple2")))
        self.purple2_clr_button.grid(row=1, column=7)

        self.prev1_color_button = Button(self.pri_colors, bg="white" ,width=3,
                                         command = lambda:self.stroke_clr_b.set(self.prev1_color.get()))
        self.prev1_color_button.grid(row=0, column=8)
        self.prev1_color = StringVar()
        self.prev1_color.set("white")

        self.prev2_color_button = Button(self.pri_colors, bg="white",width=3, 
                                         command = lambda:self.stroke_clr_b.set(self.prev2_color.get()))
        self.prev2_color_button.grid(row=1, column=8)
        self.prev2_color = StringVar()
        self.prev2_color.set("white")

        self.color_label = Label(self.pri_colors, text="color", width=4, bg="light pink")
        self.color_label.grid(row=2, column =4)
        self.color_label = Label(self.pri_colors, width=4, bg="light pink")
        self.color_label.grid(row=2, column =0)
        self.color_label = Label(self.pri_colors, width=4,bg="light pink")
        self.color_label.grid(row=2, column =1)
        self.color_label = Label(self.pri_colors, width=4, bg="light pink")
        self.color_label.grid(row=2, column =2)
        self.color_label = Label(self.pri_colors, width=4,bg="light pink")
        self.color_label.grid(row=2, column =3)
        self.color_label = Label(self.pri_colors, width=4, bg="light pink")
        self.color_label.grid(row=2, column =5)
        self.color_label = Label(self.pri_colors, width=4,bg="light pink")
        self.color_label.grid(row=2, column =6)
        self.color_label = Label(self.pri_colors, width=4, bg="light pink")
        self.color_label.grid(row=2, column =7)

        self.empty = Frame(self.button_area, width=144, height=70,bg="light pink",
                                 relief=FLAT, borderwidth=4)
        self.empty.grid(row=0, column=6)

#------------------------functions-------------------------------------
    def run(self):
        self.screen.mainloop() 

      
#color pallate------------------------------------------------------
    def select_color(self):
        selected_color = colorchooser.askcolor(title= "Select Color")
        if selected_color[1] == None:
            self.stroke_clr_b.set("black")
        else:
            self.stroke_clr_b.set(selected_color[1])
            self.prev2_color.set(self.prev1_color.get())
            self.prev1_color.set(selected_color[1])
            
            self.prev1_color_button["bg"] = self.prev1_color.get()
            self.prev2_color_button["bg"] = self.prev2_color.get()
        #self.brush_color = selected_color[1]

#eraser-------------------------------------------------------------------------

    def on_EraserButton(self):
        self.canvas.bind("<B1-Motion>", self.eraser_draw)
        self.canvas["cursor"] = DOTBOX
        self.canvas.bind("<ButtonRelease-1>", self.eraser_draw_clear)
         
    def eraser_draw(self,event):
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                                capstyle = ROUND,fill = self.stroke_clr_e.get(),
                                width = self.stroke_size.get())
        self.last_x, self.last_y = event.x, event.y
        
    def eraser_draw_clear(self, event):
        self.last_x, self.last_y = None, None

#brush-----------------------------------------------------------------------
    def on_BrushButton(self):
        self.canvas.bind("<B1-Motion>", self.brush_draw)
        self.canvas["cursor"] = "pencil"
        self.canvas.bind("<ButtonRelease-1>", self.brush_draw_clear)
         
    def brush_draw(self, event):
        
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                                capstyle = ROUND, fill = self.stroke_clr_b.get(),
                                width = self.stroke_size.get())
        self.last_x, self.last_y = event.x, event.y

    def brush_draw_clear(self, event):
        self.last_x, self.last_y = None, None

    def on_defBrushButton(self):
        self.canvas.bind("<B1-Motion>", self.def_brush_draw)
        self.canvas["cursor"] = "pencil"
        self.canvas.bind("<ButtonRelease-1>", self.def_brush_draw_clear)
         
    def def_brush_draw(self, event):
        
        if self.last_x == None:
            self.last_x, self.last_y = event.x, event.y
            return
        width = 1
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, 
                                capstyle = ROUND, fill = self.stroke_clr_b.get(),
                                width=width )
        self.last_x, self.last_y = event.x, event.y

    def def_brush_draw_clear(self, event):
        self.last_x, self.last_y = None, None

#bucket fill--------------------------------------------------------------   
    def on_FillButton(self):
         self.canvas.unbind("<Button-1>")
         self.canvas.unbind("<ButtonRelease-1>")
         self.canvas.unbind("<B1-Motion>")
         self.canvas["cursor"] = "spraycan"
         self.canvas.bind("<Button-1>",self.bucket_fill)
    
    def bucket_fill(self, event):
          x, y = event.x, event.y
          pixel_color = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")

          if pixel_color != self.stroke_clr_b.get():
               stack = [(x, y)]  

               while stack:
                    curr_x, curr_y = stack.pop()
                    
                    itemId = self.canvas.find_closest(curr_x, curr_y)
                    itemColor = self.canvas.itemcget(itemId, "fill")

                    if itemColor == pixel_color:
                         self.canvas.itemconfigure(itemId, fill=self.stroke_clr_b.get())
                         stack.append((x - 1, y))  
                         stack.append((x + 1, y))  
                         stack.append((x, y - 1)) 
                         stack.append((x, y + 1)) 

          self.canvas.update()
    def def_bucket_clear(self, event):
        self.last_x, self.last_y = None, None
#color picker---------------------------------------------------------------------------------
    def on_picker_button(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas["cursor"] = "exchange"
        self.canvas.bind("<Button-1>",self.color_picker)

    def color_picker(self, event):
        x = (event.x)
        y = (event.y)
        color = self.canvas.itemcget(self.canvas.find_closest(x, y), "fill")
        self.stroke_clr_b.set( color)


#magnifier-----------------------------------------------------------------------------        

    def on_zoomInButton(self):
         self.canvas.unbind("<Button-1>")
         self.canvas.unbind("<ButtonRelease-1>")
         self.canvas.unbind("<B1-Motion>")
         self.canvas["cursor"] = "fleur"
         self.canvas.bind("<Button-1>", self.zoom_in)

    def on_zoomOutButton(self):
         self.canvas.unbind("<Button-1>")
         self.canvas.unbind("<ButtonRelease-1>")
         self.canvas.unbind("<B1-Motion>")
         self.canvas["cursor"] = "fleur"
         
         self.canvas.bind("<Button-1>", self.zoom_out)
    
    def zoom_in(self, event):
        x, y = event.x, event.y
        if self.current_zoom < 2.331: 
              self.current_zoom *= 1.1

              new_height = int(self.canvas_height * self.current_zoom)
              new_width = int(self.canvas_width * self.current_zoom)
              self.canvas.config(width = new_width, height = new_height)
              self.canvas.scale("all", x, y, 1.1, 1.1)
    
    def zoom_out(self, event):
        x, y = event.x, event.y
        if self.current_zoom > 1.0:
              self.current_zoom /= 1.1
              
              new_width = int(self.canvas_width * self.current_zoom)
              new_height = int(self.canvas_height *self.current_zoom)
              self.canvas.config(width=new_width, height=new_height)
              self.canvas.scale("all", x, y, 1/1.1, 1/1.1)
    
#--------------------------------------heart--------------------------------------------------
    def on_heartButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_heart)
        self.canvas.bind("<ButtonRelease-1>", self.draw_heart_end)

    def draw_heart(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3 = (x2 + x1) / 2
        y3 = (y2 + y1) / 2
        width = abs(x2 - x1)
        height = abs(y2 - y1)

        # Adjust the height of the heart to make it visually pleasing
        height *= 0.8

        heart_points = [
            (x3, y1 + height),                  # Top center point
            (x1, y1 + height * 0.6),             # Top left curve point
            (x1, y1 + height * 0.2),             # Left middle curve point
            (x3 - width * 0.3, y1),              # Bottom left curve point
            (x3, y1 + height * 0.2),             # Bottom center left curve point
            (x3 + width * 0.3, y1),              # Bottom right curve point
            (x2, y1 + height * 0.2),             # Bottom center right curve point
            (x2, y1 + height * 0.6),             # Right middle curve point
        ]

        self.shape_id = self.canvas.create_polygon(heart_points,
                                                   outline=self.stroke_clr_b.get(), width=self.stroke_size.get(), fill="")

    def draw_heart_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#-----------------------------------circle---------------------------------------------------
    def on_circleButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_circle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_circle_end)

    def draw_circle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x-radius) , (self.last_y-radius)
        x2, y2 = (self.last_x+radius) , (self.last_y+radius)

        self.shape_id = self.canvas.create_oval(x1, y1, x2, y2, outline = self.stroke_clr_b.get(),
                                                width = self.stroke_size.get())
    def draw_circle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#--------------------------------------------------cube---------------------------------------------
    def on_cubeButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_cube)
        self.canvas.bind("<ButtonRelease-1>", self.draw_cube_end)

    def draw_cube(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        radius = abs(self.last_x-event.x) + abs(self.last_y-event.y)
        x1, y1 = (self.last_x-radius) , (self.last_y-radius)
        x2, y2 = (self.last_x+radius) , (self.last_y+radius)

        self.shape_id = self.canvas.create_rectangle(x1, y1, x2, y2, outline = self.stroke_clr_b.get(),
                                                       width = self.stroke_size.get())
    def draw_cube_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

#-----------------------------------------------rectangle----------------------------------------------
    def on_rectangleButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_rectangle_end)

    def draw_rectangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_rectangle(self.last_x, self.last_y, event.x, event.y
                                                     , outline = self.stroke_clr_b.get(),
                               width = self.stroke_size.get())
    def draw_rectangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

#---------------------------------------pentagon---------------------------------------------
    def on_pentagonButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_pentagon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_pentagon_end)

    def draw_pentagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        total_radius = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        outer_radius = total_radius / 2

        angle = 53.92
        penta_points = []  
        for i in range(5):
            pent_angle = math.radians(i * 72 + angle)
            x = x1 + outer_radius * math.cos(pent_angle)
            y = y1 + outer_radius * math.sin(pent_angle)
            penta_points.extend([x, y])

        self.shape_id = self.canvas.create_polygon(penta_points, outline = self.stroke_clr_b.get(),
                               width = self.stroke_size.get(), fill="")
    def draw_pentagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#-----------------------------------hexagon--------------------------------------
    def on_hexagonButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_hexagon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_hexagon_end)

    def draw_hexagon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        total_radius = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        outer_radius = total_radius / 2

        hexa_points = []
        for i in range(6):
            outer_angle = 2 * i * math.pi / 6
            x = x1 + outer_radius * math.cos(outer_angle)
            y = y1 + outer_radius * math.sin(outer_angle)
            hexa_points.extend([x, y])
        self.shape_id = self.canvas.create_polygon(hexa_points, outline = self.stroke_clr_b.get(),
                                                    width = self.stroke_size.get(), fill="")
    def draw_hexagon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
#---------------------------------oval---------------------------------------
    def on_ovalButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_oval)
        self.canvas.bind("<ButtonRelease-1>", self.draw_oval_end)

    def draw_oval(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_oval(self.last_x, self.last_y, event.x, event.y, 
                                                outline = self.stroke_clr_b.get(), width = self.stroke_size.get())
    def draw_oval_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#--------------------------------------------triangle--------------------------------------
    def on_equitriangleButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_equitriangle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_equitriangle_end)

    def draw_equitriangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3= ((x2+x1)-x2-(x2-x1))
        y3 = y2
        self.shape_id=self.canvas.create_polygon(x1,y1 , x2, y2, x3,y3,
                                                 outline = self.stroke_clr_b.get(),width = self.stroke_size.get(), fill="")
    def draw_equitriangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#--------------------------------------------------------right triangle------------------------------------------
    def on_rightTriangleButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_rightTriangle)
        self.canvas.bind("<ButtonRelease-1>", self.draw_rightTriangle_end)
    def draw_rightTriangle(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3 = x2-(x2-x1)
        y3 = y2
        self.shape_id=self.canvas.create_polygon(x1,y1 , x2, y2, x3,y3,
                                                 outline = self.stroke_clr_b.get(),width = self.stroke_size.get(), fill="")
    def draw_rightTriangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#-------------------------------------------star-----------------------------------------
    def on_starButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_star)
        self.canvas.bind("<ButtonRelease-1>", self.draw_star_end)

    def draw_star(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3 = (x2 + x1) / 2
        y3 = (y2 + y1) / 2
        total_radius = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        angle = 53.92
        outer_radius = total_radius / 2  
        inner_radius = outer_radius / 2

        star_points = []  
        for i in range(5):
            star_angle_outer = math.radians(i * 72 + angle)
            outer_x = x3 + outer_radius * math.cos(star_angle_outer)
            outer_y = y3 + outer_radius * math.sin(star_angle_outer)

            star_angle_inner = math.radians(i * 72 + 36 + angle)
            inner_x = x3 + inner_radius * math.cos(star_angle_inner)
            inner_y = y3 + inner_radius * math.sin(star_angle_inner)

            star_points.extend([outer_x, outer_y, inner_x, inner_y])
        self.shape_id = self.canvas.create_polygon(star_points,
                                               outline=self.stroke_clr_b.get(), width=self.stroke_size.get(), fill="")
    def draw_star_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


#---------------------------------------polygon--------------------------------------------

    def on_polygonButton_pressed(self):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "crosshair"
        self.canvas.bind("<B1-Motion>", self.draw_polygon)
        self.canvas.bind("<ButtonRelease-1>", self.draw_polygon_end)

    def draw_polygon(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        num_sides = int(self.current_polygon.get())
        if num_sides:
            total_radius = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            outer_radius = total_radius / 2
            polygon_points = self.calculate_polygon_points(num_sides, x1, y1, outer_radius)
            self.shape_id = self.canvas.create_polygon(polygon_points, outline=self.stroke_clr_b.get(),
                                                      width=self.stroke_size.get(), fill="")
        
    def calculate_polygon_points(self, num_sides, x1, y1, outer_radius):
        polygon_points = []
        for i in range(num_sides):
            poly_angle = 2 * i * math.pi / num_sides
            x = x1 + outer_radius * math.cos(poly_angle)
            y = y1 + outer_radius * math.sin(poly_angle)
            polygon_points.extend([x, y])
        return polygon_points
    
    def set_polygon(self, num_sides):
        self.current_polygon.set(num_sides)

    def draw_polygon_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

#--------------------------------------------------line-----------------------------------------------
    def on_lineButton_pressed(self):
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")
            self.canvas["cursor"] = "crosshair"
            self.canvas.bind("<B1-Motion>", self.draw_line)
            self.canvas.bind("<ButtonRelease-1>", self.draw_line_end)

    def draw_line(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        self.shape_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y
                                                     ,width = self.stroke_size.get(), fill=self.stroke_clr_b.get(),capstyle= ROUND)
    def draw_line_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None

#-----------------------------------------------curve----------------------------------------

    def on_curveButton_pressed(self):
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<B3-Motion>")
            self.canvas["cursor"] = "crosshair"
            self.canvas.bind("<Button-1>",self.start_draw)
            self.canvas.bind("<B1-Motion>", self.drawing)
            self.canvas.bind("<B3-Motion>",self.or_draw_kro)

    def drawing(self, event):
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        self.end_x=event.x
        self.end_y=event.y
        if self.center_x is None or self.center_y is None:
            self.shape_id = self.canvas.create_line(self.last_x, self.last_y, event.x, event.y
                                                     ,width = self.stroke_size.get(),smooth=TRUE, fill=self.stroke_clr_b.get(),capstyle=ROUND)


    def start_draw(self, event):
            self.last_x, self.last_y = event.x, event.y

    def or_draw_kro(self,event):


        self.center_x, self.center_y = event.x, event.y
        if self.shape_id is not None:
            self.canvas.delete(self.shape_id)

        if self.shape_id1 is not None:
            self.canvas.delete(self.shape_id1)

        self.shape_id1 = self.canvas.create_line(self.last_x, self.last_y,self.center_x,self.center_y,self.end_x, self.end_y
                                                     ,width = self.stroke_size.get(), fill=self.stroke_clr_b.get(),smooth=TRUE, capstyle=ROUND)

#---------------------------------------------------------selection-------------------------------------------------------

    def on_selectionButton(self):
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "tcross"
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
     

    def on_button_press(self, event):
        self.last_x, self.last_y = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.last_x, self.last_y, self.last_x, self.last_y, outline="")
        self.selected_region = None
        self.drag_data = None
        self.painting_items = self.canvas.find_overlapping(self.last_x, self.last_y, self.last_x, self.last_y)


    def on_button_motion(self, event):
        curr_x = event.x
        curr_y = event.y
        self.canvas.coords(self.rect, self.last_x, self.last_y, curr_x, curr_y)


    def on_button_release(self, event):
        self.selected_region = self.canvas.coords(self.rect)
        self.drag_data = {"x": event.x, "y": event.y}

        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas["cursor"] = "fleur"
        self.canvas.bind("<ButtonPress-1>", self.on_selection_click)
        self.canvas.bind("<B1-Motion>", self.on_selection_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_selection_release)


    def on_selection_click(self, event):
        
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)[0]
        rect2 = self.canvas.bbox(self.drag_data["item"])
        self.canvas.addtag_enclosed("drag", *rect2)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_selection_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        
        wid = self.canvas.winfo_width()
        high = self.canvas.winfo_height()
        rect2 = self.canvas.bbox(self.drag_data["item"])
        if 0:
            if rect2[3] + dy > high:
               dy = 0 
            if rect2[1] + dy < 0:
               dy = 0 
            if rect2[2] + dx > wid: 
               dx = 0 
            if rect2[0] + dx < 0: 
               dx = 0 
        else:
            pic=7
            if rect2[1] + dy + pic > high: 
               dy = 0 
            if rect2[3] + dy - pic < 0:
               dy = 0 
            if rect2[0] + dx + pic > wid:
               dx = 0 
            if rect2[2] + dx - pic < 0: 
               dx = 0 

        self.canvas.move("drag", dx, dy)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

   
    def on_selection_release(self, event):
        self.drag_data["item"] = None
        self.drag_data["x"] = 0
        self.drag_data["y"] = 0
        self.canvas.dtag("drag", "drag")

        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_button_motion)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

   

#---------------------------------------------------save-----------------------------------------------
    def clear_canvas(self):
        messagebox.askokcancel("MK Paint", "Do you want to clear?")
        self.canvas.delete("all")


    def save_opt(self):
        file_location = filedialog.asksaveasfilename(defaultextension="jpg")
        if file_location:
            x= self.canvas.winfo_rootx() + self.screen.winfo_rootx()
            y= self.canvas.winfo_rooty() + self.screen.winfo_rooty()-60
            ImageGrab.grab(bbox=(x, y, x+1100, y+440)).save(file_location)
     

    def create_new(self):
        if messagebox.askyesno("MK Paint", "Do you want to create new?"):
            messagebox.askyesno("MK Paint", "Do you want to save the file?")
            self.save_opt()
        self.canvas.delete("all")
   
    def load_canvas(self):
        file_location = filedialog.askopenfilename(defaultextension="jpg")
        if file_location:
            self.canvas.delete("all")
            image = PhotoImage()
            real_image = ImageTk.PhotoImage(file=file_location)
            self.image = real_image
            self.canvas.create_image(0, 0, image=self.image, anchor=NW)



             
   

MkPaint(1360, 700, "MK Paint").run()

