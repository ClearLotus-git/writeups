Difficulty: 1/5

Team up with Bow Ninecandle to send web requests from the command line using Curl, 
learning how to interact directly with web servers and retrieve information like a pro!  

<img width="707" height="471" alt="image" src="https://github.com/user-attachments/assets/fdd69f0c-7c52-431d-8cb8-73c1d72cfe23" />


Challenge: 

```
Welcome to Curling Fun!  We will learn some basic curl commands while playing a round of curling.

───────────────────────────────────────────────────────────────────────────────────────────────

Are you ready to begin? [y]es: yes
```

```
1) Unlike the defined standards of a curling sheet, embedded devices often have web servers on non-standard ports.  Use curl to retrieve the web page on host "curlingfun" port 8080.
If you need help, run the 'hint' command.

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl http://curlingfun:8080/
You have successfully accessed the site on port 8080!

If you need help, please remember to run "hint" for a hint!

```

```
2) Embedded devices often use self-signed certificates, where your browser will not trust the certificate presented.  Use curl to retrieve the TLS-protected web page at https://curlingfun:9090/

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl -k https://curlingfun:9090/
You have successfully bypassed the self-signed certificate warning!
Subsequent requests will continue to require "--insecure", or "-k" for short.
```

```
3) Working with APIs and embedded devices often requires making HTTP POST requests. Use curl to send a request to https://curlingfun:9090/ with the parameter "skip" set to the value "alabaster", declaring Alabaster as the team captain.

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl -k -X POST -d "skip=alabaster" https://curlingfun:9090/
You have successfully made a POST request!
```

```
4) Working with APIs and embedded devices often requires maintaining session state by passing a cookie.
Use curl to send a request to https://curlingfun:9090/ with a cookie called "end" with the value "3", indicating we're on the third end of the curling match.

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl -k --cookie "end=3" https://curlingfun:9090/
You have successfully set a cookie!
```

```
5) Working with APIs and embedded devices sometimes requires working with raw HTTP headers.  Use curl to view the HTTP headers returned by a request to https://curlingfun:9090/

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl -k -I https://curlingfun:9090/
HTTP/1.1 200 OK
Server: nginx/1.18.0 (Ubuntu)
Date: Mon, 10 Nov 2025 01:01:14 GMT
Content-Type: text/plain;charset=UTF-8
Connection: keep-alive
Custom-Header: You have found the custom header!
```

```
6) Working with APIs and embedded devices sometimes requires working with custom HTTP headers.  Use curl to send a request to https://curlingfun:9090/ with an HTTP header called "Stone" and the value "Granite".

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl -k -H "Stone: Granite" https://curlingfun:9090/
You have successfully set a custom HTTP header!
```

```
7) curl will modify your URL unless you tell it not to.  For example, use curl to retrieve the following URL containing special characters: https://curlingfun:9090/../../etc/hacks

───────────────────────────────────────────────────────────────────────────────────────────────

alabaster@curlingfun:~$ curl -k --path-as-is https://curlingfun:9090/../../etc/hacks
You have successfully utilized --path-as-is to send a raw path!
```

```
Great work! 
 
Once HHC grants your achievement, you may close this terminal.
```






