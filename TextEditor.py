#!/usr/bin/env python

from tkinter import *
from tkinter import filedialog,messagebox,font,colorchooser
from tkinter.ttk import Combobox

import os,speech_recognition as sr




class TextEditor:


	current_file=None

	def change_font(self):
		self.text_area.config(font = self.fonts[self.text_font.get()])

	def text_color(self):
		clr=colorchooser.askcolor()

		self.text_area.config(foreground=clr[1])

	def bg_color(self):
		clr=colorchooser.askcolor()

		self.text_area.config(bg=clr[1])


	def getAudio(self):
		if messagebox.askquestion("Audio","Press OK and say something in ur lovely voice to write on editor\nThe less you say, the faster it is :P")=='yes':
			r = sr.Recognizer()
			with sr.Microphone() as source:
			
				audio = r.listen(source)
				try:
					text = r.recognize_google(audio)
					self.text_area.insert(INSERT,text)
					
				except:
					messagebox.showerror("Oops","Oops, Poor internet or you were not clear : P\nYou may try again")



	#open File method
	
	def openFile(self,event=""):
		open_return=filedialog.askopenfilename()
		if open_return:

			open_return=open_return.replace("/","//")
			
			self.master.title(os.path.basename(open_return) + " - Notepad")
			self.text_area.delete(1.0,END)

			file_object=open(open_return,"r")

			
			self.text_area.insert(END,file_object.read())
			#file_object.close()

	def saveAsFile(self,event=""):
		file_object=filedialog.asksaveasfile(mode='w', defaultextension=".txt")
		if file_object:
			self.current_file=file_object.name
			file_object.write(self.text_area.get(1.0,END))
			file_object.close()

	def saveFile(self,event=""):
		if self.current_file:
			file_object=open(self.current_file,"w")
			file_object.write(self.text_area.get(1.0,END))
			file_object.close()
		else:
			self.saveAsFile()

	def newFile(self,event=""):
		self.master.title("Untitled")
		self.text_area.delete(1.0,END)
		self.current_file=None

	def newWindowFile(self,event=""):
		top=Toplevel()
		obj=TextEditor(top)



	def copy(self,event=""):
		self.text_area.event_generate("<<Copy>>")


	def cut(self,event=""):
		self.text_area.event_generate("<<Cut>>")

	def paste(self,event=""):
		self.text_area.event_generate("<<Paste>>")

	def undo(self,event=""):
		try:
			self.text_area.edit_undo()
		except:
			pass

	def redo(self,event=""):
		try:
			self.text_area.edit_undo()
		except:
			pass

	
	def __init__(self,master):
		self.master=master
		self.master.title("My Text Editor")
	
		
		text_font=font.Font(family="Calibri", size=14)
		self.text_area=Text(self.master, undo=True, wrap="word", font=text_font)
		self.text_area.pack(fill="both", expand=1)

		#Menu Bar function
		def createMenuBar():

			
			self.menu_bar=Menu(self.master,)
			self.master.config(menu=self.menu_bar)

			#creating File Menu
			self.file_menu=Menu(self.menu_bar,tearoff=0)
			self.menu_bar.add_cascade(label="File",menu=self.file_menu)

			self.file_menu.add_command(label="New",command=self.newFile)
			self.file_menu.add_command(label="New Window",command=self.newWindowFile)
			self.file_menu.add_command(label="Open",command=self.openFile)
			self.file_menu.add_separator()
			self.file_menu.add_command(label="Save",command=self.saveFile)
			self.file_menu.add_command(label="Save As",command=self.saveAsFile)
			self.file_menu.add_separator()
			self.file_menu.add_command(label="Close",command=self.master.destroy)
			self.file_menu.add_separator()
			self.file_menu.add_command(label="Exit",command=self.master.quit)



			#creating Edit menu
			self.edit_menu=Menu(self.menu_bar,tearoff=0)
			self.menu_bar.add_cascade(label="Edit",menu=self.edit_menu)

			self.edit_menu.add_command(label="Undo",command=self.undo)
			self.edit_menu.add_command(label="Redo",command=self.redo)
			self.edit_menu.add_separator()
			self.edit_menu.add_command(label="Copy",command=self.copy)
			self.edit_menu.add_command(label="Cut",command=self.cut)
			self.edit_menu.add_command(label="Paste",command=self.paste)


			#creating Font menu
			self.font_menu=Menu(self.menu_bar,tearoff=0)
			self.menu_bar.add_cascade(label="Fonts", menu=self.font_menu)

			self.style_submenu=Menu(self.font_menu,tearoff=0)
			self.font_menu.add_cascade(label="Style",menu=self.style_submenu)

			def style():
				self.text_font = StringVar()
				self.text_font.set("Calibri")

				self.fonts = {}
				for f in ("Calibri","Times","Arial", "Consoles", "Courier", "Tahoma"):
					self.fonts[f] = font.Font(font=f)
					self.style_submenu.add_radiobutton(label=f, variable=self.text_font, command=self.change_font)

			style()

			self.color_submenu=Menu(self.font_menu,tearoff=0)
			self.font_menu.add_cascade(label="Color",menu=self.color_submenu)
			self.color_submenu.add_command(label="Text color", command=self.text_color)
			self.color_submenu.add_command(label="Background color", command=self.bg_color)








			#creating Help menu
			def help():
				messagebox.showinfo("Help", "God helps those who help themselves :P")
			self.menu_bar.add_command(label="Help",command=help)



			#creating About menu
			def about():
				messagebox.showinfo("About", "Developed with love by - Prateek Jha")
			self.menu_bar.add_command(label="About",command=about)


			#Audio Menu


			self.menu_bar.add_command(label="Audio", command=self.getAudio)

	 


		#calling Menu Bar creating function
		createMenuBar()

		self.master.bind("<Control-x>",self.cut)
		self.master.bind("<Control-c>",self.copy)
		self.master.bind("<Control-v>",self.paste)
		self.master.bind("<Control-z>",self.undo)
		self.master.bind("<Shift-Control-z>",self.redo)



root=Tk()
te=TextEditor(root)
root.mainloop()

