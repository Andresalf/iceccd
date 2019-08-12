import socket
import fcntl
import struct

class SchedulerFinder():
    def __init__(self
                 , broadcast_ip
                 , port
                 , network_interface
                 , wait_timeout_in_secs
                 , scheduler_udp_port
                 , scheduler_version
                 , scheduler_net_name):
        self.broadcast_ip = broadcast_ip
        self.port = port
        self.network_interface = network_interface
        self.wait_timeout_in_secs = wait_timeout_in_secs
        self.scheduler_udp_port = scheduler_udp_port
        self.scheduler_version = scheduler_version
        self.scheduler_net_name = scheduler_net_name
        self.scheduler_response_size = 268


    def __get_network_interface_ip_address(self, s, interface_name):
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', interface_name[:15])
            )[20:24])


    def get_scheduler_ip_address(self):
        address = ""
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server_socket.settimeout(self.wait_timeout_in_secs)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        server_socket.bind((self.__get_network_interface_ip_address(server_socket, self.network_interface), self.port)) # Listen for any response from a scheduler.
        server_socket.sendto(chr(self.scheduler_version), (self.broadcast_ip, self.scheduler_udp_port)) # Send broadcast message

        try:
            response_data, addr = server_socket.recvfrom(self.scheduler_response_size)
            if self.scheduler_net_name in response_data:
                print "Icecream scheduler found at %s" % addr[0]
                address = addr[0]
            else:
                print "Icecream scheduler with netwok name %s could not be found.\nTry with another one." % self.scheduler_net_name
        except socket.timeout:
            print "Timeout trying to find a scheduler!\nTry again."
            print "Parameters used:"
            print "     Broadcast IP: %s" % self.broadcast_ip
            print "     Scheduler UDP port: %s" % str(self.scheduler_udp_port)
            print "     Finder UDP port: %s" % str(self.port)
            print "     Version: %s" % str(self.scheduler_version)
            print "     Net name: %s" % self.scheduler_net_name

        server_socket.close()

        return address
