#!/usr/bin/env python3
'''
Testbed for DNS resolvers
See https://github.com/icann/resolver-testbed for more information
Must be run in the same directory as the config files
'''

import glob, json, os, shutil, subprocess, sys, time

# Constants
LOG_FILE_NAME = "log_for_resolver_test.txt"
LOG_F = open(LOG_FILE_NAME, mode="a")
DEBUG_LOG_FILE_NAME = "debug_log_for_resolver_test.txt"
DEBUG_LOG_F = open(DEBUG_LOG_FILE_NAME, mode="a")
MAIN_CONFIG = "config_for_resolver_test.json"
PROG_DIR = os.getcwd()
BASES_DIR = "Bases"
SOURCES_DIR = "Sources"
TESTS_DIR = "Tests"
LOCAL_DIRS_LIST = (BASES_DIR, SOURCES_DIR, TESTS_DIR)
RESOLVER_TEST_LOWEST_BASE = "restest1604"
PROVISION_FILE = "run_at_start.sh"
TCPDUMP_PREFIX = "tcpdump -i"
SUDO_NOHUP_TCPDUMP_PREFIX = "sudo nohup tcpdump -i"

HELP_TEXT = '''
Available commands are:
help:           Show this text
list:           Show the resolver names and their tags
update_sources: Update all resolver tarballs
fill_configs:   Update all resolver configuration files
make_bases:     Make the base images; this is probably only run once
build:          Build one or more resolvers; needs exactly one argument,
                   either "all", the name of a resolver, or a tag
test:           Run a test; needs exactly two arguments, the test name
                   and either "all", the name of a resolver, or a tag
'''.strip()

BASE_TEMPLATE = '''
Vagrant.configure("2") do |config|
  config.vm.box = "THIS_BOX"
  config.vm.provision "shell", path: "THIS_PROVISION_FILE"
  config.vm.define "THIS_BASE" do |THIS_BASE|
  end
end
'''.strip().replace("THIS_PROVISION_FILE", PROVISION_FILE)

def log(log_message):
    ''' log to the main log '''
    LOG_F.write("{}: {}\n".format(time.strftime("%Y-%m-%d-%H-%M-%S"), log_message))

def debug(debug_message):
    ''' Print debug info '''
    DEBUG_LOG_F.write("{}\n".format(debug_message))
    DEBUG_LOG_F.flush()

def log_and_print(log_message):
    ''' log, then print to the user '''
    print("{}: {}".format(time.strftime("%Y-%m-%d-%H-%M-%S"), log_message))
    log(log_message)

def die(in_str):
    ''' log, print, then exit  '''
    err_str = in_str + " Exiting."
    log_and_print(err_str)
    exit()

def show_help():
    ''' show some help text to the user '''
    print(HELP_TEXT)

def get_configs():
    ''' Make sure the configuration file is good; die if not.
        Returns objects with main config data '''
    # See if the files exist
    if not os.path.exists(MAIN_CONFIG):
        die("Could not find {}.".format(MAIN_CONFIG))
    # See if the main config file is valid JSON
    main_config_f = open(MAIN_CONFIG)
    try:
        in_config = json.load(main_config_f)
    except Exception as this_e:
        die("{} is not valid JSON: {}.".format(MAIN_CONFIG, this_e))
    # Walk through the MAIN_CONFIG list of dicts
    #   Be sure name url make start stop all exist
    #   Be sure there are no repeated name values
    #   If all is good, add to build_info
    build_info = (in_config["builds"]).copy()
    bases_info = in_config["bases"]
    templates_info = in_config["templates"]
    tests_info = in_config["tests"]
    # In templates, if a value is a list instead of a string, convert it into a string
    for this_template in templates_info:
        if isinstance(templates_info[this_template], list):
            templates_info[this_template] = "\n".join(templates_info[this_template])
    for this_item in build_info:
        this_dict = build_info[this_item]
        for this_req in ("url", "base", "tags", "desc", "make_str", "start"):
            if this_req not in this_dict.keys():
                die("In the configuration sanity check, '{}' does not have a '{}' key, which is required.".format(this_dict, this_req))
        for this_must_be_filled_in in ("url", "base", "conf_type", "make_str"):  ##### Later add "start"
            if this_dict[this_must_be_filled_in] == "":
                die("The value for {} in {} is blank, and cannot be.".format(this_must_be_filled_in, this_dict))
        # Look for items that start with "!", and replace their value
        holder = (build_info[this_item]).copy()  # Needed so we can replace in the loop
        for this_key in build_info[this_item]:
            if this_key == "tags":
                continue
            if (build_info[this_item][this_key]).startswith("!"):
                this_sub = templates_info.get(build_info[this_item][this_key])
                if not this_sub:
                    die("The value '{}' is not a template in the configuration.".format(build_info[this_item][this_key]))
                holder[this_key] = this_sub
        (build_info[this_item]).update(holder)
        # See if any bases listed in "builds" are not also in "bases"
        if build_info[this_item]["base"] not in bases_info.keys():
            die("The base listed in {} is not a base in the configuration.".format(this_item))
    # The templates info doesn't need to be returned because it is already is part of build_info
    return build_info, bases_info, tests_info

