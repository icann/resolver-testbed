#!/usr/bin/env python3
'''
Build software on VM that is part of a testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files
'''

import os, subprocess, sys, time, json, tempfile

# Some program-wide constants
PROG_DIR = os.path.abspath(os.getcwd())
BUILD_CONFIG = "{}/build_config.json".format(PROG_DIR)
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
    print(die_out)
    sys.exit(1)


log("## Starting run on date {}".format(time.strftime("%Y-%m-%d")))
# Parse the input
if len(sys.argv) < 2:
    die("There were no arguments on the command line.")
# Get the build_config_dict from the config file
try:
    build_f = open(BUILD_CONFIG, mode="rt")
except:
    die("Could not find {}.".format(BUILD_CONFIG))
try:
    build_config_dict = json.load(build_f)
except:
    die("The JSON in {} is broken.".format(BUILD_CONFIG))
# Sanity check the input
if not (("builds" in build_config_dict) and ("templates" in build_config_dict)):
    die("{} does not have the right components.".format(BUILD_CONFIG))
# Be sure that the needed directories are there
for this_dir in (SOURCE_DIR, TARGET_DIR):
    if not os.path.exists(this_dir):
        try:
            os.mkdir(this_dir)
        except:
            die("Could not create {}.".format(this_dir))
# Get the name to build
package_name = sys.argv[1]
if not package_name in build_config_dict["builds"]:
    all_builds = " ".join(sorted((build_config_dict["builds"]).keys()))
    die("The name '{}' was not found in the builds configuration:\n{}\n".format(package_name, all_builds))
try:
    package_url = build_config_dict["builds"][package_name]["url"]
except:
    die("There is no URL for {}.".format(package_name))
try:
    package_make_str = build_config_dict["builds"][package_name]["make_str"]
except:
    die("There is no make string for {}.".format(package_name))
# Replace the make string abbreviation (starts with "!") with the full string
if package_make_str.startswith("!"):
    if package_make_str in build_config_dict["templates"]:
        package_make_str = build_config_dict["templates"][package_make_str]
    else:
        die("{} has a make string of {}, but there is no equivalent for that.".format(package_name, package_make_str))
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

