import os
import pytest
import requests
import testinfra.utils.ansible_runner
import urllib2

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

def test_cuckoo_service_is_running(host):
    cuckoo_service = host.service('cuckoo.service')
    assert cuckoo_service.is_running

#def test_cuckoo_api_server_is_accessible_on_port_8090(host):
#    host_ip = host.interface("eth0").addresses[0]
#    api_response = requests.get('http://'+host_ip+':8090/cuckoo/status')
#    assert api_response.json()
