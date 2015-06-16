timeline.me
==========================

### About
- ```timeline.me``` is a project let you backup your timeline, such as twitter, weibo, and rss feeds ...
- a [demo](http://i.caoyue.me)

### features
- sync your timeline
- update status, support twitter, weibo and "your own twitter" ([moments](http://i.caoyue.me/moments))
- this day in history posts ([past](http://i.caoyue.me/past))
- simple charts about your timeline ([chart](http://i.caoyue.me/chart))

### How to
1. install requirments

    ```shell
    pip install -r deploy/requirements.txt
    ```

2. mysql
    * create database

        ```shell
        mysql -u USERNAME -p < deploy/init.sql
        ```
    * support emoji in MySQL
        + MySQL server v5.5.3+
        + set ```CHARSET``` to ```utf8mb4```

3. set config
    * rename ```config.example.py``` to ```config.py``` and set your configs

4. nginx
    * nginx config example is available in ```/deploy/timeline.conf```

5. start server
    - command

        ```shell
        python timeline.py --port=8888
        ```
    - supervisor
        * supervisor config example is available in ```/deploy/supervisor.conf```

6. sign in
    - http://your-domain/signin
    - sign in with your twitter/weibo/...
    - bind other accounts (http://your-domain/admin/accounts)

7. sync your timeline
    - use cron
        * cron example is available in ```/deploy/cron```
    - web
        * http://your-domain/admin