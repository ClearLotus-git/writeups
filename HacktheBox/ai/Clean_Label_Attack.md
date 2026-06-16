# Clean Label Attack

Implement a clean label attack to misclassify Class 2 Index 334 as Class 1, train a model using the provided code, and 
submit the trained model to the docker instance using the last cell in the notebook. 
Submit the flag you receive for a valid attack as the answer to this question.

___

<img width="1913" height="657" alt="image" src="https://github.com/user-attachments/assets/67980229-5233-45fd-b01b-ce4236dbfad8" />

Navigate to the bottom and install `numpy`, `scikit-learn`, and `matplotlib` Python libraries:

<img width="1329" height="418" alt="image" src="https://github.com/user-attachments/assets/e6c5109e-4dc2-48cd-8c86-16f91ac4650b" />

 Adjust the value in the EPSILON_CROSS variable from 0.4 to 0.25:

<img width="1323" height="582" alt="image" src="https://github.com/user-attachments/assets/7ea3d0d8-05c9-41c0-ba3e-ab298fb5c275" />

Perform the Clean Label Attack:

```
    # Implement the clean label attack logic here
    if target_class == perturb_class:
        raise ValueError("Target class and perturbing class cannot be the same.")

    # Create Copies to avoid modifying original data
    X_train_poisoned = X_train_orig.copy()
    y_train_poisoned = y_train_orig.copy() # Labels remain unchanged.

    # Train a temporary baseline model (OvR Logistic Regression)
    # We need this to find the decision boundary between target_class and perturb_class
    try:
        temp_base_estimator = LogisticRegression(
            random_state=seed, C=1.0, solver="liblinear"
        )
        temp_model = OneVsRestClassifier(temp_base_estimator)
        temp_model.fit(X_train_orig, y_train_orig)
        print("Temporary baseline model trained.")

        if not (
            hasattr(temp_model, "estimators_")
            and len(temp_model.estimators_) > max(target_class, perturb_class)
        ):
            raise RuntimeError(
                "Temporary model did not produce expected number of estimators."
            )

        w_target = temp_model.estimators_[target_class].coef_[0]
        b_target = temp_model.estimators_[target_class].intercept_[0]
        w_perturb = temp_model.estimators_[perturb_class].coef_[0]
        b_perturb = temp_model.estimators_[perturb_class].intercept_[0]
        print(
            f"Extracted weights/intercepts for Class {target_class} and Class {perturb_class}."
        )

    except Exception as e:
        print(f"Error: Failed to train or extract params from temporary model: {e}")
        raise RuntimeError("Failed to initialize temporary model for attack.") from e

    # Identify neighbors of perturb_class closest to the target point
    X_target_point = X_train_orig[target_idx]
    perturb_class_indices_train = np.where(y_train_orig == perturb_class)[0]

    if len(perturb_class_indices_train) == 0:
        raise ValueError(
            f"No points found for perturb_class ({perturb_class}). Cannot find neighbors."
        )
    if n_neighbors > len(perturb_class_indices_train):
        print(
            f"Warning: Requested {n_neighbors} neighbors, but only {len(perturb_class_indices_train)} points of Class {perturb_class} exist. Using all available."
        )
        n_neighbors = len(perturb_class_indices_train)
    if n_neighbors == 0:
        raise ValueError("n_neighbors is zero, cannot proceed with perturbation.")

    X_perturb_class_train = X_train_orig[perturb_class_indices_train]
    print(f"Finding {n_neighbors} nearest neighbors from Class {perturb_class}...")
    nn_finder = NearestNeighbors(n_neighbors=n_neighbors, algorithm="auto")
    nn_finder.fit(X_perturb_class_train)
    distances, indices_relative = nn_finder.kneighbors(X_target_point.reshape(1, -1))

    # Map relative indices back to original X_train indices
    neighbor_indices_absolute = perturb_class_indices_train[indices_relative.flatten()]
    X_neighbors_original = X_train_orig[neighbor_indices_absolute]
    print(f"Found neighbors at indices: {neighbor_indices_absolute}")

    # Calculate the perturbation vector
    #    Push direction is opposite to the normal vector of the boundary (w_target - w_perturb)
    w_diff_boundary = w_target - w_perturb
    b_diff_boundary = (
        b_target - b_perturb
    )  # Not needed for direction, but good for checks

    push_direction = w_diff_boundary
    norm_push_direction = np.linalg.norm(push_direction)

    if norm_push_direction < 1e-9:
        raise ValueError(
            "Boundary vector norm is close to zero. Cannot determine reliable push direction."
        )

    unit_push_direction = push_direction / norm_push_direction
    perturbation_vector = epsilon_cross * unit_push_direction
    print(f"Calculated perturbation vector (delta): {perturbation_vector}")

    # Apply perturbations to the neighbors' features in the copied dataset
    perturbed_indices_list = []
    print("Applying perturbations...")
    for i, neighbor_idx in enumerate(neighbor_indices_absolute):
        X_neighbor_orig = X_neighbors_original[i]
        X_perturbed_neighbor = X_neighbor_orig + perturbation_vector

        # Update the feature vector in the poisoned dataset
        X_train_poisoned[neighbor_idx] = X_perturbed_neighbor
        # DO NOT change y_train_poisoned[neighbor_idx]

        perturbed_indices_list.append(neighbor_idx)

        # Check if perturbation crossed the temporary baseline boundary
        f_boundary_orig = X_neighbor_orig @ w_diff_boundary + b_diff_boundary
        f_boundary_pert = X_perturbed_neighbor @ w_diff_boundary + b_diff_boundary
        # Expect f_boundary_orig < 0 (perturb class side), f_boundary_pert > 0 (target class side)
        print(
            f"  Neighbor {neighbor_idx}: Orig f={f_boundary_orig:.4f}, Perturbed f={f_boundary_pert:.4f}"
        )
        if f_boundary_pert <= 0:
            print(
                f"     Warning: Perturbed point {neighbor_idx} might not have crossed the boundary (f<=0)."
            )

    print(f"Applied perturbations to {len(perturbed_indices_list)} neighbors.")
    perturbed_indices = np.array(perturbed_indices_list)  # Return as numpy array

    # Final check: ensure target point wasn't accidentally perturbed
    if target_idx in perturbed_indices:
        print(
            f"CRITICAL Error: Target index {target_idx} was selected as a neighbor and perturbed! Check logic."
        )
        # Depending on desired strictness, could raise an error here

    print("--- Clean Label Attack Implementation Finished")
    
    return X_train_poisoned, y_train_poisoned, perturbed_indices
```

