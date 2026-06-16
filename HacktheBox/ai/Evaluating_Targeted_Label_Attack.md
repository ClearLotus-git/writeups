# Evaluating the Targeted Label Attack - Lab HTB

Download the targeted_label_student.zip file attached to this question, and extract the notebook template and dataset file within it.
Using the techniques that have been demonstrated in this section, implement a targeted label flipping attack in the provided targeted_class_label_flip 
method stub to poison at least 50% of the class 0 labels as class 1 in thedataset, train a model using the provided code, and submit the trained model
to the docker instance using the last cell in the notebook. Submit the flag you receive for a valid attack as the answer to this question.

---

<img width="1909" height="258" alt="image" src="https://github.com/user-attachments/assets/5b640d91-cd6e-4dd2-95e5-8bf26bc4a203" />

Download and unzip the file used for this lab:

```
unzip targeted_label_student.zip
Archive:  targeted_label_student.zip
  inflating: label_flipping_dataset.npz  
  inflating: __MACOSX/._label_flipping_dataset.npz  
  inflating: targeted-label-student-template.ipynb  
  inflating: __MACOSX/._targeted-label-student-template.ipynb
```

If not installed, install miniconda to machine: 

```
wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod +x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh -b -u


PREFIX=/home/htb-ac-943240/miniconda3
Unpacking bootstrapper...
Unpacking payload...

Installing base environment...

Preparing transaction: ...working... done
Executing transaction: ...working... done
installation finished.
```

```
eval "$(/home/$USER/miniconda3/bin/conda shell.$(ps -p $$ -o comm=) hook)"
```

Accept Terms of service:

```
$ conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
accepted Terms of Service for https://repo.anaconda.com/pkgs/main

$ conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
accepted Terms of Service for https://repo.anaconda.com/pkgs/r
```

Using conda to install JupyterLab: 

```
conda install -y jupyter jupyterlab notebook ipykernel

Channels:
 - defaults
Platform: linux-64
Collecting package metadata (repodata.json): done
Solving environment: done

<SNIP>

```

Start JupyterLab:

```
start JupyterLab
```

Resul;ts will look like this: 

<img width="1916" height="833" alt="image" src="https://github.com/user-attachments/assets/78d2f687-7ea3-4f33-baf0-f5eac2b12b69" />


There will be a simultaneous redirect to URL.

Navigate to this file:

<img width="1909" height="637" alt="image" src="https://github.com/user-attachments/assets/78aa01b4-fc6d-4701-94b9-de623860ea0c" />

Navigate to the bottom and click on an empty cell to install `numpy` and `scikit-learn` Python libraries. 

<img width="1918" height="414" alt="image" src="https://github.com/user-attachments/assets/4a3f348f-bb4f-4b5d-a2d6-57dfdd7122e1" />

Run it. 

Results: 

<img width="1298" height="592" alt="image" src="https://github.com/user-attachments/assets/26f627f8-6970-4f0f-88a6-79ee6450e434" />

Replace the value in the `evaluator_base_url` variable in the first cell with the IP:PORT from the spawned target and set the `POISON_FRACTION` variable to 0.70:

<img width="1295" height="592" alt="image" src="https://github.com/user-attachments/assets/206eea4e-195f-4120-b0af-bba6ecef6dbd" />

Navigate to the second cell and modify the targeted_class_label_flip function to perform the Targeted Label Flipping attack:

<img width="1313" height="565" alt="image" src="https://github.com/user-attachments/assets/3a0802b0-f54c-4386-a80b-6e27aaf5e876" />

Run it.

<img width="861" height="136" alt="image" src="https://github.com/user-attachments/assets/efcdea56-bf0a-4835-91b4-f85e659444ee" />
<img width="1085" height="169" alt="image" src="https://github.com/user-attachments/assets/be81a516-3c1f-4193-b191-2d610ed3983f" />
<img width="652" height="104" alt="image" src="https://github.com/user-attachments/assets/2c5708d9-ce4b-4774-973b-967efcc69b9a" />
<img width="702" height="117" alt="image" src="https://github.com/user-attachments/assets/b0c838a9-43ed-449b-bea7-97fbb69ba4b4" />
<img width="738" height="131" alt="image" src="https://github.com/user-attachments/assets/c70a1e15-ae50-4d7e-9d76-e70b50d71041" />



Obtain the flag:

<img width="1255" height="511" alt="image" src="https://github.com/user-attachments/assets/8023d3c2-6f68-4e20-b4f0-8da25951f04f" />