def vagrant_sanity():
    ''' Tests whether virtualbox and vagrant are installed.
        Also Checks that RESOLVER_TEST_LOWEST_BASE exists. Dies if any of these fail '''
    vagrant_check = subprocess.getoutput("which vagrant")
    if not vagrant_check:
        die("vagrant is not installed.")
    virtualbox_check = subprocess.getoutput("which virtualbox")
    if not virtualbox_check:
        die("virtualbox is not installed.")
    box_list_text = subprocess.getoutput("vagrant box list")
    for this_box_line in box_list_text.splitlines():
        if RESOLVER_TEST_LOWEST_BASE in this_box_line:
            return
    die("Did not find {} in 'vagrant box list'; use 'vagrant box add {}' first.".format(RESOLVER_TEST_LOWEST_BASE, RESOLVER_TEST_LOWEST_BASE))

def directory_sanity():
    ''' Checks if the local directories exist where they should '''
    for this_dir in LOCAL_DIRS_LIST:
        if not os.path.exists(this_dir):
            os.mkdir(this_dir)
        if not os.path.isdir(this_dir):
            die("{} exists but is not a directory.".format(this_dir))

def get_config_names_and_tags(build_info):
    ''' Text of the names and tags in the configuration '''
    config_names_and_tags = "\nName                 Tags\n"
    for this_name in sorted(build_info):
        config_names_and_tags += "{:20s} {}\n".format(this_name, " ".join(build_info[this_name]["tags"]))
    return config_names_and_tags.rstrip()

def fill_sources(this_base):
    ''' Copy the contents of SOURCES_DIR and TESTS_DIR into an existing base '''
    # Need to copy files instead of symlinking because VirtualBox shared directories with symlinks can have problems
    log_and_print("Filling sources in {}.".format(this_base))
    start_dir = os.getcwd()
    os.chdir(PROG_DIR)
    orig_sources = "{}/{}".format(SOURCES_DIR, this_base)
    target_sources = "{}/{}/{}".format(BASES_DIR, this_base, SOURCES_DIR)
    if os.path.exists(target_sources):
        try:
            shutil.rmtree(target_sources)
        except Exception as this_e:
            die("Unable to remove {}: {}".format(target_sources, this_e))
    try:
        shutil.copytree(orig_sources, target_sources)
    except Exception as this_e:
        die("Copying {} into {} failed: {}.".format(orig_sources, target_sources, this_e))
    # Clean up
    os.chdir(start_dir)

def fill_configs(this_base):
    ''' Copy the contents of SOURCES_DIR and TESTS_DIR into an existing base '''
    # Need to copy files instead of symlinking because VirtualBox shared directories with symlinks can have problems
    log_and_print("Filling configs in {}.".format(this_base))
    start_dir = os.getcwd()
    os.chdir(PROG_DIR)
    orig_configs = "{}".format(TESTS_DIR)
    target_configs = "{}/{}/{}".format(BASES_DIR, this_base, TESTS_DIR)
    if os.path.exists(target_configs):
        try:
            shutil.rmtree(target_configs)
        except Exception as this_e:
            die("Unable to remove {}: {}".format(target_configs, this_e))
    try:
        shutil.copytree(orig_configs, target_configs)
    except Exception as this_e:
        die("Copying {} into {} failed: {}.".format(orig_configs, target_configs, this_e))
    # Clean up
    os.chdir(start_dir)

