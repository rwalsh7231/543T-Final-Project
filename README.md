# Disease Spread Optimization Model (543T Final Project)

Github Link: https://github.com/rwalsh7231/543T-Final-Project

This repository contains Python code for simulating and optimizing interventions in a disease outbreak using an extended SIRD model. The project explores the trade-offs between minimizing deaths and mitigating the social and economic costs of interventions such as quarantine and vaccination.

## Overview

This project extends the classical Susceptible, Infected, Recovered, Dead (SIRD) model by:
- Modeling quarantine compliance and duration
- Supporting dynamic vaccination rollout strategies
- Simulating cross-infection between multiple populations
- Defining cost functions to quantify economic and social burdens
- Applying numerical optimization to find optimal intervention policies

All experiments and results correspond to those documented in our final project report.

## Repository Contents
- `DiseaseAnalysis.py` - Core simulation engine with the `Population` class, SIRD logic, and vaccination, quarantine, and cross-infection methods.
- `Disease Analysis.ipynb` - Notebook containing simulations, plots, and optimization routines used to generate the report results.
- `report.pdf` - The final report PDF.

## Requirements

We recommend using Pythin 3.8+ and a virtual environment.

## Install dependencies:
```bash
pip install matplotlib numpy scipy
```

How to use code: Open and run DiseaseAnalysis.ipynb. This file contains all of our main code and experiments done.
To see different results, adjust population statistics that are defined throughout the notebook.
Alternatively, you can uncomment the code in DiseaseAnalysis.py and run it to see our initial testing with the SIRD algorithm.