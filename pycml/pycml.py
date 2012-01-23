# pyCML: A library for writing Chemical Markup Language XML from Python
#
# Public Domain Waiver:
# To the extent possible under law, Cameron Neylon has waived all 
# copyright and related or neighboring rights to lablogpost.py
# This work is published from United Kingdom.
#
# See http://creativecommons.org/publicdomain/zero/1.0/
#
# Dependencies: The application requires a range of modules from the
# Python 2.7 standard library including ElementTree, warning,
#
#################################

import xml.etree.ElementTree as ET
import warnings
import numpy


class CMLDoc:
    """Class for the CML tree and document

    This is an abstract object representing the CML document. For implementation
    reasons it does not inherit from ElementTree but contains a reference to an
    ElementTree instance which is the XML object for the CML document. This abstract
    document object is intended to be subclassed to represent specific CML
    conventions.
    """

    def __init__(self):
        """Set up the XML tree and register generic name spaces."""
        self._root = self._initRootElement()
        self.convention = None
        self.cmlelements = []

    ########################################################
    #
    # Initialisation methods for the document object
    #
    ########################################################

    def _initRootElement(self):
        """Set up cml root and register common namespaces."""

        self.registerNamespace('cml', 'http://www.xml-cml.org/schema')
        self.registerNamespace('convention',
                                 'http://www.xml-cml.org/convention/')
        self.registerNamespace('xsd',
                                 'http://www.w3.org/2001/XMLSchema')

        root = ET.Element('{http://www.xml-cml.org/schema}cml')

        return root

    ########################################################
    #
    # Public methods on the overall document object
    #
    ########################################################

    def registerNamespace(self, prefix, uri):
        """Convenience method for registering relevant namespaces."""

        ET.register_namespace(prefix, uri)    

    def getElements(self):
        return self.elements

    def appendElement(self, element):
        try:
            assert(issubclass(type(element), ET.Element))
        except AssertionError:
            raise CMLError

        self.elements.append(element)
        return self.elements

    def serialise(self, fp):
        """Serialise full tree to a file-like object.

        :param :fp A file like object to serialise the full tree to
        :type :fp file object
        :return: Returns the file object for immediate closure or manipulation
        :rtype: file like object
        """

        self._root.extend(self.cmlelements)
        tree = ET.ElementTree(self._root)
        tree.write(fp, encoding='UTF-8', xml_declaration=True, method="xml" )
        return fp


    def getConvention(self):
        """Return the current convention as a list of Python dictionaries.

        A convention defines a set of name spaces and the organisation of a CML
        document. Conventions are represented in a limited way in pycml via a
        list of dictionaries. The list represents the logical ordering of the
        file and are used to retain a sensible ordering and human readability.
        The intention is that by iterating over the list and dictionary keys
        it is possible to programmatically identify all required elements to
        adhere to the convention.

        Nodes are represented as dictionaries as follows:

        {'required' : True/False,
         'arg'      : True,        # Indicator of instantiation arguments
                                   # required for this class eg 'list' for
                                   # parameterList. 
          'attrib'   : {dict}      # Several element types have required
                                   # attributes such as a specified
                                   # dictRef. This is set as eg.
                                   # 'dictRef': 'jobsList'
                                   # Elements that have a required
                                   # attribute but not a set value
                                   # eg a title element are shown as
                                   # 'title' : True
                                   # Other attributes that are recommended are
                                   # shown as 'attribute' : False
           'class'  : classname    # The class to be used to instantiate
                                   # the relevant node.
           'children': list        # A list of child nodes represented in
        }                          # the same dictionary format.
        
        Conventions are represented as a list of such nodes at the top level
        with dictionaries nested as required for the desired heirachy as
        in this example which specifies a subset of the compchem convention:
        
[
{'root' : {'namespaces' : {'xsd' : 'http://www.w3.org/2001/XMLSchema',
                           'convention':'http://www.xml-cml.org/convention/', }
           'convention' : 'convention:compchem',
           'attrib'     : {dict of any other attributes of root}
           }
},
{'required': True,
 'attrib'  : {'dictRef: 'compchem.jobsList'
              'title' : True},
 'class'   : pycml.Module
 'children': [
              {'required' : True,
               'attrib'   : {'dictRef': 'compchem:job'
                            'title'  : True},
               'class'    : pycml.Module
               'children' : [
                             {'required' : True,
                              'attrib'   : {'dictRef':'compchem:initialization',
                                            'title'  : True}
                              'class'    : pycml.Module
                              'children' : [
                                           {'required': False,
                                            'list'    : True
                                            'class'   : pycml.ParameterList},
                                           {'required': False,
                                              'class' : pycml.Molecule}
                                            ]
                              }
                             ]
                }
               ]
 }
]
                      
        """

        return self.convention







