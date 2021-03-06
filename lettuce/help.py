#!/usr/bin/python
# Copyright (C) 2013 Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
#
# author: Wlodzimierz Wencel

import datetime
import os
import sys


class TestHistory ():
    def __init__(self):
        self.date = self.present_time()
        self.start_time = None
        self.stop_time = None
        self.time_elapsed = None
        self.passed = 0
        self.ran = 0
        self.failed = 0
        self.percent = 0.0
        self.tags = None
        self.path = None

        from features.init_all import SOFTWARE_UNDER_TEST
        self.software_type = str(SOFTWARE_UNDER_TEST)
        
        #TODO: implement this
        self.bind10_version = "N/A"
        self.dibbler_version = "N/A"
        self.isc_dhcp_version = "N/A"

        self.check_file()

    def present_time(self):
        return datetime.datetime.now()

    def start(self):
        self.start_time = self.present_time() 

    def information(self, passed, ran, tags, path):
        self.stop_time = self.present_time()
        self.passed = passed
        self.ran = ran
        self.failed = ran - passed
        if ran > 0:
            self.percent = (1.0 * passed/ran) * 100
        else:
            self.percent = 0
        self.tags = tags
        self.path = path
        
    def check_file(self):
        if not os.path.exists('history.html'):
            new_file = open('history.html', 'w')
            new_file.close()
    
    def build_report(self):
        scenarios = self.read_result() 
        scenarios.reverse()
        scenarios_html = '<tr><th colspan="2" align = left>TESTS:</th></tr><tr><td>NAME:</td><td>RESULT:</td></tr>'
        
        for i in range(len(scenarios)/2):
            name = str(scenarios.pop())
            result = str(scenarios.pop())
            if 'True' in result:
                result = 'FAILED'
                color = 'red'
            elif 'False':
                result = 'PASSED'
                color = 'green'
            else:
                result = 'N/A'
                color = 'black'                
            scenarios_html += '<tr><td>'+name+'</td><td bgcolor = \''+color+'\'>'+result+'</td></tr>'
            
        report = open('history.html', 'a')
        self.time_elapsed = self.stop_time - self.start_time
        report.write('<table border = \'1\' style = \"font-family: monospace; font-size:12\"><tr><td>DATE:</td><td>'
                     + str(self.date.year)+'.'+str(self.date.month)+'.'+str(self.date.day)+'; '+str(self.date.hour)+':'
                     + str(self.date.minute)+'</td></tr><tr><td> SOFTWARE TYPE: </td><td>'+self.software_type
                     + '</td></tr><tr><td> TAGS: </td><td>'+str(self.tags)+' </td></tr><tr><td> PATH: </td><td>'
                     + str(self.path)+' </td></tr><tr><td> RAN: </td><td>'+str(self.ran)
                     + ' </td></tr><tr><td> PASSED: </td><td>'+str(self.passed)+' </td></tr><tr><td> FAILED: </td><td>'
                     + str(self.failed)+' </td></tr><tr><td> PASS-RATE: </td><td>'+str('%2.3f' % self.percent)
                     + ' </td></tr><tr><td> TIME ELAPSED: </td><td>'+str(self.time_elapsed)
                     + ' </td></tr>'+scenarios_html+'</table><br/>\n')
        report.close()

    def read_result(self):
        res = []
        result = open('result', 'r')
        for line in result:
            res.append(line)
        result.close()
        
        os.remove('result')
        return res


