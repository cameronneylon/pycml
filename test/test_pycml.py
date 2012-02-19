import unittest
from pycml.pycml import *

###
#Testing of CML Elements
####

class TestElement(unittest.TestCase):

    def setUp(self):
        self.text = 'test text'
        self.tag = 'testingtag'
        self.int = 5
        self.float = 6.321
        self.attrib = {'dataType' : 'test:dataType',
                       'units'    : 'test:units',
                       'title'    : 'test:title',
                       'dictRef'  : 'test:dictRef'}

    def tearDown(self):
        self.test = None

class TestScalarGeneration(TestElement):

    def setUp(self):
        TestElement.setUp(self)
        self.stringin = """<scalar dataType='test:dataType' units='test:units'>test text</scalar>"""
        self.xml = ET.fromstring(self.stringin)
        self.test = self.testGenerate()

    def testGenerate(self):
        return Scalar(self.text, self.attrib)

    def testEqual(self):
        self.assertEqual(ET.tostring(self.xml), ET.tostring(self.test))


class TestScalarDataTypeRequirement(TestElement):

    def testDataTypeReq(self):
        self.attrib.pop('dataType')
        self.assertRaises(CMLError, Scalar, self.text, self.attrib)

class TestScalarUnitsRequirement(TestElement):

    def testDataTypeReq(self):
        self.attrib.pop('units')
        self.assertRaises(CMLError, Scalar, self.text, self.attrib)

class BaseArrayTest(TestElement):

    def setUp(self):
        TestElement.setUp(self)
        self.intlist = range(1,100,3)
        self.stringinint = \
"""<array dataType="xsd:int" delimiter=" " length="33" units="test:units">1 4 7 10 13 16 19 22 25 28 31 34 37 40 43 46 49 52 55 58 61 64 67 70 73 76 79 82 85 88 91 94 97</array>"""
        self.strlist = ['a', 'bb', 'CCC', 'dddd']
        self.stringinstr = """<array dataType="xsd:str" delimiter=" " length="4"
                         units="test:units">a bb CCC dddd</array>"""
        self.floatlist = [1.3, 5.6, 7.3, 1.5e6, 26782.]
        self.stringinfloat = """<array dataType="xsd:double" delimiter=" " length="5"
                                units="test:units">1.3 5.6 7.3 1500000.0 26782.0</array>"""
        self.mixedlist = [1, 2, 3, 4, 'gtr']


class TestArrayGeneration(BaseArrayTest):

    def testIntList(self):
        self.test = Array(self.intlist, self.attrib)
        self.xml = ET.fromstring(self.stringinint)
        self.assertEqual(ET.tostring(self.test), ET.tostring(self.xml))
        self.assertEqual(self.test.attrib['length'], "33")
        self.assertEqual(self.test.attrib['dataType'], "xsd:int")

    def testStrList(self):
        self.test = Array(self.strlist, self.attrib)
        self.xml = ET.fromstring(self.stringinstr)
        self.assertEqual(ET.tostring(self.test), ET.tostring(self.xml))
        self.assertEqual(self.test.attrib['length'], "4")
        self.assertEqual(self.test.attrib['dataType'], "xsd:str")

    def testFloatList(self):
        self.test = Array(self.floatlist, self.attrib)
        self.xml = ET.fromstring(self.stringinfloat)
        self.assertEqual(ET.tostring(self.test), ET.tostring(self.xml))
        self.assertEqual(self.test.attrib['length'], "5")
        self.assertEqual(self.test.attrib['dataType'], "xsd:double")

    def testMixedList(self):
        self.assertRaises(NotImplementedError, Array, self.mixedlist, self.attrib)

class TestArrayUnitsReq(BaseArrayTest):

    def testDataTypeReq(self):
        self.attrib.pop('units')
        self.assertRaises(CMLError, Array, self.intlist, self.attrib)

class TestCMLElement(TestElement):

    def testGenerateCMLElement(self):
        self.test = CMLElement(self.tag, self.attrib)
        self.assertIsInstance(self.test, CMLElement)
        self.assertEqual(self.test.tag, self.tag)

    def testDictRefReq(self):
        self.attrib.pop('dictRef')
        self.assertRaises(CMLError, CMLElement, self.tag, self.attrib)