def get_our_pids(this_base):
    ''' Runs ps ax, returns the list of PIDs whose comand starts with "/res_binaries/ '''
    # Get the id of the running box; Vagrant should accept the name but doesn't; https://github.com/mitchellh/vagrant/issues/8691
    id_of_base = ""
    for this_line in (subprocess.getoutput("vagrant global-status")).splitlines():
        if this_base in this_line:
            (id_of_base, _) = this_line.split(" ", 1)
            break
    if not id_of_base:
        die("No id could be found for {}.".format(this_base))
    this_command = "vagrant ssh --command \"ps ax o pid,args --no-headers\" {}".format(id_of_base)
    this_ps = subprocess.getoutput(this_command)
    pids_to_return = []
    for this_line in this_ps.splitlines():
        (this_pid, this_cmd) = (this_line.strip()).split(" ", 1)
        if this_cmd.startswith("/res_binaries/"):
            pids_to_return.append((this_pid, this_cmd))
    return pids_to_return

def kill_all_resolvers(this_base):
    ''' Find the list of PIDs whose comand starts with "/res_binaries/, kill -9 each PID, starting from the lowest '''
    # Get the id of the running box; Vagrant should accept the name but doesn't; https://github.com/mitchellh/vagrant/issues/8691
    id_of_base = ""
    for this_line in (subprocess.getoutput("vagrant global-status")).splitlines():
        if this_base in this_line:
            (id_of_base, _) = this_line.split(" ", 1)
            break
    if not id_of_base:
        die("No id could be found for {}.".format(this_base))
    this_command = "vagrant ssh --command \"sudo ps ax o pid,args --no-headers\" {}".format(id_of_base)
    this_ps = subprocess.getoutput(this_command)
    pids_to_kill = []
    for this_line in this_ps.splitlines():
        (this_pid, this_cmd) = (this_line.strip()).split(" ", 1)
        if this_cmd.startswith("/res_binaries/"):
            pids_to_kill.append(this_pid)
    if len(pids_to_kill) == 0:
        return  # Nothing to do
    log("About to kill {}".format(", ".join(pids_to_kill)))
    kill_command = ""
    for this_pid in pids_to_kill:
        kill_command += "sudo kill -9 {}; ".format(this_pid)
    subprocess.getoutput("vagrant ssh --command \"{}\" {}".format(kill_command, id_of_base))
    after_kill_list = get_our_pids(this_base)
    if len(after_kill_list) > 0:
        die("After trying to kill all the PIDs in {}, PIDs {} were still alive.".format(this_base, after_kill_list))

def start_tcpdump(test_name, test_target):
    ''' Starts tcpdump on the host system. Returns nothing, but dies if it cannot start. '''
    # Require that the interface is defined
    this_interface = os.environ.get("RESOLVER_TEST_INTERFACE")
    if not this_interface:
        die("The environment variable 'RESOLVER_TEST_INTERFACE' must be set.")
    # See if tcpdump is already running
    running_check_text = subprocess.getoutput("sudo ps ax o pid,args --no-headers")
    if TCPDUMP_PREFIX in running_check_text:
        for this_line in running_check_text.splitlines():
            if TCPDUMP_PREFIX in this_line:
                die("tcpdump is already running: '{}'. Kill it before trying again.".format(this_line))
    this_tcpdump_file = "{}/dump-{}-{}.pcap".format(PROG_DIR, test_name, test_target)
    if os.path.exists(this_tcpdump_file):
        old_tcpdump_file = "{}/dump-{}-{}-{}.pcap".format(PROG_DIR, test_name, test_target, time.strftime("%Y-%m-%d-%H-%M-%S"))
        try:
            shutil.move(this_tcpdump_file, old_tcpdump_file)
        except Exception as this_e:
            die("Could not move '{}' to '{}': {}.".format(this_tcpdump_file, old_tcpdump_file, this_e))
        log_and_print("'{}' already exists; moved to '{}'".format(this_tcpdump_file, old_tcpdump_file))
    sudo_tcpdump_command = "{} {} -U -n port 53 -w {} &".format(SUDO_NOHUP_TCPDUMP_PREFIX, this_interface, this_tcpdump_file)
    try:
        subprocess.call(sudo_tcpdump_command, shell=True)
        log_and_print("Started tcpdump on interface {} into file \"{}\"".format(this_interface, this_tcpdump_file))
    except Exception as this_e:
        die("In starting tcpdump with '{}', got error '{}'.".format(sudo_tcpdump_command, this_e))
    log_and_print("Started tcpdump file {}".format(this_tcpdump_file))

