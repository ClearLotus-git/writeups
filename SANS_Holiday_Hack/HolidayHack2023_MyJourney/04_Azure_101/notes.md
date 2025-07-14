## Objective 5 – Azure 101


---

###  Objective

Sparkle Redberry needed help brushing up on Azure CLI commands. I found her near a terminal on Christmas Island and stepped in to help her navigate through a series of Azure tasks using the command line interface.

---

###  Hints

- Azure CLI comes with a built-in help system. You can use `az help` or access Microsoft's [Azure CLI documentation](https://learn.microsoft.com/en-us/cli/azure/reference-index?view=azure-cli-latest).
- For every command, you can append `--help` to get full usage info.

---

###  Procedure

####  Start with Azure CLI Help
To get started, I used the help system to see available commands and syntax:
```bash
az help | less
```

---

####  Check Account Info
I checked the currently configured account using:
```bash
az account show
```

```json
{
  "environmentName": "AzureCloud",
  "id": "2b0942f3-9bca-484b-a508-abdae2db5e64",
  "isDefault": true,
  "name": "northpole-sub",
  "state": "Enabled",
  "tenantId": "90a38eda-4006-4dd5-924c-6ca55cacc14d",
  "user": {
    "name": "northpole@northpole.invalid",
    "type": "user"
  }
}
```

---

####  List Resource Groups
To find existing resource groups:
```bash
az group list --output table
```

```json
[
  {
    "name": "northpole-rg1",
    "location": "eastus",
    "provisioningState": "Succeeded"
  },
  {
    "name": "northpole-rg2",
    "location": "westus",
    "provisioningState": "Succeeded"
  }
]
```

---

####  List Function Apps in RG1
Checked for function apps deployed in `northpole-rg1`:
```bash
az functionapp list --resource-group northpole-rg1
```

---

####  List Virtual Machines in RG2
To identify what VMs were available in the second resource group:
```bash
az vm list --resource-group northpole-rg2
```

```json
[
  {
    "name": "NP-VM1",
    "location": "eastus",
    "vmSize": "Standard_D2s_v3",
    "image": "UbuntuServer 16.04-LTS"
  }
]
```

---

####  Execute a Remote Command on VM
Ran a shell script remotely on the VM to get a directory listing:
```bash
az vm run-command invoke -g northpole-rg2 -n NP-VM1 --command-id RunShellScript --scripts "ls"
```

```json
{
  "value": [
    {
      "code": "ComponentStatus/StdOut/succeeded",
      "message": "bin\net\etc\home\jinglebells\lib\usr"
    }
  ]
}
```

---

###  Result

Successfully completed each task, from basic CLI navigation to resource enumeration and executing remote commands on a VM. Sparkle was thrilled, and the mission was a success.

---

###  Lesson Learned

Azure CLI is a powerful tool, and knowing how to explore resource groups, VMs, and remote execution commands can be a big advantage — especially when working in cloud environments with limited UI access.