class TestPropParam(BaseArrayTest):

    def setUp(self):
        BaseArrayTest.setUp(self)
        self.stringinfloat = """<testingtag dictRef="test:dictRef"><scalar
        dataType="xsd:double" units="test:units">6.321</scalar></testingtag>"""
        self.stringinstr = """<testingtag dictRef="test:dictRef"><scalar
        dataType="xsd:str" units="test:units">test text</scalar></testingtag>"""
        self.stringinint = """<testingtag dictRef="test:dictRef"><scalar
        dataType="xsd:int" units="test:units">5</scalar></testingtag>"""


    def testGeneratePropParamString(self):
        self.test = PropParam(self.tag, self.text, self.attrib)
        self.assertIsInstance(self.test, PropParam)
        self.assertEqual(self.test.tag, self.tag)
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                        (self.stringinstr)))
        self.assertIsInstance(self.test.find('scalar'), Scalar)
        self.assertIsInstance(self.test.find('scalar'), Scalar)

    def testGeneratePropParamInt(self):
        self.test = PropParam(self.tag, self.int, self.attrib)
        self.assertIsInstance(self.test, PropParam)
        self.assertEqual(self.test.tag, self.tag)
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                        (self.stringinint)))
        self.assertIsInstance(self.test.find('scalar'), Scalar)

    def testGeneratePropParamFloat(self):
        self.test = PropParam(self.tag, self.float, self.attrib)
        self.assertIsInstance(self.test, PropParam)
        self.assertEqual(self.test.tag, self.tag)
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                        (self.stringinfloat)))
        self.assertIsInstance(self.test.find('scalar'), Scalar)


class TestPropParamList(BaseArrayTest):

    def setUp(self):
        BaseArrayTest.setUp(self)
        self.testppstrlist = """<testingtag dictRef="test:dictRef"><array
        dataType="xsd:str" delimiter=" " length="4" units="test:units"
        >a bb CCC dddd</array></testingtag>"""
        self.testppintlist = """<testingtag dictRef="test:dictRef"><array
        dataType="xsd:int" delimiter=" " length="33" units="test:units">1 4 7 10 13 16 19 22 25 28 31 34 37 40 43 46 49 52 55 58 61 64 67 70 73 76 79 82 85 88 91 94 97</array></testingtag>"""
        self.testppfloatlist = """<testingtag dictRef="test:dictRef"><array
        dataType="xsd:double" delimiter=" " length="5" units="test:units"
        >1.3 5.6 7.3 1500000.0 26782.0</array></testingtag>"""
        

    def testGeneratePropParamArrayStr(self):
        self.testppstrlist = """<testingtag dictRef="test:dictRef"><array
        dataType="xsd:str" delimiter=" " length="4" units="test:units"
        >a bb CCC dddd</array></testingtag>"""
        self.test = PropParam(self.tag, self.strlist, self.attrib)
        self.assertIsInstance(self.test, PropParam)
        self.assertEqual(self.test.tag, self.tag)
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                (self.testppstrlist)))
        self.assertIsInstance(self.test.find('array'), Array)
        
    def testGeneratePropParamArrayInt(self):
        self.test = PropParam(self.tag, self.intlist, self.attrib)
        self.assertIsInstance(self.test, PropParam)
        self.assertEqual(self.test.tag, self.tag)
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                (self.testppintlist)))
        self.assertIsInstance(self.test.find('array'), Array)
        
    def testGeneratePropParamArrayFloat(self):
        self.testppfloatlist = """<testingtag dictRef="test:dictRef"><array
        dataType="xsd:double" delimiter=" " length="5" units="test:units"
        >1.3 5.6 7.3 1500000.0 26782.0</array></testingtag>"""

        self.test = PropParam(self.tag, self.floatlist, self.attrib)
        self.assertIsInstance(self.test, PropParam)
        self.assertEqual(self.test.tag, self.tag)
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                (self.testppfloatlist)))
        self.assertIsInstance(self.test.find('array'), Array)