def stop_tcpdump():
    ''' Stops tcpdump on the host system. Returns nothing. '''
    running_check_text = subprocess.getoutput("sudo ps ax o pid,args --no-headers")
    if TCPDUMP_PREFIX in running_check_text:
        for this_line in running_check_text.splitlines():
            if TCPDUMP_PREFIX in this_line:
                # Do not kill the "sudo nohup" commands because this causes extra output at the end of the pcap file
                if SUDO_NOHUP_TCPDUMP_PREFIX not in this_line:
                    (pid, _) = (this_line.strip()).split(" ", 1)
                    try:
                        subprocess.check_call("sudo kill -9 {}".format(pid), shell=True)
                    except Exception as this_e:
                        die("In trying to kill '{}', got exception '{}'".format(this_line, this_e))
                    log_and_print("Stopped tcpdump on pid {}".format(pid))

def send_start_and_end(in_str, test_name, target):
    ''' Make a bogus DNS query in order to have it be caught in tcpdump '''
    # Be sure there are no spaces in the arguments
    for arg in (in_str, test_name, target):
        if " " in arg:
            die("There was a space character in '{}' argument for the send_start_and_end function.".format(arg))
    # Ignore the output
    subprocess.getoutput("dig +time=1 +tries=0 @255.53.53.53 {}.{}.{}.invalid".format(in_str, test_name, target))

def do_update_sources(build_info):
    ''' Action for update_sources: look at the current tarballs and get what is missing; expand as files are downloaded '''
    os.chdir(SOURCES_DIR)
    downloaded = False
    # Find which URLs from the config needs to be downloaded
    for this_record in build_info:
        this_base = build_info[this_record]["base"]
        this_url = build_info[this_record]["url"]
        this_end = os.path.basename(this_url)
        if not os.path.exists(this_base):
            os.mkdir(this_base)
        os.chdir(this_base)
        files_in_this_base = glob.glob("*")
        os.chdir("..")
        if this_end not in files_in_this_base:
            # Get the file
            os.chdir(this_base)
            try:
                log_and_print("Downloading {}".format(this_url))
                subprocess.check_call("wget {}".format(this_url), shell=True)
                downloaded = True
            except Exception as this_e:
                die("Could not download {}: {}.".format(this_url, this_e))
            # Expand the file
            log_and_print("Expanding {}".format(this_end))
            try:
                subprocess.check_call("tar -xf {}".format(this_end), shell=True)
            except Exception as this_e:
                log_and_print("Could not expand {}: {}.".format(this_end, this_e))
            os.chdir("..")
    if not downloaded:
        log_and_print("No tarballs needed to be downloaded.")
    # Refill the sources and configs in the bases
    os.chdir(PROG_DIR)
    os.chdir(BASES_DIR)
    bases_list = glob.glob("*")
    for this_base in bases_list:
        if not os.path.exists(this_base):
            os.mkdir(this_base)
        fill_sources(this_base)
        fill_configs(this_base)
    # Get back to program base
    os.chdir(PROG_DIR)

def do_fill_configs():
    ''' Action for fill_configs: resync the config files '''
    os.chdir(PROG_DIR)
    os.chdir(BASES_DIR)
    bases_list = glob.glob("*")
    for this_base in bases_list:
        if not os.path.exists(this_base):
            os.mkdir(this_base)
        fill_configs(this_base)
    # Get back to program base
    os.chdir(PROG_DIR)

