# PyCML - A Python Library for writing CML compliant data files

CML is an XML schema which defines certain tags useful in chemistry and more widely in the biological sciences. CML is used within the context of conventions that define more closely the format and structure of CML documents. The PyCML library is intended to support developers in writing out CML which is compliant with specific CML conventions.

## Design and architecture

### CML Element Classes

The PyCML library contains a set of classes that define specific CML types including scalar, array, module, parameter, property, parameterList, propertyList. A number of abstract classes are also included. These classes are subtyped from the ElementTree.Element class. 

In most cases the __init__ method is overwritten to create specific tags and enforce requirements defined by CML. In some cases the classes are built to construct hierarchies. Thus the Parameter class takes a specified parameter and required metadata and generates a structure of the form:

<parameter dictRef="dictref">
	<scalar dataType="xsd:datatype" units="units">
		value
	</scalar>
<parameter>

Where "dictRef" and "units" are references to dictionaries with a registered namespace, "xsd:datatype" is a reference to one of "xsd:double", xsd:string, or xsd:int, and value is the value the parameter has. The Parameter __init__ method will determine whether the parameter is a scalar or an array (matrices are not currently supported).

The developer may wish to create new classes relevant to their specific type. In this case they may wish to enforce requirements for attributes on those classes. The EnforcementMixin is provided for this use case. The general use will be to develop a new class with inheritance from both the desired base element and the EnforcementMixin. The new class will include an internal variable (self.requirements) containing the requirements description in the __init__ method for the new class prior to calling EnforcementMixin.__init__(self, requirements). However classes may also be created dynamically by passing the requirements to the newly created class at run time.

### The CML Document

The CML document class is provided as a template for the creation of convention documents. The developer has two choices in approach to creating their convention library. The recommended approach is to subclass new CML elements that define the building blocks of the document convention. These elements will be designed to expose an __init__ method and optionally a populate() method that can accept a defined data object and use it to instantiate the full CML tree for that object. Elements that are fully populated at initialisation time or act only as containers to elements that are better suited to being populated (e.g. a compchem:job vs a compchem:initialisation) should not implement a populate method. Those elements that do should test on initialisation for an optional input variable containing the required data for population and call populate if it is found.

These elements should also implement a getRequired() method which returns True for elements that are required and False for those that are available. This method can also return "recommended" if desired but there is no guarantee that this will not be parsed programmatically to True.

The intention is that these elements will be at the highest level of the XML hierachy possible. In some cases further nesting will be required (e.g. for implementation of compchem cml files with multiple compchem:job's within a compchem:jobsList) Ideally it is preferable for the full jobsList to be serialised from the initiating code programmatically and this to be referred to the API that the jobsList element exposes. If necessary it is recommended that where this is not possible that the nested elements be represented by nested CMLDocument derived objects. 

CMLDocument is then subclassed to provide an object (here referred to as 'doc' for the instantiated object) which include these core elements as internal objects. These should be listed in the desired order in the internal list variable self.elements. The function doc.appendElement(element) is provided for this purpose. The method doc.getElements() will return the core element list. 