class TestParameter(TestPropParamList):

    def setUp(self):
        TestPropParamList.setUp(self)
        self.testppfloatlist = """<parameter dictRef="test:dictRef"><array
        dataType="xsd:double" delimiter=" " length="5" units="test:units"
        >1.3 5.6 7.3 1500000.0 26782.0</array></parameter>"""

    def tearDown(self):
        TestPropParamList.tearDown(self)
        self.testppfloatlist = None

    def testGenerateParameter(self):
        self.test = Parameter(self.floatlist, self.attrib)
        self.assertIsInstance(self.test, Parameter)
        self.assertEqual(self.test.tag, 'parameter')
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                (self.testppfloatlist)))
        self.assertIsInstance(self.test.find('array'), Array)

    def testParameterRequirements(self):
        for key in ['dictRef', 'units']:
            for value in [self.int, self.text, self.float, self.intlist, self.floatlist, self.strlist]:
                self.attrib.pop(key)
                self.assertRaises(CMLError, Parameter, value, self.attrib)
                self.tearDown()
                self.setUp()

class TestProperty(TestPropParamList):

    def setUp(self):
        TestPropParamList.setUp(self)
        self.testppstrlist = """<property dictRef="test:dictRef"><array
        dataType="xsd:str" delimiter=" " length="4" units="test:units"
        >a bb CCC dddd</array></property>"""

    def tearDown(self):
        TestPropParamList.tearDown(self)
        self.testppstrlist = None


    def testGenerateProperty(self):
        self.test = Property(self.strlist, self.attrib)
        self.assertIsInstance(self.test, Property)
        self.assertEqual(self.test.tag, 'property')
        self.assertEqual(ET.tostring(self.test), ET.tostring(ET.fromstring
                                                (self.testppstrlist)))
        self.assertIsInstance(self.test.find('array'), Array)

    def testPropertyRequirements(self):
        for key in ['dictRef', 'units']:
            for value in [self.int, self.text, self.float, self.intlist, self.floatlist, self.strlist]:
                self.attrib.pop(key)
                self.assertRaises(CMLError, Property, value, self.attrib)
                self.tearDown()
                self.setUp()

class TestAbstractList(TestPropParamList):

    def testGenerateAbstractListSingleItem(self):
        for value in [self.int, self.text, self.float]: 
            list = [{'value': value, 'attrib':self.attrib}]
            self.test = AbstractList('propertyList', list)
            self.assertIsInstance(self.test, AbstractList)
            self.assertEqual(self.test.tag, 'propertyList')
            self.assertIsInstance(self.test.find('property'), Property)
            self.assertIsNotNone(self.test.find('property').find('scalar'))

        for value in [self.intlist, self.floatlist, self.strlist]:
            list = [{'value': value, 'attrib':self.attrib}]
            self.test = AbstractList('propertyList', list)
            self.assertIsInstance(self.test, AbstractList)
            self.assertEqual(self.test.tag, 'propertyList')
            self.assertIsInstance(self.test.find('property'), Property)
            self.assertIsNotNone(self.test.find('property').find('array')) 
        
        for value in [self.int, self.text, self.float]:
            list = [{'value': value, 'attrib':self.attrib}]
            self.test = AbstractList('parameterList', list)
            self.assertIsInstance(self.test, AbstractList)
            self.assertEqual(self.test.tag, 'parameterList')
            self.assertIsInstance(self.test.find('parameter'), Parameter)
            self.assertIsNotNone(self.test.find('parameter').find('scalar'))

        for value in [self.intlist, self.floatlist, self.strlist]:
            list = [{'value': value, 'attrib':self.attrib}]
            self.test = AbstractList('parameterList', list)
            self.assertIsInstance(self.test, AbstractList)
            self.assertEqual(self.test.tag, 'parameterList')
            self.assertIsInstance(self.test.find('parameter'), Parameter)
            self.assertIsNotNone(self.test.find('parameter').find('array'))
        
    def generateAbstractListMultipleItems(self):
        list= []
        for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]: 
            list.append({'value': value, 'attrib':self.attrib})
        self.test = AbstractList('propertyList', list)
        self.assertIsInstance(self.test, AbstractList)
        self.assertEqual(self.test.tag, 'propertyList')
        self.assertIsInstance(self.test.find('property'), Property)
        self.assertIsNotNone(self.test.find('property').find('scalar'))
        self.assertIsNotNone(self.test.find('property').find('array')) 
        
        list=[]
        for value in [self.int, self.text, self.float]:
            list.append({'value': value, 'attrib':self.attrib})
        self.test = AbstractList('parameterList', list)
        self.assertIsInstance(self.test, AbstractList)
        self.assertEqual(self.test.tag, 'parameterList')
        self.assertIsInstance(self.test.find('parameter'), Parameter)
        self.assertIsNotNone(self.test.find('property').find('scalar'))
        self.assertIsNotNone(self.test.find('parameter').find('array'))

    def testAbstractListRequirements(self):
        for key in ['dictRef', 'units']:
            for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]:
                self.attrib.pop(key)
                list = [{'value':value, 'attrib': self.attrib}]
                self.assertRaises(CMLError, AbstractList, 'propertyList', list)
                self.tearDown()
                self.setUp()

        self.assertRaises(CMLError, AbstractList, 'propertyList', 'test')
        # Shouldn't fail as can now create blank nodes
        #self.assertRaises(CMLError, AbstractList, 'propertyList', [])

        for key in ['dictRef', 'units']:
            for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]:
                self.attrib.pop(key)
                list = [{'value':value, 'attrib': self.attrib}]
                self.assertRaises(CMLError, AbstractList, 'parameterList', list)
                self.tearDown()
                self.setUp()

        self.assertRaises(CMLError, AbstractList, 'parameterList', 'test')
        # Shouldn't fail as can now create blank nodes
        # self.assertRaises(CMLError, AbstractList, 'parameterList', [])

        self.assertRaises(CMLError, AbstractList, 'test',
                            [{'value':self.int, 'attrib': self.attrib}])