Modify the evaluator base url with the docker ip and port : 

<img width="1497" height="438" alt="image" src="https://github.com/user-attachments/assets/45276c45-ab93-4ebd-be77-ad538f04cfc4" />


Run it and obtain the flag:

<img width="1335" height="300" alt="image" src="https://github.com/user-attachments/assets/ada44c48-0c8e-4c77-a735-188c8ed3f63d" />
<img width="1041" height="54" alt="image" src="https://github.com/user-attachments/assets/ea939c9a-307f-4654-9395-7e8c316e206d" />
<img width="1563" height="602" alt="image" src="https://github.com/user-attachments/assets/7b882d71-7440-423b-9f05-3c16316f40b9" />
<img width="1521" height="593" alt="image" src="https://github.com/user-attachments/assets/42d19f14-692e-423a-9a27-1fbfc4783df1" />
<img width="1520" height="328" alt="image" src="https://github.com/user-attachments/assets/e9be3efa-05e2-4c77-b79c-ce241aaef90b" />
<img width="1504" height="603" alt="image" src="https://github.com/user-attachments/assets/d6fca9da-6f52-44f2-9b96-04dd233aae6f" />
<img width="1208" height="120" alt="image" src="https://github.com/user-attachments/assets/db5e78a2-4b5b-402d-bcc2-f11bee527edd" />

<img width="1518" height="396" alt="image" src="https://github.com/user-attachments/assets/eadd01df-1454-470b-9d64-cd32873906a9" />








