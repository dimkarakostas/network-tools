import subprocess
import os
from bs4 import BeautifulSoup


def add_spaces(total_length, covered):
    return ' '*(total_length-len(covered))

network = '192.168.1.0/24'
proc = subprocess.Popen(['sudo', 'nmap', '-oX', '-', '-sn', '-PS21,22,25,3389', network], stdout=subprocess.PIPE, preexec_fn=os.setpgrp)

nmap_output = proc.communicate()[0]

print 'Hostname{}|IPv4{}|MAC{}|Vendor'.format(
    add_spaces(30, 'Hostname'),
    add_spaces(18, 'IPv4'),
    add_spaces(20, 'MAC')
)
print '--------------------------------------------------------------------------------------'

soup = BeautifulSoup(nmap_output, 'html.parser')
for host in soup.findAll('host'):
    host_attrs = {}
    host_attrs['mac'] = ''
    host_attrs['vendor'] = ''

    address_list = host.findAll('address')
    for address in address_list:
        addr_attrs = dict(address.attrs)
        if addr_attrs[u'addrtype'] == 'ipv4':
            host_attrs['ipv4'] = addr_attrs[u'addr']
        elif addr_attrs[u'addrtype'] == 'mac':
            host_attrs['mac'] = addr_attrs[u'addr']
            host_attrs['vendor'] = addr_attrs[u'vendor'] if 'vendor' in addr_attrs else ''

    hostname = host.find('hostname')
    if 'name' in hostname.attrs:
        host_attrs['hostname'] = hostname.attrs['name']

    print '{}{}|{}{}|{}{}|{}'.format(
        host_attrs['hostname'], add_spaces(30, host_attrs['hostname']),
        host_attrs['ipv4'], add_spaces(18, host_attrs['ipv4']),
        host_attrs['mac'], add_spaces(20, host_attrs['mac']),
        host_attrs['vendor']
    )