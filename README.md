timeline.me
==========================

### About
```timeline.me``` is a project lets you backup your timeline from multiple source, such as twitter, weibo, github ...

### How to
- install requirments

    ```shell
    pip install -r deploy/requirements.txt
    ```

- create database

    ```shell
    mysql -u USERNAME -p < deploy/init.sql
    ```
- start server

    ```shell
    python timeline.py
    ```

- use nginx<br/>
     nginx config example is available in ```/deploy/```

- support emoji in MySQL
    * MySQL server v5.5.3+
    * set ```CHARSET``` to ```utf8mb4```