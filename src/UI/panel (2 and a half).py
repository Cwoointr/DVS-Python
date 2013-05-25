import wx, os
import sys
import guitest
from Controller import *


# file filter for pictures: bitmap and jpeg files
IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
          "|*.jpg; *.jpeg; *.jpe; *.jfif|" \
          "Raw Files |*.cr2; *crw|" \
          "All Files |*.*"

class My_App(wx.App):

    def OnInit(self):
        self.frame = My_Frame(None)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True


class My_Frame(wx.Frame):

    def __init__(self, image, parent=None,id=-1, title='Generic Title',
                 pos=wx.DefaultPosition, style=wx.CAPTION | wx.STAY_ON_TOP):     

        size = wx.DisplaySize()
        wx.Frame.__init__(self, parent, id, 'Digital Vision Screening',
                          pos, size)

        sizer_h = wx.BoxSizer(wx.HORIZONTAL)

        self.panel0 = User_Interaction0(self)       
        sizer_h.Add(self.panel0, 1, wx.EXPAND)

        self.panel1 = User_Interaction1(self)       
        sizer_h.Add(self.panel1, 1, wx.EXPAND)

        self.SetSizer(sizer_h)

        self.panel0.ShowYourself()

    def ShutDown(self):
        self.Destroy()


class User_Interaction0(wx.Panel):

    def __init__(self, parent, id=-1):

        wx.Panel.__init__(self, parent, id)
        self.PhotoMaxSize = 440

        # Passes to createWidgets method definition
        self.createWidgets()

        self.Show(True)        
        self.Show(True)

    def createWidgets(self):
        # Welcome message
        welcome = "Welcome to DVS!"
        welcomeFont = wx.Font(13, wx.NORMAL, wx.NORMAL, wx.BOLD)
        welcomemsg = wx.StaticText(self, -1, welcome)
        welcomemsg.SetFont(welcomeFont)

        # Horizontal Image
        horImg = wx.EmptyImage(440,440)
        self.horImgCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                  wx.BitmapFromImage(horImg))

        # Displays path of horizontal image
        self.horPhotoTxt = wx.TextCtrl(self, size=(350,-1))

        horiBtn = wx.Button(self, label='Horizontal')
        horiBtn.Bind(wx.EVT_BUTTON, self.horOpenFile)


        # Vertical Image
        # I did this the dumb way because I don't know how to use parameters
        # in Python :/ So I made an exact replica of a method.. haha. Might
        # be helpful to differentiate, however.
        vertImg = wx.EmptyImage(440,440)
        self.vertImgCtrl = wx.StaticBitmap(self, wx.ID_ANY,
                                        wx.BitmapFromImage(vertImg))

        # Displays path of vertical image
        self.vertPhotoTxt = wx.TextCtrl(self, size=(350,-1))
        
        vertiBtn = wx.Button(self, label='Vertical')
        vertiBtn.Bind(wx.EVT_BUTTON, self.vertOpenFile)


        self.Raise()
        self.SetPosition((0,0))
        self.Fit()  
        self.Hide()

