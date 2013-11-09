import wx, os

IMGMASK = "JPEG Files(*.jpg;*.jpeg;*.jpe;*.jfif) " \
          "|*.jpg; *.jpeg; *.jpe; *.jfif|" \
          "Raw Files |*.cr2; *crw|" \
          "All Files |*.*"

class interaction:

    upPath = ""

    def __init__(self):
      upPath = ""



# BUTTONS

    # upload button
    def upload(self, page, imgCtrl, text):
      # pops up box for user to upload image
      upBox = wx.FileDialog(page, "Choose an image.", os.getcwd(), "",
                            IMGMASK, wx.OPEN)
      if upBox.ShowModal() == wx.ID_OK:
        self.upPath = upBox.GetPath()
        self.upPaint(page, self.upPath, imgCtrl)
        text.SetValue(self.upPath)
          
    # reset button
    def reset(self, page, imgCtrl1, imgCtrl2, text1, text2):
        empty = wx.EmptyImage(440,440)     # Create empty image
        # Sets the 2 image controls to empty
        imgCtrl1.SetBitmap(wx.BitmapFromImage(empty))
        imgCtrl2.SetBitmap(wx.BitmapFromImage(empty))
        # Resets path names
        text1.SetValue("Please upload an image.")
        text2.SetValue("Please upload an image.")
        page.Refresh()

    # display the uploaded picture
    def upPaint(self, page, upPath, imgCtrl):
      newImg = wx.Image(upPath, wx.BITMAP_TYPE_ANY)
      
      width = newImg.GetWidth()
      height = newImg.GetHeight()
      maxSize = 440

      # scale the image to preserving the aspect ratio
      '''
      if width > height and width > maxSize:
        newWidth = maxSize
        newHeight = height / (width / float(maxSize))
      elif width > height and width < maxSize:
        newWidth = maxSize
        newHeight = height * (width / float(maxSize))
      elif width == maxSize:
        newWidth = maxSize

      if height > width and height > maxSize:
        newHeight = maxSize
        newWidth = width / (height / float(maxSize))
      elif height > width and height < maxSize:
        newHeight = maxSize
        newWidth = width * (height / float(maxSize))
      elif height == maxSize:
        newHeight = maxSize
      '''

      # This scaling works, but may have problems in future
      if width > height:
          newWidth = maxSize
          newHeight = maxSize * height/ width
      else:
          newHeight = maxSize
          newWidth = maxSize * width/ height
          
      newImg = newImg.Scale(newWidth,newHeight)
      imgCtrl.SetBitmap(wx.BitmapFromImage(newImg))
      page.Refresh()


# page movement functions
'''
    def ShowYourself(self):
        self.Raise()
        self.SetPosition((0,0))
        self.Fit()
        self.GetParent().GetSizer().Show(self)
        self.GetParent().GetSizer().Layout()

    def OnBack(self, event):
        self.Hide()
        self.GetParent().panel0.ShowYourself()
        self.GetParent().GetSizer().Layout()

    def OnNext(self, event):
        self.Hide()
        self.GetParent().panel2.ShowYourself()
        self.GetParent().GetSizer().Layout()

    def OnCancelAndExit(self, event):
        self.GetParent().ShutDown()
'''
