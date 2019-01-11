# -*- coding: utf-8 -*-
"""
Author: Liam Henderson
Written using python 3.5

"""
import re
from functools import reduce
import sys
"""

Resources used:
    https://stackoverflow.com/questions/2052390/manually-raising-throwing-an-exception-in-python
    http://book.pythontips.com/en/latest/map_filter.html
    https://bost.ocks.org/mike/algorithms/
    https://docs.python.org/3/library/pydoc.html
    
"""
class SubnetCalculator:
    """
    Calculates subnets given an IP address and a subnet mask in slash form.
    
    All calculations are stored in variables without a '_' in front.
    """
    _ipAddress = "0.0.0.0"
    _subnetMask = 32
    _defaultSM = 0
    
    def __init__(self, ip, sm):
        """
        All the calculations happen here.
        """
        #verify the format of the ip address is valid.
        self.verifyIp(ip)
        
        
        
        self._ipAddress = ip
        
        self._defaultSM = self.classify()
        #verify the format of the subnet mask is valid.
        self.verifySubnetMask(sm)
        
        #Check to make sure subnet mask is in slash notation.
        if type(sm) is type(""):
            #counts the number of 1's in a subnet mask in dotted decimal format.
            self._subnetMask = reduce(lambda x, y: x + y, [1 for x in self.ipToBinary(sm) if x == "1"])
        else:
            self._subnetMask = sm

        

        
                
        
        if self._defaultSM >= self._subnetMask:
            print("Default subnet mask is greater than or equal to given subnet mask.")
        
        
        #Calculations
        self.hostIp = ("IP Address: %s" % self._ipAddress)
        self.networkAddress = ("Network Address: %s" % self.calculateNetworkAddress(self._ipAddress))
        self.firstHost = ("First Host: %s" % self.calculateValidHostRange(self._ipAddress)[0])
        self.lastHost = ("Last Host: %s" % self.calculateValidHostRange(self._ipAddress)[1])
        self.broadcastAddress = ("Broadcast Address: %s" % self.calculateBroadcastAddress(self._ipAddress))
        self.totalHosts = ("Total hosts: %s" % self.calculateTotalHosts())
        self.usableHosts = ("Usable Hosts: %s" % (self.calculateTotalHosts() - 2))
        self.subnetId = ("Subnet ID: %d" % self.getSubnetId())
        self.slash = ("Subnet Mask Slash Notation: /%s" % self._subnetMask)
        self.subnetMask = ("Subnet Mask: %s" % self.getSubnetMaskDecimal())
        self.subnetMaskBinary = ("Binary Subnet Mask: %s" % self.getSubnetMaskBinary() )
        self.ipAddressClass = ("IP class: %s" % {8:'A',16:'B',24:'C'}[self._defaultSM])
        
        
        #Table generation
        #self.tableTitle = ("All %d of the possible /%d networks like %s" % (self.calculateSubnets(), self._subnetMask, self._ipAddress)) # Puts a title above the table.
        
        self.tableHeader = ("%s, %s, %s" % ("Network Address", "Usable Range", "Broadcast Address"))
        
        self.table = []
        ip = [self.ipToBinary(self._ipAddress)[:self._defaultSM], self.ipToBinary(self._ipAddress)[self._subnetMask:] ]
        
        for i in range(self.calculateSubnets()):
            
            # makes a temporary ip for each individual subnet.
            temp = self.binaryToIp("".join([ip[0], ("{:0"+str((self._subnetMask-self._defaultSM))+"b}").format(i), ip[1]]))
            self.table.append([self.calculateNetworkAddress(temp), self.calculateValidHostRange(temp)[0]+ " - " + self.calculateValidHostRange(temp)[1],\
                  self.calculateBroadcastAddress(temp)])
            
            
            
    
    def verifyIp(self, ipAddress):
        """
        Verifies the IP address. Throws an exception if the IP address is invalid.
        """
        ipPattern = re.compile(r"\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
        
        if ipPattern.match(ipAddress) is None:
            raise ValueError("Bad IP Address format. The ip doesn't match standard decimal format.")
        # converts the first octet of the IP address to a number,
        # then checks for illegal values.
        elif int(ipAddress.split(".")[0]) in set(range(224,256)).union({127, 0}):
            raise ValueError("Bad IP Address. The first octet can't be 0, 127, or greater than 223.")
        
        
    
    def verifySubnetMask(self, subnetMask):
        """
        Verifies the subnet mask based on its form.
        """
        #print (type(subnetMask) is type(0), type(""))
        if type(subnetMask) is type(0) and (subnetMask >= 31 or subnetMask - self._defaultSM < 0):
            raise ValueError("Bad Subnet Mask Format.")
        elif type(subnetMask) is type(""): 
            s = subnetMask.split(".")
            # a list of the valid subnet mask octets is found below
            validMasks = {0, 255, 254, 252, 248, 240, 224, 192, 128}
            # verifies each octet of the subnet mask is valid.
            if [True for x in s if int(x) not in validMasks] or s[3] == "255":
                raise ValueError("Bad Subnet Mask format.")
                
        elif type(subnetMask) is not type("") and type(subnetMask) is not type(0):
            raise ValueError("Subnet address wrong type.")
    
    def getSubnetId(self):
        """
        Gets the Subnet id for a given IP Address and Subnet Mask.
        """
        return int("".join(self.ipToBinary(self._ipAddress)[self._defaultSM:self._subnetMask]), base=2)
    
    def getSubnetMaskDecimal(self):
        """
        Gets the subnet mask in dotted-decimal format.
        """
        return ".".join(["{:d}".format(int(("1"*self._subnetMask + "0"*(32-self._subnetMask))[x:x+8], base=2)) for x in range(0, 32, 8)])
    
    def getSubnetMaskBinary(self):
        """
        Gets a subnet mask in binary format, with any leading 0s included.
        """
        return (".".join(["{:08b}".format(int(("1"*self._subnetMask + "0"*(32-self._subnetMask))[x:x+8], base=2)) for x in range(0, 32, 8)]))
        
    def ipToBinary(self, ipAddress):
        """
        Converts a dotted-decimal format IP Address to a String of 32 bits.
        """
        return "".join(["{:08b}".format(int(x)) for x in ipAddress.split(".")])
    
    def binaryToIp(self, ipAddress):
        """
        Converts a String of 32 bits into a dotted-decimal format IP Addresss.
        """
        # ex. 11000000101010001111111000000000
        # to: 192.168.254.0
        return ".".join(["{:d}".format(int(ipAddress[x:x+8], base=2)) for x in range(0, 32, 8)])
    
    def calculateNetworkAddress(self, ipAddress):
        """
        Calculates a network address for a given IP Address and Subnet Mask.
        """
        # convert each octet of the ip address to an 8 bit binary representation string.
        binary = self.ipToBinary(ipAddress)
        return self.binaryToIp(binary[:self._subnetMask] + "0" * (32 - self._subnetMask))
    
    def calculateValidHostRange(self, ipAddress):
        
        """
        Calculates the valid host range. Returns a list such that the 
        first element is the IP Address of the first host, and the last element
        is the IP Address of the last host.
        """
        
        binary = self.ipToBinary(ipAddress)
        hostBits = binary[self._subnetMask+1:]
        
        firstHost = binary[:self._subnetMask] + "".join(["0"*(len(hostBits)) + "1"])
        lastHost = binary[:self._subnetMask] + "".join(["1"*(len(hostBits)) + "0"])
        
        return (self.binaryToIp(firstHost), self.binaryToIp(lastHost))
    
    def calculateTotalHosts(self):
        """
        Caculates total hosts available for a given subnet mask, including Broadcast and Network Addresses.
        """
        return 2**(32-(self._subnetMask))
    
    def calculateSubnets(self):
        """
        Calculates the number of possible subnets for a given IP Address and Subnet Mask.
        """
        return 2**(self._subnetMask-self._defaultSM)
    
    def calculateBroadcastAddress(self, ipAddress):
        """
        Takes an ipAddress as a parameter.
        Outputs an IP address as a String.
        """
        binary = self.ipToBinary(ipAddress)
        hostBits = binary[self._subnetMask+1:]
        return self.binaryToIp(binary[:self._subnetMask] + "".join(["1"*(len(hostBits)+1)]))
    
    def classify(self):
        """
        Gets the default subnet mask based on the ip address provided when SubnetCalculator was initialized.
        Returns The slash notation of the default subnet mask.
        """
        return [ v for k, v in {192:24, 128:16, 1:8}.items() if int(self._ipAddress[:self._ipAddress.index(".")]) >= k][0]



if __name__ == "__main__":
    
    #print("Please enter the IP address, press return, then enter a subnet mask in slash notation.")
    calculator = None
    # If command line arguments are presented
    if len(sys.argv) > 1:
        # Get the ip and subnet mask from the command line
        ip = sys.argv[1]
        sm = sys.argv[2]
        
        if len(sm) > 2:
            print("Please enter your Subnet Mask in slash notation!")
        else:
            calculator = SubnetCalculator(ip, int(sm))
        
    else:
        calculator = SubnetCalculator("192.168.1.129", 30)
    
    #Table printing
    for k in vars(calculator):
        if k[0] != "_":
            if k != "table":
                print(vars(calculator)[k])
                print()
            else:
                r = 0
                for row in vars(calculator)[k]:
                    print(r, end=' ')
                    
                    for column in row:
                        
                        print(column,end=", ")
                    
                    r += 1
                    print()
    
    