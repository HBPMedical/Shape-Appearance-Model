#!/usr/bin/env python

import os, subprocess
from argparse import ArgumentParser

def build_settings_file(template_file, output_file, k, vx, v_settings, a_settings, mu_settings, maxit, result_name, result_dir, batch_size):
    with open(template_file) as f:
        template_string = f.read()

    template_string = template_string.replace("__K__", k)
    template_string = template_string.replace("__VX__", vx)
    template_string = template_string.replace("__V_SETTINGS__", v_settings)
    template_string = template_string.replace("__A_SETTINGS__", a_settings)
    template_string = template_string.replace("__MU_SETTINGS__", mu_settings)
    template_string = template_string.replace("__MAXIT__", maxit)
    template_string = template_string.replace("__RESULT_NAME__", result_name)
    template_string = template_string.replace("__RESULT_DIR__", result_dir)
    template_string = template_string.replace("__BATCHSIZE__", batch_size)

    with open(output_file, 'w') as f:
        f.write(template_string)

def run_app(file_names, settings):
    path, fil = os.path.split(__file__)
    app_file = os.path.join(path, "runPG")

    cmdStr = "runPG {0} {1}".format(
                                  file_names,
                                  settings)
    #cmdStr = "cat {0}".format(settings)
    print "CMD = {0}".format(cmdStr)
    try:
        result = subprocess.check_output(cmdStr,
                                         shell=True, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
	print "Error is {0}".format(e.output)
  

def file_exists(parser, file_name):
    if not os.path.exists(file_name):
        parser.error("File not found: %s" % file_name)
    return file_name

def main(args=None):
    print "Yo"
    parser = ArgumentParser(description="A script that creates the settings file for the runPG application")
    parser.add_argument("filenames", type=lambda x: file_exists(parser, x), help="JSON file containing the file names.")
    parser.add_argument("k", type=int,
                        help="Number of shape and appearance components. Example: 64")
    parser.add_argument("vx", type=str, help="Voxel sizes (mm - matches those of \"imported\" images). Example: [1.5 1.5 1.5]")
    parser.add_argument("v_settings", type=str, help="Registration regularisation settings. Example: [1e-05,0.01,0.2,0.025,0.05].")
    parser.add_argument("a_settings", type=str, help="Appearance regularisation settings. Example: [0.01,1,0].")
    parser.add_argument("mu_settings", type=str, help="Mean image regularisation settings. Example: [0.001,0.1,0].")
    parser.add_argument("maxit", type=int, help="Number of iterations. Example: 8.")
    parser.add_argument("result_name", type=str, help="Name of results files. Example: test.")
    parser.add_argument("result_dir", type=str, help="Name of result directory. Example: /tmp")
    parser.add_argument("batch_size", type=int, help="Batch-size (for local parallelisation). Example: 4.")

    results=parser.parse_args() if args is None else parser.parse_args(args)
    
    print results
    path, fil = os.path.split(__file__)
    template_file = os.path.join(path, "template.json")
    build_settings_file(template_file, ".test.json",
                      str(results.k),
                      results.vx,
                      results.v_settings,
                      results.a_settings,
                      results.mu_settings,
                      str(results.maxit),
                      results.result_name,
                      results.result_dir,
                      str(results.batch_size))
    run_app(results.filenames,'.test.json')

if  __name__ == "__main__":
    main()
