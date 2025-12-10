# """
# Integration with your existing evaluation pipeline
# Add this to your evaluation notebook (Notebook 05)
# """

# import numpy as np
# import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn.metrics import confusion_matrix

# # After you run cross-validation and have predictions
# # Assuming you store results in each fold

# def plot_confusion_matrices_from_fold(fold_results, fold_number):
#     """
#     Plot confusion matrices from fold results
    
#     Parameters:
#     -----------
#     fold_results : dict
#         Dictionary with keys: 'y_true', 'y_pred'
#     fold_number : int
#         Fold number for labeling
#     """
    
#     y_true = fold_results['y_true']
#     y_pred_exact = fold_results['y_pred']
    
#     # Generate extended predictions (±1 tolerance)
#     y_pred_extended = []
#     for true_val, pred_val in zip(y_true, y_pred_exact):
#         if abs(true_val - pred_val) <= 1:
#             y_pred_extended.append(true_val)
#         else:
#             y_pred_extended.append(pred_val)
#     y_pred_extended = np.array(y_pred_extended)
    
#     # Create confusion matrices
#     cm_exact = confusion_matrix(y_true, y_pred_exact, labels=[1,2,3,4,5,6,7])
#     cm_extended = confusion_matrix(y_true, y_pred_extended, labels=[1,2,3,4,5,6,7])
    
#     # Plot
#     fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
#     sns.heatmap(cm_exact, annot=True, fmt='d', cmap='Blues', 
#                 xticklabels=[1,2,3,4,5,6,7], yticklabels=[1,2,3,4,5,6,7],
#                 ax=axes[0])
#     axes[0].set_xlabel('Predicted FMS Level')
#     axes[0].set_ylabel('True FMS Level')
#     axes[0].set_title('Exact Label Accuracy')
    
#     sns.heatmap(cm_extended, annot=True, fmt='d', cmap='Blues',
#                 xticklabels=[1,2,3,4,5,6,7], yticklabels=[1,2,3,4,5,6,7],
#                 ax=axes[1])
#     axes[1].set_xlabel('Predicted FMS Level')
#     axes[1].set_ylabel('True FMS Level')
#     axes[1].set_title('Extended Label Accuracy')
    
#     fig.suptitle(f'Confusion Matrices for Fold {fold_number}', fontweight='bold')
#     plt.tight_layout()
    
#     # Save
#     plt.savefig(f'confusion_matrices_fold{fold_number}.png', dpi=300, bbox_inches='tight')
#     plt.show()
    
#     # Calculate accuracies
#     exact_acc = np.mean(y_true == y_pred_exact)
#     extended_acc = np.mean(y_true == y_pred_extended)
    
#     print(f"Fold {fold_number} - Exact: {exact_acc:.4f}, Extended: {extended_acc:.4f}")
    
#     return cm_exact, cm_extended


# # ==============================================================
# # EXAMPLE: Use with your cross-validation loop
# # ==============================================================

# # In your evaluation loop, collect predictions:
# all_fold_results = []

# for fold_idx, (train_idx, test_idx) in enumerate(kfold.split(X), 1):
#     # Your existing training code...
#     # After prediction:
    
#     fold_results = {
#         'y_true': y_test,
#         'y_pred': y_pred,
#         'fold': fold_idx
#     }
#     all_fold_results.append(fold_results)
    
#     # Plot confusion matrices for this fold
#     plot_confusion_matrices_from_fold(fold_results, fold_idx)


# # ==============================================================
# # OR: Load from saved predictions
# # ==============================================================

# # If you saved predictions during evaluation:
# import pickle

# with open('../models/evaluation_results.pkl', 'rb') as f:
#     eval_results = pickle.load(f)

# for fold_idx, fold_data in enumerate(eval_results['folds'], 1):
#     plot_confusion_matrices_from_fold(fold_data, fold_idx)
