# network-monitor
A networking monitor for your home network

## monitor.py
1. Gets:
  + Internal ping (loss & rtt)
  + External ping (loss & rtt)
2. Uploads data to server

## config.json
Contains the configurations for SFTP (SSH) access to the server:
```json
{
  "username":"your_username",
  "host":"your_server",
  "password":"your_password",
  "current-path":"/path/to/current.txt"
}
```
The ```password``` value is optional - if left empty, it uses your SSH key
