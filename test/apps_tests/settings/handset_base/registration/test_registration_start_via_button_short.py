'''
Created on Dec 10, 2012

@author: gigaset
'''

import os, sys
import unittest2
import subprocess, time
from xmlrunner import XMLTestRunner

try:
    for p in os.environ['PYTHONPATH'].split(':'):
        if not p in sys.path:
            sys.path.append(p)
except:
    pass
    
try:
    sys.path.append(os.path.join(os.environ['LA_TEST_PROJECT_HOME'], 'src'))
except:
    pass

from com.android.monkeyrunner import MonkeyDevice, MonkeyRunner
from com.gigaset.android.viewclient import View, TextView, EditText, ViewClient


SERIALNO = 'emulator-5554'
sys.argv = ['TestRegistrationSetUp', SERIALNO]
device, serialno = ViewClient.connectToDeviceOrExit()



'''testing class'''
class TestRegistrationSetUp(unittest2.TestCase): 

    def setUp(self):
         # subprocess.Popen(["/home/gigaset/android-sdk-linux/platform-tools/adb", "start-server"], bufsize=2048, shell=False)
         self.device = device
         self.serialno = serialno
         DEBUG = True
         FLAG_ACTIVITY_NEW_TASK = 0x10000000
         package = 'com.android.settings'
         activity = '.Settings'
         component = package + "/" + activity
         device.startActivity(component=component, flags=FLAG_ACTIVITY_NEW_TASK)
         MonkeyRunner.sleep(3)
         
         
         self.device.drag((150, 470), (150, 20))
         MonkeyRunner.sleep(2)         
         self.vc = ViewClient(self.device, self.serialno)       
         hb = self.vc.findViewWithText('Handset + Base')
         MonkeyRunner.sleep(2) 
         if hb:
            # (x,y) = hb.getXY()
            hb.touch()
            self.vc.dump()
            self.assertIsNotNone(hb, "There is not 'Handset + Base' button")
            MonkeyRunner.sleep(2)
        
    def tearDown(self):
        self.device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
        MonkeyRunner.sleep(2)
        self.device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)
        print >> sys.stderr, "Test finished and now tearDown function made initial conditions"
        MonkeyRunner.sleep(2)
        self.device.shell("am force-stop 'com.android.settings")
        time.sleep(2)
        subprocess.Popen(["/home/gigaset/android-sdk-linux/platform-tools/adb", "kill-server"], bufsize=2048, shell=False)
        time.sleep(4)
    
        
    def testStartRegistrationPinIput(self):
         'start registration: touch register button, PIN input and checking if registration popup is correct'
        
         
         register = self.vc.findViewWithText('Register')
                    
         if register:
            # (x, y) = register.getXY()
            # print >>sys.stderr, "clicking button register @ (%d,%d) ..." % (x, y)

 
            for i in xrange(1, 3):
                print >> sys.stderr, " This is %d test execution number" % (i) 
                MonkeyRunner.sleep(1)
                register.touch()
                self.vc.dump()
                MonkeyRunner.sleep(2)
                pineditor = self.vc.findViewById('id/dialog_pin_editor_inputtext') 
                
                if pineditor:
                     pineditor.type('0000')
                     # MonkeyRunner.sleep(1)
                     # self.vc.dump()
                     # realpin=pineditor.getText() 
                     # self.assertEqual('0000', realpin, "Wrong PIN was entered by device!!!")
                     # print realpin
                     self.vc.dump()
                     MonkeyRunner.sleep(2)
                     ok = self.vc.findViewById('id/dialog_pin_editor_btn_ok')
                                  
                     if ok:
                         ok.touch()
                         self.vc.dump()
                         MonkeyRunner.sleep(2)
                         searchpopup = self.vc.findViewById('id/dialog_search_for_base_promptmessage')
                         cancel = self.vc.findViewById('id/dialog_search_for_base_btn_cancel')
                         progressbar = self.vc.findViewById('id/dialog_search_for_base_progressbar')
                         MonkeyRunner.sleep(2)
                         text = 'Searching for a base which is in registration mode'
                         realtext = searchpopup.getText()
                         print >> sys.stderr , 'Text which is it the popup is: %s ' % realtext
                         
                         self.assertIsNotNone(searchpopup, 'There is no popup with information about registration running')
                         self.assertIsNotNone(cancel, 'There is no Cancel button')
                         self.assertIsNotNone(progressbar, 'There is no Progressbar animation')
                         
                         if cancel and searchpopup and progressbar:
                             self.assertEqual(text, realtext, "Registration popup is not correct in English")
                             print >> sys.stderr, "Registration has started and popup is ok"
                             cancel.touch()
                             self.vc.dump()
                             # self.device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
                             MonkeyRunner.sleep(1)
                             
                         else:
                              print >> sys.stderr, "text in the Registration popup is not correct "
                              cancel.touch()
                              # self.vc.device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
                              MonkeyRunner.sleep(2)
                
         else:
              self.assertIsNotNone(register, " Register button not found") 
                        
         MonkeyRunner.sleep(3)
         print >> sys.stderr, "test finished"



'''test loader and runner'''    
suite = unittest2.TestLoader().loadTestsFromTestCase(TestRegistrationSetUp)
XMLTestRunner('/home/gigaset/test_report').run(suite)
