# Boutiques package

This folder contains the files used to creates a [Boutiques](http://github.com/boutiques/boutiques) package for the pipeline.

* Dockerfile: file used to build a Docker container for the pipeline.
** Requires that the pipeline is compiled with `mcc`. SPM12 needs to be installed and compiled to do this.  To compile the runPG, I used the Compilation.m script modified to place the results in the this directory.  Command-line compilation resulted in nanmax not working.  This has been tested on matlab 2017b and run with the same Matlab runtime environment.
* runPG.json: the Boutiques descriptor, used to integrate the pipeline in platforms supporting Boutiques, such as [CBRAIN](http://github.com/aces/cbrain).
* create_settings.py: a script that creates `settings.json` from parameters passed on the command line and runs the matlab code.  There will be a file created called out.dat that holds the stdout and stderr for the run so that you can see if there are any errors.
* template.json: template JSON file for `settings.json`, used by `create_settings.py`.

A corresponding Docker Image under shots47s/shape-appear is available that comes ready to run the software with boutiques.

To execute the pipeline:

* Install boutiques from pip or from github (https://github.com/boutiques/boutiques)
* From Matlab, compile the runPG code (can provide explicit instructions if needed, but the Compilation.m script above is pretty self explanitory, just make sure to addpath to your SPM12 install directory.
* Place the .nii files in the directory boutiques/files, then you will need to create the filename.json input file.  An example is provided for a collection files.
* Create the input.json, which as all of the command line flags for the run.  You can start from the example in the boutiques directory and alter it to your needs.
* Then from boutiques directory, run bosh exec -x launch cbrain-plugins-runpg/cbrain_task_descriptors/runPG.json input.json and the task should begin.  If it fails, check the file out.dat in your direcotry for further information.