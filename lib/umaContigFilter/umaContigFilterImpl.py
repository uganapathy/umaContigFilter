# -*- coding: utf-8 -*-
#BEGIN_HEADER
#END_HEADER


class umaContigFilter:
    '''
    Module Name:
    umaContigFilter

    Module Description:
    A KBase module: umaContigFilter
This sample module contains one small method - filter_contigs.
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/uganapathy/umaContigFilter.git"
    GIT_COMMIT_HASH = "1dbe433ebc3c516b99cbf5c8219fad635b15ac1c"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        #END_CONSTRUCTOR
        pass


    def filter_contigs(self, ctx, params):
        """
        The actual function is declared using 'funcdef' to specify the name
        and input/return arguments to the function.  For all typical KBase
        Apps that run in the Narrative, your function should have the
        'authentication required' modifier.
        :param params: instance of type "FilterContigsParams" (A 'typedef'
           can also be used to define compound or container objects, like
           lists, maps, and structures.  The standard KBase convention is to
           use structures, as shown here, to define the input and output of
           your function.  Here the input is a reference to the Assembly data
           object, a workspace to save output, and a length threshold for
           filtering. To define lists and maps, use a syntax similar to C++
           templates to indicate the type contained in the list or map.  For
           example: list <string> list_of_strings; mapping <string, int>
           map_of_ints;) -> structure: parameter "assembly_input_ref" of type
           "assembly_ref" (A 'typedef' allows you to provide a more specific
           name for a type.  Built-in primitive types include 'string',
           'int', 'float'.  Here we define a type named assembly_ref to
           indicate a string that should be set to a KBase ID reference to an
           Assembly data object.), parameter "workspace_name" of String,
           parameter "min_length" of Long
        :returns: instance of type "FilterContigsResults" (Here is the
           definition of the output of the function.  The output can be used
           by other SDK modules which call your code, or the output
           visualizations in the Narrative.  'report_name' and 'report_ref'
           are special output fields- if defined, the Narrative can
           automatically render your Report.) -> structure: parameter
           "report_name" of String, parameter "report_ref" of String,
           parameter "assembly_output" of type "assembly_ref" (A 'typedef'
           allows you to provide a more specific name for a type.  Built-in
           primitive types include 'string', 'int', 'float'.  Here we define
           a type named assembly_ref to indicate a string that should be set
           to a KBase ID reference to an Assembly data object.), parameter
           "n_initial_contigs" of Long, parameter "n_contigs_removed" of
           Long, parameter "n_contigs_remaining" of Long
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN filter_contigs

        # Print statements to stdout/stderr are captured and available as the App log
        print('Starting Filter Contigs function. Params=')
        print(params)

        # Step 1 - Parse/examine the parameters and catch any errors
        # It is important to check that parameters exist and are defined, and that nice error
        # messages are returned to users.  Parameter values go through basic validation when
        # defined in a Narrative App, but advanced users or other SDK developers can call
        # this function directly, so validation is still important.
        print('Validating parameters.')
        if 'workspace_name' not in params:
            raise ValueError('Parameter workspace_name is not set in input arguments')
        workspace_name = params['workspace_name']
        if 'assembly_input_ref' not in params:
            raise ValueError('Parameter assembly_input_ref is not set in input arguments')
        assembly_input_ref = params['assembly_input_ref']
        if 'min_length' not in params:
            raise ValueError('Parameter min_length is not set in input arguments')
        min_length_orig = params['min_length']
        min_length = None
        try:
            min_length = int(min_length_orig)
        except ValueError:
            raise ValueError('Cannot parse integer from min_length parameter (' + str(min_length_orig) + ')')
        if min_length < 0:
            raise ValueError('min_length parameter cannot be negative (' + str(min_length) + ')')


        if params['kmer_args'] is not None:
            print("NNNNNNNNNNNNNNOOOOOOOOOOOOOOOOOOO  k-mer args")
        else:
            aargs = params['kmer_args']
            print("kkkkkkkkkkkkkmer args: " + str(aargs['mink_arg']) + " " +
                                                  str(aargs['maxk_arg']) + " " +
                                                      str(aargs['step_arg']))

        # Step 2 - Download the input data as a Fasta and
        # We can use the AssemblyUtils module to download a FASTA file from our Assembly data object.
        # The return object gives us the path to the file that was created.
        print('Downloading Assembly data as a Fasta file.')
        assemblyUtil = AssemblyUtil(self.callback_url)
        fasta_file = assemblyUtil.get_assembly_as_fasta({'ref': assembly_input_ref})

        # Step 3 - Actually perform the filter operation, saving the good contigs to a new fasta file.
        # We can use BioPython to parse the Fasta file and build and save the output to a file.
        good_contigs = []
        n_total = 0
        n_remaining = 0
        for record in SeqIO.parse(fasta_file['path'], 'fasta'):
            n_total += 1
            if len(record.seq) >= min_length:
                good_contigs.append(record)
                n_remaining += 1

        print('Filtered Assembly to ' + str(n_remaining) + ' contigs out of ' + str(n_total))
        filtered_fasta_file = os.path.join(self.shared_folder, 'filtered.fasta')
        SeqIO.write(good_contigs, filtered_fasta_file, 'fasta')

        # Step 4 - Save the new Assembly back to the system
        print('Uploading filtered Assembly data.')
        new_assembly = assemblyUtil.save_assembly_from_fasta({'file': {'path': filtered_fasta_file},
                                                              'workspace_name': workspace_name,
                                                              'assembly_name': fasta_file['assembly_name']
                                                              })

        # Step 5 - Build a Report and return
        reportObj = {
            'objects_created': [{'ref': new_assembly, 'description': 'Filtered contigs'}],
            'text_message': 'Filtered Assembly to ' + str(n_remaining) + ' contigs out of ' + str(n_total)
        }
        report = KBaseReport(self.callback_url)
        report_info = report.create({'report': reportObj, 'workspace_name': params['workspace_name']})

        # STEP 6: contruct the output to send back
        output = {'report_name': report_info['name'],
                  'report_ref': report_info['ref'],
                  'assembly_output': new_assembly,
                  'n_initial_contigs': n_total,
                  'n_contigs_removed': n_total - n_remaining,
                  'n_contigs_remaining': n_remaining
                  }
        print('returning:' + pformat(output))

        #END filter_contigs

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method filter_contigs return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def myStringFunc(self, ctx, test_params):
        """
        :param test_params: instance of type "TestParams" -> structure:
           parameter "workspace_name" of String, parameter "testStr" of type
           "strType" (*  start addition  *), parameter "testInt" of Long
        :returns: instance of type "testResult" -> structure: parameter
           "result_str" of type "strType" (*  start addition  *), parameter
           "result_length" of type "intType"
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN myStringFunc

        print('Validating parameters.')
        if 'workspace_name' not in test_params:
            raise ValueError('Parameter workspace_name is not set in input arguments')
        workspace_name = test_params['workspace_name']

        if 'testStr' not in test_params:
            raise ValueError('Parameter testStr is not set in input arguments')
        testStr = test_params['testStr']

        if 'testInt' not in test_params:
            raise ValueError('Parameter testInt is not set in input arguments')
        testInt_orig = test_params['testInt']
        testInt = None
        try:
            testInt = testInt_orig
        except ValueError:
            raise ValueError('Cannot parse integer from testInt parameter (' + str(testInt_orig) + ')')
        if testInt < 0:
            raise ValueError('testInt parameter cannot be negative (' + str(testInt) + ')')

        resultStr = testStr + str(testInt) + str(testInt)

        output = {'result_str': resultStr,
                  'result_length': len(resultStr)
                 }

        #END myStringFunc

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method myStringFunc return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
