#!/usr/bin/env python
"""Run the libvirt test cases.
Usage:
  run_tests.py (-h | --help)
  run_tests.py [options]

Examples:
  run_tests.py -s +ts5,-ts2 -c -tc3 -n 2

Options:
  -h, --help
  -s, --testsuite suites    #add/remove some testsuites
  -c, --testcase cases      #remove some testcases (not support 'add')
  -n, --procnum num         #multiprocess num of the running test suites
  -r, --report              #send test result to virt dashborad system
  -t, --testid testid       #testid for result uploading
"""
import os
import sys
from datetime import datetime
import subprocess
import json
import socket
from multiprocessing import Pool
from lxml import etree
from docopt import docopt
import requests
from utils import utils

test_log = 'test.log'
case_dir = 'ali-cases'
suites = ['vm_lifecycle', 'boot', 'vcpu', 'memory', 'disk', 'network',
          'reboot', 'multiqueue', 'cpu_feature', 'gshell']
#suites = ['memory',  'multiqueue', 'network']
run_cmd = 'sudo %s libvirt-test-api -c %s -f %s 2>&1 | tee -a %s'
default_proc_num = 3
test_type = 'FT'
web_ip = '11.238.144.40'
web_port = '80'
upload_url = 'http://%s:%s/api/report/function_test' % (web_ip, web_port)
token = 'virt-api-key'

kernel = utils.get_host_kernel_version()
if kernel.startswith('2.6.32'):
    python = '/usr/local/python/bin/python'
else:
    # always use the houyi python
    python = '/usr/local/python/bin/python'


def add_remove(tlist, opt_list):
    '''
    add/remove item in tlist.
    opt_list is a list like ['+ts5', '-ts2'] or ['+tc5', '-tc3'].
    '''
    for i in opt_list:
        i = i.strip()
        if i.startswith('+'):
            tlist.append(i[1:])
        elif i.startswith('-'):
            if i[1:] in tlist:
                tlist.remove(i[1:])
            else:
                print 'bad argument: %s is not in %s' % (i[1:], tlist)
                print 'trying to ignore it'
        else:
            print 'bad argument: %s' % i
    return tlist


def run_tcase(conf, log_xml):
    ''' run a single test case'''
    subprocess.call(run_cmd % (python, conf, log_xml, test_log), shell=True)


def run_tsuite(tsuite, tc_arg=None, proc_num=1):
    '''
    run test cases of a test suite with $proc_num processes.
    currently, only support single process when running cases in a test suite.
    reason #1: log_xml is per test suite.
    reason #2: the guest names of the cases in a suite can be repeated.
    reason #3: 'daemonic processes are not allowed to have children'
      - use 'from concurrent.futures import ProcessPoolExecutor as Pool'
      - need to 'pip install futures'
    '''
    #pool_t = Pool(proc_num)
    print 'running: run_tsuite %s' % tsuite
    log_xml = 'log-%s.xml' % tsuite
    subprocess.call('rm -f %s' % log_xml, shell=True)
    cases = sorted([i.split('.conf')[0]
                    for i in os.listdir(os.path.join(case_dir, tsuite))
                    if i.endswith('.conf')])
    print 'cases: %s' % cases
    # test case add is not supported yet.
    if tc_arg:
        tc_opt_list = tc_arg.strip().split(',')
        cases = add_remove(cases, tc_opt_list)
    for j in cases:
        conf = os.path.join(case_dir, tsuite, '%s.conf' % j)
        print 'running: run_tcase %s' % conf
        run_tcase(conf, log_xml)
        #pool_t.apply_async(run_tcase, args=(conf, log_xml))
    #pool_t.close()
    #pool_t.join()
    return parse_log(tsuite, cases, log_xml)


def run_tests(tsuites, ts_arg=None, tc_arg=None, proc_num=default_proc_num):
    '''
    run all of the test cases with $proc_num processes.
    '''
    ret = {'testsuite': []}
    if proc_num:
        proc_num = int(proc_num)
    else:
        proc_num = default_proc_num
    if ts_arg:
        ts_opt_list = ts_arg.strip().split(',')
        tsuites = add_remove(tsuites, ts_opt_list)
    if os.path.isdir(case_dir):
        pool = Pool(proc_num)
        subprocess.call('rm -f log-*.xml', shell=True)
        p_list = []
        for i in tsuites:
            p_list.append(pool.apply_async(run_tsuite, args=(i, tc_arg, 1)))
        pool.close()
        pool.join()
        ret['testsuite'] = [p.get() for p in p_list]
    else:
        print 'case_dir: %s is wrong.' % case_dir
        sys.exit(1)
    return ret