def do_make_bases(bases_info):
    ''' Action for make_bases: see which bases are not yet built, and build them '''
    log_and_print("Bases from the config: {}".format(" ".join(sorted(bases_info.keys()))))
    current_boxes_text = subprocess.getoutput("vagrant box list")
    current_boxes_list = []
    for this_line in current_boxes_text.splitlines():
        (name, _) = this_line.split(" ", 1)
        if name == RESOLVER_TEST_LOWEST_BASE:
            continue
        current_boxes_list.append(name)
    log_and_print("Boxes already installed: {}".format(" ".join(sorted(current_boxes_list))))
    for this_base in bases_info.keys():
        if this_base in current_boxes_list:  # Don't do boxes that already exist
            continue
        log_and_print("Building {}".format(this_base))
        os.chdir(BASES_DIR)
        if os.path.exists(this_base):
            log_and_print("{}/{} already exists; removing.".format(BASES_DIR, this_base))
            try:
                shutil.rmtree("{}".format(this_base))
            except Exception as this_e:
                die("Removing {}/{} failed with '{}'.".format(BASES_DIR, this_base, this_e))
        os.mkdir(this_base)
        # Fill the sources and configs in this directory
        fill_sources(this_base)
        fill_configs(this_base)
        os.chdir(this_base)
        # First Vagrantfile uses RESOLVER_TEST_LOWEST_BASE as the box, and the first provision file does all the apt goop
        out_text = BASE_TEMPLATE
        out_text = out_text.replace("THIS_BOX", RESOLVER_TEST_LOWEST_BASE)
        out_text = out_text.replace("THIS_BASE", this_base)
        vagrantfile_f = open("Vagrantfile", mode="wt")
        vagrantfile_f.write(out_text)
        vagrantfile_f.close()
        provision_f = open(PROVISION_FILE, mode="wt")
        provision_f.write("apt update\napt -y upgrade\nmkdir -m 0777 /res_binaries\n")
        provision_f.write("\n".join(bases_info[this_base]))
        provision_f.write("\nmkdir ~/temp_build\n")
        provision_f.close()
        log_and_print("Bringing up {} the first time".format(this_base))
        # Vagrant returns 0 even when there are errors, so there is no need to check for the return value <sigh>
        subprocess.call("vagrant up", shell=True)
        log_and_print("Packaging {}".format(this_base))
        subprocess.call("vagrant package", shell=True)  # Do not include the Vagrantfile because it has the provision
        if not os.path.exists("package.box"):
            die("After packaging, there was no 'package.box' file.")
        log_and_print("Adding box for {}".format(this_base))
        subprocess.call("vagrant box add --clean --name {} ./package.box".format(this_base), shell=True)
        # Get rid of the large package.box file; it's no longer needed
        os.unlink("package.box")
        # Second Vagrantfile uses this_base as the box, and the second provision file is a placeholder
        out_text = BASE_TEMPLATE
        out_text = out_text.replace("THIS_BOX", this_base)
        out_text = out_text.replace("THIS_BASE", this_base)
        vagrantfile_f = open("Vagrantfile", mode="wt")
        vagrantfile_f.write(out_text)
        vagrantfile_f.close()
        provision_f = open(PROVISION_FILE, mode="wt")
        provision_f.write("# Now empty\n")
        provision_f.close()
        log_and_print("Starting up the {} box itself.".format(this_base))
        subprocess.call("vagrant up --provision", shell=True)
        # Clean up
        os.chdir(PROG_DIR)
    # Show the list of bases and the status of the bases
    out_text = subprocess.getoutput("vagrant box list")
    log_and_print("After processing, the full list of boxes is:\n{}".format(out_text))
    out_text = subprocess.getoutput("vagrant global-status")
    log_and_print("After processing, the full status of the bases is:\n{}".format(out_text))

