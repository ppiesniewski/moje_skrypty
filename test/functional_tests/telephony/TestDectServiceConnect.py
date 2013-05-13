'''
Created on Dec 13, 2012

@author: gigaset
'''

# ! /usr/bin/env monkeyrunner
import sys, time
import os
import subprocess
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

LIB_PATH = "src/test/lib"
TEST_OUT_EXISTS = "test-report"
string = 'onReceive: intent action=android.intent.action.BOOT_COMPLETED'
test_string = 'GC_DECT_UNSOL_MIL_CONNECTED'

if  LIB_PATH not in sys.path:
    sys.path.append(LIB_PATH)
    from xmlrunner import XMLTestRunner
    import unittest2

class TestDectServiceConnect(unittest2.TestCase):
    
    def setUp(self):
	try:
 	  self.device = MonkeyRunner.waitForConnection(10)
          strProperty = self.device.getProperty('model')
        except:
          self.device = None
          self.assertIsNotNone(self.device, 'Check connection with the DUT')
          sys.exit()
        
	p = subprocess.Popen(["adb", "logcat", "-b", "main"], shell=False, stdout=subprocess.PIPE)
        while True:
          l = p.stdout.readline()
          if string in l:
            sys.stdout.write("\nfound: \n" + string + '\n')
            break
        
    def tearDown(self):
        pass

    def testReadAndParseRadioLogcat(self):
	 print '\n Searching: ' + test_string
 	 p = subprocess.Popen(["adb", "logcat", "-b", "radio", "-v", "time", "-d"], shell=False, stdout=subprocess.PIPE)
         l = p.stdout.readlines()
         test = False
	 for line in l:
           if test_string in line:
	     print '\nfound: \n' + line
             test = True
	     break
         self.assertEqual(test, True, 'onRequest: GC_DECT_UNSOL_MIL_CONNECTED')   




if TEST_OUT_EXISTS == False:
    suite = unittest2.TestLoader().loadTestsFromTestCase(TestDectServiceConnect)
    unittest2.main().run(suite)
else:
    TEST_OUT_DIR = "test-report"
    print "TEST_OUT_DIR set to", TEST_OUT_DIR
    suite = unittest2.TestLoader().loadTestsFromTestCase(TestDectServiceConnect)
    unittest2.main(testRunner=XMLTestRunner(output=TEST_OUT_DIR)).run(suite)

