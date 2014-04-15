#!/usr/bin/python

"""a small tool to measure if TCP is stable by using ssh
"""

import argparse
import time
import subprocess

def get_parser():
    """gets us an argparse.ArgumentParser for natmeasure.py"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", "-H",
                        default="rd",
                        help="ssh host to connect to.")
    parser.add_argument("--mintime", "-m",
                        default=0,
                        type=int,
                        help="minimum wait time in seconds to test")
    parser.add_argument("--maxtime", "-M",
                        default=60,
                        type=int,
                        help="maximum wait time in seconds to test")
    parser.add_argument("--timeinterval", "-i",
                        default=5,
                        type=int,
                        help="test waittime step")
    parser.add_argument("--report-file", "-r", "-o",
                        required=True,
                        help="write the report to this file.")
    return parser


def test_access_with_wait(output_file, host, wait):
    """test that we can connect to host, wait "wait" seconds and
    continue receiving data.
    """
    remotecmd = "echo $(date) %d START ; sleep %d ; echo $(date) %d OK" % (
        wait, wait, wait)
    subprocess.Popen(["ssh", host,
                      remotecmd],
                     stdout=output_file)
    time.sleep(1)

def main():
    "main program of natmeasure.py"
    parser = get_parser()
    args = parser.parse_args()
    with open(args.report_file, "w") as file_obj:
        file_obj.write(">>> Starting SSH tests at %s localtime\n" % \
                           (time.strftime("%Y/%m/%d %H:%M:%S",
                                          time.localtime(time.time())), ))
        file_obj.write(">>> Report should be finished by %s localtime\n" % \
                       (time.strftime("%Y/%m/%d %H:%M:%S",
                                      time.localtime(time.time() +
                                                     args.maxtime + 15)), ))
        file_obj.write(">>> Arguments used: %r\n" % (args, ))
        file_obj.write(">>> Peak TCP usage: %d concurrent TCP connections\n" % \
                           ((args.maxtime - args.mintime) / args.timeinterval))

    output = open(args.report_file, "a")
    for wait in reversed(range(args.mintime,
                               args.maxtime + 1,
                               args.timeinterval)):
        test_access_with_wait(output, args.host, wait)

if __name__ == "__main__":
    main()