class UserHelp ():
    def __init__(self):
        self.tags = ''
        self.all_tags = ''

    def check_tags(self, line):
        """
        Add only unique tags to list
        """
        tag_list = line.split('@')
        tag_list = [x.strip() for x in tag_list]
        for tag in tag_list:
            if tag is not None:
                if tag in self.tags or tag == 'v4' or tag == 'v6':
                    pass
                else:
                    self.tags += tag + ', '
        
    def test(self, ip_version, more):
        """
        Generate list of test sets, features, test names and all available tags
        """
        #  make for each in number because it starts in two points: in forge.py by using -l option,
        #  then it create list only for one IP version,
        #  and in help.py generating whole test list.

        print "Test tree schema:\nroot directory\n\ttest set (available by option -s in forge.py)\n\t\ttest feature"
        if more:
            print "\t\t\ttest name (available by option -n in forge.py)"
        for each_number in ip_version: 
            self.tags = ''
            sets_number = 0
            features_number = 0
            tests_number = 0
            outline_tests_number = 0
            outline_generate_test = 0
            outline_tag = False
            freespace = "  "
            #  this code is ugly hack! make it much better
            print "\nIPv" + each_number + " Tests:"
            print "features/dhcpv" + each_number + "/"
            for path, dirs, files in os.walk("features/dhcpv" + each_number + "/"):
                if len(path[16:]) > 1 and len(path[16:]) < 10:
                    print freespace + path[16:]
                if len(path[23:]) > 1:
                    print freespace*2 + path[23:]
                    sets_number += 1 
                for each_file in files:
                    print freespace*3, each_file[:-8], '\n', freespace*4, 'Test Names:'
                    features_number += 1
                    names = open(path + '/' + each_file, 'r')
                    for line in names:
                        line = line.strip()
                        if len(line) > 0:
                            if line[0] == '@':
                                self.check_tags(line)
                            elif "Scenario" in line:
                                if "Outline" in line:
                                    outline_tag = True
                                    outline_tests_number += 1
                                    if more:
                                        print freespace*6 + line[18:]
                                else:
                                    outline_tag = False
                                    tests_number += 1
                                    if more:
                                        print freespace*6 + line[10:]
                            elif "|" in line and outline_tag:
                                outline_generate_test += 1
                            else:
                                pass

                    names.close()
            print "Totally: \n\t", outline_generate_test + tests_number - outline_tests_number, "tests. ",\
                tests_number, "simple tests and", outline_tests_number, "multi-tests. Grouped in", features_number,\
                "features, and in", sets_number, "sets.\n\nTest tags you can use: \n", self.tags[:-2], "\n"

            if not more:
                print 'For more information, use help.py to generate UserHelp document.\n'

    def steps(self):
        """
        Generate list of available steps in tests.
        """
        files = ['srv_control', 'srv_msg']  # if you add file that help will be generated, add also description below.
        message = ['All steps available in preparing DHCP server configuration:',
                   'All steps available in building tests procedure:']
        
        for file_name, text in zip(files, message):
            steps = open('features/' + file_name + '.py', 'r')
            print '\n', text,
            for line in steps:
                line = line.strip()
                if len(line) > 0:
                    if line[0] == '#' and len(line) > 1:
                        if line[1] == '#':
                            print '\n\t', line[2:]
                    elif line[0] == '@':
                        print "\t\t    ", line[7:-2]
            steps.close()
        print "\nFor definitions of (\d+) (\w+) (\S+) check Python " \
              "regular expressions at http://docs.python.org/2/library/re.html"


def find_scenario(name, IPversion):
    from features.init_all import SOFTWARE_UNDER_TEST
    testType = ""
    for each in SOFTWARE_UNDER_TEST:
        if "client" in each:
            testType = "client"
        elif "server" in each:
            testType = "server"

    scenario = 0
    for path, dirs, files in os.walk("features/dhcpv" + IPversion + "/" + testType + "/"):
        for each_file in files:
            file_name = open(path + '/' + each_file, 'r')
            for each_line in file_name:
                if 'Scenario' in each_line:
                    scenario += 1
                    tmp_line = each_line.strip()
                    if name == tmp_line[10:]:
                        file_name.close()
                        return path + '/' + each_file, str(scenario)
            else:
                scenario = 0
                file_name.close()
    return None, 0


def find_scenario_in_path(name, path):
    from features.init_all import SOFTWARE_UNDER_TEST
    for each_software_name in SOFTWARE_UNDER_TEST:
        if "server" in each_software_name:
            testType = "server"
        elif "client" in each_software_name:
            testType = "client"

    scenario = 0
    for path, dirs, files in os.walk(path):
        for each_file in files:
            file_name = open(path + '/' + each_file, 'r')
            for each_line in file_name:
                if 'Scenario' in each_line:
                    scenario += 1
                    tmp_line = each_line.strip()
                    if name == tmp_line[10:]:
                        file_name.close()
                        return path + '/' + each_file, str(scenario)
            else:
                scenario = 0
                file_name.close()
    return None, 0
    
