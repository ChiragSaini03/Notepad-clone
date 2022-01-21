import os
from tkinter import *
import tkinter
from tkinter.messagebox import *
from tkinter.filedialog import *
import pickle
import sys
from PIL import ImageTk, Image
import time
import subprocess
from datetime import date,datetime
# from pyautogui import press

class Notepad:
	__root = Tk()
	__root.geometry("0x0+0+0")
	__thisWidth = 300
	__thisHeight = 300
	__thisstatusbar=Frame(__root,bg='gray90',height=15,width=50)
	__thisMenuBar = Menu(__root)
	__rightmenubar=Menu(__root,tearoff=0,bg='black',fg='SpringGreen2',font='calibri 12')
	__thisFileMenu = Menu(__thisMenuBar,tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisEditMenu = Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisHelpMenu = Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisaddMenu= Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thissizeMenu = Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisviewMenu=Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisthemeMenu=Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisWindowMenu=Menu(__thisMenuBar, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__fontoptions=Menu(__thisaddMenu, tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisrightsizemenu=Menu(__rightmenubar,tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thiscommandmenu=Menu(__rightmenubar,tearoff=0,bg='black',fg='green2',font= 'calibri 12')
	__thisScrollBarx = Scrollbar(__root,cursor='arrow', orient='horizontal')	
	__thisScrollBary = Scrollbar(__root,cursor='arrow',)	
	__file = None
	size=16
	font='Lucida Console'
	bold_counter=1
	counter_1=0
	theme_counter=1
	__allwindata=['']
	Int1=IntVar()
	Int1.set(1)
	Intxx=IntVar()
	Intxa=IntVar()
	Intxl=IntVar()
	Intxp=IntVar()
	Intxb=IntVar()
	__addnewwincoun=1
	__winno=1
	__wintiles=[]
	__wintiles+=['Untitled']
	__winpaths=[__file]
	wintot=0
	en1=''
	highlight_counter=0
	_wrapcounter=0
	__highlight_stor={}
	prev=1
	frame_cop=Frame(__root)
	sizepal=Label(frame_cop)
	redrawvr='redraw'
	def __init__(self,**kwargs):
		self.__thisTextArea = CustomText(self.__root,insertbackground='green2', font= ('Lucida Console', 16),bg='black',height=500,width=20,fg='green2',insertwidth=3,padx=2,pady=2,undo=True,spacing1=7,spacing3=5,wrap=WORD)
		self._t0= self.__thisTextArea.get(1.0,'end-1c')
		try:
				self.__root.wm_iconbitmap("Notepad.ico")
		except:
				pass
		try:
			self.__thisWidth = kwargs['width']
		except KeyError:
			pass

		try:
			self.__thisHeight = kwargs['height']
		except KeyError:
			pass
		# Set the window text
		self.__root.title("Untitled - Notepad Advance")
		self.__root.state('zoomed')

		# Center the window
		screenWidth = self.__root.winfo_screenwidth()
		screenHeight = self.__root.winfo_screenheight()
	
		# For left-alling
		left = (screenWidth / 2) - (self.__thisWidth / 2)
		
		# For right-allign
		top = (screenHeight / 2) - (self.__thisHeight /2)
		# For top and bottom					
		self.__root.geometry('%dx%d+%d+%d' % (self.__thisWidth,
											self.__thisHeight,
											left, top))
		# To make the textarea auto resizable
		self.__root.grid_rowconfigure(0, weight=1)
		self.__root.grid_columnconfigure(0, weight=1)
		# Add controls (widget)	
		self.linenumbers = TextLineNumbers(self.__root, width=15,bg='SeaGreen2')
		self.linenumbers.attach(self.__thisTextArea)
	#	self.linenumbers.pack(side="left", fill="y")
	#	self.text.pack(side="right", fill="both", expand=True)
		self.linenumbers.grid(row=0,column=1,sticky='ns')
		self.__thisstatusbar.grid(row=2,column=0,columnspan=3,sticky='we')
		self.__thisScrollBary.grid(row=0,column=2,sticky=N+S)
		self.__thisScrollBarx.grid(row=1,column=0,sticky='we')
		self.__thisTextArea.grid(row=0,column=0,sticky=N+E+S+W)
		self.l1=Button(self.__thisstatusbar,text='	    	                		Line: 1   Col: 1',bg='SeaGreen2',font=('Calibri',12),borderwidth=0,command=self.__gotoline)
		self.l1.grid(row=0,column=0)
		self.l2=Label(self.__thisstatusbar,text=f'			                                                           	Font: {self.font}           ',bg='gray90')
		self.l2.grid(row=0,column=1)
		self.l4=Label(self.__thisstatusbar,text=f'		        	Size: {self.size}		                        ',bg='gray90')
		self.l4.grid(row=0,column=2)
		self.l3=Label(self.__thisstatusbar,text='UTF-8                                              ',bg='gray90')
		self.l3.grid(row=0,column=3)
		self.__thisScrollBarx.config(command=self.__thisTextArea.xview)	
		self.__thisTextArea.config(xscrollcommand=self.__thisScrollBarx.set)
		# Scrollbar will adjust automatically according to the content
		self.__thisScrollBary.config(command=self.__thisTextArea.yview)	
		self.__thisTextArea.config(yscrollcommand=self.__thisScrollBary.set)
		self.__thisScrollBarx.tk.call("grid", "remove", self.__thisScrollBarx)
		# To open new file
		self.__thisFileMenu.add_command(label="New File",
										command=self.__newFile)
		self.__thisFileMenu.add_command(label="New Window",
										command=self.__neww)	
		# To open a already existing file
		self.__thisFileMenu.add_command(label="Open",accelerator="Ctrl+o",
										command=self.__openFile)
		# To save current file
		self.__thisFileMenu.add_command(label="Save",accelerator="Ctrl+s",
										command=self.__saveFile)
		self.__thisFileMenu.add_command(label="Save as",accelerator='Ctrl+Shift+s',
										command=self.__saveFileAs)
		# To create a line in the dialog		
		self.__thisFileMenu.add_separator()	
		self.__thisFileMenu.add_command(label="Close Current File",
										command=self.__closecurrwin,state=DISABLED)								
		self.__thisFileMenu.add_command(label="Close Window",
										command=self.__quitApplication)
		self.__thisFileMenu.add_command(label="Exit",
										command=self.__exitApplication)
		self.__thisFileMenu.add_separator()
		self.__thisFileMenu.add_command(label="Save as binary",accelerator="Ctrl+Shift+b",
										command=self.__saveasbin)
		self.__thisFileMenu.add_command(label="Retrieve from binary",accelerator="Ctrl+Shift+n",
										command=self.__getfrombin)
		self.__thisFileMenu.add_separator()
		self.__thisFileMenu.add_command(label="Print -Export as pdf",accelerator="Ctrl+p",
										command=self.__exportaspdf)
		self.__thisMenuBar.add_cascade(label=" File ",underline=1,
									menu=self.__thisFileMenu)
		# To give a feature of cut
		self.__thisEditMenu.add_command(label="Cut",accelerator='Ctrl+x',
										command=self.__cut)			
		# to give a feature of copy	
		self.__thisEditMenu.add_command(label="Copy",accelerator='Ctrl+c',
										command=self.__copy)		
		# To give a feature of paste
		self.__thisEditMenu.add_command(label="Paste",accelerator='Ctrl+v',
										command=self.__paste)
		self.__thisEditMenu.add_separator()
		self.__thisEditMenu.add_command(label="Select All",accelerator="Ctrl+a",
										command=self.__selectall)
		self.__thisEditMenu.add_separator()
		self.__thisEditMenu.add_command(label="Undo",accelerator='Ctrl+x',
										command=self.__thisTextArea.edit_undo)
		self.__thisEditMenu.add_command(label="Redo",accelerator='Ctrl+y',
										command=self.__thisTextArea.edit_redo)
		self.__thisEditMenu.add_separator()
		self.__thisEditMenu.add_command(label="Find",accelerator='Ctrl+f',
										command=self.find_win)
		self.__thisEditMenu.add_command(label="Replace",accelerator='Ctrl+r',
										command=self.find_win)
		self.__thisEditMenu.add_command(label="Highlight",accelerator='Ctrl+h',
										command=self.highl_win)
		# To give a feature of editing
		self.__thisMenuBar.add_cascade(label=" Edit ",
									menu=self.__thisEditMenu,underline=1)
		self.__thissizeMenu.add_command(label="Increase Font Size",accelerator='Ctrl +',
										command=self.__size2)
		self.__thissizeMenu.add_command(label=f"Current Size",accelerator=f"{self.size}",
										command=self.__size)
		self.__thissizeMenu.add_command(label="Decrease Font Size",accelerator='Ctrl -',
										command=self.__size1)
		self.__thisMenuBar.add_cascade(label=" Zoom ",
									menu=self.__thissizeMenu)
		self.__thisviewMenu.add_command(label="Full Screen",
										command=self.__fullscr)
		self.__thisviewMenu.add_command(label="Landscape mode",
										command=self.__landscape)
		self.__thisviewMenu.add_command(label="Portrait mode",
										command=self.__portrait)
		self.__thisviewMenu.add_checkbutton(label="Pin to Screen",variable=self.Intxp,selectcolor="green2",
										command=self.__pinscreen)
		self.__thisMenuBar.add_cascade(label=" View ",
									menu=self.__thisviewMenu)
		# To create a feature of description of the notepad
		self.__thisthemeMenu.add_command(label="Dark",accelerator="Default",
										command=self.__theme_dark)
		self.__thisthemeMenu.add_command(label="Light",
										command=self.__theme_light)
		self.__thisthemeMenu.add_separator()
		self.__thisthemeMenu.add_command(label="Cool",
										command=self.__theme_cool)
		self.__thisthemeMenu.add_separator()
		self.__thisthemeMenu.add_command(label="Monokai",
										command=self.__theme_monokai)
		self.__thisthemeMenu.add_command(label="Monokai2",
										command=self.__theme_monokai2)
		self.__thisMenuBar.add_cascade(label=" Theme ",
									menu=self.__thisthemeMenu)
		self.__fontoptions.add_command(label="Lucida Console",accelerator="Default",
										command=self.__font_lucidia_console)		
		self.__fontoptions.add_command(label="Calibri",
										command=self.__font_calibri)
		self.__fontoptions.add_command(label="Consolas",
										command=self.__font_consolas)
		self.__fontoptions.add_command(label="Courier New",
										command=self.__font_courier)
		self.__fontoptions.add_command(label="Lucidia",
										command=self.__font_Lucidia)
		self.__fontoptions.add_command(label="Arial Black",
										command=self.__font_arial_black)
		self.__fontoptions.add_command(label="Castellar",
										command=self.__font_castellar)
		self.__fontoptions.add_command(label="Script",
										command=self.__font_segoe_script)
		self.__thisaddMenu.add_cascade(label="Font",
										menu=self.__fontoptions,font='Times 13',foreground='white',background='coral3')
		self.__thisaddMenu.add_checkbutton(label="Bold",accelerator='Ctrl+b',variable=self.Intxb,selectcolor="green2",
										command=self.__bold)
		self.__thisaddMenu.add_checkbutton(label="Disable Word Wrap",
										command=self.__wrap,variable=self.Intxx,selectcolor="green2")
		self.__thisaddMenu.add_checkbutton(label="Disable Status Bar",
										command=self.__status,variable=self.Intxa,selectcolor="green2")
		self.__thisaddMenu.add_checkbutton(label="Disable Line Numbers",
										command=self.__linenum,variable=self.Intxl,selectcolor="green2")
		self.__thisaddMenu.add_command(label="System Info",
									command=self._systeminfo)
		self.__thisMenuBar.add_cascade(label=" Options ",
									menu=self.__thisaddMenu)
		self.__thisWindowMenu.add_command(label="Add new File +",
										command=self.__addwin,font='Times 13',foreground='white',background='coral3')
		self.__thisWindowMenu.add_radiobutton(label=f"Untitled",variable=self.Int1,value=self.__winno,
										command=self.__thiswin,selectcolor="green2")
		self.__thisMenuBar.add_cascade(label=" Window ",
									menu=self.__thisWindowMenu)	
		self.__thisHelpMenu.add_command(label="Additional pallete",
										command=self.frame_gen)
		self.__thisHelpMenu.add_separator()							
		self.__thisHelpMenu.add_command(label="About Notepad",
										command=self.__showAbout)
		self.__thisHelpMenu.add_separator()
		self.__thisHelpMenu.add_command(label="Additional Shortcuts",
										command=self.__shortcuts)		
		self.__thisMenuBar.add_cascade(label=" Help ",
									menu=self.__thisHelpMenu)
		self.__root.config(menu=self.__thisMenuBar)
		self.__rightmenubar.add_command(label ="Cut",command=self.__cut)
		self.__rightmenubar.add_command(label ="Copy",command=self.__copy)
		self.__rightmenubar.add_command(label ="Paste",command=self.__paste)
		self.__rightmenubar.add_command(label ="Select All",command=self.__selectall)
		self.__rightmenubar.add_separator()
		self.__rightmenubar.add_command(label="Undo",accelerator='Ctrl+x',
										command=self.__thisTextArea.edit_undo)
		self.__rightmenubar.add_command(label="Redo",accelerator='Ctrl+y',
										command=self.__thisTextArea.edit_redo)
		self.__rightmenubar.add_separator()
		self.__rightmenubar.add_command(label ="Save",command=self.__saveFile)
		self.__rightmenubar.add_command(label ="Close Current Win",command=self.__closecurrwin,state=DISABLED)
		self.__rightmenubar.add_separator()
		self.__thiscommandmenu.add_command(label="=> ",command=self.__cm1)
		self.__thiscommandmenu.add_command(label="### ",command=self.__cm2)
		self.__thiscommandmenu.add_separator()
		self.__thiscommandmenu.add_command(label="( )",command=self.__cm3)
		self.__thiscommandmenu.add_command(label="{ }",command=self.__cm4)
		self.__thiscommandmenu.add_separator()
		self.__thiscommandmenu.add_command(label='" "',command=self.__cm5)
		self.__thiscommandmenu.add_command(label='Tab',command=self.__cm6)
		self.__thiscommandmenu.add_command(label='Date',command=self.__cm7)
		self.__thiscommandmenu.add_command(label='Date/Time',command=self.__cm8)
		self.__rightmenubar.add_cascade(label="Commands ",menu=self.__thiscommandmenu,font='Times 13',foreground='white',background='coral3')
		self.__thisrightsizemenu.add_command(label ="Inc Font Size",command=self.__size2)
		self.__thisrightsizemenu.add_command(label ="Dec Font Size",command=self.__size1)
		self.__rightmenubar.add_cascade(label ="Size",menu=self.__thisrightsizemenu)
		self.__rightmenubar.add_command(label ="Switch Font",command=self.__switchfonts)
		self.__rightmenubar.add_separator()
		self.__rightmenubar.add_command(label ="Pallete",command=self.frame_gen)
		self.__rightmenubar.add_separator()
		self.__rightmenubar.add_command(label ="Shortcuts",command=self.__shortcuts)
		bg5=Image.open(r'\icons\more.png')
		bg5 =bg5.resize((50,15), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.__root,image=bg5,command=self.frame_gen,bg='black',borderwidth=0,fg='gray80',height=15,width=50,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.place(x=1000,y=0)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)

	def _systeminfo(self):
		Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
		new = []
		for item in Id:
		    new.append(str(item.split("\r")[:-1]))
		r=''
		for i in new:
		    r+=f"{i[2:-2]}\n"
		self.__thisTextArea.delete(1.0,END)
		self.__thisTextArea.insert(1.0,r)

	def __quitApplication(self):
		if self.__thisTextArea.get(1.0,'end-1c') == self._t0:
			self.__root.destroy()
		else:
			rep=askyesnocancel('Quit','''Want to Save the file before closing.
    File->Save''')
			if rep:
				self.__saveFile()
			elif rep is None:
				pass
			else:
				self.__root.destroy()

	def __exitApplication(self):
		if self.__thisTextArea.get(1.0,'end-1c') == self._t0:
			self.__root.destroy()
			sys.exit()
		else:
			rep=askyesnocancel('Quit','''Want to Save the file before closing.
    File->Save''')
			if rep:
				self.__saveFile()
			elif rep is None:
				pass
			else:
				self.__root.destroy()
				sys.exit()
	def __gotoline(self):
		p=self.__thisTextArea.index(INSERT)
		p=p.split('.')
		linego=Toplevel()
		linego.resizable(height=False,width=False)
		linego.title('Go to Index/Line')
		linego.config(bg='Black')
		Label(linego,text='Line',bg='Black',fg='DarkGoldenrod1',font=('Calibri',13),width=13).grid(row=0,column=0)
		Label(linego,text='Column',bg='Black',fg='DarkGoldenrod1',font=('Calibri',13),width=13).grid(row=0,column=1)
		self.linego=IntVar()
		self.colgo=IntVar()
		self.linego.set(int(p[0]))
		self.colgo.set(int(p[1]))
		Entry(linego,textvariable=self.linego,bg='DarkGoldenrod1',fg='Black',font=('Calibri',13),width=13).grid(row=1,column=0)
		Entry(linego,textvariable=self.colgo,bg='DarkGoldenrod1',fg='Black',font=('Calibri',13),width=13).grid(row=1,column=1)
		Button(linego,text='Go to',bg='DarkGoldenrod1',command=self.__gotof,fg='Black',font=('Calibri',12),width=29).grid(row=3,column=0,columnspan=2,pady=5)
	def __gotof(self):
		self.__thisTextArea.mark_set(INSERT,f'{self.linego.get()}.{self.colgo.get()}')
		self.__updatewinx()
		# press('right')
		# press('left')
	def _on_change(self, event=None):
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
	def __pinscreen(self):
		if self.Intxp.get()==1:
			self.__root.attributes('-topmost',True)
		else:
			self.__root.attributes('-topmost',False)

	def __wrap(self):
		if self.Intxx.get()==1:
			self.__thisTextArea.configure(wrap='none')
			self.__thisScrollBarx.grid()
		elif self.Intxx.get()==0:
			self.__thisTextArea.configure(wrap=WORD)
			self.__thisScrollBarx.tk.call("grid", "remove", self.__thisScrollBarx)

	def __status(self):
		if self.Intxa.get()==1:
			self.__thisstatusbar.tk.call("grid", "remove", self.__thisstatusbar)
		elif self.Intxa.get()==0:
			self.__thisstatusbar.grid()
	def __linenum(self):
		if self.Intxl.get()==1:
			self.linenumbers.tk.call("grid", "remove", self.linenumbers)
		elif self.Intxl.get()==0:
			self.linenumbers.grid()

	def __neww(self):
		os.system("\Notepad_advance.pyw")
		# exec(open(r"\Notepad_advance.pyw").read())

	def __saveasbin(self,event=None):
		fileb= asksaveasfilename(initialfile='Untitled.bin',
											defaultextension=".bin",
											filetypes=[("Binary files","*.*"),
												("Binary Documents","*.bin")])
		te=self.__thisTextArea.get(1.0,'end-1c')
		res = ' '.join(format(ord(i), '08b') for i in te)
		with open(fileb,'w+') as f:
			f.write(res)
	
	def __getfrombin(self,event=None):
		filebin= askopenfilename(initialfile='Untitled.bin',
											defaultextension=".bin",
											filetypes=[("Binary files","*.*"),
												("Binary Documents","*.bin")])
		with open(filebin,'r+') as f:
			filebin=f.read()
		filebin=filebin.split(' ')
		ascii_string=''
		for i in filebin:
			an_integer = int(i, 2)
			ascii_character = chr(an_integer)
			ascii_string += ascii_character
		self.__thisTextArea.delete(1.0,END)
		self.__thisTextArea.insert(1.0,ascii_string)
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __closecurrwin(self):
		del self.__wintiles[self.__winno-1]
		del self.__winpaths[self.__winno-1]
		del self.__allwindata[self.__winno-1]
		if self.__winno>1:
			self.__winno-=1
			x=self.Int1.get()
			self.Int1.set(x-1)
			self.__thisclose()
			if self.__addnewwincoun==1:
				self.__rightmenubar.entryconfig(9,state=DISABLED)
				self.__thisFileMenu.entryconfig(6,state=DISABLED)
		elif self.__winno==1:
			self.Int1.set(1)
			self.__winno=1
			self.__thisclose()
			if self.__addnewwincoun==1:
				self.__rightmenubar.entryconfig(9,state=DISABLED)
				self.__thisFileMenu.entryconfig(6,state=DISABLED)
		locgetint1=self.Int1.get()
		self.Int1.set(-2)
		for value in range(self.wintot+1,0,-1):
			self.__thisWindowMenu.delete(value)
		p=1
		for i in self.__wintiles:
			self.__thisWindowMenu.add_radiobutton(label=f"{i}",variable=self.Int1,value=p,
										command=self.__thiswin,selectcolor="green2")
			p+=1
		self.Int1.set(locgetint1)
		self.wintot=self.wintot-1
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
	
	def __thisclose(self):
		_sentwinno=self.Int1.get()
		self.__winno=_sentwinno
		self.__thisTextArea.delete(1.0,END)
		self.__thisTextArea.insert(1.0,self.__allwindata[_sentwinno-1])
		self.__root.title(f'{self.__wintiles[((self.__winno)-1)]} - Notepad Advance')
		self.__file=self.__winpaths[self.__winno-1]
		self.__addnewwincoun-=1


	def __cm1(self):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,'=> ')
	
	def __cm2(self):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,'### ')
	def __cm3(self):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,'()')
	def __cm4(self):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,'{}')
	def __cm5(self):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,'""')
	def __cm6(self):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,'	')
	def __cm7(self):
		today = date.today()
		d1 = today.strftime(r"%d/%m/%Y")
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,f'{d1} ')
	def __cm8(self):
		now = datetime.now()
		dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,f'{dt_string} ')
	def __switch_window(self,event=None):
		_tempstore1=self.__thisTextArea.get(1.0,'end-1c')
		self.__allwindata[self.__winno-1]=_tempstore1
		if self.__winno==self.wintot+1:
			self.__winno=1
			self.Int1.set(1)
			self.__thisTextArea.delete(1.0,END)
			self.__thisTextArea.insert(1.0,(self.__allwindata[0]))
			self.__root.title(f'{self.__wintiles[0]} - Notepad Advance')
			self.__file=self.__winpaths[0]
		else:
			_sentwinno=self.Int1.get()
			self.__winno=self.__winno+1
			self.Int1.set(_sentwinno+1)
			self.__thisTextArea.delete(1.0,END)
			self.__thisTextArea.insert(1.0,(self.__allwindata[_sentwinno]))
			self.__root.title(f'{self.__wintiles[((self.__winno)-1)]} - Notepad Advance')
			self.__file=self.__winpaths[self.__winno-1]
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
		self.__updatewinx()
	
	def __thiswin(self):
		_tempstore1=self.__thisTextArea.get(1.0,'end-1c')
		self.__allwindata[self.__winno-1]=_tempstore1
		_sentwinno=self.Int1.get()
		self.__winno=_sentwinno
		self.__thisTextArea.delete(1.0,END)
		self.__thisTextArea.insert(1.0,(self.__allwindata[_sentwinno-1]))
		self.__root.title(f'{self.__wintiles[((self.__winno)-1)]} - Notepad Advance')
		self.__file=self.__winpaths[self.__winno-1]
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
		self.__updatewinx()

	def __addwin(self):
		_tempstore1=self.__thisTextArea.get(1.0,'end-1c')
		self.__allwindata[self.__winno-1]=_tempstore1
		self.__thisTextArea.delete(1.0,END)
		self.__addnewwincoun+=1
		self.__winno=self.__addnewwincoun		 ## Wrong method :self.__winno+=1  ##
		self.Int1.set(self.wintot+2)
		self.__thisWindowMenu.add_radiobutton(label="Untiled",variable=self.Int1,value=self.wintot+2,
										command=self.__thiswin,selectcolor="green2")
		self.__root.title('Untitled - Notepad Advance')
		self.__wintiles+=['Untitled']
		self.__winpaths+=[None]
		self.__rightmenubar.entryconfig(9,state=NORMAL)
		self.__thisFileMenu.entryconfig(6,state=NORMAL)
		self.__allwindata+=['']
		self.__file=None
		self.wintot+=1
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __showAbout(self):
		showinfo("About Notepad","You can write your text here")

	def __shortcuts(self):
		showinfo("Notepad Shortcuts",'''Ctrl+m => Switch themes
Ctrl+g => Switch fonts
Ctrl++ => Increase font Size
Ctrl+- => Increase font Size''')

	def __openFile(self):
		global _t0
		self.__file = askopenfilename(defaultextension=".dat",
									filetypes=[("All Files","*.*"),
										("Data files","*.dat")])

		if self.__file == "":
			
			# no file to open
			self.__file = None
		else:
			
			# Try to open the file
			# set the window title
			self.__root.title(os.path.basename(self.__file) + " - Notepad Advance")
			self.__thisTextArea.delete(1.0,END)

			file = open(self.__file,"r+",encoding="utf-8")
			x=file.read()        # l1=pickle.load(file)
			self.__thisTextArea.insert(1.0,x)       # self.__thisTextArea.insert(1.0,l1[0])
			file.close()
			self._t0= self.__thisTextArea.get(1.0,'end-1c')
		self.__thisWindowMenu.entryconfigure(((self.__winno)),label=f'{os.path.basename(self.__file)}')
		self.__winpaths[self.__winno-1]=self.__file
		self.__wintiles[self.__winno-1]=os.path.basename(self.__file)
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
		self.__updatewinx()

	def __openFile_key(self,event=None):
		global _t0
		self.__file = askopenfilename(defaultextension=".dat",
									filetypes=[("All Files","*.*"),
										("Data files","*.dat")])
		if self.__file == "":
			
			# no file to open
			self.__file = None
		else:
			
			# Try to open the file
			# set the window title
			self.__root.title(os.path.basename(self.__file) + " - Notepad Advance")
			self.__thisTextArea.delete(1.0,END)
			file = open(self.__file,"r+",encoding="utf-8")
			x=file.read()        # l1=pickle.load(file)
			self.__thisTextArea.insert(1.0,x)       # self.__thisTextArea.insert(1.0,l1[0])
			file.close()
			self._t0= self.__thisTextArea.get(1.0,'end-1c')
		self.__thisWindowMenu.entryconfigure(((self.__winno)),label=f'{os.path.basename(self.__file)}')
		self.__winpaths[self.__winno-1]=self.__file
		self.__wintiles[self.__winno-1]=os.path.basename(self.__file)
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
		self.__updatewinx()
		
	def __newFile(self):
		global _t0
		self.__root.title("Untitled - Notepad Advance")
		self.__file = None
		self.__thisTextArea.delete(1.0,END)
		self._t0= self.__thisTextArea.get(1.0,'end-1c')
		self.__wintiles[self.__winno-1]='Untitled - Notepad Advance'
		self.__winpaths[self.__winno-1]=self.__file

	def __saveFile(self):
		global _t0
		x=self.__thisTextArea.get(1.0,'end-1c')
		l1=[x]
		if self.__file == None:
			# Save as new file
			self.__file = asksaveasfilename(initialfile='Untitled.txt',
											defaultextension=".txt",
											filetypes=[("All Files","*.*"),
												("Text Documents","*.txt")])

			if self.__file == "":
				self.__file = None
			else:
				
				# Try to save the file
				file = open(self.__file,"w+",encoding="utf-8")		# If using pickle use mode='wb+'
				file.write(x)        # pickle.dump(l1,file)
				file.close()
				
				# Change the window title
				self.__root.title(os.path.basename(self.__file) + " - Notepad Advance")
				
		else :
			file = open(self.__file,"w+",encoding="utf-8")
			file.write(x)       # pickle.load(l1,f) 
			file.close()
		self._t0= self.__thisTextArea.get(1.0,'end-1c')
		self.__wintiles[self.__winno-1]=os.path.basename(self.__file)
		self.__thisWindowMenu.entryconfigure(((self.__winno)),label=f'{os.path.basename(self.__file)}')
		self.__winpaths[self.__winno-1]=self.__file
			

	def __saveFile_key(self,event=None):
		global _t0
		x=self.__thisTextArea.get(1.0,'end-1c')
		l1=[x]
		if self.__file == None:
			# Save as new file
			self.__file = asksaveasfilename(initialfile='Untitled.txt',
											defaultextension=".txt",
											filetypes=[("All Files","*.*"),
												("Text Documents","*.txt")])

			if self.__file == "":
				self.__file = None
			else:
				
				# Try to save the file
				file = open(self.__file,"w+",encoding="utf-8")		# If using pickle use mode='wb+'
				file.write(x)        # pickle.dump(l1,file)
				file.close()
				
				# Change the window title
				self.__root.title(os.path.basename(self.__file) + " - Notepad Advance")
				
		else :
			file = open(self.__file,"w+",encoding="utf-8")
			file.write(x)       # pickle.load(l1,f) 
			file.close()
		self._t0= self.__thisTextArea.get(1.0,'end-1c')
		self.__wintiles[self.__winno-1]=os.path.basename(self.__file)
		self.__thisWindowMenu.entryconfigure(((self.__winno)),label=f'{os.path.basename(self.__file)}')
		self.__winpaths[self.__winno-1]=self.__file

	def __saveFileAs(self):
		global _t0
		x=self.__thisTextArea.get(1.0,'end-1c')
		l1=[x]
		# Save as new file
		self.__file = asksaveasfilename(initialfile='Untitled.txt',
										defaultextension=".txt",
										filetypes=[("All Files","*.*"),
											("Text Documents","*.txt")])
		if self.__file == "":
			self.__file = None
		else:
			# Try to save the file
			file = open(self.__file,"w+",encoding="utf-8")		# If using pickle use mode='wb+'
			file.write(x)        # pickle.dump(l1,file)
			file.close()
			# Change the window title
			self.__root.title(os.path.basename(self.__file) + " - Notepad Advance")
		self._t0= self.__thisTextArea.get(1.0,END)
		self.__wintiles[self.__winno-1]=os.path.basename(self.__file)
		self.__thisWindowMenu.entryconfigure(((self.__winno)),label=f'{os.path.basename(self.__file)}')
		self.__winpaths[self.__winno-1]=self.__file

	def __saveFileAs_key(self,event):
		global _f0
		x=self.__thisTextArea.get(1.0,'end-1c')
		l1=[x]
		# Save as new file
		self.__file = asksaveasfilename(initialfile='Untitled.txt',
										defaultextension=".txt",
										filetypes=[("All Files","*.*"),
											("Text Documents","*.txt")])
		if self.__file == "":
			self.__file = None
		else:
			# Try to save the file
			file = open(self.__file,"w+",encoding="utf-8")		# If using pickle use mode='wb+'
			file.write(x)        # pickle.dump(l1,file)
			file.close()
			# Change the window title
			self.__root.title(os.path.basename(self.__file) + " - Notepad Advance")
		self._t0= self.__thisTextArea.get(1.0,'end-1c')
		self.__wintiles[self.__winno-1]=os.path.basename(self.__file)
		self.__thisWindowMenu.entryconfigure(((self.__winno)),label=f'{os.path.basename(self.__file)}')
		self.__winpaths[self.__winno-1]=self.__file
				
	def __cut(self):
		self.__thisTextArea.event_generate("<<Cut>>")

	def __copy(self):
		self.__thisTextArea.event_generate("<<Copy>>")

	def __paste(self):
		self.__thisTextArea.event_generate("<<Paste>>")
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __size(self):
		pass

	def __size1(self,event=None):
		if self.size>10:
			self.size-=2
			self.__thissizeMenu.entryconfig(1,accelerator=f"{self.size}")
			if self.bold_counter%2==0:
				self.__thisTextArea.configure(font=(self.font,self.size,'bold'))
			else:
				self.__thisTextArea.configure(font=(self.font,self.size))
			self.l4.config(text=f'		        	Size: {self.size}		                        ')
			# self.linenumbers.size1()
			ind=self.__thisTextArea.index(INSERT)
			if self.redrawvr=='redraw':
				self.linenumbers.redraw(ind)
			elif self.redrawvr=='redraw1':
				self.linenumbers.redraw1(ind)
			self.linenumbers.size1(self.size)
			self.sizepal.config(text=self.size)
	def __size2(self,event=None):
		if self.size<70:
			self.size+=2
			self.__thissizeMenu.entryconfig(1,accelerator=f"{self.size}")
			if self.bold_counter%2==0:
				self.__thisTextArea.configure(font=(self.font,self.size,'bold'))
			else:
				self.__thisTextArea.configure(font=(self.font,self.size))
			self.l4.config(text=f'		        	Size: {self.size}		                        ')
			# self.linenumbers.size2()
			ind=self.__thisTextArea.index(INSERT)
			if self.redrawvr=='redraw':
				self.linenumbers.redraw(ind)
			elif self.redrawvr=='redraw1':
				self.linenumbers.redraw1(ind)
			self.linenumbers.size2(self.size)
			self.sizepal.config(text=self.size)
	def __theme_dark(self):
		self.__thisTextArea.configure(bg='black',fg='green2',insertbackground='green2')
		self.__thisFileMenu.configure(bg='black',fg='green2')
		self.__thisEditMenu.configure(bg='black',fg='green2')
		self.__thisHelpMenu.configure(bg='black',fg='green2')
		self.__thisaddMenu.configure(bg='black',fg='green2')
		self.__thissizeMenu.configure(bg='black',fg='green2')
		self.__thisthemeMenu.configure(bg='black',fg='green2')
		self.__thisviewMenu.configure(bg='black',fg='green2')
		self.__fontoptions.configure(bg='black',fg='green2')
		self.__rightmenubar.configure(bg='black',fg='green2')
		self.__thisrightsizemenu.configure(bg='black',fg='green2')
		self.__thisWindowMenu.configure(bg='black',fg='green2')
		self.__thiscommandmenu.configure(bg='black',fg='green2')
		self.linenumbers.config(bg='SeaGreen2')
		self.theme_counter=1
		self.linenumbers.filldark()
		self.__thisstatusbar.config(bg='gray90')
		self.l1.config(bg='SeaGreen2')
		self.l2.config(bg='gray90')
		self.l3.config(bg='gray90')
		self.l4.config(bg='gray90')
		self._on_change()
	def __theme_light(self):
		self.__thisTextArea.configure(bg='white',fg='black',insertbackground='black')
		self.__thisFileMenu.configure(bg='white',fg='black')
		self.__thisEditMenu.configure(bg='white',fg='black')
		self.__thisHelpMenu.configure(bg='white',fg='black')
		self.__thisaddMenu.configure(bg='white',fg='black')
		self.__thissizeMenu.configure(bg='white',fg='black')
		self.__thisthemeMenu.configure(bg='white',fg='black')
		self.__thisviewMenu.configure(bg='white',fg='black')
		self.__fontoptions.configure(bg='white',fg='black')
		self.__rightmenubar.configure(bg='white',fg='black')
		self.__thisrightsizemenu.configure(bg='white',fg='black')
		self.__thisWindowMenu.configure(bg='white',fg='black')
		self.__thiscommandmenu.configure(bg='white',fg='black')
		self.linenumbers.config(bg='gray90')
		self.theme_counter=2
		self.linenumbers.filllight()
		self.__thisstatusbar.config(bg='gray90')
		self.l1.config(bg='gray80')
		self.l2.config(bg='gray90')
		self.l3.config(bg='gray90')
		self.l4.config(bg='gray90')
		self._on_change()
	def __theme_cool(self):
		self.__thisTextArea.configure(bg='gold',fg='black',insertbackground='cyan')
		self.__thisFileMenu.configure(bg='OliveDrab1',fg='red')
		self.__thisEditMenu.configure(bg='OliveDrab1',fg='red')
		self.__thisHelpMenu.configure(bg='OliveDrab1',fg='red')
		self.__thisaddMenu.configure(bg='OliveDrab1',fg='red')
		self.__thissizeMenu.configure(bg='OliveDrab1',fg='red')
		self.__thisthemeMenu.configure(bg='OliveDrab1',fg='red')
		self.__thisviewMenu.configure(bg='OliveDrab1',fg='red')
		self.__fontoptions.configure(bg='OliveDrab1',fg='red')
		self.__rightmenubar.configure(bg='OliveDrab1',fg='red')
		self.__thisrightsizemenu.configure(bg='OliveDrab1',fg='red')
		self.__thisWindowMenu.configure(bg='OliveDrab1',fg='red')
		self.__thiscommandmenu.configure(bg='OliveDrab1',fg='red')
		self.linenumbers.config(bg='DarkGoldenrod1')
		self.theme_counter=3
		self.linenumbers.fillcool()
		self.__thisstatusbar.config(bg='gray90')
		self.l1.config(bg='DarkGoldenrod1')
		self.l2.config(bg='gray90')
		self.l3.config(bg='gray90')
		self.l4.config(bg='gray90')
		self._on_change()
	def __theme_monokai(self):
		self.__thisTextArea.configure(bg='Royalblue1',fg='white',insertbackground='white')
		self.__thisFileMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisEditMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisHelpMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisaddMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thissizeMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisthemeMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisviewMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__fontoptions.configure(bg='RoyalBlue4',fg='green yellow')
		self.__rightmenubar.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisrightsizemenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thisWindowMenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.__thiscommandmenu.configure(bg='RoyalBlue4',fg='green yellow')
		self.linenumbers.config(bg='chartreuse2')
		self.theme_counter=4
		self.linenumbers.filllight()
		self.__thisstatusbar.config(bg='gray90')
		self.l1.config(bg='chartreuse2')
		self.l2.config(bg='gray90')
		self.l3.config(bg='gray90')
		self.l4.config(bg='gray90')
		self._on_change()
	def __theme_monokai2(self):
		self.__thisTextArea.configure(bg='gray18',fg='Darkorange1',insertbackground='white')
		self.__thisFileMenu.configure(bg='Grey14',fg='light blue')
		self.__thisEditMenu.configure(bg='Grey14',fg='light blue')
		self.__thisHelpMenu.configure(bg='Grey14',fg='light blue')
		self.__thisaddMenu.configure(bg='Grey14',fg='light blue')
		self.__thissizeMenu.configure(bg='Grey14',fg='light blue')
		self.__thisthemeMenu.configure(bg='Grey14',fg='light blue')
		self.__thisviewMenu.configure(bg='Grey14',fg='light blue')
		self.__fontoptions.configure(bg='Grey14',fg='light blue')
		self.__rightmenubar.configure(bg='Grey14',fg='light blue')
		self.__thisrightsizemenu.configure(bg='Grey14',fg='light blue')
		self.__thisWindowMenu.configure(bg='Grey14',fg='light blue')
		self.__thiscommandmenu.configure(bg='Grey14',fg='light blue')
		self.linenumbers.config(bg='light coral')
		self.theme_counter=5
		self.linenumbers.filldark()
		self.__thisstatusbar.config(bg='gray90')
		self.l1.config(bg='light coral')
		self.l2.config(bg='gray90')
		self.l3.config(bg='gray90')
		self.l4.config(bg='gray90')
		self._on_change()
	def __switchthemes(self,event):
		if self.theme_counter==1:
			self.__theme_light()
		elif self.theme_counter==2:
			self.__theme_cool()
		elif self.theme_counter==3:
			self.__theme_monokai()
		elif self.theme_counter==4:
			self.__theme_monokai2()
		elif self.theme_counter==5:
			self.__theme_dark()
	def __font_lucidia_console(self):
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('Lucida Console',self.size,'bold'))
			self.font='Lucida Console'
			self.l2.config(text=f'  			                                                                     	Font: {self.font}')
		else:
			self.__thisTextArea.configure(font=('Lucida Console',self.size))
			self.font='Lucida Console'
			self.l2.config(text=f'  			                                                                     	Font: {self.font}')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)


	def __font_calibri(self):
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('calibri',self.size,'bold'))
			self.font='Calibri'     
			self.l2.config(text=f'      			                                                                	Font: {self.font}')
		else:
			self.__thisTextArea.configure(font=('calibri',self.size))
			self.font='Calibri'     
			self.l2.config(text=f'      			                                                                	Font: {self.font}')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __font_consolas(self):
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('consolas',self.size,'bold'))
			self.font='Consolas'
			self.l2.config(text=f'      			                                                                  	Font: {self.font}       ')
		else:
			self.__thisTextArea.configure(font=('consolas',self.size))
			self.font='Consolas'
			self.l2.config(text=f'      			                                                                  	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
	def __font_Lucidia(self):
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('Lucidia',self.size,'bold'))
			self.font='Lucidia'
			self.l2.config(text=f'	        		                                                                  	Font: {self.font}       ')
		else:
			self.__thisTextArea.configure(font=('Lucidia',self.size))
			self.font='Lucidia'
			self.l2.config(text=f'	        		                                                                  	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __font_courier(self):
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('Courier New',self.size,'bold'))
			self.font='Courier New'
			self.l2.config(text=f'			                                                                           	Font: {self.font}       ')
		else:
			self.__thisTextArea.configure(font=('Courier New',self.size))
			self.font='Courier New'
			self.l2.config(text=f'			                                                                           	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __font_arial_black(self):
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('Arial Black',self.size,'bold'))
			self.font='Arial Black'
			self.l2.config(text=f'			                                                                        	Font: {self.font}       ')
		else:
			self.__thisTextArea.configure(font=('Arial Black',self.size))
			self.font='Arial Black'
			self.l2.config(text=f'			                                                                        	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __font_castellar(self): 
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('castellar',self.size,'bold'))
			self.font='Castellar'
			self.l2.config(text=f'			                                                                           	Font: {self.font}       ')
		else:
			self.__thisTextArea.configure(font=('castellar',self.size))
			self.font='Castellar'
			self.l2.config(text=f'			                                                                           	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
	
	def __font_segoe_script(self): 
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=('Segoe Script',self.size,'bold'))
			self.font='Script'
			self.l2.config(text=f'                                                                          	Font: {self.font}       ')
		else:
			self.__thisTextArea.configure(font=('Segoe Script',self.size))
			self.font='Script'
			self.l2.config(text=f'                                                                          	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __switchfonts(self,event=None):
		fonts=['Lucida Console','Calibri','Consolas','Courier New','Lucidia','Arial Black','Castellar','Segoe Script']
		use1=fonts.index(self.font)
		if use1<7 :
			use1+=1
		else:
			use1=0
		self.font=fonts[use1]
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=(self.font,self.size,'bold'))
		else:
			self.__thisTextArea.configure(font=(self.font,self.size))
		self.l2.config(text=f'			                                                                           	Font: {self.font}       ')
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def __bold(self,event=None):
		self.bold_counter+=1
		if self.bold_counter%2==0:
			self.__thisTextArea.configure(font=(self.font, self.size, 'bold'))
			self.Intxb.set(1)
		else:
			self.__thisTextArea.configure(font=(self.font, self.size))
			self.Intxb.set(0)

	def __fullscr(self):
		self.__root.attributes('-fullscreen',True)
		self.__thisMenuBar.add_command(label='  Close X ',command=self.__quitApplication)
		self.counter_1=1
	def __landscape(self):
		if self.counter_1==1:
			self.__thisMenuBar.delete(9)
			self.counter_1=0
		else:
			pass
		self.__root.attributes('-fullscreen',False)
		self.__root.geometry('1000x500+0+0')
	def __portrait(self):
		if self.counter_1==1:
			self.__thisMenuBar.delete(9)
			self.counter_1=0
		else:
			pass
		self.__root.attributes('-fullscreen',False)
		self.__root.geometry('350x600+0+0')
	def __selectall(self):
		self.__thisTextArea.tag_add('sel', '1.0', 'end')
		return "break"
	def _rightclickmenu(self,event):
		try:
			self.__rightmenubar.tk_popup(event.x_root, event.y_root)
		finally:
			self.__rightmenubar.grab_release()

	def ctrl_back(self,event=None):
		end_idx = self.__thisTextArea.index(tkinter.INSERT)
		end=end_idx+'-1c'
		start_idx = self.__thisTextArea.index(f'{end} wordstart')
		self.__thisTextArea.delete(start_idx, end_idx)
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def ctrl_barrow(self,event=None):
		cur=self.__thisTextArea.index(INSERT)
		self.__root.after(40,self.part_ctrl_barrow(cur))
	def part_ctrl_barrow(self,cur):
		end=cur+'+1c'
		self.__thisTextArea.mark_set(INSERT,end)
		start_idx = self.__thisTextArea.index(f'{end} wordstart')
		self.__thisTextArea.mark_set(INSERT,start_idx)
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def ctrl_farrow(self,event=None):
		cur=self.__thisTextArea.index(tkinter.INSERT)
		self.__root.after(40,self.part_ctrl_farrow(cur))
	def part_ctrl_farrow(self,cur):
		end=cur+'+1c'
		end_idx = self.__thisTextArea.index(f'{end} wordend')
		self.__thisTextArea.mark_set(INSERT,end_idx)
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)

	def find_win(self,event=None):
		__winfind=Toplevel()
		__winfind.attributes('-topmost',True)
		__winfind.title('Find and replace')
		__winfind.configure(bg='light pink')
		__winfind.resizable(width=FALSE,height=FALSE)
		Label(__winfind,text='Text to find: ',font=('Lucidia', 10),padx=2,pady=2,bg='light pink').grid(row=0,column=1,padx=2,pady=2)
		self.en1=StringVar()
		self.en1.set('')
		Entry(__winfind,font=('Lucidia', 10),textvariable=self.en1).grid(row=0,column=2)
		self.c=IntVar()
		self.c.set(0)
		Checkbutton(__winfind,text='Match case',font=('Lucidia', 10),bg='light pink',variable=self.c).grid(row=0,column=3,padx=5,pady=5)
		Button(__winfind,text='Find',command=self.find,bg='light green').grid(row=0,column=4,padx=5,pady=5)
		Label(__winfind,text='Text to repace: ',font=('Lucidia', 10),padx=2,pady=2,bg='light pink').grid(row=1,column=1,padx=2,pady=2)
		self.en2=StringVar()
		self.en2.set('')
		Entry(__winfind,font=('Lucidia', 10),textvariable=self.en2).grid(row=1,column=2)
		Button(__winfind,text='Replace',command=self.replace,bg='light green').grid(row=1,column=3,padx=5,pady=5)
		__winfind.mainloop()
	
	def highl_win(self,event=None):
		__winhigh=Toplevel()
		__winhigh.attributes('-topmost',True)
		__winhigh.title('Highlight Text')
		__winhigh.configure(bg='light pink')
		__winhigh.resizable(width=FALSE,height=FALSE)
		Label(__winhigh,text='Text to highlight: ',font=('Lucidia', 10),padx=2,pady=2,bg='light pink').grid(row=0,column=1,padx=2,pady=2)
		self.en1=StringVar()
		self.en1.set('')
		Entry(__winhigh,font=('Lucidia', 10),textvariable=self.en1).grid(row=0,column=2)
		self.c1=IntVar()
		self.c1.set(0)
		Checkbutton(__winhigh,text='Match case',font=('Lucidia', 10),bg='light pink',variable=self.c1).grid(row=0,column=3,padx=5,pady=5)
		self.foreg=StringVar()
		self.foreg.set('maroon1')
		colors=[
			'light blue',
			'salmon',
			'maroon1',
			'HotPink1',
			'green2',
			'medium blue',
			'tan1',
			'MediumOrchid1',
			'lime green',
			'purple',
			'cyan',
			'DarkOliveGreen1'
		]
		self.backgr=StringVar()
		self.backgr.set('white')
		bg_col=[
			'white',
			'black',
			'grey',
			'yellow'
		]
		op=OptionMenu(__winhigh,self.foreg,*colors)
		op.grid(row=0,column=4,padx=5,pady=5)
		op.config(bg='pink')
		op=OptionMenu(__winhigh,self.backgr,*bg_col)
		op.grid(row=0,column=5,padx=5,pady=5)
		op.config(bg='pink')
		Button(__winhigh,text='Highlight',command=self.highlight,bg='light green').grid(row=0,column=6,padx=5,pady=5)
		Button(__winhigh,text='Remove all highlights',command=self.remohigh,bg='light green').grid(row=1,column=6,padx=5,pady=5)
		self.lang=StringVar()
		self.lang.set('None')
		self.file_highl_type=self.lang.get()
		lan=[
			'Python file',
			'JavaScript'
		]
		op1=OptionMenu(__winhigh,self.lang,*lan)
		op1.grid(row=2,column=4,padx=5,pady=5)
		op1.config(bg='pink')
		Button(__winhigh,text='Highlight',command=self.lanhigh,bg='light green').grid(row=2,column=6,padx=5,pady=5)
		__winhigh.mainloop()

	def lanhigh(self):
		self.file_highl_type=self.lang.get()
		if self.lang.get()=='Python file':
			ls={'#':'red',"'":'yellow','"':'yellow','(':'orange',')':'orange','print':'light blue','import':'maroon1','=':'red','+':'red','-':'red','*':'red','/':'red','if ':'light green','else ':'light green','elif ':'light green','def ':'light green','class':'light green','for ':'light green','while ':'light green',' in ':'light green',' or ':'light green',' and ':'light green','.':'purple',",":'purple',':':'purple','[':'orange','[':'orange'}
			for s in ls.keys():
				if s:
					idx = '1.0'
					while 1:
						#searches for desired string from index 1
						idx = self.__thisTextArea.search(s, idx, nocase=1,
										stopindex=END)
						if not idx: break

						#last index sum of current index and
						#length of text
						lastidx = '%s+%dc' % (idx, len(s))
						#overwrite 'Found' at idx
						self.__thisTextArea.tag_add(f'highlight{self.highlight_counter}', idx, lastidx)
						idx = lastidx
					#mark located string as red
					self.__thisTextArea.tag_config(f'highlight{self.highlight_counter}',foreground=ls[s])
					self.highlight_counter+=1
		elif self.lang.get()=='JavaScript':
			ls={'#':'red',"'":'yellow','"':'yellow','(':'orange',')':'orange','print':'light blue','import':'maroon1','=':'red','+':'red','-':'red','*':'red','/':'red','if ':'light green','else ':'light green','elif ':'light green','def ':'light green','class':'light green','for ':'light green','while ':'light green',' in ':'light green',' or ':'light green',' and ':'light green','.':'purple',",":'purple',':':'purple','[':'orange','[':'orange'}
			for s in ls.keys():
				if s:
					idx = '1.0'
					while 1:
						#searches for desired string from index 1
						idx = self.__thisTextArea.search(s, idx, nocase=1,
										stopindex=END)
						if not idx: break

						#last index sum of current index and
						#length of text
						lastidx = '%s+%dc' % (idx, len(s))
						#overwrite 'Found' at idx
						self.__thisTextArea.tag_add(f'highlight{self.highlight_counter}', idx, lastidx)
						idx = lastidx
					#mark located string as red
					self.__thisTextArea.tag_config(f'highlight{self.highlight_counter}',foreground=ls[s])
					self.highlight_counter+=1

	def higl_switch(self):
		if self.file_highl_type=='Python file':
			self.lanhigh()
		elif self.file_highl_type=='JavaScript':
			self.lanhigh()

	def remohigh(self):
		#remove tag 'found' from index 1 to END
		self.lang.set('None')
		for i in range(0,self.highlight_counter+1):
			self.__thisTextArea.tag_remove(f'highlight{i}', '1.0', END)

	def highlight(self,event=None):
		self.highlight_counter+=1
		self.__highlight_stor[self.en1.get()]=self.foreg.get()
		edit=self.en1
		if self.c1.get()==1:
			case=0	# match upper case and lower case
		elif self.c1.get()==0:
			case=1
		#returns to widget currently in focus
		s = edit.get()		## edit= word to be found
		if s:
			idx = '1.0'
			while 1:
				#searches for desired string from index 1
				idx = self.__thisTextArea.search(s, idx, nocase=case,
								stopindex=END)
				if not idx: break

				#last index sum of current index and
				#length of text
				lastidx = '%s+%dc' % (idx, len(s))
				#overwrite 'Found' at idx
				self.__thisTextArea.tag_add(f'highlight{self.highlight_counter}', idx, lastidx)
				idx = lastidx
			#mark located string as red
			self.__thisTextArea.tag_config(f'highlight{self.highlight_counter}',foreground=self.foreg.get(),background=self.backgr.get())
	def highlight_pal(self,event=None):
		self.highlight_counter+=1
		self.__highlight_stor[self.__thisTextArea.selection_get()]='black'
		s = self.__thisTextArea.selection_get()
		if s:
			idx = '1.0'
			while 1:
				#searches for desired string from index 1
				idx = self.__thisTextArea.search(s, idx, nocase=0,
								stopindex=END)
				if not idx: break

				#last index sum of current index and
				#length of text
				lastidx = '%s+%dc' % (idx, len(s))
				#overwrite 'Found' at idx
				self.__thisTextArea.tag_add(f'highlight{self.highlight_counter}', idx, lastidx)
				idx = lastidx
			#mark located string as red
			self.__thisTextArea.tag_config(f'highlight{self.highlight_counter}',foreground='black',background='light pink')

	def find(self,event=None):
		if self.theme_counter==1:		## dark
			foreg='light blue'
			backgr='red'
		elif self.theme_counter==2:		## light
			foreg='maroon1'
			backgr='gray80'
		elif self.theme_counter==3:		## cool
			foreg='RoyalBlue1'
			backgr='gray30'
		elif self.theme_counter==4:		## monokai
			foreg='maroon1'
			backgr='gray99'
		elif self.theme_counter==5:		## monokai2
			foreg='light blue'
			backgr='red'
		edit=self.en1
		if self.c.get()==1:
			case=0	# match upper case and lower case
		elif self.c.get()==0:
			case=1
		#remove tag 'found' from index 1 to END
		self.__thisTextArea.tag_remove('found', '1.0', END)
		#returns to widget currently in focus
		s = edit.get()		## edit= word to be found
		if s:
			idx = '1.0'
			while 1:
				#searches for desired string from index 1
				idx = self.__thisTextArea.search(s, idx, nocase=case,
								stopindex=END)
				if not idx: break

				#last index sum of current index and
				#length of text
				lastidx = '%s+%dc' % (idx, len(s))
				#overwrite 'Found' at idx
				self.__thisTextArea.tag_add('found', idx, lastidx)
				idx = lastidx
			#mark located string as red
			self.__thisTextArea.tag_config('found',foreground=foreg,background=backgr)

	def replace(self):
		x=self.__thisTextArea.get("1.0", "end-1c")
		self.__thisTextArea.delete("1.0", "end")   # Deletes previous data
		self.__thisTextArea.insert(tkinter.END, x.replace(self.en1.get(),self.en2.get()))
		_tempstore1=self.__thisTextArea.get(1.0,'end-1c')
		self.__allwindata[self.__winno-1]=_tempstore1

	def __updatewin(self,event=None):
		edit=''
		self.__thisTextArea.tag_remove('found', '1.0', END)
		cur = self.__thisTextArea.index(tkinter.INSERT)
		cur=cur.split('.')
		self.l1.config(text=f'	    	                		Line: {(int(cur[0]))}   Col: {(int(cur[1])+1)}')
	def __updatewinx(self,event=None):
		self.__root.after(50,self.__updatewin)
		self.__root.after(50,self._on_change)
		self.__root.after(1,self.bigcur)
		self.__root.after(2,self.__algo_linno)
	def on_enter(self,e):
		e.widget['background'] = 'DarkGoldenrod1'
		e.widget['foreground'] = 'black'
	def on_leave(self,e):
		e.widget['background'] = '#FBFBFB'
		e.widget['foreground'] = 'black'
	def on_enterx(self,e):
		e.widget['background'] = 'red'
		e.widget['foreground'] = 'white'
	def on_entery(self,e):
		e.widget['background'] = 'gray50'
		e.widget['foreground'] = 'white'
	def frame_gen(self):
		self.frame_cop.destroy()
		self.redrawvr='redraw1'
		self.frame_cop=Frame(self.__root,bg='#FBFBFB',width=self.__root.winfo_screenwidth())
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
		Label(self.frame_cop,text=' ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=0,pady=2)
		bg5=Image.open(r'\icons\cut-white.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__cut,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=1,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\copy-white.png')
		bg5 =bg5.resize((41,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__copy,bg='#FBFBFB',fg='gray80',height=45,width=41,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=2,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\paste-white.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__paste,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=3,padx=5,pady=2)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\selectall.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__selectall,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=4,padx=5,pady=2)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		Label(self.frame_cop,text='  |  ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=5,padx=15,pady=2)
		bg5=Image.open(r'\icons\undo-white.png')
		bg5 =bg5.resize((63,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__thisTextArea.edit_undo,bg='#FBFBFB',fg='gray80',height=45,width=63,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=6,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\redo-white.png')
		bg5 =bg5.resize((63,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__thisTextArea.edit_redo,bg='#FBFBFB',fg='gray80',height=45,width=63,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=7,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		Label(self.frame_cop,text='  |  ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=8,padx=15,pady=2)
		bg5=Image.open(r'\icons\plus-white.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__size2,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=9,pady=7,padx=2)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		self.sizepal=Label(self.frame_cop,text=f'{self.size}',bg='#FBFBFB',fg='#1269CD',borderwidth=0,font=('Calibri',25,'bold'))
		self.sizepal.grid(row=0,column=10,padx=15,pady=2)
		bg5=Image.open(r'\icons\minus-white.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__size1,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=11,padx=2)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		Label(self.frame_cop,text='  |  ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=12,padx=15,pady=2)
		bg5=Image.open(r'\icons\select.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.highlight_pal,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=13,padx=2)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		Label(self.frame_cop,text='  |  ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=14,padx=15,pady=2)
		bg5=Image.open(r'\icons\new-file.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__addwin,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=15,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\switch-file.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__switch_window,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=16,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\open-icon.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__openFile,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=17,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\save-icon.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__saveFile,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=18,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		bg5=Image.open(r'\icons\savebin-icon.png')
		bg5 =bg5.resize((40,45), Image.ANTIALIAS)
		bg5 = ImageTk.PhotoImage(bg5)
		bt5=Button(self.frame_cop,image=bg5,command=self.__saveasbin,bg='#FBFBFB',fg='gray80',height=45,width=40,borderwidth=0,font=('Calibri',20,'bold'))
		bt5.image=bg5
		bt5.grid(row=0,column=19,padx=5)
		bt5.bind("<Enter>", self.on_enter)
		bt5.bind("<Leave>", self.on_leave)
		Label(self.frame_cop,text='  |  ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=20,padx=15,pady=2)
		bt5=Button(self.frame_cop,text='?',command=self.__showAbout,bg='#FBFBFB',fg='black',borderwidth=0,width=3,font=('Calibri',17,'bold'))
		bt5.grid(row=0,column=21,sticky=E,padx=2)
		bt5.bind("<Enter>", self.on_entery)
		bt5.bind("<Leave>", self.on_leave)
		bt5=Button(self.frame_cop,text='X',command=self.frame_destroy,bg='#FBFBFB',fg='black',borderwidth=0,width=3,font=('Calibri',17,'bold'))
		bt5.grid(row=0,column=22,sticky=E,padx=5)
		bt5.bind("<Enter>", self.on_enterx)
		bt5.bind("<Leave>", self.on_leave)
		Label(self.frame_cop,text=' ',bg='#FBFBFB',fg='black',borderwidth=0,font=('Calibri',20,'bold')).grid(row=0,column=23,padx=2,pady=2)
		self.frame_cop.place(x=0,y=0)
	def pass1(self):
		pass
	def frame_destroy(self):
		self.redrawvr='redraw'
		ind=self.__thisTextArea.index(INSERT)
		if self.redrawvr=='redraw':
			self.linenumbers.redraw(ind)
		elif self.redrawvr=='redraw1':
			self.linenumbers.redraw1(ind)
		self.frame_cop.place_forget()
	def __updatewinx_but(self,event=None):
		self.__root.after(50,self.__updatewin)
		self.__root.after(1,self.bigcur_but)
		self.__updatewin()
		self.__algo_linno()
		self._on_change()
		# print(self.__thisTextArea.selection_get())
	def __algo_linno(self):
		to=self.__thisTextArea.index(END)
		to=to.split('.')[0]
		al=len(to)
		self.linenumbers.config(width=15*int(al))
	def __exportaspdf(self,event=None):
		from fpdf import FPDF
		pdf=FPDF()
		pdf.add_page()
		pdf.set_font("Courier", size = 10)
		text=self.__thisTextArea.get('1.0','end-1c')
		text=text.split('\n')
		lne=0
		for i in text:
			lne+=1
			pdf.cell(200, 6, txt = i, 
         			ln = lne, align = 'L')
		pdffile=asksaveasfilename(initialfile='Untitled.pdf',
										defaultextension=".pdf",
										filetypes=[("pdf files","*.*"),
											("pdf files","*.pdf")])
		try:
			pdf.output(pdffile) 
		except Exception as e:
			pass
		
	def _on_mousewheel(self, event):
		self.__thisTextArea.yview_scroll(int(-1*(event.delta/120)), "units")
	
	def __shiftenter_after(self,event=None):
		ind=self.__thisTextArea.index(INSERT)
		self.__thisTextArea.insert(ind,': ')

	def __shiftenter(self,event=None):
		self.__root.after(10,self.__shiftenter_after)

	def bigcur(self,event=None):
		selected=self.__thisTextArea.get('sel.first', 'sel.last')
		if selected=='None':
			self.fgln=['yellow','blue','red','cyan','white']
			self.__thisTextArea.tag_configure("bigfont", font=(f"{self.font}", f"{(self.size)+1}"),foreground=self.fgln[self.theme_counter-1])
			self.__thisTextArea.tag_remove('bigfont',1.0,END)
			tin=self.__thisTextArea.index(INSERT)
			t=tin.split('.')
			self.__thisTextArea.tag_add('bigfont',f'{int(t[0])}.0',f'{int(t[0])+1}.0')
			# ln=self.__thisTextArea.get(f'{int(t[0])}.0', f'{int(t[0])}.end')
			# self.__thisTextArea.delete(f'{int(t[0])}.0', f'{int(t[0])}.end')
			# self.__thisTextArea.insert(f'{int(t[0])}.0', f"{ln}",("bigfont",))
			# self.__thisTextArea.mark_set(INSERT,tin)
			self.prev=int(tin.split('.')[0])
		else: ...
	def bigcur_but(self,event=None):
		selected=self.__thisTextArea.get('sel.first', 'sel.last')
		self.now=int(self.__thisTextArea.index(INSERT).split('.')[0])
		if selected=='None' and self.now!=self.prev:
			self.fgln=['yellow','blue','red','cyan','white']
			self.__thisTextArea.tag_configure("bigfont", font=(f"{self.font}", f"{(self.size)+1}"),foreground=self.fgln[self.theme_counter-1])
			self.__thisTextArea.tag_remove('bigfont',1.0,END)
			tin=self.__thisTextArea.index(INSERT)
			t=tin.split('.')
			self.__thisTextArea.tag_add('bigfont',f'{int(t[0])}.0',f'{int(t[0])+1}.0')
			# ln=self.__thisTextArea.get(f'{int(t[0])}.0', f'{int(t[0])}.end')
			# self.__thisTextArea.delete(f'{int(t[0])}.0', f'{int(t[0])}.end')
			# self.__thisTextArea.insert(f'{int(t[0])}.0', f"{ln}",("bigfont",))
			# self.__thisTextArea.mark_set(INSERT,tin)
			self.prev=int(tin.split('.')[0])
		else: ...
	def updatebq(self,event=None):
		ind=self.__thisTextArea.index(INSERT)
		inuse=ind.split('.')
		ind2=f'{int(inuse[0])}.{int(inuse[1])-1}'
		brq=self.__thisTextArea.get(ind2,ind)
		if brq=='(':
			self.__thisTextArea.insert(ind,')')
		elif brq=='[':
			self.__thisTextArea.insert(ind,']')
		elif brq=='{':
			self.__thisTextArea.insert(ind,'}')			
		elif brq=='"':
			self.__thisTextArea.insert(ind,'"')
		elif brq=="'":
			self.__thisTextArea.insert(ind,"'")
		elif brq=="<":
			self.__thisTextArea.insert(ind,">")
		self.__thisTextArea.mark_set(INSERT,ind)
		self.__updatewinx()
	def __updatbrac(self,event=None):
		self.__root.after(2,self.updatebq)
	def __movetxt(self,event=None):
		print('hello')
	def run(self):
		# Run main application
		self.__root.bind('<Control-s>',self.__saveFile_key)
		self.__root.bind('<Control-o>',self.__openFile_key)
		self.__root.bind('<Control-=>',self.__size2)
		self.__root.bind('<Control-minus>',self.__size1)
		self.__root.bind('<Control-b>',self.__bold)
		self.__root.bind('<Control-Shift-S>',self.__saveFileAs_key)
		self.__root.bind('<Control-g>',self.__switchfonts)
		self.__root.bind('<Control-m>',self.__switchthemes)
		self.__root.bind('<Control-Shift-B>',self.__saveasbin)
		self.__root.bind('<Control-Shift-N>',self.__getfrombin)
		self.__root.protocol("WM_DELETE_WINDOW",self.__quitApplication)
		self.__thisTextArea.bind("<Button-3>", self._rightclickmenu)
		self.__root.bind('<Control-BackSpace>', self.ctrl_back)
		self.__root.bind('<Control-f>', self.find_win)
		self.__root.bind('<Control-r>', self.find_win)
		self.__root.bind('<Control-h>', self.highl_win)
		self.__root.bind('<Control-p>', self.__exportaspdf)
		self.__root.bind("<Key>", self._on_change)
		self.__root.bind("<Button-1>", self._on_change)
		self.__thisTextArea.bind("<Key>", self.__updatewinx)
		self.__thisTextArea.bind("<Button-1>", self.__updatewinx_but)
		self.__thisTextArea.bind("<(>", self.__updatbrac)
		self.__thisTextArea.bind("<'>", self.__updatbrac)
		self.__thisTextArea.bind('<">', self.__updatbrac)
		self.__thisTextArea.bind('<{>', self.__updatbrac)
		self.__thisTextArea.bind('<[>', self.__updatbrac)
		self.__thisTextArea.bind("<Alt-Button-1>", self.__movetxt)
		self.__thisTextArea.bind("<Shift-Return>", self.__shiftenter)
		self.__thisTextArea.bind("<Control-Tab>", self.__switch_window)
		# self.__thisTextArea.bind("<<>", self.__updatbrac)
		self.__thisTextArea.bind("<<Change>>", self._on_change)
		self.__thisTextArea.bind("<Configure>", self._on_change)
		self.__thisTextArea.bind('<Control-Left>',self.ctrl_barrow)
		self.__thisTextArea.bind('<Control-Right>',self.ctrl_farrow)
		self.linenumbers.bind_all("<MouseWheel>", self._on_mousewheel)
		self.frame_gen()
		self.__root.mainloop()

class TextLineNumbers(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None
        self.size=14
        self.fill='white'

    def attach(self, text_widget):
        self.textwidget = text_widget
        
    def size2(self,*args):
        if args[0]==12 or args[0]==10:
            self.size=11
        elif args[0]==14 :
            self.size=12
        else :
            self.size=14
    def size1(self,*args):
        if args[0]==12 or args[0]==10:
            self.size=11
        elif args[0]==14 :
            self.size=12
        else : 
            self.size=14
    def filllight(self):
        self.fill='maroon'
    def filldark(self):
        self.fill='white'
    def fillcool(self):
        self.fill='SteelBlue3'
    def redraw(self,ind, *args,event=None):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            if linenum==ind.split('.')[0]:
            	self.create_text(2,y,anchor="nw", text=linenum,font=('Lucida Console', self.size+2,'bold'),fill=self.fill)
            else:
            	self.create_text(2,y,anchor="nw", text=linenum,font=('Lucida Console', self.size))
            i = self.textwidget.index("%s+1line" % i)
    def redraw1(self,ind, *args,event=None):
        '''redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            if linenum=='1' or linenum=='2':
            	self.create_text(2,y,anchor="nw", text='',font=('Lucida Console', self.size+2,'bold'),fill=self.fill)
            elif linenum==ind.split('.')[0]:
            	self.create_text(2,y,anchor="nw", text=str(int(linenum)-2),font=('Lucida Console', self.size+2,'bold'),fill=self.fill)
            else:
            	self.create_text(2,y,anchor="nw", text=str(int(linenum)-2),font=('Lucida Console', self.size))
            i = self.textwidget.index("%s+1line" % i)

class CustomText(Text):
    def __init__(self, *args, **kwargs):
        Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, *args):
        # let the actual widget perform the requested action
    #    cmd = (self._orig,) + args
    #    result = self.tk.call(cmd)

        # generate an event if something was added or deleted,
        # or the cursor position changed
    #    if (args[0] in ("insert", "replace", "delete") or 
    #        args[0:3] == ("mark", "set", "insert") or
    #        args[0:2] == ("xview", "moveto") or
    #        args[0:2] == ("xview", "scroll") or
    #        args[0:2] == ("yview", "moveto") or
    #        args[0:2] == ("yview", "scroll")
    #    ):
    #        self.event_generate("<<Change>>", when="tail")
        # return what the actual widget returned
    #    return result
	#######################################################################
    	# avoid error when copying
        if args[0] == 'get' and (args[1] == 'sel.first' and args[2] == 'sel.last') and not self.tag_ranges('sel'): return
		# avoid error when deleting
        if args[0] == 'delete' and (args[1] == 'sel.first' and args[2] == 'sel.last') and not self.tag_ranges('sel'): return
        cmd = (self._orig,) + args
        result = self.tk.call(cmd)
        if args[0] in ('insert', 'delete', 'replace'):
    	    self.event_generate('<<TextModified>>')
        elif (args[0:2] == ("xview", "moveto") or
           	args[0:2] == ("xview", "scroll") or
           	args[0:2] == ("yview", "moveto") or
           	args[0:2] == ("yview", "scroll")	):
    	    self.event_generate("<<Change>>", when="tail")
        return result
notepad = Notepad(width=600,height=400)
notepad.run()
