# network-monitor
A networking monitor for your home network

## monitor.py
1. Gets:
  + Internal ping (loss & rtt)
  + External ping (loss & rtt)
2. Uploads data to server

## config.json
Contains the configurations for SFTP (SSH) access to the server (you will need to create it in the same dir as `monitor.py`):
```json
{
  "username":"your_username",
  "host":"your_server",
  "password":"your_password",
  "local-path-to-current":"/local/path/to/current.txt",
  "server-path-to-current":"/server/path/to/current.txt"
}
```
The `password` value is optional - if left empty, it uses your SSH key

After the script has run once (without failure) the results will be accessible on your server at the location you specified in `server-path-to-current` in the config file.
