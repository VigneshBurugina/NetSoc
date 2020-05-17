-------
NetSoc
-------
A simple wrapper module for Python3's socket module to help in easy transmission of objects in networks
-------
Instructions
-------
Create netsoc object:  
<code>
ns = netsoc(role=[client/server],target=(ip,port))
</code>
Send object:  
<code>
[netsoc object].send([object to send])  
</code>
Recieve object:  
<code>
[netsoc object].recv()  
</code>
Target argument:  
  For client - IP and port of server  
  For server - IP(localhost) and port to listen  
