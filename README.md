# PFAS PBK model

This repository contains the model code of...

# Model implementation

The model implementation files can be found in the model folder. The file [PBK_PFAS.ant](model/PBK_PFAS.ant) contains the Antimony implementation. The file [PBK_PFAS.csv](model/PBK_PFAS.csv) contains the unit specifications and the model element annotations according the FAIR PBK standard, using the harmonized terminology of the [PBPKO ontology](https://github.com/InSilicoVida-Research-Lab/pbpko).

# Running the model 

The Jupyter notebook [test_dosing.ipynb](notebooks/test_dosing.ipynb) demonstrates how this model can be used in simulations. To run this notebook, you need Python with Jupyter Notebook and the python packages listed in the [requirements](requirements.txt) file.

Install the required python packages using the command:

```
pip install -r requirements.txt
```

### Compile models

Converts the Antimony model implementations to SBML and annotates the models:

```
python ./scripts/compile_models.py
```

### Run simulations

Run simulation scenarios:

```
python ./scripts/run_simulations.py
```

### Create model docs

Create model documentation pages:

```
python ./scripts/create_model_docs.py
```
