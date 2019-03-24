#!/usr/bin/env python3
'''
Build software on VM that is part of a testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files
'''

import os, subprocess, sys, time, tempfile

# Some program-wide constants
PROG_DIR = os.path.abspath(os.getcwd())
SOURCE_DIR = "/root/Source"
TARGET_DIR = "/root/Target"

this_log_filename = tempfile.mktemp()
this_log_f = open(this_log_filename, mode="wt")


def log(in_str):
	''' Prints a message , but only if the message is non-null; returns nothing '''
	if not in_str:
		return
	out = "{}: {}\n".format(time.strftime("%H-%M-%S"), in_str)
	this_log_f.write(out)

def die(in_str):
    ''' log then exit  '''
    err_str = in_str + " Exiting.\n"
    log(err_str)
    this_log_f.close()
    die_out = open(this_log_filename, mode="rt").read()
    print(die_out, file=sys.stderr)
    sys.exit(1)


log("## Starting run on date {}".format(time.strftime("%Y-%m-%d")))
# Parse the input
if len(sys.argv) < 4:
    die("There were not enough arguments on the command line.")
# Be sure that the needed directories are there
for this_dir in (SOURCE_DIR, TARGET_DIR):
    if not os.path.exists(this_dir):
        try:
            os.mkdir(this_dir)
        except:
            die("Could not create {}.".format(this_dir))
# Get the name to build
package_name = sys.argv[1]
package_url = sys.argv[2]
package_make_str = sys.argv[3]
try:
    os.chdir(SOURCE_DIR)
except:
    die("Could not chdir to {}.".format(SOURCE_DIR))
# Get the compressed file into SOURCE_DIR
log("Getting {}".format(package_url))
p = subprocess.Popen("wget {}".format(package_url), stderr=subprocess.PIPE, shell=True)
p_ret = p.wait()
if p_ret > 0:
    die("wget failed with '{}'.".format((p.stderr.read()).decode("latin-1")))
# Uncompress into package_name
log("Uncompressing {}".format(os.path.basename(package_url)))
p = subprocess.Popen("tar -xf {}".format(os.path.basename(package_url)), shell=True)
p_ret = p.wait()
if p_ret > 0:
    die("tar -xf failed with '{}'.".format((p.stderr.read()).decode("latin-1")))
# Verify that the expected directory exists, then chdir there
package_source_dir = (os.path.splitext(os.path.basename(package_url))[0]).replace(".tar", "")
if not os.path.exists(package_source_dir):
    die("Getting and expanding {} did not result in a directory {}.".format(package_url, package_source_dir))
try:
    os.chdir(package_source_dir)
except:
    die("Could not chdir into {}".format(package_source_dir))
# Change PREFIX_GOES_HERE in package_make_str into TARGET_DIR/package_name
full_make_str = package_make_str.replace("PREFIX_GOES_HERE", "{}/{}".format(TARGET_DIR, package_source_dir))
log("Making with '{}'".format(full_make_str))
# Make
p = subprocess.Popen(full_make_str, stderr=subprocess.PIPE, shell=True)
p_ret = p.wait()
if p_ret > 0:
    die("making failed with '{}'.".format((p.stderr.read()).decode("latin-1")))
log("## Finished run")
this_log_f.close()
try:
    os.remove(this_log_filename)
except:
    print("Weird, could not delete the log file")
exit()

