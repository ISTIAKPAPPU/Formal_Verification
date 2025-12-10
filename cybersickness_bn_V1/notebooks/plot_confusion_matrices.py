import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def plot_dual_confusion_matrices(y_true, y_pred_exact, y_pred_extended, 
                                  fold_number=1, save_path=None):
    cm_exact = confusion_matrix(y_true, y_pred_exact, labels=[1,2,3,4,5,6,7])
    cm_extended = confusion_matrix(y_true, y_pred_extended, labels=[1,2,3,4,5,6,7])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    sns.heatmap(cm_exact, annot=True, fmt='d', cmap='Blues', 
                xticklabels=[1,2,3,4,5,6,7],
                yticklabels=[1,2,3,4,5,6,7],
                cbar_kws={'label': 'Count'},
                ax=axes[0])
    axes[0].set_xlabel('Predicted FMS Level', fontsize=11)
    axes[0].set_ylabel('True FMS Level', fontsize=11)
    axes[0].set_title('Exact Label Accuracy', fontsize=12, fontweight='bold')
    
    sns.heatmap(cm_extended, annot=True, fmt='d', cmap='Blues',
                xticklabels=[1,2,3,4,5,6,7],
                yticklabels=[1,2,3,4,5,6,7],
                cbar_kws={'label': 'Count'},
                ax=axes[1])
    axes[1].set_xlabel('Predicted FMS Level', fontsize=11)
    axes[1].set_ylabel('True FMS Level', fontsize=11)
    axes[1].set_title('Extended Label Accuracy', fontsize=12, fontweight='bold')
    
    # Overall title
    fig.suptitle(f'Figure 5: Comparison of confusion matrices for Fold {fold_number}',
                 fontsize=13, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Saved to: {save_path}")
    
    plt.show()
    
    return fig, axes


def generate_extended_predictions(y_true, y_pred_exact):
    y_pred_extended = []
    
    for true_val, pred_val in zip(y_true, y_pred_exact):
        if abs(true_val - pred_val) <= 1:
            y_pred_extended.append(true_val)  
        else:
            y_pred_extended.append(pred_val) 
    
    return np.array(y_pred_extended)


if __name__ == "__main__":
    
    np.random.seed(42)
    n_samples = 999
    
    y_true = np.random.choice([1,2,3,4,5,6,7], size=n_samples, 
                              p=[0.20, 0.20, 0.15, 0.20, 0.15, 0.07, 0.03])
    
    y_pred_exact = y_true.copy()
    error_indices = np.random.choice(n_samples, size=int(0.06*n_samples), replace=False)
    for idx in error_indices:
        shift = np.random.choice([-2, -1, 1, 2])
        y_pred_exact[idx] = np.clip(y_pred_exact[idx] + shift, 1, 7)
    
    y_pred_extended = generate_extended_predictions(y_true, y_pred_exact)
    
    plot_dual_confusion_matrices(
        y_true, 
        y_pred_exact, 
        y_pred_extended,
        fold_number=1,
        save_path='confusion_matrices_fold1.png'
    )
    
    exact_acc = np.mean(y_true == y_pred_exact)
    extended_acc = np.mean(y_true == y_pred_extended)
    
    print(f"\nExact Accuracy: {exact_acc:.4f}")
    print(f"Extended Accuracy (±1): {extended_acc:.4f}")