######################################################################
#
# Classes representing CML elements
#
######################################################################

class Scalar(ET.Element):
    """A class representing scalar elements in CML.

    Scalar class requires the elements datatype and units as attributes"""

    def __init__(self, text, attrib=None):
        ET.Element.__init__(self, 'scalar')
        try:
            for attribute in ['dataType', 'units']:
                self.attrib[attribute] = attrib[attribute]
        except KeyError:
            raise CMLError

        self.text = str(text)

class Array(ET.Element):
    """Class representing CML Arrays.

    CML arrays are lists conventionally delimited by spaces. CML conventions
    suggest that an array should have dataType and units attributes and this
    is enforced here. CML REQUIRES that an array have a length attribute and
    that this be correct. The __init__ method obtains dataType directly from
    the list of values passed to the method. The length of the array is
    determined within the method. That leaves only the units as a required
    input for production of the array.

    The only list delimeter currently implemented is a space and this is hard
    coded into the content generation for the element.
    """

    def __init__(self, valuelist, attrib):
        ET.Element.__init__(self, 'array')
        assert type(valuelist) == list , \
                     "Value of an array element must be a Python list"

        try:
            for attribute in ['units']:
                self.attrib[attribute] = attrib[attribute]
        except KeyError:
            raise CMLError

        typelist = [type(value) for value in valuelist]
        # Check if all types are the same. Using approach described at:
        # http://stackoverflow.com/questions/3844801/
        # check-if-all-elements-in-a-list-are-identical
        if (typelist.count(typelist[0]) != len(valuelist)):
            raise NotImplementedError, \
                "Array elements must be of the same Python type at the moment"
            #TODO Implement some intelligent fallback mechanisms for the type
            # elements, probably int -> float -> string
        else:
            self.attrib['length'] = str(len(valuelist))
            self.attrib['dataType'] = py2xsdtype(valuelist[0])
            self.attrib['delimiter'] = " "
            arraylist = ''
            for value in valuelist:
                arraylist += str(value) + " "
            self.text = arraylist.rstrip()

class Matrix(ET.Element):
    def __init__(self):
        raise NotImplementedError

class CMLElement(ET.Element):
    """Base class representing all CML elements that require a dictRef.

    All CML elements except for a subset of core parameters (scalar, array,
    matrix, molecule[?] require a dictref. This minor subclass of ET.Element
    enforces that requirement.

    TODO: Enforce the id tag as well?
    """

    def __init__(self, tag, attrib):
        ET.Element.__init__(self, tag)
        try:
            for attribute in ['dictRef']:
                self.attrib[attribute] = attrib[attribute]
        except KeyError:
            raise CMLError

        self.attrib = attrib

class PropParam(CMLElement):
    """Base class representing CML properties and parameters.

    CML parameters and properties are required to have a dictRef and may contain
    scalar, array or matrix elements as the actual values of the parameter. The
    child element contains the data type and units. In this implementation the
    classes Parameter and Property enforce this convention. If it is desired to
    create Parameter and Property elements that do no adhere to this convention
    the user should subclass AbstractParam separately.
    """
        
    def __init__(self, tag, value, attrib):

        try:
            for attribute in ['dictRef', 'units']:
                attrib[attribute]
        except KeyError:
            raise CMLError

        CMLElement.__init__(self, tag, {'dictRef': attrib['dictRef']})

        t = type(value)
        if t == list:
            paramchild = Array(value, {'units' : attrib['units']})

        elif t == numpy.ndarray:
            paramchild = Matrix(value, {'units' : attrib['units']})

        # If the value is an unsupported type this will be caught at py2xsdtype
        else:
            paramchild = Scalar(value, {'dataType' : py2xsdtype(value),
                                        'units' : attrib['units']})

        self.append(paramchild)


