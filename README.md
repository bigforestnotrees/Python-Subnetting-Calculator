# Python-Subnetting-Calculator

A subnetting calculator. Calculates network, first host, last host, and broadcast addresses. Prints all that and more.

# Information Displayed

1. IP Address: the IP Address you provided
2. Network Address: the Network Address of the IP Address you provided
3. First Host: The first host in the subnet (dotted-decimal IP Address format)
4. Last Host: The last host in the subnet (dotted-decimal IP Address format)
5. Broadcast Address: the network broadcast address (dotted-decimal IP Address format)
6. Total Hosts: the total number of hosts on the subnet, including broadcast and network addresses
7. Usable Hosts: the available hosts. Total number of hosts minus the broadcast and network addresses
8. Subnet ID: the identity or index of the subnet
9. Subnet Mask Slash Notation: the subnet mask in slash notation
10. Subnet Mask: the subnet mask in dotted-decimal format
11. Binary Subnet Mask: the subnet mask converted to binary
12. IP Class: the class of the IP Address, ranging from A to C

TABLE
Displays: 
1. Subnet index given network address and subnet mask 
2. Network address of subnet
3. Usable range of valid IP Addresses separated by a dash
4. Broadcast Address


# Usage 

After retrieving the file "calc.py", run using the script name in a command prompt, providing an IP-Address in dotted-decimal format and a slash notation subnet mask.

Be aware that a table of all possible subnets given the network address and subnet mask prints. If your given subnet mask is /26, and your ip address is class A (/8 default subnet mask) the table will be huge. 2^18 huge.

Examples:

$ python ./calc.py 192.168.2.1 25

$ python ./calc.py 191.168.2.1 25