class TestPropertyList(TestPropParamList):

    def testGeneratePropertyListSingleItem(self):
        for value in [self.int, self.text, self.float]: 
            list = [{'value': value, 'attrib':self.attrib}]
            self.test = PropertyList(list)
            self.assertIsInstance(self.test, PropertyList)
            self.assertEqual(self.test.tag, 'propertyList')
            self.assertIsInstance(self.test.find('property'), Property)

    def generatePropertyListMultipleItems(self):
        list= []
        for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]: 
            list.append({'value': value, 'attrib':self.attrib})
        self.test = PropertyList(list)
        self.assertIsInstance(self.test, PropertyList)
        self.assertEqual(self.test.tag, 'propertyList')
        self.assertIsInstance(self.test.find('property'), Property)
        self.assertIsNotNone(self.test.find('property').find('scalar'))
        self.assertIsNotNone(self.test.find('property').find('array')) 

    def testPropertyListRequirements(self):
        for key in ['dictRef', 'units']:
            for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]:
                self.attrib.pop(key)
                list = [{'value':value, 'attrib': self.attrib}]
                self.assertRaises(CMLError, PropertyList, list)
                self.tearDown()
                self.setUp()

        self.assertRaises(CMLError, PropertyList, 'test')
        # Shouldn't fail as can now create blank nodes
        #self.assertRaises(CMLError, PropertyList, 'propertyList', [])

class TestParameterList(TestPropParamList):

    def testGenerateParameterListSingleItem(self):
        for value in [self.int, self.text, self.float]: 
            list = [{'value': value, 'attrib':self.attrib}]
            self.test = ParameterList(list)
            self.assertIsInstance(self.test, ParameterList)
            self.assertEqual(self.test.tag, 'parameterList')
            self.assertIsInstance(self.test.find('parameter'), Parameter)

    def generateParameterListMultipleItems(self):
        list= []
        for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]: 
            list.append({'value': value, 'attrib':self.attrib})
        self.test = ParameterList(list)
        self.assertIsInstance(self.test, ParameterList)
        self.assertEqual(self.test.tag, 'parameterList')
        self.assertIsInstance(self.test.find('parameter'), Parameter)
        self.assertIsNotNone(self.test.find('parameter').find('scalar'))
        self.assertIsNotNone(self.test.find('parameter').find('array')) 

    def testParameterListRequirements(self):
        for key in ['dictRef', 'units']:
            for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]:
                self.attrib.pop(key)
                list = [{'value':value, 'attrib': self.attrib}]
                self.assertRaises(CMLError, ParameterList, list)
                self.tearDown()
                self.setUp()

        self.assertRaises(CMLError, ParameterList, 'test')
        # Shouldn't fail as can now create blank nodes
        # self.assertRaises(CMLError, ParameterList, [])

