import os
import sys
from ipaddress import ip_network, ip_address
from git import Repo


source_url='https://github.com/firehol/blocklist-ipsets'
clone_url = '{0}{1}'.format(source_url, '.git')
repo_dir = source_url.split('/')[4]
block_list = {}    
    
    
def isIPinCIDR(ip, ip_range):
    """
    This method is used to check whether an IP is part of the CIDR IP range or not
    
    Arguments
        ip(string): IP address you want to check
        ip_range(string): IP range in block list
        
    Returns
        result(boolean): True if in CIDR or False if not
    """
    
    if ip_address(ip) in ip_network(ip_range):
        return True
    return False

    
def parse():
    """
    This method is used to clone the source repository and parse the '.netset' files
    and add the IPs in it to thehe block list
    """
    
    Repo.clone_from(clone_url, repo_dir, single_branch=True, b='master')
    for path, subdirs, files in os.walk('/Users/mohankumar/Downloads/blocklist-ipsets'):
        for name in files:
            if '.netset' in path:
                file_path = os.path.join(path,name)
                with open (file_path) as fp:
                    for line in fp:
                        line = str(line).strip()
                        if line[0] != '#' and line !='':
                            block_list.apend(line)


def search(ip):
    """
    This method is used to determine whether an IP is present in the block list or not
    
    Arguments
        ip(string) - ip address which you want to check  
    
    Returns
        status(string) - returns 'Block' if ip is in block list or 'Good' if not
    """
    
    for each_ip in block_list:
        if '/' in each_ip:
            result = isIPinCIDR(ip, each_ip)
            if result:
                print('Block')
                return 'Block'
        if each_ip == ip:
            print('Block')
            return 'Block'
    print('Good')
    return 'Good'
    

if __name__ == '__main__':

    """
    Main Method
    """
    parse()
    search(sys.argv[1])