def parse_log(suite, cases, logfile):
    '''
    parse the XML log file of a test suite.
    @return: a result dict of the test suite.
    '''
    case_num = 0
    ret = {'name': suite, 'testcase': []}
    tree = etree.parse(logfile)
    test_id = tree.xpath('//test/@id')
    results = [node.text for node in tree.xpath('//test/result')]
    log_paths = [node.text for node in tree.xpath('//test/path')]
    for i in results:
        if i not in ['PASS', 'FAIL']:
            print 'unknown result: %s' % i
            sys.exit(1)
    if len(results) == len(cases):
        for i, j, k in zip(cases, results, log_paths):
            case_num += 1
            temp_dict = {}
            temp_dict['id'] = case_num
            temp_dict['name'] = i
            temp_dict['result'] = j
            temp_dict['info'] = 'logfile: %s' % k
            temp_dict['log'] = k
            ret['testcase'].append(temp_dict)
    else:
        x = -1
        for i, j, k in zip(test_id, results, log_paths):
            if i == '001':
                x += 1
            case_num += 1
            temp_dict = {}
            temp_dict['id'] = case_num
            temp_dict['name'] = cases[x]
            temp_dict['result'] = j
            temp_dict['info'] = 'logfile: %s' % k
            temp_dict['log'] = k
            ret['testcase'].append(temp_dict)
    return ret


def console_summary(result):
    '''
    summarize the result for console output.
    '''
    total_cases = 0
    passed_cases = 0
    failed_cases = 0
    suite_summary = []
    failed_list = []
    for i in result['testsuite']:
        temp_dict = {'name': i['name'], 'passed': 0, 'failed': 0}
        for j in i['testcase']:
            total_cases += 1
            if j['result'] == 'PASS':
                passed_cases += 1
                temp_dict['passed'] += 1
            elif j['result'] == 'FAIL':
                failed_cases += 1
                temp_dict['failed'] += 1
                failed_list.append({'suite': i['name'], 'case': j['name'],
                                    'log': j['log']})
        suite_summary.append(temp_dict)
    pass_rate = '%d%%' % int(round(passed_cases * 100.0) / total_cases)
    print '==Total cases: %d, pass_rate: %s, %d FAIL, %d PASS==' % \
        (total_cases, pass_rate, failed_cases, passed_cases)
    print 'summary of each test suite:'
    for i in suite_summary:
        print 'testsuite %s : %d PASS, %d FAIL' % \
            (i['name'], i['passed'], i['failed'])
    print '==FAIL testcase list:=='
    for i in failed_list:
        print 'FAIL. testsuite: %s, testcase: %s, log: %s' % (i['suite'],
                                                              i['case'],
                                                              i['log'])


def get_self_ip():
    ''' get the ip of current machine'''
    return socket.gethostbyname(socket.gethostname())


def cal_time(dt1, dt2):
    ''' calculate the interval in seconds between datetime1 and datetime2 '''
    return (dt2 - dt1).seconds


def upload_result(url, test_id, test_type, start_time, run_time, machine_ip,
                  token, data):
    ''' upload test result to virt dashboard system '''
    upload_data = {
                    "test_run_id": test_id,
                    "test_type": test_type,
                    "test_start_time": start_time,
                    "test_run_time": run_time,
                    "machine_ip": machine_ip,
                    "token": token,
                    "result_data": data
    }
    r = requests.post(url, data=json.dumps(upload_data))
    if r.status_code != requests.codes.ok:
        print 'error! http code: %s' % r.status_code
    else:
        res_data = r.json()
        if res_data['status'] != 'ok':
            print 'response NOT ok! status:%s, msg:%s' % (res_data['status'],
                                                          res_data['message'])
        else:
            print 'upload data. OK.'


if __name__ == '__main__':
    args = docopt(__doc__)
    cise_start_line = '##TESTCASE START##'
    cise_end_line = '##TESTCASE END##'
    ts_arg = args.get('--testsuite')
    tc_arg = args.get('--testcase')
    proc_num = args.get('--procnum')
    need_report = args.get('--report')
    test_id = args.get('--testid')
    start_time = datetime.now()
    cise_result = run_tests(suites, ts_arg, tc_arg, proc_num)
    end_time = datetime.now()
    print cise_start_line
    print json.dumps(cise_result, indent=4)
    print cise_end_line
    print '====================Console Output====================='
    console_summary(cise_result)
    print '====================The END============================'
    if need_report:
        if not test_id:
            print 'error! upload test result but you don not have a test_id'
            sys.exit(1)
        print 'uploading test result ...'
        upload_result(upload_url, test_id, test_type,
                      start_time.strftime("%Y-%m-%d %H:%M:%S"),
                      cal_time(start_time, end_time), get_self_ip(),
                      token, cise_result)
    else:
        print 'no need to upload test result.'