def do_build(build_info, list_of_builds):
    ''' Build resolvers based on the incoming list '''
    for this_build in list_of_builds:
        this_base = build_info[this_build]["base"]
        log_and_print("Building '{}' in '{}'".format(this_build, this_base))
        # Get to the BASES_DIR directory first, then check if the base directory exists
        os.chdir(BASES_DIR)
        try:
            os.chdir(this_base)
        except Exception as this_e:
            die("Changing to {}/{} failed: {}.".format(BASES_DIR, this_base, this_e))
        # See if the directory with the right source exists
        this_source_dir = "{}/{}".format(SOURCES_DIR, this_build)
        if not os.path.exists(this_source_dir):
            die("The directory {} did not exist.".format(this_source_dir))
        # Change the PROVISION_FILE to be the make instructions
        make_instructions = "# /usr/bin/env bash\n"
        make_instructions += "# Instructions for {}\n".format(this_build)
        make_instructions += "[ -e /res_binaries/{0} ] && echo \"The binary for {0} already exists.\" && exit\n".format(this_build)
        make_instructions += "rm -rf ~/temp_build/*\n"
        make_instructions += "cp -rp /vagrant/{0}/{1} ~/temp_build/ && cd ~/temp_build/{1}\n".format(SOURCES_DIR, this_build)
        make_instructions += "{}\n".format(build_info[this_build]["make_str"])
        make_instructions = make_instructions.replace("PREFIX_GOES_HERE", "/res_binaries/{}".format(this_build))
        prov_f = open(PROVISION_FILE, mode="wt")
        prov_f.write(make_instructions)
        prov_f.close()
        subprocess.call("vagrant provision", shell=True)
        # Clean up
        os.chdir(PROG_DIR)

def do_test(build_info, tests_info, test_name, test_targets):
    ''' Run a test based on the test name and the target resolver '''
    log_and_print("Attempting to run test {} on '{}'".format(test_name, ", ".join(test_targets)))
    for this_target in test_targets:
        # Make sure there is a start
        this_start = build_info[this_target]["start"]
        if not this_start:
            die("There was no 'start' in {}.".format(this_target))
        # The command always starts with /res_binaries/ and the name of the target
        this_start = this_start.replace("PREFIX_GOES_HERE", "/res_binaries/{}".format(this_target))
        this_base = build_info[this_target]["base"]
        this_conf_type = build_info[this_target]["conf_type"]
        if "CONF_FILE_NAME" in this_start:
            this_conf_file = "{}-{}.conf".format(this_conf_type, test_name)
            if not os.path.exists("{}/{}".format(TESTS_DIR, this_conf_file)):
                die("The file {}, which is needed for {}, does not exist.".format("{}/{}".format(TESTS_DIR, this_conf_file), this_conf_type))
            this_start = this_start.replace("CONF_FILE_NAME", "/vagrant/{}/{}".format(TESTS_DIR, this_conf_file))
        # There shoud not be any resolvers running yet
        start_pids = get_our_pids(this_base)
        if len(start_pids) > 0:
            log_and_print("At the start, there were still resolvers already running: {}.".format(start_pids))
            kill_all_resolvers(this_base)
        os.chdir(BASES_DIR)
        try:
            os.chdir(this_base)
        except Exception as this_e:
            die("Changing to '{}/{}' failed: {}.".format(BASES_DIR, this_base, this_e))
        test_instructions = "# /usr/bin/env bash\n"
        test_instructions += "{}\n".format(this_start)
        test_instructions += "sleep 1\n"
        # If there is a "on-vm" given, make sure it exists and then add it to the test_instructions
        this_on_vm = (tests_info[test_name]).get("on-vm")
        if this_on_vm:
            if not os.path.exists("{}/{}".format(TESTS_DIR, this_on_vm)):
                die("The file '{}' specified for this test for 'on-vm' does not exist.".format(this_on_vm))
            test_instructions += "/vagrant/{}/{}\n".format(TESTS_DIR, this_on_vm)
        prov_f = open(PROVISION_FILE, mode="wt")
        prov_f.write(test_instructions)
        prov_f.close()
        log_and_print("Running test {} on {}".format(test_name, this_target))
        send_start_and_end("start", test_name, this_target)
        test_provision_out = subprocess.getoutput("vagrant provision")
        # Nuke any resolver stuff that got started
        kill_all_resolvers(this_base)
        send_start_and_end("end", test_name, this_target)
        log("Output of {} on {}:\n{}".format(test_name, this_target, test_provision_out))
        if "non-zero" in test_provision_out:
            log_and_print("That test probably failed; see the logs for 'Output of {} on {}'.".format(test_name, this_target))
        debug("Output of {} on {}:\n{}".format(test_name, this_target, test_provision_out))
        # Clean up
        os.chdir(PROG_DIR)

