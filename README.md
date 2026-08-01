# stedmund_summer_codecamp_2026
All material for the summer codecamp at St Edmund College, Cambridge

## Contact
Cheng-Yu Huang "Kou" (cyh37@cam.ac.uk)

## Pre-requirement of the workshop

Please prepare the following before the workshop:

- Please install [Miniconda](https://www.anaconda.com/download/success#miniconda) on your laptop. We will use miniconda to create an environment for coding (i.e. venv)

- Follow the **Creating a Python Environment for the workshop** workflow below for the setup.

- Please install [Github desktop](https://desktop.github.com/download/) on your laptop. This will help with collaborative coding

- install [Visual Studio Code](https://code.visualstudio.com/download). We will use this as the coding interface (IDE)

## Creating a Python Environment for the workshop

1. Open Anaconda Prompt. 
    - if you are using a **Windows OS machine**, look for **anaconda prompt (miniconda)** in **Start**
    - if you are using a **Mac OS machine**, look for **terminal**.


2. With the Anaconda prompt, create a virtual environment with the name “sted-workshop-venv”

    ```powershell
    conda create --name sted-workshop-venv python=3.14
    ```

3. Then activate the environment

    ```powershell
    conda activate sted-workshop-venv
    ```
    You should notice that the start of the command line is now `(sted-workshop-venv)`
    
4. Install all the basic python packages with

    ```powershell
    conda install numpy matplotlib scipy scikit-image ipywidgets jupyter jupyterlab pandas scikit-learn seaborn
    ```

5. Extra packages to install:
    Napari:
    ```
    python -m pip install "napari[all]"
    ```
    Dimension Reduction
    ```
    conda install scikit-learn seaborn umap-learn 
    ```
    and
    ```
    conda install -c conda-forge hdbscan
    ```

P.S. other useful conda command:
`conda env list` to list all available environment

## Other resources
- Other conda command: https://docs.conda.io/projects/conda/en/4.6.0/user-guide/tasks/manage-environments.html

## Project teams:

* ...Coming!