import requests
from django.conf import settings



def vultr_api(plan, name_vm):
    json = {
        "region": "ewr",
        "plan": plan,
        "label": name_vm,
        "os_id": "244"
    }

    requests.post('https://api.vultr.com/v2/instances', json=json, headers={
        "Authorization": f"Bearer {settings.API_KEY_VULTR}"
    })


def get_ip_address(plan, name_vm):
    response = requests.get(
        'https://api.vultr.com/v2/instances',
        headers={
            "Authorization": f"Bearer {settings.API_KEY_VULTR}"
        }
    )
    id_inst = None
    ip_addr = '0.0.0.0'
    for inst in response.json()['instances']:
        if inst['plan'] == plan and inst['label'] == name_vm:
            id_inst = inst['id']
    while ip_addr == '0.0.0.0':
        response2 = requests.get(
            f'https://api.vultr.com/v2/instances/{id_inst}',
            headers={
                "Authorization": f"Bearer {settings.API_KEY_VULTR}"
            }
        )
        ip_addr = response2.json()['instance']['main_ip']

    return ip_addr
