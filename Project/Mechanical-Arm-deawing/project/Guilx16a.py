# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import cv2
import numpy
import pyserial
import lewansoul_lx16a
import time

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		gSizer1 = wx.GridSizer( 7, 2, 0, 0 )
		self.ser = pyserial.Serial('COM9', 9600, timeout=1)
		#self.ser = serial.Serial('COM4', 9600, timeout=1)
		self.SERIAL_PORT = "COM7"
		self.prv_step = 0
		self.pulse = 0

		self.controller = lewansoul_lx16a.ServoController(serial.Serial(self.SERIAL_PORT, 115200, timeout=1), )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Servo 1", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		gSizer1.Add( self.m_staticText1, 0, wx.ALL, 7 )

		self.m_spinCtrl1 = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		gSizer1.Add( self.m_spinCtrl1, 0, wx.ALL, 7)

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Servo 2", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		gSizer1.Add( self.m_staticText2, 0, wx.ALL, 7 )

		self.m_spinCtrl2 = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		gSizer1.Add( self.m_spinCtrl2, 0, wx.ALL, 7 )

		self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"Servo 3", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		gSizer1.Add( self.m_staticText3, 0, wx.ALL, 7 )

		self.m_spinCtrl3 = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		gSizer1.Add( self.m_spinCtrl3, 0, wx.ALL, 7 )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Servo 4", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		gSizer1.Add( self.m_staticText4, 0, wx.ALL, 7 )

		self.m_spinCtrl4 = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		gSizer1.Add( self.m_spinCtrl4, 0, wx.ALL, 7 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"Servo 5", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		gSizer1.Add( self.m_staticText5, 0, wx.ALL, 7 )

		self.m_spinCtrl5 = wx.SpinCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0 )
		gSizer1.Add( self.m_spinCtrl5, 0, wx.ALL, 7 )

		self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"Step 0", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText6.Wrap(-1)
		gSizer1.Add(self.m_staticText6, 0, wx.ALL, 7)

		self.m_spinCtrl6 = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 0, 10, 0)
		gSizer1.Add(self.m_spinCtrl6, 0, wx.ALL, 7)

		self.m_button1 = wx.Button( self, wx.ID_ANY, u"RESET", wx.DefaultPosition, wx.DefaultSize, 0 )
		gSizer1.Add( self.m_button1, 0, wx.ALL, 7 )


		self.SetSizer( gSizer1 )
		self.Layout()

		self.Centre(wx.BOTH)
		self.m_spinCtrl1.SetRange(1, 1000)
		self.m_spinCtrl1.SetValue(1)

		self.m_spinCtrl2.SetRange(1, 1000)
		self.m_spinCtrl2.SetValue(1)

		self.m_spinCtrl3.SetRange(1, 1000)
		self.m_spinCtrl3.SetValue(1)

		self.m_spinCtrl4.SetRange(1, 1000)
		self.m_spinCtrl4.SetValue(1)

		self.m_spinCtrl5.SetRange(1, 170)
		self.m_spinCtrl5.SetValue(10)

		self.m_spinCtrl6.SetRange(1, 21000)
		self.m_spinCtrl6.SetValue(1)



		# Connect Events
		self.m_spinCtrl1.Bind( wx.EVT_SPINCTRL, self.Servo1 )
		self.m_spinCtrl1.Bind( wx.EVT_TEXT_ENTER, self.Servo1 )
		self.m_spinCtrl2.Bind( wx.EVT_SPINCTRL, self.Servo2 )
		self.m_spinCtrl2.Bind( wx.EVT_TEXT_ENTER, self.Servo2 )
		self.m_spinCtrl3.Bind( wx.EVT_SPINCTRL, self.Servo3 )
		self.m_spinCtrl3.Bind( wx.EVT_TEXT_ENTER, self.Servo3 )
		self.m_spinCtrl4.Bind( wx.EVT_SPINCTRL, self.Servo4 )
		self.m_spinCtrl4.Bind( wx.EVT_TEXT_ENTER, self.Servo4 )
		self.m_spinCtrl5.Bind( wx.EVT_SPINCTRL, self.Servo5 )
		self.m_spinCtrl5.Bind( wx.EVT_TEXT_ENTER, self.Servo5 )
		self.m_spinCtrl6.Bind(wx.EVT_SPINCTRL, self.Step0)
		self.m_spinCtrl6.Bind(wx.EVT_TEXT_ENTER, self.Step0)
		self.m_button1.Bind(wx.EVT_BUTTON, self.OnButtonSetSpinCtrl1)

	def OnButtonSetSpinCtrl1(self, event):
		delay = 2000  # จำนวนมิลลิวินาทีที่ต้องการให้เวลาดีเลย์

		def set_spin_ctrl_with_delay(ctrl, value, time_delay):
			wx.CallLater(time_delay, ctrl.SetValue, value)

		set_spin_ctrl_with_delay(self.m_spinCtrl1, 423, 0)
		set_spin_ctrl_with_delay(self.m_spinCtrl2, 10, delay * 1)
		set_spin_ctrl_with_delay(self.m_spinCtrl3, 500, delay * 2)
		set_spin_ctrl_with_delay(self.m_spinCtrl4, 500, delay * 3)
		set_spin_ctrl_with_delay(self.m_spinCtrl5, 0, delay * 4)
		set_spin_ctrl_with_delay(self.m_spinCtrl6, 1, delay * 5)

		wx.CallLater(delay * 6, self.use_spin_ctrl_values)

	def use_spin_ctrl_values(self):
			# นำค่าไปใช้งาน
			self.controller.move(1, self.m_spinCtrl1.GetValue(), 1000)
			time.sleep(0.1)
			self.controller.move(2, self.m_spinCtrl2.GetValue(), 1000)
			time.sleep(0.1)
			self.controller.move(3, self.m_spinCtrl3.GetValue(), 1000)
			time.sleep(0.1)
			self.controller.move(4, self.m_spinCtrl4.GetValue(), 1000)
			time.sleep(0.1)
			SV = self.m_spinCtrl5.GetValue()
			myStr = str(SV)
			res = bytes('S' + myStr, 'utf-8')
			self.ser.write(res + b'\n')
			print(res)
			print(SV)
			time.sleep(0.1)
			SV = self.m_spinCtrl6.GetValue()
			print(SV)
			if SV >= self.prv_step:
				myStr = str(abs(SV - self.prv_step))
				self.prv_step = SV
				self.pulse = SV
				res = bytes('L' + myStr, 'utf-8')
				self.ser.write(res + b'\n')
				print(res)
				print(self.prv_step)
			else:
				myStr = str(abs(SV - self.prv_step))
				self.prv_step = SV
				self.pulse = SV
				res = bytes('R' + myStr, 'utf-8')
				self.ser.write(res + b'\n')
				print(res)
				print(self.prv_step)
	def __del__( self ):
		pass


	# Virtual event handlers, override them in your derived class
	def Servo1( self, event ):
		#event.Skip()


		m1 = int(event.GetPosition())
		print("m1=", m1)
		self.controller.move(1, m1, 1000)
		time.sleep(.1)


	def Servo2( self, event ):
		#event.Skip()

		m2 = int(event.GetPosition())
		print("m2=", m2)
		self.controller.move(2, m2, 1000)
		time.sleep(.1)


	def Servo3( self, event ):
		#event.Skip()

		m3 = int(event.GetPosition())
		print("m3=", m3)
		self.controller.move(3, m3, 1000)
		time.sleep(.1)


	def Servo4( self, event ):
		#event.Skip()

		m4 = int(event.GetPosition())
		print("m4=", m4)
		self.controller.move(4, m4, 1000)
		time.sleep(.1)


	def Servo5( self, event ):

		SV = int(event.GetPosition())
		myStr = str(SV)
		res = bytes('S' + myStr, 'utf-8')
		self.ser.write(res + b'\n')
		print(res)
		print(SV)
		time.sleep(.1)


	def Step0( self, event ):

		SV = int(event.GetPosition())
		print(SV)

		if(SV >= self.prv_step):
			myStr = str(abs(SV - self.prv_step))
			self.prv_step = SV
			self.pulse = SV
			res = bytes('L' + myStr, 'utf-8')
			self.ser.write(res + b'\n')
			print(res)
			print(self.prv_step)
			# print(SV)
		else:
			myStr = str(abs(SV - self.prv_step))
			self.prv_step = SV
			self.pulse = SV
			res = bytes('R' + myStr, 'utf-8')
			self.ser.write(res + b'\n')
			print(res)
			print(self.prv_step)
			# print(SV)


		# res = bytes('S' + myStr, 'utf-8')
		# self.ser.write(res + b'\n')
		# print(res)
		# print(SV)
		time.sleep(.1)




class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame1(parent=None, )
        self.frame.Show()
        return True



app = MyApp()
app.MainLoop()