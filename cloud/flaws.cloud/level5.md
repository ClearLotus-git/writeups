# Level 5

<img width="1009" height="692" alt="image" src="https://github.com/user-attachments/assets/265cf5f7-8613-4d69-a8e5-551c6ae61870" />

Inside the etc/nginx/sites-available/default

```
location  ~* ^/proxy/((?U).+)/(.*)$ {
  limit_except GET {
    deny   all;
  }
  limit_req zone=one burst=1;
  set $proxyhost '$1';
  set $proxyuri '$2';
  proxy_limit_rate 4096;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header Host      $proxyhost;
  resolver 8.8.8.8;
  proxy_pass http://$proxyhost/$proxyuri;
}
```












