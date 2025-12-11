# Docker for DICE Verification

## Installation & Setup
```bash
# Check Docker version
docker --version

# Test Docker is working
docker run hello-world

# Pull DICE image
docker pull sholtzen/dice

# Verify DICE image is downloaded
docker images
```

## Docker Images Available
```bash
# List all images
docker images

# Expected output:
# REPOSITORY        TAG       IMAGE ID         SIZE
# hello-world       latest    f7931603f70e     20.3kB
# sholtzen/dice     latest    5aadf3edfa7a     5.06GB
```

## Running DICE with Docker

### Option 1: Through Python (RECOMMENDED)
```python
from dice_integration_FIXED import DICEVerifier

verifier = DICEVerifier('../models/bn_trained1.pkl', use_docker=True)
results = verifier.verify_with_dice(evidence=None)
```

### Option 2: Manual Docker Command (Manual Verification)
```bash
# Run DICE directly in Docker container
docker run --rm -v D:\Formal\Docker_Claude\cybersickness_bn_wu2025\notebooks\dice_verification:/workspace sholtzen/dice dice /workspace/verify.dice
```

### Option 3: Interactive Shell (For Manual Testing)
```bash
# Open bash shell inside DICE container
docker run -it --rm -v "%cd%":/workspace sholtzen/dice bash

# Inside container:
cd /workspace
dice verify.dice
exit
```

## Useful Docker Troubleshooting
```bash
# Show all running containers
docker ps

# Show all containers (including stopped)
docker ps -a

# Remove an image
docker rmi sholtzen/dice

# Re-download DICE image
docker pull sholtzen/dice

# Check Docker daemon status
docker info

# View Docker logs
docker logs <container-id>
```

## Current Setup
```
✅ Docker version: 28.5.2
✅ DICE image: sholtzen/dice (5.06GB)
✅ Status: Ready to use
✅ Usage: Through Python with use_docker=True
```

## Quick Commands

### Verify Everything Works
```bash
docker --version
docker images
docker run sholtzen/dice dice --help
```

### Check DICE Image
```bash
docker images | grep sholtzen/dice
```

### Remove and Reinstall DICE (if needed)
```bash
docker rmi sholtzen/dice
docker pull sholtzen/dice
```

## Python Code (What Uses Docker Behind the Scenes)
```python

from dice_integration_FIXED import DICEVerifier

verifier = DICEVerifier('../models/bn_trained_final.pkl', use_docker=True)

# Test 1: Baseline
results = verifier.verify_with_dice(evidence=None)

# Test 2: With Evidence
comparison = verifier.compare_with_pgmpy({'Motion_Intensity': 4, 'GSR': 5})

# Test 3: Properties
verify_key_properties(model)
```

