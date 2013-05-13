'''
Created on Dec 10, 2012

@author: Andrzej Jasinski

This test script check  in Logcat if message  onRequest: DECT_MM_REQUEST_SUB_SEARCH is sent after start Base search
Test steps:
1. go to Settings -> Handset + Base
2.Find and touch on Register button.
3. Insert string "0000" to PIN editor .
4. Press "ok" button.
5. Check required message appeared in LogCat.

additional assertion checks if all buttons and popups if they're ok

'''

import os
import sys, time
import subprocess
import unittest2
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
from gats_20.

SERIALNO = 'emulator-5554'
sys.argv = ['TestRegistrationSetUp', SERIALNO]
device, serialno = ViewClient.connectToDeviceOrExit()



'''testing class'''
class TestRegistrationDectActiveRadio(unittest2.TestCase): 

    def setUp(self):
         # subprocess.Popen(["/home/gigaset/android-sdk-linux/platform-tools/adb", "start-server"], bufsize=2048, shell=False)
         self.device = device
         self.serialno = serialno
         '''printing all running processes on the Device'''
         self.processes = str(device.shell('ps'))
         print self.processes

         
         DEBUG = True
         FLAG_ACTIVITY_NEW_TASK = 0x10000000
         package = 'com.android.settings'
         activity = '.Settings'
         component = package + "/" + activity
         device.startActivity(component=component, flags=FLAG_ACTIVITY_NEW_TASK)
         MonkeyRunner.sleep(3)
         self.test_string = "onRequest: DECT_MM_REQUEST_SUB_SEARCH"

         
         self.device.drag((150, 470), (150, 20))
         MonkeyRunner.sleep(2)         
         self.vc = ViewClient(self.device, self.serialno)       
         hb = self.vc.findViewWithText('Handset + Base')
         MonkeyRunner.sleep(2)
 
         if hb:
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
                   
    def testStartRegistrationRadioRequest(self):
          'start registration and checking if DECT_MM_REQUEST_SUB_SEARCH is in logcat'''
        
         
          register = self.vc.findViewWithText('Register')
          '''in this loop number of test repetition can be set'''
          proc = 'com.gigaset.android.registration'
          pid = str()
          for i in range(1, 3):
             if proc in self.processes:
                 for line in self.processes.splitlines():
                   if proc in line:
                      pid = line.split()[1]
             device.shell('kill ' + pid)
             '''check if registration process is active and if yes then it is killed'''
             
             MonkeyRunner.sleep(2)          
             if register:
                print >> sys.stderr, " This is %d test execution" % (i) 
                register.touch()
                self.vc.dump()
                MonkeyRunner.sleep(2)
                pineditor = self.vc.findViewById('id/dialog_pin_editor_inputtext') 
                if pineditor:
                    pineditor.device.type('0000')
                    # MonkeyRunner.sleep(1)
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
                       
                        
                        '''Catching  message from Logcat'''
                        p = subprocess.Popen(["/home/gigaset/android-sdk-linux/platform-tools/adb", "logcat", "-b", "radio", "-v", "time", "-d"], bufsize=2048, stdout=subprocess.PIPE, shell=False)
                        log_list = p.stdout.readlines()
                        result = False
                        for line in log_list:
                            if self.test_string in line:
                                print "Message has been found :      %s" % line
                                result = True 
                                break 
                                             
                        self.assertEqual(result, True, 'onRequest: DECT_MM_REQUEST_SUB_SEARCH not found') 
                                          
                        cancel = self.vc.findViewById('id/dialog_search_for_base_btn_cancel')
                        MonkeyRunner.sleep(1)
                        if cancel :
                            print >> sys.stderr, "Registration has started"                            
                            cancel.touch()
                            self.vc.dump()
                            # self.device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)
                            MonkeyRunner.sleep(1)
                            # self.vc.device.shell("am force-stop 'com.gigaset.android.registration'")
                        else:
                            print >> sys.stderr, "text in the Registration popup is not correct "
                            cancel.touch()
                            

                
             else:
 
                self.assertIsNotNone(register, " Register button not found")
                            
          MonkeyRunner.sleep(3)
          print >> sys.stderr, "test finished"   

        
      
'''test loader and runner'''    
suite = unittest2.TestLoader().loadTestsFromTestCase(TestRegistrationDectActiveRadio)
XMLTestRunner('/home/gigaset/test_report').run(suite)   
