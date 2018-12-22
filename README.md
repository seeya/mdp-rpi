# Bluetooth on the RPI

Modify `/etc/systemd/system/dbus-org.bluez.service`

Change this the parameter to compatability mode.

```
# OLD
ExecStart=/usr/lib/bluetooth/bluetoothd

# NEW
ExecStart=/usr/lib/bluetooth/bluetoothd -C
ExecStartPost=/usr/bin/sdptool add SP
```

Next add serial profile
```
sudo sdptool add SP
```

Then restart services

```
sudo systemctl daemon-reload 
sudo service bluetooth restart 
```

# Update Permissions to not use root

```
sudo usermod -G bluetooth -a pi
sudo chgrp bluetooth /var/run/sdp
```

Paste the code into this file `sudo vim /etc/systemd/system/var-run-sdp.path`

```
[Unit]
Descrption=Monitor /var/run/sdp

[Install]
WantedBy=bluetooth.service

[Path]
PathExists=/var/run/sdp
Unit=var-run-sdp.service
```

And this `/etc/systemd/system/var-run-sdp.service`

```
[Unit]
Description=Set permission of /var/run/sdp

[Install]
RequiredBy=var-run-sdp.path

[Service]
Type=simple
ExecStart=/bin/chgrp bluetooth /var/run/sdp
ExecStartPost=/bin/chmod 662 /var/run/sdp
```

Finally restart the services
```
sudo systemctl daemon-reload
sudo systemctl enable var-run-sdp.path
sudo systemctl enable var-run-sdp.service
sudo systemctl start var-run-sdp.path
```