if __name__ == '__main__':
    #orginal_stdout = sys.stdout
    help_file = file('UserHelp.txt', 'w')
    sys.stdout = help_file
    generate_help = UserHelp()
    print """
    This is User Help to Forge project. If you looking for installation guide,
    plz read documentation or visit Forge project web site.
    
    First part of help is guide how to use existing test and test steps.
    
    How to run specific tests:
        - all tests for IPv6
            forge.py -6
        - all tests from specific set e.g. relay_agent (one test set is a whole directory e.g. test_v6/address_validation):
            forge.py -6 -s relay_agent
        - all tests from specific set with specific tag:
            forge.py -6 -s relay_agent -t basic
        - you can also use only tags:
            forge.py -6 -t basic
        - or multiple tags (then you start tests with both of tags):
            forge.py -6 -t basic, relay
        - you can start test with specific name, only one name at the time:
            forge.py -6 -n v6.basic.message.unicast.solicit
    
    Lettuce verbosity (-v option):
        1 - dots for each feature
        2 - scenario names
        3 - full feature print, but colorless
        4 - full feature print, but colorful, DEFAULT level

    
    Below there is automatically generated list of all tests. If you design new keeping the build procedure, 
    just start help.py again and you will see updated list (build procedure is described at the end of that document).
    
    AVAILABLE TESTS:  
    """
    generate_help.test(["4", "6"], 1)
    help_file.flush()
    print """Tests are simple Scenarios, multi-test are Scenarios Outline.

    AVAILABLE STEPS:"""
    generate_help.steps()
    help_file.flush()
    print """
    Step "Run configuration command: (.+)" is unique, it's for Kea servers only. All test with that step will
    automatically fail when variable SOFTWARE_UNDER_TEST in init_all.py will be different then: kea, kea4 or kea6.
    This step is designed to put one line commands to configuration file (e.g. config set Dhcp6/renew-timer 999)
    but it can be used to more complicated things if you put command in right order.
    Be aware of fact that command passed to config file it's all after "Run configuration command:"
    to the end of the line!
    
    HOW TO DESIGN NEW SETPS?
    
    All the informations automatically generated and included in this file are result of parsing two files:
        srv_msg.py
        srv_control.py 
        in directory isc-forge/lettuce/features/
    As you can see there are test steps marked with '@step' and steps family marked with '##'
    (don't remove #, it's need to be double).

    When designing new step please put them in correct family.
    
    Test example:
    
feature name >>                Feature: Standard DHCPv6 address validation
feature description >>         This feature is for checking respond on messages send on UNICAST address. Solicit, Confirm, Rebind, Info-Request should be discarded. Request should be answered with Reply message containing option StatusCode with code 5. 
        
tags >>                             @basic @v6 @unicast  
test name (simple scenario)>>       Scenario: v6.basic.message.unicast.solicit
    
configure server >>                 Test Setup:
                                    Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
                                    Server is started.
    
Test steps >>                       Test Procedure:
           >>                       Client requests option 7.
           >>                       Client chooses UNICAST address.
           >>                       Client sends SOLICIT message.
                    
                                    Pass Criteria:
send/receive msg >>                 Server MUST NOT respond with ADVERTISE message.
                                
                                    Test Procedure:
                                    Client requests option 7.
                                    Client sends SOLICIT message.
                                
                                    Pass Criteria:
                                    Server MUST respond with ADVERTISE message.
    
Information about references >>     References: RFC3315 section 15

That was example of a simple test scenario, there is another type of tests: Scenario Outline

tags >>                                    @v6 @solicit_invalid @invalid_option @outline
test name (multi scenario)>>                    Scenario Outline: v6.solicit.invalid.options.outline
     
configure server >>                             Test Setup:
                                                Server is configured with 3000::/64 subnet with 3000::1-3000::ff pool.
                                                Server is started.

Test steps >>                                   Test Procedure:
                   >>                           Client requests option 7.
<opt_name> will be replaced by text in example>>Client does include <opt_name>.
Test steps >>                                   Client sends SOLICIT message.

                                                Pass Criteria:
send/receive msg >>                             Server MUST NOT respond with ADVERTISE message.
    
                                                Test Procedure:
                                                Client requests option 7.
                                                Client sends SOLICIT message.

                                                Pass Criteria:
                                                Server MUST respond with ADVERTISE message.
    
                                                References: RFC3315 section 15.2, 17.2.1

list of test cases >>                           Examples:
field name >>                                   | opt_name       |
test case, every line after 'opt_name'          | relay-msg      |
will create separate scenario.                  | preference     |
                                                | server-unicast |
                                                | status-code    |
                                                | interface-id   |
                                                | reconfigure    |

    More info about Scenario Outlines: http://pythonhosted.org/lettuce/intro/wtf.html#outlined
    Unfortunately Lettuce is little messy with Scenario Outline. Scenario Outline is not Scenario so parts like @after.each_scenario are not considered when Lettuce execute
    Scenario Outline, you need to use @before.outline and @after.outline which are not mentioned in Lettuce documentation.

    Do NOT use 'Scenario' in tests in other places then test name, right below tags (e.g. @my_tag)
    For tags always use '@' before without white spaces:
        good tag: @basic 
        bad tag: @ basic
    For efficient work of Forge project DO NOT put lots of different tags in one feature. It takes a lot of time for lettuce to parsing tags. It's better to make two separate 
    features (as it is with options.feature in options_validation set).
    
    You can use multiple parts like Test Procedure/ Pass Criteria but using Test Setup please be advised that remote server will be restarted,
    configuration removed, generated new configuration and start server with it.
    
    That's all what you should keep while designing new tests ;)
    
    If someone would redesign directory tree for test or files listed above, plz make sure that automatically generated help still working properly.
    """
    
    help_file.close()
    
    #sys.stdout = orginal_stdout
