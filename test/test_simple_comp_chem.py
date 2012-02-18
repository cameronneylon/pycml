import unittest
from test_pycml import TestParameterList
from pycml.conventions.simple_comp_chem import *

###
#Testing of Simple CompChem CML Elements
####

class TestCompChemModule(TestParameterList):

    def testGenerate(self):
        self.test = CompChemModule('test-dictRef', 'test-title')
        self.assertIsInstance(self.test, CompChemModule)
        self.assertEqual(self.test.attrib['dictRef'], 'test-dictRef')
        self.assertEqual(self.test.attrib['title'], 'test-title')

    def testRequirements(self):
        self.assertRaises(TypeError, CompChemModule)
        self.assertRaises(UserWarning, CompChemModule, 'test-dictRef')

if __name__ == '__main__':
    warnings.simplefilter('error')
    unittest.main()
    