def run_main():
    ''' The main program; always exits '''
    # Parse the input
    if len(sys.argv) < 2:
        show_help()
        die("There were no arguments on the command line.")
    vagrant_sanity()  # Will die if it does not pass
    directory_sanity()  # Build the needed directories
    build_info, bases_info, tests_info = get_configs()  # Fills in the configuration dicts
    log("build_info: {}".format(build_info))
    log("bases_info: {}".format(bases_info))
    # Get the list of all the resolver names
    all_resolver_names = build_info.keys()
    all_resolver_tags = set()
    for this_name in all_resolver_names:
        for this_tag in build_info[this_name]["tags"]:
            all_resolver_tags.add(this_tag)
    all_test_names = tests_info.keys()
    # Get the command
    cmd = sys.argv[1]
    cmd_args = sys.argv[2:]
    debug("Starting a run at {}".format(time.strftime("%Y-%m-%d-%H-%M-%S")))
    # Figure out which command it was
    if cmd == "help":  # Help
        show_help()
    elif cmd == "list":  # List the resolvers in the configuration file
        log_and_print(get_config_names_and_tags(build_info))
        log_and_print("\nTests names: {}".format(", ".join([x for x in tests_info])))
    elif cmd == "update_sources":  # Get all the tarballs
        do_update_sources(build_info)
    elif cmd == "fill_configs":  # Update the configs
        do_fill_configs()
    elif cmd == "make_bases":  # Build base images
        do_make_bases(bases_info)
    elif cmd == "build":  # Build resolver containers
        # Needs to have an argument
        if len(cmd_args) != 1:
            print(get_config_names_and_tags(build_info).lstrip())
            die("'build' needs exactly one argument, either 'all' or a name of a resolver or a tag.")
        build_arg = cmd_args[0]
        # Determine if the argument is "all", or a resolver name, or a tag
        if build_arg == "all":
            do_build(build_info, sorted(all_resolver_names))
        elif build_arg in all_resolver_names:  # Look for a single name
            do_build(build_info, [build_arg])
        elif build_arg in all_resolver_tags:  # Look for a tag
            matched_tags = []
            for this_name in all_resolver_names:
                if build_arg in build_info[this_name]["tags"]:
                    matched_tags.append(this_name)
            do_build(build_info, sorted(matched_tags))
        else:
            die("The '{}' argument to 'build' is unrecognized.".format(build_arg))
    elif cmd == "test":  # Run a test
        # Needs to have two arguments
        if len(cmd_args) != 2:
            die("'test' needs exactly two arguments: the test name and the target resolver. Tests are:\n{}\n".format(sorted(all_test_names)))
        test_name = cmd_args[0]
        test_target = cmd_args[1]
        if test_name not in all_test_names:
            die("The test name '{}' is not in the list '{}'.".format(test_name, ", ".join(sorted(all_test_names))))
        # Start up tcpdump
        start_tcpdump(test_name, test_target)
        # Determine if the second argument is "all", or a resolver name, or a tag
        if test_target == "all":
            do_test(build_info, tests_info, test_name, sorted(all_resolver_names))
        elif test_target in all_resolver_names:  # Look for a single name
            do_test(build_info, tests_info, test_name, [test_target])
        elif test_target in all_resolver_tags:  # Look for a tag
            matched_tags = []
            for this_name in all_resolver_names:
                if test_target in build_info[this_name]["tags"]:
                    matched_tags.append(this_name)
            do_test(build_info, tests_info, test_name, sorted(matched_tags))
        else:
            die("The target argument to 'test', '{}' is not recognized.".format(test_target))
        stop_tcpdump()
        # Change all the ownerships of dump-* to the owner of the log file
        log_stat = os.stat(LOG_FILE_NAME)
        for this_dump in glob.glob("dump-*"):
            try:
                subprocess.check_call("sudo chown {0}:{1} {2}".format(log_stat[4], log_stat[5], this_dump), shell=True)
            except Exception as this_e:
                log_and_print("Failed to chown '{}' because '{}'. Continuing.".format(this_dump, this_e))
    else:
        log_and_print("'{}' is not a valid command.".format(cmd))
        show_help()
    # We're done, so exit
    exit()

# Run the main program
if __name__ == "__main__":
    run_main()
