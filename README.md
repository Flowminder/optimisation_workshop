[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Flowminder/optimisation_workshop/main?labpath=wdf_workshop.ipynb)

# optimisation_workshop

If you already have an existing [`conda` package manager](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed, then use it to install `mamba` into the base environment
```shell
conda install mamba -n base -c conda-forge
```
Alternatively, download and install [mambaforge](https://github.com/conda-forge/miniforge#mambaforge).

Install `wdf_workshop` conda environment from environment file `environment.yml`
```shell
mamba env create --name wdf_workshop -f environment.yml
```
Activate the `wdf_workshop` conda environment, then create a Python kernel and link it to jupyter
```shell
conda activate wdf_workshop
python -m ipykernel install --user --name="wdf_workshop"
```
Your python environment is now ready for launching Jupyter lab with the `wdf_workshop` kernel available for use
```shell
jupyter lab
```
