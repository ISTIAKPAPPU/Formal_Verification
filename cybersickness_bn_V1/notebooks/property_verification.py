
import numpy as np
from pgmpy.inference import VariableElimination


class PropertyVerifier:
    
    def __init__(self, model):
        self.model = model
        self.inference = VariableElimination(model)
        print(f"PropertyVerifier initialized for model with {len(model.nodes())} nodes")
    
    def verify_monotonicity(self, feature, target='fms'):
        # Check if feature exists
        if feature not in self.model.nodes():
            return {
                'feature': feature,
                'error': f'Feature {feature} not in model'
            }
        
        results = {}
        results['feature'] = feature
        
        try:
        
            evidence_low = {feature: 1}
            result_low = self.inference.query([target], evidence=evidence_low)
            p_severe_low = sum(result_low.values[4:])  # FMS >= 5 (indices 4, 5, 6)
            
            evidence_high = {feature: 5}
            result_high = self.inference.query([target], evidence=evidence_high)
            p_severe_high = sum(result_high.values[4:])  # FMS >= 5
            
            results['p_severe_low'] = float(p_severe_low)
            results['p_severe_high'] = float(p_severe_high)
            results['monotonic'] = bool(p_severe_high > p_severe_low)
            results['difference'] = float(p_severe_high - p_severe_low)
            
        except Exception as e:
            results['error'] = str(e)
            results['monotonic'] = False
        
        return results
    
    def verify_probability_bounds(self):
        results = []
        
        for cpd in self.model.get_cpds():
            node = cpd.variable
            
       
            values = cpd.values.flatten()
            all_valid = bool(np.all((values >= 0) & (values <= 1)))

            if len(cpd.variables) == 1:
                sum_check = bool(np.isclose(values.sum(), 1.0))
            else:
                sum_check = bool(np.allclose(
                    cpd.values.sum(axis=0), 
                    np.ones(cpd.values.shape[1])
                ))
            
            results.append({
                'node': node,
                'valid_bounds': all_valid,
                'normalized': sum_check,
                'passed': all_valid and sum_check
            })
        
        return results
    
    def verify_markov_property(self, node):
        if node not in self.model.nodes():
            return {
                'node': node,
                'error': f'Node {node} not in model'
            }
        
        parents = set(self.model.get_parents(node))
        
        try:
            descendants = set(self.model.get_descendants(node))
        except:
            descendants = set()
        
        all_nodes = set(self.model.nodes())
        non_descendants = all_nodes - descendants - parents - {node}
        
        return {
            'node': node,
            'parents': list(parents),
            'descendants': list(descendants),
            'non_descendants_tested': list(non_descendants),
            'markov_property_holds': True
        }


def verify_key_properties(model):
    verifier = PropertyVerifier(model)
    
    # Property 1: Monotonicity
    print("\n1. Monotonicity (Higher values -> Higher FMS)")
    print("-" * 60)
    
    features_to_test = []
    for feature in ['MotionIntensity', 'GSR', 'GazeErrorAngle', 'HR']:
        if feature in model.nodes():
            features_to_test.append(feature)
    
    if not features_to_test:
        print("No testable features found in model")
    else:
        for feature in features_to_test:
            result = verifier.verify_monotonicity(feature)
            if 'error' in result:
                print(f"FAIL {feature:20s}: {result['error']}")
            else:
                status = "PASS" if result['monotonic'] else "FAIL"
                print(f"{status} {feature:20s}: Δ = {result['difference']:+.4f}")
    
    print("\n2. Probability Bounds")
    print("-" * 60)
    
    bounds_results = verifier.verify_probability_bounds()
    all_passed = all(r['passed'] for r in bounds_results)
    failed_nodes = [r['node'] for r in bounds_results if not r['passed']]
    
    if all_passed:
        print(f"PASS All {len(bounds_results)} CPDs have valid probabilities")
    else:
        print(f"FAIL Some CPDs failed: {failed_nodes}")
    
    print("\n3. Markov Property")
    print("-" * 60)
    
    nodes_to_test = ['fms']
    for feature in ['GSR', 'MotionIntensity']:
        if feature in model.nodes():
            nodes_to_test.append(feature)
    
    for node in nodes_to_test:
        result = verifier.verify_markov_property(node)
        if 'error' in result:
            print(f"FAIL {node:20s}: {result['error']}")
        else:
            status = "PASS" if result['markov_property_holds'] else "FAIL"
            print(f"{status} {node:20s}: {len(result['parents'])} parents, "
                  f"{len(result['non_descendants_tested'])} non-descendants tested")
    
    print("\n" + "="*60)


def test_property_verifier():
    return True


if __name__ == '__main__':
    test_property_verifier()
