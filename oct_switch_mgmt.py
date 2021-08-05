import pexpect


def login(hostname, username, password):
    """Login to switch using either a password"""

    console = pexpect.spawn('ssh ' + username + '@' + hostname)

    console.expect('password:')
    console.sendline(password)
    console.expect('>')
    console.sendline('enable')
    console.expect('Password:')
    console.sendline(password)

    return console


def disconnect(console):
    """End the session. Must be at the main prompt. Handles the scenario
    where the switch only exits out of enable mode and doesn't actually
    log out"""

    console.sendline('copy running-config startup-config')
    console.expect('yes/no')
    console.sendline('yes')
    console.expect('copied')
    console.sendline('exit')

    alternatives = [pexpect.EOF, '>']
    if console.expect(alternatives):
        console.sendline('exit')

def create_and_add_vlan_to_trunk(console, vlan_id, vlan_name, ports):

    console.sendline('conf t')
    console.sendline('interface vlan ' + vlan_id)
    console.sendline('name ' + vlan_name)
    console.sendline('no ip address')
    console.sendline('tagged ' + ports)
    console.sendline('no shutdown')
    console.sendline('exit')
    console.sendline('exit')


switches = [{"hostname": "10.1.0.11", "trunk_ports": "Port-channel 1"},
            {"hostname": "10.1.0.12", "trunk_ports": "Port-channel 1"},
            {"hostname": "10.1.0.13", "trunk_ports": "Port-channel 1"},
            {"hostname": "10.1.0.14", "trunk_ports": "Port-channel 1"},
            {"hostname": "10.1.0.101", "trunk_ports": "Port-channel 10-11"},
            {"hostname": "10.1.0.102", "trunk_ports": "Port-channel 10-11"},
            {"hostname": "10.1.0.103", "trunk_ports": "Port-channel 1-6,10"},
            ]

SSH_USERNAME = "username"
SSH_PASSWORD = "password"

for switch in switches:
    print("working on " + switch["hostname"])
    session = login(switch["hostname"], SSH_USERNAME, SSH_PASSWORD)
    create_and_add_vlan_to_trunk(
        session, "10", "MOC-CSAIL-10", switch["trunk_ports"])
    disconnect(session)