#------------------------------------------------------------------------------

        # Resolve Layout Issues
        self.full = wx.BoxSizer(wx.VERTICAL)
        
        self.header = wx.BoxSizer(wx.HORIZONTAL)
        self.body = wx.BoxSizer(wx.HORIZONTAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.horBrowseAndText = wx.BoxSizer(wx.HORIZONTAL)
        self.vertBrowseAndText = wx.BoxSizer(wx.HORIZONTAL)

        self.footer = wx.BoxSizer(wx.HORIZONTAL)

        # This aligns the whole layout vertically, including header, body,
        # and bottom line (staticLine).
        self.full.Add(self.header, 0, wx.ALL | wx.CENTER, 5)
        self.full.Add(wx.StaticLine(self, wx.ID_ANY),
                      0, wx.ALL|wx.EXPAND, 5)
        self.full.Add(self.body, 0, wx.ALL | wx.CENTER, 5)
        self.full.Add(wx.StaticLine(self, wx.ID_ANY),
                        0, wx.ALL|wx.EXPAND, 5)
        self.full.Add(self.footer, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        # This centers the welcome message ("Welcome to DVS!") and puts
        # it at the top.
        self.header.Add(welcomemsg, 0, wx.ALL | wx.EXPAND | wx.CENTER, 5)
        #self.footer.Add(confBtn, 0, wx.ALL | wx.EXPAND, 5)

        # This portions the left side of the layout, including left
        # image, left browse button (horizontal button), and left text
        # control box, which contains the path of the horizontal image.
        self.body.Add(self.leftSizer, 0, wx.LEFT | wx.EXPAND, 5)
        self.leftSizer.Add(self.horImgCtrl, 0, wx.ALL | wx.LEFT, 5)

        # Within the leftSizer container, we have a miniature sizer, called
        # horBrowseAndText, which allows us to format the text control box
        # and the horizontal browse button. 
        self.leftSizer.Add(self.horBrowseAndText, 0, wx.ALL | wx.LEFT |
                           wx.EXPAND, 5)

        self.horBrowseAndText.Add(self.horPhotoTxt, 0, wx.ALL | wx.LEFT, 5)
        self.horBrowseAndText.Add(horiBtn, 0, wx.ALL | wx.LEFT, 5)


        # This portions the right side of the layout, including right image,
        # right browse button (vertical button), and right text control box,
        # which contains the path of the horizontal image.
        self.body.Add(self.rightSizer, 0, wx.RIGHT | wx.EXPAND, 5)
        self.rightSizer.Add(self.vertImgCtrl, 0, wx.ALL | wx.RIGHT, 5)

        # Within the rightSizer container, we have a miniature sizer called
        # vertBrowseAndText, which allows us to format the text control box
        # and the vertical browse button.
        self.rightSizer.Add(self.vertBrowseAndText, 0, wx.ALL | wx.RIGHT |
                            wx.EXPAND, 5)
        self.vertBrowseAndText.Add(self.vertPhotoTxt, 0, wx.ALL | wx.RIGHT, 5)
        self.vertBrowseAndText.Add(vertiBtn, 0, wx.ALL | wx.RIGHT, 5)

        # build the bottom row
        btnBack = wx.Button(self, -1, 'Back')
        self.Bind(wx.EVT_BUTTON, self.OnBack, id=btnBack.GetId())
        btnNext = wx.Button(self, -1, 'Next')
        #self.Bind(wx.EVT_BUTTON, self.OnNext, id=btnNext.GetId())
        btnNext.Bind(wx.EVT_BUTTON, lambda event:
                     self.checkConf(event, self.horPhotoTxt.GetValue(),
                                    self.vertPhotoTxt.GetValue()))
        
        btnCancelExit = wx.Button(self, -1, 'Cancel and Exit')
        self.Bind(wx.EVT_BUTTON, self.OnCancelAndExit, id=btnCancelExit.GetId())
        rowbottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowbottomsizer.Add(btnBack, 0, wx.ALIGN_LEFT)
        rowbottomsizer.AddSpacer(5)
        rowbottomsizer.Add(btnNext, 0)
        rowbottomsizer.AddSpacer(5)
        rowbottomsizer.AddStretchSpacer(1)
        rowbottomsizer.Add(btnCancelExit, 0, wx.ALIGN_RIGHT)
        self.footer.Add(rowbottomsizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)


        self.SetSizer(self.full)
        self.Layout()

    ##################################################
    def checkConf(self, event, horiImg, vertImg):
        if horiImg == '' and vertImg == '':
            errorTxt1 = "No Images Detected, Please Enter Images"
            errMsg1 = wx.MessageDialog(self, errorTxt1, "No Images Detected", wx.OK)
            errMsg1.ShowModal()
            errMsg1.Destroy()
        elif horiImg == '':
            errorTxt2 = "No Horizontal Image Detected, Please Enter a Horizontal Image"
            errMsg2 = wx.MessageDialog(self, errorTxt2, "No Horizontal Image", wx.OK)
            errMsg2.ShowModal()
            errMsg2.Destroy()
        elif vertImg == '':
            errorTxt3 = "No Vertical Image Detected, Please Enter a Vertical Image"
            errMsg3 = wx.MessageDialog(self, errorTxt3, "No Vertical Image", wx.OK)
            errMsg3.ShowModal()
            errMsg3.Destroy()
        else:
            self.Hide()
            self.EyeDetect()
            self.GetParent().panel1.ShowYourself()
    ###################################################

#---------------------------------------------------------------------------
        
    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        aboutText = "Eye Diagnostic Program: Please Enter a Vertical and Horizontal Photo"
        dlg = wx.MessageDialog( self, aboutText, "About Sample Editor", wx.OK )
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True) # Close the frame.
 
    def horOpenFile(self, event):
        horDlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", IMGMASK,
                            wx.OPEN)
        if horDlg.ShowModal() == wx.ID_OK:
            horPath = horDlg.GetPath()
            self.horPhotoTxt.SetValue(horPath)
            self.horOnPaint()                  # moved to make code more stable
        # Can't load image from file '': file does not exist

        horDlg.Destroy()

    def horOnPaint(self):
        horFilepath = self.horPhotoTxt.GetValue()
        horImg = wx.Image(horFilepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        horW = horImg.GetWidth()
        horH = horImg.GetHeight()

        if horW > horH:
            NewhorW = self.PhotoMaxSize
            NewhorH = self.PhotoMaxSize * horH / horW
        else:
            NewhorH = self.PhotoMaxSize
            NewhorW = self.PhotoMaxSize * horW / horH
        horImg = horImg.Scale(NewhorW,NewhorH)

        self.horImgCtrl.SetBitmap(wx.BitmapFromImage(horImg))
        self.Refresh()


    def vertOpenFile(self, event):
        vertDlg = wx.FileDialog(self, "Choose a file", os.getcwd(), "", IMGMASK,
                            wx.OPEN)
        if vertDlg.ShowModal() == wx.ID_OK:
            vertPath = vertDlg.GetPath()
            self.vertPhotoTxt.SetValue(vertPath)
            self.vertOnPaint()             # moved to make code more stable

        vertDlg.Destroy()
        #self.OnPaint2()

    def vertOnPaint(self):
        vertFilepath = self.vertPhotoTxt.GetValue()
        vertImg = wx.Image(vertFilepath, wx.BITMAP_TYPE_ANY)

        # scale the image, preserving the aspect ratio
        vertW = vertImg.GetWidth()
        vertH = vertImg.GetHeight()

        if vertW > vertH:
            NewvertW = self.PhotoMaxSize
            NewvertH = self.PhotoMaxSize * vertH / vertW
        else:
            NewvertH = self.PhotoMaxSize
            NewvertW = self.PhotoMaxSize * vertW / vertH
        vertImg = vertImg.Scale(NewvertW,NewvertH)

        self.vertImgCtrl.SetBitmap(wx.BitmapFromImage(vertImg))
        self.Refresh()

#------
    def EyeDetect(self):
        horFilepath = self.horPhotoTxt.GetValue()
        vertFilepath = self.vertPhotoTxt.GetValue()
        thisPatient = detectEyes( horFilepath, vertFilepath )


    def ShowYourself(self):
        self.Raise()
        self.SetPosition((0,0))
        self.Fit()
        self.GetParent().GetSizer().Show(self)
        self.GetParent().GetSizer().Layout()


    def OnBack(self, event):
        self.Hide()
        self.GetParent().panel1.ShowYourself()
        self.GetParent().GetSizer().Layout()

    def OnNext(self, event):
        self.Hide()
        self.GetParent().panel1.ShowYourself()
        self.GetParent().GetSizer().Layout()

    def OnCancelAndExit(self, event):
        self.GetParent().ShutDown()

#-------------------------------------------------------------------

class User_Interaction1(wx.Panel):

    def __init__(self, parent, id=-1):

        wx.Panel.__init__(self, parent, id)

        # master sizer for the whole panel
        mastersizer = wx.BoxSizer(wx.VERTICAL)
        #mastersizer.SetMinSize((475, 592))
        mastersizer.AddSpacer(15)


        # build the top row
        txtHeader = wx.StaticText(self, -1, 'Read about This Boring\nProgram', (0, 0))
        font = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        txtHeader.SetFont(font)
        txtOutOf = wx.StaticText(self, -1, '2 out of 7', (0, 0))                
        rowtopsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowtopsizer.Add(txtHeader, 3, wx.ALIGN_LEFT) 
        rowtopsizer.Add((0,0), 1)  
        rowtopsizer.Add(txtOutOf, 0, wx.ALIGN_RIGHT) 
        mastersizer.Add(rowtopsizer, 0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15) 


        # build the middle row
        text = 'PANEL 1\n\n'
        text = text + 'This could be a giant blob of boring text.\n'

        txtBasic = wx.StaticText(self, -1, text)
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        txtBasic.SetFont(font)
        mastersizer.Add(txtBasic, 1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)  


        # build the bottom row
        btnBack = wx.Button(self, -1, 'Back')
        self.Bind(wx.EVT_BUTTON, self.OnBack, id=btnBack.GetId())
        btnNext = wx.Button(self, -1, 'Next')
        self.Bind(wx.EVT_BUTTON, self.OnNext, id=btnNext.GetId())
        btnCancelExit = wx.Button(self, -1, 'Cancel and Exit')
        self.Bind(wx.EVT_BUTTON, self.OnCancelAndExit, id=btnCancelExit.GetId())
        rowbottomsizer = wx.BoxSizer(wx.HORIZONTAL)
        rowbottomsizer.Add(btnBack, 0, wx.ALIGN_LEFT)
        rowbottomsizer.AddSpacer(5)
        rowbottomsizer.Add(btnNext, 0)
        rowbottomsizer.AddSpacer(5)
        rowbottomsizer.AddStretchSpacer(1)
        rowbottomsizer.Add(btnCancelExit, 0, wx.ALIGN_RIGHT)
        mastersizer.Add(rowbottomsizer, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=15)

        # finish master sizer
        mastersizer.AddSpacer(15)   
        self.SetSizer(mastersizer)

        self.Raise()
        self.SetPosition((0,0))
        self.Fit()  
        self.Hide()


    def ShowYourself(self):
        self.Raise()
        self.SetPosition((0,0))
        self.Fit()
        self.GetParent().GetSizer().Show(self)


    def OnBack(self, event):
        self.Hide()
        self.GetParent().panel0.ShowYourself()

    def OnNext(self, event):
        self.Hide()
        self.GetParent().panel0.ShowYourself()

    def OnCancelAndExit(self, event):
        self.GetParent().ShutDown()


def main():
    app = My_App(redirect = False)
    app.MainLoop()


if __name__ == '__main__':
    main()
