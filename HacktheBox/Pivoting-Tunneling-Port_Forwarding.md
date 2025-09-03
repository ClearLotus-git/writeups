# Scenario
A team member started a Penetration Test against the Inlanefreight environment but was moved to another project at the last minute. Luckily for us, they left a web shell in place for us to get back into the network so we can pick up where they left off. We need to leverage the web shell to continue enumerating the hosts, identifying common services, and using those services/protocols to pivot into the internal networks of Inlanefreight. Our detailed objectives are below:

### Objectives: 
- Start from external and access the first system via the web shell left in place.
- Use the web shell access to enumerate and pivot to an internal host.
- Continue enumeration and pivoting until you reach the Inlanefreight Domain Controller and capture the associated flag.
- Use any data, credentials, scripts, or other information within the environment to enable your pivoting attempts.
- Grab any/all flags that can be found.

### To Be Answered:

1. Once on the webserver, enumerate the host for credentials that can be used to start a pivot or tunnel to another host in the network. In what user's directory can you find the credentials? Submit the name of the user as the answer.
2. Submit the credentials found in the user's home directory.
3. Enumerate the internal network and discover another active host.
4. Use the information you gathered to pivot to the discovered host.
5. In previous pentests against Inlanefreight, we have seen that they have a bad habit of utilizing accounts with services in a way that exposes the users credentials and the network as a whole. What user is vulnerable?
6. For your next hop enumerate the networks and then utilize a common remote access solution to pivot. Submit the C:\Flag.txt located on the workstation.
7. Submit the contents of C:\Flag.txt located on the Domain Controller.

> This is for training purposes. The answers won't be revealed.


### LAB 

