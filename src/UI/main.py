import wx, os
#from Controller import *
from interaction import *
from base import *
from page import *

app = wx.App()

#base frame holds everything
#wx.Frame(parent, id=-1, title=EmptyString, pos=DefaultPosition,
#	size=DefaultSize, style=DEFAULT_FRAME_STYLE, name=FrameNameStr)
base(None, -1, 'Digital Vision Screening',
	pos = wx.DefaultPosition,
	size = (1000,600),
	style = wx.DEFAULT_FRAME_STYLE)


# The mainloop is an endless cycle. It catches and dispatches all events 
# that exist during the life of our application.
app.MainLoop()