class TestModule(TestElement):

    def testModuleGeneration(self):
        self.test = CMLModule(self.attrib)
        self.assertIsInstance(self.test, CMLModule)
        self.assertEqual(self.test.tag, 'module')

class TestEnforcedModule(CMLModule):
    def __init__(self, attrib, requirements):
        enforce(attrib, requirements)
        CMLModule.__init__(self, attrib)


class TestEnforcementMixin(TestPropParam):

    def testChecking(self):
        for attribute in ['dataType', 'units', 'title', 'dictRef']:
            for status in ['recommended', 'required']:
                requirements = { attribute : { 'status' : status,
                                           'message': 'The test message'}}

                self.test = TestEnforcedModule(self.attrib, requirements)
                self.assertIsInstance(self.test, TestEnforcedModule)
                self.assertEqual(self.test.tag, 'module')


                list= []
                for value in [self.int, self.text, self.float, self.intlist,
                          self.floatlist, self.strlist]: 
                    list.append({'value': value, 'attrib':self.attrib})
                testelement = ParameterList(list)
                self.test.append(testelement)
                self.tearDown()
                self.setUp()

    def testFailure(self):
        requirements = {'randomteststring' : {'status' : 'required',
                                               'message': 'The test message'}}
        self.assertRaises(CMLError, TestEnforcedModule,
                               self.attrib, requirements)

        warnings.simplefilter('error')
        requirements = {'randomteststring' : {'status' : 'recommended',
                                               'message': 'The test message'}}
        self.assertRaises(UserWarning, TestEnforcedModule,
                               self.attrib, requirements)


class TestPy2xsd(TestElement):

    def testpy2xsd(self):
        self.assertEqual(py2xsdtype(self.int), 'xsd:int')
        self.assertEqual(py2xsdtype(self.text), 'xsd:str')
        self.assertEqual(py2xsdtype(self.float), 'xsd:double')

        self.assertRaises(CMLError, py2xsdtype, [])
        self.assertRaises(CMLError, py2xsdtype, {})
        self.assertRaises(CMLError, py2xsdtype, None)

###
#Testing of CML Document object
####

class CMLDocTestBaseClass(TestParameterList):

    def setUp(self):
        self.test = CMLDoc()
        TestParameterList.setUp(self)
        self.values =  [self.int, self.text, self.float]
        self.list = [{'value': value, 'attrib':self.attrib} for value in self.values]
        self.test.cmlelements.append(ParameterList(self.list))
        self.test.cmlelements.append(CMLModule({'title':'test-title',
                                          'dictRef' : 'test-dictRef'}))
        self.test.cmlelements.append(PropertyList(self.list))

    def tearDown(self):
        self.test = None

    def testCMLDocGeneration(self):
        self.assertIsInstance(self.test._root, ET.Element)
        self.assertEqual(len(self.test.cmlelements), 3)
        self.assertIsNone(self.test.convention)

    def testAddElementToCMLDoc(self):
        self.assertIsInstance(self.test.cmlelements[0], ParameterList)
        self.assertIsInstance(self.test.cmlelements[1], CMLModule)
        self.assertIsInstance(self.test.cmlelements[2], PropertyList)

    def testRegisterNamespace(self):
        self.test.registerNamespace('foo', 'http://bar.com/')
        # Todo Figure out how to test namespace is correctly registered

    def testSerialise(self):      
        f = open('test.xml', 'w')
        self.test.serialise(f).close()
        
                                  
        
        
        

if __name__ == '__main__':
    unittest.main()
    


        
        
