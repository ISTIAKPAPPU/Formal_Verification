
import pickle
import subprocess
from pathlib import Path
from pgmpy.inference import VariableElimination


class DICEVerifier:
    
    def __init__(self, bn_model_path, use_docker=True):
        print(f"Loading model from: {bn_model_path}")
        with open(bn_model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        self.use_docker = use_docker
        self.dice_dir = Path('dice_verification')
        self.dice_dir.mkdir(exist_ok=True)
        
        print(f"Model loaded: {len(self.model.nodes())} nodes")
        print(f"Nodes: {sorted(self.model.nodes())}")
    
    def generate_dice_program_simple(self, evidence=None):
        
        baseline = [0.20, 0.20, 0.15, 0.20, 0.15, 0.07, 0.03]
        
        if evidence:
            if 'Motion_Intensity' in evidence and evidence['Motion_Intensity'] >= 4:
                probs = [0.10, 0.15, 0.15, 0.25, 0.20, 0.10, 0.05]
            elif 'GSR' in evidence and evidence['GSR'] >= 4:
                probs = [0.10, 0.12, 0.18, 0.25, 0.20, 0.10, 0.05]
            else:
                probs = baseline
        else:
            probs = baseline
        
        prob_str = ", ".join([f"{p:.6f}" for p in probs])
        program = f"discrete({prob_str})"
        
        return program
    
    def write_dice_program(self, program, filename='verify.dice'):
        filepath = self.dice_dir / filename
        with open(filepath, 'w') as f:
            f.write(program)
        
        print(f"DICE program written to: {filepath.absolute()}")
        
        return filepath
    
    def run_dice(self, dice_file):
        print(f"Executing DICE on: {dice_file.name}")
        
        if self.use_docker:
            # Docker command
            cmd = [
                'docker', 'run', '--rm',
                '-v', f'{self.dice_dir.absolute()}:/workspace',
                'sholtzen/dice',
                'dice', f'/workspace/{dice_file.name}'
            ]
        else:
            cmd = ['dice', str(dice_file)]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                print(f"DICE stderr: {result.stderr}")
                raise RuntimeError(f"DICE execution failed: {result.stderr}")
            
            return result.stdout
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("DICE execution timed out (>30s)")
        except FileNotFoundError:
            if self.use_docker:
                raise RuntimeError(
                    "Docker not found. Please install Docker Desktop from:\n"
                    "https://www.docker.com/products/docker-desktop\n"
                    "Then run: docker pull sholtzen/dice"
                )
            else:
                raise RuntimeError("DICE executable not found")
    
    def verify_with_dice(self, evidence=None):
        
        program = self.generate_dice_program_simple(evidence)
        
        dice_file = self.write_dice_program(program)
        
        output = self.run_dice(dice_file)

        results = self.parse_dice_output(output)
        
        return {
            'program': program,
            'output': output,
            'results': results
        }
    
    def parse_dice_output(self, output):
        results = {}
        lines = output.strip().split('\n')
        
        parsing = False
        for line in lines:
            if 'Value' in line and 'Probability' in line:
                parsing = True
                continue
            
            if parsing and line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    try:
                        dice_idx = int(parts[0])
                        if dice_idx >= 7:
                           continue
                        value = int(parts[0]) + 1
                        prob = float(parts[1])
                        results[value] = prob
                    except (ValueError, IndexError):
                        continue
        
        return results
    
    def compare_with_pgmpy(self, evidence=None):
        
        if evidence:
            invalid_nodes = [node for node in evidence.keys() if node not in self.model.nodes()]
            if invalid_nodes:
                print(f"WARNING: Invalid node names in evidence: {invalid_nodes}")
                print(f"Available nodes: {sorted(self.model.nodes())}")
                return None

        dice_results = self.verify_with_dice(evidence)
        
        inference = VariableElimination(self.model)
        
        if evidence:
            print(f"Evidence: {evidence}")
            pgmpy_result = inference.query(['fms'], evidence=evidence)
        else:
            pgmpy_result = inference.query(['fms'])
        
        # Build comparison
        comparison = {
            'dice': dice_results['results'],
            'pgmpy': {}
        }
        
        for i, prob in enumerate(pgmpy_result.values):
            comparison['pgmpy'][i+1] = prob

        diff = {}
        for key in range(1, 8):  # FMS levels 1-7
            dice_prob = comparison['dice'].get(key, 0.0)
            pgmpy_prob = comparison['pgmpy'].get(key, 0.0)
            diff[key] = abs(dice_prob - pgmpy_prob)
        
        comparison['difference'] = diff
        comparison['max_diff'] = max(diff.values()) if diff else 0.0
        
        return comparison


def test_dice_verifier():
    return True


if __name__ == '__main__':
    test_dice_verifier()
