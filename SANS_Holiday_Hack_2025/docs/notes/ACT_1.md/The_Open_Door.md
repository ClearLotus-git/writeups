The Open Door 

Difficulty: 1/5

Objective: Help Goose Lucas in the hotel parking lot find the dangerously misconfigured Network Security Group rule that's allowing unrestricted internet access to sensitive ports like RDP or SSH.

Task: 

<img width="448" height="339" alt="image" src="https://github.com/user-attachments/assets/f44102c8-c456-4e9d-b1d4-7fda049dce02" />

```
🎄 Welcome to The Open Door Challenge! 🎄
You're connected to a read-only Azure CLI session in "The Neighborhood" tenant.
Your mission: Review their network configurations and find what doesn't belong.
Connecting you now... ❄️


───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$
```

```
Welcome back! Let's start by exploring output formats.
First, let's see resource groups in JSON format (the default):
$ az group list
JSON format shows detailed structured data.


───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$ az group list
[
  {
    "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/theneighborhood-rg1",
    "location": "eastus",
    "managedBy": null,
    "name": "theneighborhood-rg1",
    "properties": {
      "provisioningState": "Succeeded"
    },
    "tags": {}
  },
  {
    "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/theneighborhood-rg2",
    "location": "westus",
    "managedBy": null,
    "name": "theneighborhood-rg2",
    "properties": {
      "provisioningState": "Succeeded"
    },
    "tags": {}
  }
] 
```

```
Great! Now let's see the same data in table format for better readability 👀
$ az group list -o table
Notice how -o table changes the output format completely!
Both commands show the same data, just formatted differently.


───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$  az group list -o table
Name                 Location    ProvisioningState
-------------------  ----------  -------------------
theneighborhood-rg1  eastus      Succeeded
theneighborhood-rg2  westus      Succeeded
```

```
Lets take a look at Network Security Groups (NSGs).
To do this try: az network nsg list -o table
This lists all NSGs across resource groups.
For more information:
https://learn.microsoft.com/en-us/cli/azure/network/nsg?view=azure-cli-latest

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$ az network nsg list -o table
Location    Name                   ResourceGroup
----------  ---------------------  -------------------
eastus      nsg-web-eastus         theneighborhood-rg1
eastus      nsg-db-eastus          theneighborhood-rg1
eastus      nsg-dev-eastus         theneighborhood-rg2
eastus      nsg-mgmt-eastus        theneighborhood-rg2
eastus      nsg-production-eastus  theneighborhood-rg1
```

```
Inspect the Network Security Group (web)  🕵️
Here is the NSG and its resource group:--name nsg-web-eastus --resource-group theneighborhood-rg1 

Hint: We want to show the NSG details. Use | less to page through the output.
Documentation: https://learn.microsoft.com/en-us/cli/azure/network/nsg?view=azure-cli-latest#az-network-nsg-show

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$ az network nsg show \
  --name nsg-web-eastus \
  --resource-group theneighborhood-rg1 \
  --output json | less

```

```
{
  "id": "/subscriptions/2b0942f3-9bca-484b-a508-abdae2db5e64/resourceGroups/theneighborhood-rg1/providers/Microsoft.Network/networkSecurityGroups/nsg-web-eastus",
  "location": "eastus",
  "name": "nsg-web-eastus",
  "properties": {
    "securityRules": [
      {
        "name": "Allow-HTTP-Inbound",
        "properties": {
          "access": "Allow",
          "destinationPortRange": "80",
          "direction": "Inbound",
          "priority": 100,
          "protocol": "Tcp",
          "sourceAddressPrefix": "0.0.0.0/0"
        }
      },
      {
        "name": "Allow-HTTPS-Inbound",
        "properties": {
          "access": "Allow",
          "destinationPortRange": "443",
          "direction": "Inbound",
          "priority": 110,
          "protocol": "Tcp",
          "sourceAddressPrefix": "0.0.0.0/0"
        }
      },
      {
        "name": "Allow-AppGateway-HealthProbes",
        "properties": {
          "access": "Allow",
          "destinationPortRange": "80,443",
          "direction": "Inbound",
                   "priority": 130,
          "protocol": "Tcp",
          "sourceAddressPrefix": "AzureLoadBalancer"
        }
      },
      {
        "name": "Allow-Web-To-App",
        "properties": {
          "access": "Allow",
          "destinationPortRange": "8080,8443",
          "direction": "Inbound",
          "priority": 200,
          "protocol": "Tcp",
          "sourceAddressPrefix": "VirtualNetwork"
        }
      },
      {
        "name": "Deny-All-Inbound",
        "properties": {
          "access": "Deny",
          "destinationPortRange": "*",
          "direction": "Inbound",
          "priority": 4096,
          "protocol": "*",
          "sourceAddressPrefix": "*"
        }
      }
    ]
  },
  "resourceGroup": "theneighborhood-rg1",
  "tags": {
    "env": "web"
  }
}
```

```
Inspect the Network Security Group (mgmt)  🕵️
Here is the NSG and its resource group:--nsg-name nsg-mgmt-eastus --resource-group theneighborhood-rg2 

Hint: We want to list the NSG rules
Documentation: https://learn.microsoft.com/en-us/cli/azure/network/nsg/rule?view=azure-cli-latest#az-network-nsg-rule-list

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$ az network nsg rule list \
>   --nsg-name nsg-mgmt-eastus \
>   --resource-group theneighborhood-rg2 \
>   --output table
Access    Direction    Name                        Priority    Protocol    NSG              SourceAddressPrefix    SourcePortRange    DestinationAddressPrefix    DestinationPortRange
--------  -----------  --------------------------  ----------  ----------  ---------------  ---------------------  -----------------  --------------------------  ----------------------
Allow     Inbound      Allow-AzureBastion          100         Tcp         nsg-mgmt-eastus  AzureBastion           *                  *                           443
Allow     Inbound      Allow-Monitoring-Inbound    110         Tcp         nsg-mgmt-eastus  AzureMonitor           *                  *                           443
Allow     Inbound      Allow-DNS-From-VNet         115         Udp         nsg-mgmt-eastus  VirtualNetwork         *                  *                           53
Deny      Inbound      Deny-All-Inbound            4096        *           nsg-mgmt-eastus  *                      *                  *                           *
Allow     Outbound     Allow-Monitoring-Outbound   200         Tcp         nsg-mgmt-eastus  *                      *                  AzureMonitor                443
Allow     Outbound     Allow-AD-Identity-Outbound  210         Tcp         nsg-mgmt-eastus  *                      *                  AzureActiveDirectory        443
Allow     Outbound     Allow-Backup-Outbound       220         Tcp         nsg-mgmt-eastus  *                      *                  AzureBackup                 443
```

```
Take a look at the rest of the NSG rules and examine their properties.
After enumerating the NSG rules, enter the command string to view the suspect rule and inspect its properties.
Hint: Review fields such as direction, access, protocol, source, destination and port settings.

Documentation: https://learn.microsoft.com/en-us/cli/azure/network/nsg/rule?view=azure-cli-latest#az-network-nsg-rule-show

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
neighbor@a3037749367b:~$
```

















