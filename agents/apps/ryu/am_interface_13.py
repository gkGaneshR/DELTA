import socket
from os.path import expanduser

class AMInterface:
    def __init__(self, obj):
        from app_agent_13 import AppAgent
        self.appAgent = obj
        print self.appAgent

    def setServerAddr(self):
        server_address = ('10.0.2.2', 3366)
        home = expanduser("~")
        f = open(home + "/agent.cfg", "r")

        while True:
            line = f.readline()
            if not line: break

            if "MANAGER_IP" in line:
               manager_ip = line.split("=")[1].rstrip()
            elif "MANAGER_PORT" in line:
               manager_port = int(line.split("=")[1].rstrip())
        server_address = (manager_ip, manager_port)

        return server_address


    def connectServer(self, server_address):
        from app_agent_13 import AppAgent

        print self.appAgent

        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect the socket to the port where the server is listening

        if not server_address:
            server_address = ('10.0.2.2', 3366)

        print '[AMInterface] Connecting to %s port %s' % server_address
        sock.connect(server_address)

        try:
            # Send AppAgent Message
            message = 'AppAgent'
            m = '\x00' + '\x08' + message
            print "AppAgent: " + message
            sock.send(m)

            # Receive OK Message (4bytes)
            data = sock.recv(4)
            print "AgentManager: " + data

            # Receive Code
            data = sock.recv(1024)

            if "3.1.020" in data:
                self.appAgent.testControlMessageDrop()
            elif "3.1.030" in data:
                self.appAgent.testInfiniteLoops()
            elif "3.1.040" in data:
                self.appAgent.testInternalStorageAbuse()
            elif "3.1.070" in data:
                self.appAgent.testFlowRuleModification()
            elif "3.1.080" in data:
                self.appAgent.testFlowTableClearance()
            elif "3.1.090" in data:
                self.appAgent.testEventListenerUnsubscription()
            else:
                print "AgentManager: " + data
        finally:
            sock.close()

if __name__ == "__main__":
     AMInterface()
