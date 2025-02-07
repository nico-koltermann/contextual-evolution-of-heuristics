# CEoH 

[![Build](https://github.com/nico-koltermann/contextual-evolution-of-heuristics/actions/workflows/build.yaml/badge.svg)](https://github.com/nico-koltermann/contextual-evolution-of-heuristics/actions/workflows/build.yaml)
[![Docker](https://github.com/nico-koltermann/contextual-evolution-of-heuristics/actions/workflows/docker.yaml/badge.svg)](https://github.com/nico-koltermann/contextual-evolution-of-heuristics/actions/workflows/docker.yaml)

Optimal block stacking warehouse reshuffling (premarshalling) for layouts with multiple bays.

## Adaptation of EoH

The base Idea of EoH is adapdet by the repository: 
[EoH-Repo](https://github.com/FeiLiu36/EoH) by Fei Liu (fliu36-c@my.cityu.edu.hk) et. al. 
licensed under the MIT License. The original code has been modified. 
The original license is retained in the respective files.

## Multibay reshuffeling 

Previous work: 
- [Sorting Multibay Block Stacking Storage Systems with Multiple Robots](https://doi.org/10.1007/978-3-031-71993-6_3)
- [Sorting multibay block stacking storage systems](    
https://doi.org/10.48550/arXiv.2405.04847)

### **The Unit-Load Pre-Marshalling Problem (UPMP)**  

The **UPMP** focuses on reorganizing unit loads within a **block-stacking warehouse** to eliminate retrieval blockages. A block-stacking warehouse consists of a **3D grid** of storage locations (columns, rows, and tiers) where unit loads are stacked without additional infrastructure.

![Bay Layout](docs/images/bay.png)

During **pre-marshalling**, no new unit loads enter or leave the warehouse. A unit load is **blocking** if it obstructs access to a higher-priority load, where priorities are typically assigned based on retrieval urgency.

This study particularly focuses on a **simplified UPMP scenario** with:
- **A single access direction**
This makes the problem especially challenging due to the **restricted movement possibilities** within the layout.

---

## **Running the Project**  

### **RUN with docker**

We prepared a docker for automatic configuration for GPT-4 Model:

1. Make sure to have a ```.env```file exists with your OPEN_API key

```bash
export OPENAI_API_KEY=sk-123456 # Replace with your actual key
```

2. Create the docker container ```docker build -t ceoh_runner .```

3. Run the docker script ```./ceoh_run_docker```

### **Steps to Run locally**  

0. Install required dependencies (environment.yml with conda)

1. **Select the problem to solve**:  
   - If you want to create a new problem, refer to:  
     ```src/eoh/problems/optimization```
   - If you are working on **multibay reshuffling**, as presented in this work, create an experiment file as described [here](./eoh_experiment/README.md).  

2. **Create a `.env` file** with necessary configurations (see [CEoH Config](#ceoh-config)).

3. **Run the project** using:  
   ```bash
   ./ceoh_run_local.sh
   ```

> The project **automatically verifies the connection** before execution.

---

## **CEoH Configuration**  

To configure the project, create a `.env` file inside the root folder with the required environment variables. Below is an example configuration:

```bash
# Your API Keys
export OPENAI_API_KEY=sk-123456 # Replace with your actual key
export OPENROUTER_API_KEY=sk-123456 # Replace with your actual key
export DEEPSEEK_API_KEY=sk-123456 # Replace with your actual key

# Problem selection (Choose from: 'tsp_construct', 'bp_online', 'multibay_reshuffle', 'cap_set')
export EOH_PROBLEM="<problem>"

# Model Selection
# "Local" models: ['gemma2:27b', 'Qwen2.5-Coder:32b']
# "Remote" models: ['gpt-4o', 'DeepSeekV3:685b', ]
export MODEL_NAME="<model>"
```

If you want to run the project local and not inside the docker, you also must add the paths: 

```bash
# Path configurations
export INSTANCES_PATH="<your path>" # The path to the instances, extracted from the ./instances folder
export OUTPUT_PATH="<your path>" # Where to save the output files
export BASE_PATH="<yout path>" # Base path of your repository
```

---

## **Project Structure**  

### **Working Directory**  
All work should be done inside the `src` folder.

### **Running Experiments**  
To execute the project, run:  
```bash
python run_eoh_experiments.py
```
Alternatively, for running executables at the root level, use the following import statement to access all source files from root:

```python
import sys
sys.path.insert(0, 'src')
```

### **Warehouse Configuration for Multibay Reshuffling**  
All relevant warehouse configurations for the **multibay reshuffling problem** are defined in the `bay` folder.

### **EoH Adaptation**  
The modified EoH implementation is located in the `src/eoh` folder.

---

## **Creating a New Experiment**  
For a detailed guide on setting up a new experiment, please refer to:  
[Experiment Setup](./eoh_experiment/README.md)  
