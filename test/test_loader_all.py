'''
author: Andrzej Jasinski
This script loads test scripts with attibuttes parsed to them during calling this script
'''


import os
import sys
import subprocess
import unittest2

class TestExecutor():
    
    def __init__(self, test_dir):
        self.test_dir = test_dir
            
    def load_test(self):
        
        unittest2.defaultTestLoader.discover(self.test_dir, pattern='test*.py')

    def parse_attr(self):
        
        '''creates dictionary with parsed attributes to types of tests'''
        self.test_param = dict()
        '''what kind of test: quick:short or long'''
        if "short"  in sys.argv[1:]:
            self.test_param['test_type'] = 'short_test'
            self.setattr(testExecutor, 'test_type', self.test_param['test_type'])
        elif "long"  in sys.argv[1:]:
            self.test_param['test_type'] = 'long_test'
            self.setattr(testExecutor, 'test_type', self.test_param['test_type'])
            
        '''what type of DUT we are using: device or emulator'''
        if "emulator"  in sys.argv[1:]:
            self.test_param['device_type'] = 'emulator'
            self.setattr(testExecutor, 'device_type', self.test_param['device_type'])
        elif "device" in sys.argv[1:]:
            self.test_param['device_type'] = 'hw_device'
            self.setattr(testExecutor, 'device_type', self.test_param['device_type'])
            
        ''' initial condition of the DUT before starting test. For now there is only one: wipe data'''    
        if "wipe"  in sys.argv[1:]:
            self.test_param['initial_condition'] = 'wipe_data'
            self.setattr(testExecutor, 'initial_condition', self.test_param['initial_condition'])


testExecutor = TestExecutor()
    
    
    
    
    
if __name__ == "__main__" :
    '''First we need to delete all java compiled classes *py.class. but we need to remeber to don't touch lib and src packages'''
    test_folders = ['/apps_tests', '/functional_tests', '/kernel_tests', '/us_tests']
    test_root = str(os.getcwd())
    for directory in test_folders:
        subprocess.Popen(['find', (test_root + directory), '-name', '*py.class', '-delete'], bufsize=2048)
    
    '''Now test loader function is starting'''
    
    
    for directory in test_folders:
        try:
            testExecutor.load_test(test_root + directory) 
        except ImportError:
            print "Couldn't load tests from path: %s" % test_root + directory
    