class Parameter(PropParam):
    """CML Class for Parameters"""

    def __init__(self, value, attrib):
        try:
            PropParam.__init__(self, 'parameter', value, attrib)
        except AssertionError:
            raise CMLError, \
                "A CML Parameter must be instantiated with a dictRef attribute"

class Property(PropParam):
    """CML Class for Properties"""

    def __init__(self, value, attrib):
        try:
            PropParam.__init__(self, 'property', value, attrib)
        except AssertionError:
            raise CMLError, \
                "A CML Parameter must be instantiated with a dictRef attribute"

class AbstractList(ET.Element):
    """A base class representing lists of properties and parameters.

    The propertyList and parameterList elements of CML contain parameters
    and properties. This abstract constructor element will enforce at the
    point of instantiation that only objects represented as appropriate
    for building parameters or properties are included. This cant be
    complete enforced because someone can always muck around with the XML
    tree directly. Parameter lists generally do not have any attributes
    on the list element itself and this class therefore inherits from
    ET.Element.

    The elements of the AbstractList are represented as a Python list
    containing dictionaries of the form:
    {'value'  : value, # [int, str, float, list, **numpy.ndarray],
     'attrib' : attributes} # Dictionary containing the required attributes.
                            # At minimum this will be a dictRef and units 


    ** Not yet implemented
    """

    def __init__(self, tag, paramlist=None):
        ET.Element.__init__(self, tag)
        self.tag = tag
        if paramlist:
            self.populate(paramlist)

    def populate(self, paramlist):
        try:
            assert((type(paramlist) == list) and (len(paramlist) > 0))
        except AssertionError:
            raise CMLError

        elements = self.buildList(self.tag, paramlist)
        self.extend(elements)


    def buildList(self, tag, paramlist):
        if tag == 'propertyList':
            paramclass = Property
        elif tag == 'parameterList':
            paramclass = Parameter
        else:
            raise CMLError, \
"AbstractList can only be called with propertyList or parameterList tags"
        
        elements = []
        for param in paramlist:
            paramelement = paramclass(param['value'], param['attrib'])
            elements.append(paramelement)

        return elements

class PropertyList(AbstractList):
    """Class representing the CML PropertyList element.

    See AbstractList for more comprehensive doumentation.
    """

    def __init__(self, paramlist=None):
        AbstractList.__init__(self, 'propertyList', paramlist)

class ParameterList(AbstractList):
    """Class representing the CML parameterList element.

    See AbstractList for more comprehensive doumentation.
    """

    def __init__(self, paramlist=None):
        AbstractList.__init__(self, 'parameterList', paramlist)

class CMLModule(CMLElement):
    """Base class representing CML modules."""

    def __init__(self, attrib):
        CMLElement.__init__(self, 'module', attrib)

    def setTitle(self, title):
        self.attrib['title'] = title
        return self

def py2xsdtype(value):
    """Takes a python variable and returns the appropriate xsd type

    A convenience method which is intended to consolidate conversions
    between python types and xsd types for this library. There are
    some issues in representing python types, particularly exponential
    representations of floats in XML but for the moment I am ignoring
    that issue in this implementation.
    """

    t = type(value)
    conversiondict = { int   : 'xsd:int',
                       float : 'xsd:double',
                       numpy.float64 : 'xsd:double',
                       str   : 'xsd:str'}

    try: 
        assert t in conversiondict
    except AssertionError:
        mesg = "Unsupported data type %s for conversion to cml." % str(t)
        raise CMLDataTypeError, mesg

    return conversiondict[t]

def enforce(attrib, requirements):
    """Convenience method for checking requirements on element intantiation.

    The function is intended to be used in conventions that add additional
    classes to enforce the specified requirements when the element is
    instantiated. To make use of this create the desired subclass eg.

    class ModuleEnforcedTitle(CMLElement):
        def __init__(self, attrib):
            self.requirements = {dictionary describing requirements, see below}
            CMLElement.__init__(self, 'module', attrib)

    requirements is a dictionary of form:
    {'attribute'  : {'status'  : recommended or required
                     'message' : string error/warning message
                     'value'   : value if is fixed, otherwise None}}
    """
    
    for key in requirements.iterkeys():
        if key not in attrib:
            if requirements[key]['status'] == 'required':
                raise CMLError, requirements[key]['message']
            else:
                warnings.warn(requirements[key]['message'])

class CMLError(Exception):
    pass

class CMLDataTypeError(CMLError):
    pass


