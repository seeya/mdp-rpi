# Bluetooth on the RPI

Modify `/etc/systemd/system/dbus-org.bluez.service`

Change this the parameter to compatability mode.

```
# OLD
ExecStart=/usr/lib/bluetooth/bluetoothd

# NEW
ExecStart=/usr/lib/bluetooth/bluetoothd -C
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
