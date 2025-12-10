# Probabilistic Verification of Cybersickness in Virtual Reality

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Docker](https://img.shields.io/badge/Docker-Required-blue.svg)
![Status](https://img.shields.io/badge/Status-Complete-success.svg)

> **Formal Verification Course Project**
> A probabilistic model checking approach to verify cybersickness prediction in VR environments using Bayesian Networks and DICE verification.

---

## 📋 Overview

This project implements a **Bayesian Network-based probabilistic model** to predict and formally verify cybersickness in Virtual Reality environments. The system combines machine learning with formal verification techniques to ensure reliable predictions about user comfort levels in VR.

**Key Components:**
- Bayesian Network training on VR cybersickness data
- Probabilistic property verification using DICE
- Statistical evaluation and validation
- Docker-based verification environment

---

## 🎯 Project Goal

To develop and formally verify a probabilistic model that predicts cybersickness severity based on physiological and environmental factors in VR settings, ensuring the model meets specified safety and reliability properties.

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Modeling** | Bayesian Networks (pgmpy) |
| **Verification** | DICE Probabilistic Verifier |
| **Environment** | Docker, Conda |
| **Language** | Python 3.8+ |
| **Notebooks** | Jupyter |
| **Key Libraries** | pandas, numpy, scikit-learn, matplotlib |

---

## 📁 Project Structure

```
cybersickness_bn_*/
│
├── config/                          # Configuration files
│   ├── bn_config.yaml              # Bayesian Network parameters
│   ├── discretization_config.yaml  # Data discretization settings
│   ├── features_config.json        # Feature selection configuration
│   ├── environment.yml             # Conda environment
│   └── Docker_Commands.md          # Docker setup guide
│
├── data/
│   ├── enhanced/                   # Raw and enhanced datasets
│   ├── processed/                  # Discretized and selected features
│   └── results/                    # BN structures, metrics, visualizations
│
├── models/
│   └── bn_trained_final.pkl        # Trained Bayesian Network model
│
└── notebooks/                       # Step-by-step workflow
    ├── 01_feature_selection.ipynb
    ├── 02_discretization.ipynb
    ├── 03_bn_training.ipynb
    ├── 04_evaluation.ipynb
    ├── 05_dice_verification.ipynb
    ├── dice_integration.py          # DICE-Python integration
    └── property_verification.py     # Property specifications
```

---

## 🔄 Workflow Pipeline

```
[Raw Data]
    ↓
[1. Feature Selection] → Select relevant VR/physiological features
    ↓
[2. Discretization] → Convert continuous values to discrete states
    ↓
[3. BN Training] → Learn Bayesian Network structure & parameters
    ↓
[4. Evaluation] → Validate model accuracy and performance
    ↓
[5. DICE Verification] → Formally verify probabilistic properties
    ↓
[Verified Model]
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8 or higher
- Docker (for DICE verification)
- Conda (recommended)

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Formal_Verification
   ```

2. **Create conda environment**
   ```bash
   cd cybersickness_bn_V1/config
   conda env create -f environment.yml
   conda activate cybersickness-env
   ```

3. **Install Docker and DICE**
   ```bash
   # Verify Docker installation
   docker --version

   # Pull DICE image
   docker pull sholtzen/dice

   # Verify installation
   docker images | grep sholtzen/dice
   ```

---

## 📊 Usage

### Running the Complete Pipeline

Execute notebooks in sequence:

```bash
cd cybersickness_bn_V1/notebooks
jupyter notebook
```

**Execution Order:**
1. `01_feature_selection.ipynb` - Select relevant features from dataset
2. `02_discretization.ipynb` - Discretize continuous variables
3. `03_bn_training.ipynb` - Train Bayesian Network
4. `04_evaluation.ipynb` - Evaluate model performance
5. `05_dice_verification.ipynb` - Verify probabilistic properties with DICE

### Running DICE Verification

```python
from dice_integration import DICEVerifier

# Load trained model and verify
verifier = DICEVerifier('../models/bn_trained_final.pkl', use_docker=True)
results = verifier.verify_with_dice(evidence=None)
```

---

## 🔍 Key Features

- **Bayesian Network Modeling**: Captures probabilistic dependencies between VR factors and cybersickness
- **Formal Verification**: Uses DICE to prove properties about prediction reliability
- **Hierarchical Structure**: Models complex relationships between physiological signals and symptoms
- **Docker Integration**: Seamless verification through containerized DICE environment
- **Comprehensive Evaluation**: Confusion matrices, accuracy metrics, and structure visualization

---

## 📈 Results

The trained model includes:
- **Bayesian Network structure** with learned dependencies
- **Evaluation metrics**
- **Verified properties** ensuring model reliability bounds
- **Visualizations** of network structure and performance

Results are stored in `data/results/` directory.

---

## 🐳 Docker Reference

Quick commands for DICE verification:

```bash
# Check DICE installation
docker images | grep sholtzen/dice

# Run verification (handled automatically by Python integration)
docker run --rm -v /path/to/workspace:/workspace sholtzen/dice dice /workspace/verify.dice
```

For detailed Docker commands, see [config/Docker_Commands.md](cybersickness_bn_V1/config/Docker_Commands.md)

---

## 📝 Configuration Files

| File | Purpose |
|------|---------|
| `bn_config.yaml` | Bayesian Network training parameters |
| `discretization_config.yaml` | Binning strategies for continuous variables |
| `features_config.json` | Feature selection criteria |
| `environment.yml` | Python dependencies |

---
<!-- 
## 🎓 Course Information

**Course**: Formal Verification
**Topic**: Probabilistic Model Checking
**Focus**: Verification of machine learning models in safety-critical applications

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- **DICE**: Probabilistic programming language and verifier
- **pgmpy**: Python library for Bayesian Networks
- **VR Cybersickness Research**: Dataset and domain knowledge contributors -->
