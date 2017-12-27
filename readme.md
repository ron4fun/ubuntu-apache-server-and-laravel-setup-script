# Automate Ubuntu 16.04 Server and Laravel Application Setup

**The setup scripts installs the following software:**

* Apache
* MySQL
* PHP
* Composer
* Git

Follow the interactive shell and complete the installations and configurations.

## 1. Run LAMPInstaller.py
```
sudo python LAMPInstaller.py
```

## 2. Secure your MySQL Server
```
mysql_secure_installation
```

## 3. Set correct timezone
```
dpkg-reconfigure tzdata
```

## 4. Run db_config.py
```
sudo python db_config.py
```

## 5. Run laravelInstaller.py
```
sudo python laravelInstaller.py
```





###License

This "Software" is Licensed Under  **`MIT License (MIT)`** .