#!/user/bin/env python
import wx, os
class MyFrame(wx.Frame):
    """We simply derive a new class of Frame."""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(600,700))
        panel = wx.Panel(self)

        IMGMASK = "JPEG Files |*.jpg|" \
                  ".BMP Files |*.bmp|" \
                  "All Files |*.*"

        # frame size = (width, length)
        horizontal = wx.Button(panel, 1, 'Horizontal', (50, 130), (110, -1))
        vertical = wx.Button(panel, 2, 'Vertical', (400, 130), (110, -1))

        self.Bind(wx.EVT_BUTTON, self.openFile, horizontal)
        self.Bind(wx.EVT_BUTTON, self.openFile, vertical)

        #Welcome message
        welcome = 'Welcome to DVS!'
        # SetPointSize(self, 20)
        wx.StaticText(panel, -1, welcome, pos=(250,10))

        # Setting up the menu.
        filemenu = wx.Menu()

        #wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWIdget
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)

        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

    	#Button to close
        xButton=wx.Button(panel,label="Close", pos=(500,600))
        xButton.Bind(wx.EVT_BUTTON, self.OnExit)
        
        self.Show(True)

    #add image in screens

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog( self, "A small text editor", "About Sample Editor", wx.OK )
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True) # Close the frame.


    def openFile(self, event):
        dlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            mypath = os.path.basename(path)
        dlg.Destroy()

app = wx.App(False)
frame = MyFrame(None, 'Digital Vision Screening')
app.MainLoop()
