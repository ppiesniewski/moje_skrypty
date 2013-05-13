'''
Created on Dec 13, 2012

@author: gigaset
'''


# ! /usr/bin/env monkeyrunner
import sys
import os
import subprocess
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

LIB_PATH = "src/test/lib"
TEST_OUT_EXISTS = "test-report"

if  LIB_PATH not in sys.path:
    sys.path.append(LIB_PATH)
    from xmlrunner import XMLTestRunner
    import unittest2



class TestAdbState(unittest2.TestCase):
    
    def setUp(self):
	pass

    def tearDown(self):
        pass

    def testAdbStateAfterStartingEmu(self):
	        
	p = subprocess.Popen(["adb", "get-state"], shell=False, stdout=subprocess.PIPE)
        l = p.stdout.readline()
	print 'adb get-state: ' + l
	self.assertNotEqual(l, 'unknown\n', 'Device not found')


if TEST_OUT_EXISTS == False:
    suite = unittest2.TestLoader().loadTestsFromTestCase(TestAdbState)
    unittest2.main().run(suite)
else:
    TEST_OUT_DIR = "test-report"
    print "TEST_OUT_DIR set to", TEST_OUT_DIR
    suite = unittest2.TestLoader().loadTestsFromTestCase(TestAdbState)
    unittest2.main(testRunner=XMLTestRunner(output=TEST_OUT_DIR)).run(suite)

