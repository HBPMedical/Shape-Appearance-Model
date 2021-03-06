# Boutiques based fork

This fork of the original Shape Appearance Model provides additional capabilities to run the software with a boutiques descriptor through docker.  For information on how to run this, looking the boutiques directory for hte README

# Combined Shape & Appearance Modelling of 3D volumes

The general idea is to take a bunch of 2D or 3D images and factorise them in a way that combines both shape and appearance.  Code is written in MATLAB, and relies on functions from the [SPM12](http://www.fil.ion.ucl.ac.uk/spm/software/spm12/) software.

For those with the MATLAB Compiler, the Compilation.m script allows standalone versions of the functions to be generated.  Running these will require installation of the MATLAB runtime libraries (see the readme.txt file produced by the compiler).  Once these are installed, the appropriate library search path (LD_LIBRARY_PATH) will need to be set up so that they can be found.  Two compiled functions are generated.

## runPG
This function essentially trains the combined PGA/PCA model, estimating a dictionary of basis functions that encode both shape and appearance.

    Usage: runPG filenames.jsn settings.jsn
     
    Images must first be imported using SPM12's Segment tool, giving a series of rc1*.nii and rc2*.nii files.
    The filenames.jsn is a JSON file with the following general structure, where SCANXX is some filename:
    [["rc1SCAN01.nii","rc2SCAN01.nii"],
     ["rc1SCAN02.nii","rc2SCAN02.nii"],
     ["rc1SCAN03.nii","rc2SCAN03.nii"],
            :                :         
     ["rc1SCANXX.nii","rc2SCANXX.nii"]]
     
    The settings.jsn file contains various settings, which are of the following form:
    {"K":64,                                    % Number of shape and appearance components
     "vx":[1.5 1.5 1.5],                        % Voxel sizes (mm - matches those of "imported" images)
     "v_settings":[1e-05,0.01,0.2,0.025,0.05],  % Registration regularisation settings.
     "a_settings":[0.01,1,0],                   % Appearance regularisation settings.
     "mu_settings":[0.001,0.1,0],               % Mean image regularisation settings.
     "maxit":8,                                 % Number of iterations.
     "result_name":"test",                      % Name of results files.
     "result_dir":"/tmp/",                      % Name of result directory.
     "batchsize":4}                             % Batch-size (for local parallelisation).
     
    If no settings.jsn file is provided, or if some settings are not specified,
    then default values (shown in the example above) are assumed.
     
    Depending on the amount of data, execution can take a very long time.
    Outputs are saved at each iteration in the specified result_dir.
     
    The latent variables of interest may be obtained via MATLAB:
        load(fullfile(settings.result_dir,['train' settings.result_name '.mat']))
        Z = cat(2,dat.z);
    


## runPGfit
This function uses a pre-trained combined PGA/PCA model, and computes latent variables for new images.

    Usage: runPGfit settings.jsn
     
    Input images must first be imported using SPM12's Segment tool, giving a series of rc1*.nii and rc2*.nii files.
    The settings.jsn is a JSON file with the following general structure:
    {"train":"trainXXX.mat",                     % Name of mat file generated by training.
     "output":"output.jsn",                      % Name of output file containing estimated latent variables.
     "input":[["rc1SCAN01.nii","rc2SCAN01.nii"],
              ["rc1SCAN02.nii","rc2SCAN02.nii"],
              ["rc1SCAN03.nii","rc2SCAN03.nii"],
                      :                :        
              ["rc1SCANXX.nii","rc2SCANXX.nii"]]}
    

## Acknowledgements
This work is funded as part of SP8 of the Human Brain Project (SGA1).

