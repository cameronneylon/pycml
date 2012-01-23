# pyCML.simple_comp_chem: A simple version of the compchem CML convention
#
# Public Domain Waiver:
# To the extent possible under law, Cameron Neylon has waived all 
# copyright and related or neighboring rights to lablogpost.py
# This work is published from United Kingdom.
#
# See http://creativecommons.org/publicdomain/zero/1.0/
#
# Dependencies: This library requires pycml along with all of its dependencies.
#
#################################

from pycml.pycml import *

class SimpleCompChem(CMLDoc):
    """A class representing a simple compchem CMLDocs.

    This class is currently limited to handling compchem compliant CMLDocs
    with only one job and the set of available modules limited to
    initialisation and finalisation with the optional module environment."""

    def __init__(self, env=None):
        CMLDoc.__init__(self)

        self._jobslist = JobsList()
        self._job = Job()
        self._initialisation = Initialisation()
        self._finalisation = Finalisation()
        if env:
            self._environment = Environment()
        else: self._environment = None

        self.registerNamespace('compchem',
             'http://xml-cml.org/convention/compchem')

    def write(self, fp):
        """Serialise the full tree and write out to a file.

        This function finalises the tree and writes it out to a file like
        object. The file is provided as a parameter for those who might wish
        to write to a temp file or a stream rather than an actual file. The
        file object is returned by the function so in common use the following
        pattern can be observed.

        >> f = open('filename.xml', 'w')
        >> SimpleCompChemDoc.write(f).close()
        
        :param :fp A file-like object that CML document will be serialised to
        :type :fp file
        :rtype: File-like object to which the tree has been written
        """

        if self._environment:
            self._job.append(self._environment)
        self._job.append(self._initialisation)
        self._job.append(self._finalisation)
        self._jobslist.append(self._job)
        self.cmlelements.append(self._jobslist)
        self.serialise(fp)
        return fp

    ######################################################################
    # Getters to encourage users not to interact with the internal variables
    # of the document but with the underlying elements with their exposed
    # methods.
    ######################################################################

    def jobslist(self):
        return self._jobslist

    def job(self):
        return self._job

    def initialisation(self):
        return self._initialisation

    def finalisation(self):
        return self._finalisation

    def environment(self):
        return self._environment
    

######################################################################
#
# Modules classes to represent the main elements of the SCC document
#
######################################################################

class CompChemModule(CMLModule):
    """Abstract module class for subclassing to compchem modules."""

    def __init__(self, dictref, title=None):
        """Initialisation method for jobslist module.

        The compchem convention recommends that a jobslist module have a human
        readable title. The dictRef="compchem:jobsList" attribute is required.
        The compchem convention recommends that a job module have a human
        readable title. The dictRef="compchem:job" attribute is required.
        """

        message = "A %s module must be defined by a compchem:%s attribute" \
                                   %(dictref, dictref)
        self.requirements = {'dictRef' : { 'status' : 'required',
                                           'message':  message,
                                           'value'  : ('compchem:'+dictref)},
                               'title' : { 'status' : 'recommended',
                                           'message':
                       """A human readable title is recommended for compchem modules"""}}

        self.attrib = {'dictRef' : dictref}
        if title:
            self.attrib['title'] = title
        enforce(self.attrib, self.requirements)

        CMLModule.__init__(self, self.attrib)


class JobsList(CompChemModule):
    """A CML Element Representing the JobsList module of a compchem CML doc"""

    def __init__(self, title=None):
        CompChemModule.__init__(self, 'jobsList', title)

class Job(CompChemModule):
    """A CML Element representing the Job module of a compchem CML doc"""

    def __init__(self, title=None):
        CompChemModule.__init__(self, 'job', title)

class CoreSimpleCCModule(CompChemModule):
    """An abstract class for compchem Initialisation and Finalisation Modules""" 

    def __init__(self, dictref, parameters=None, title=None):
        CompChemModule.__init__(self, dictref, title)
        self.dictref = dictref
        if parameters:
            self.populate(parameters)

    def populate(self, parameters):
        """Populate the initialisation module with a parameter list and parameters.

        In the simple compchem convention intialisation consists only of a set of
        parameters, wrapped in a parameterList. For this we can simply use the
        pycml class parameterList and pass the parameters in the form specified
        for that class.
        """

        ListClass = { 'initialisation' : ParameterList,
                      'finalisation'   : PropertyList,
                      'environment'    : PropertyList}[self.dictref]

        plist = ListClass(parameters)
        self.append(plist)
        return self


class Initialisation(CoreSimpleCCModule):

    def __init__(self, parameters=None, title=None):
        CoreSimpleCCModule.__init__(self, 'initialisation', parameters, title)

class Finalisation(CoreSimpleCCModule):

    def __init__(self, parameters=None, title=None):
        CoreSimpleCCModule.__init__(self, 'finalisation', parameters, title)

class Environment(CoreSimpleCCModule):

    def __init__(self, parameters=None, title=None):
        CoresSimpleCCModule.__init__(self, 'environment', parameters, title)










