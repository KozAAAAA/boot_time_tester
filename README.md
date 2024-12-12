# Boot Time Tester

Obtain logs:
```bash
./get_logs.sh /dev/ttyUSB0 ./logs/time.cap
```

Analyse logs:
```bash
./get_boot_time.py ./markers/astra-1680-markers.json ./logs/time.cap
```
