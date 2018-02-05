# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['FieldsTestCase::test_aggregate 1'] = {
    'data': {
        'aggregates': {
            'edges': [
                {
                    'node': {
                        'dateAdded': '2017-12-12',
                        'description': 'desc',
                        'family': 'A_4',
                        'id': 'QWdncmVnYXRlTm9kZToxNA==',
                        'prefix': '14.0.0.0/8',
                        'rir': {
                            'id': 'UklSTm9kZToxNA==',
                            'name': 'rir14'
                        }
                    }
                },
                {
                    'node': {
                        'dateAdded': '2017-01-01',
                        'description': 'desc',
                        'family': 'A_4',
                        'id': 'QWdncmVnYXRlTm9kZToxMw==',
                        'prefix': '54.0.0.0/8',
                        'rir': {
                            'id': 'UklSTm9kZToxMw==',
                            'name': 'rir13'
                        }
                    }
                },
                {
                    'node': {
                        'dateAdded': '2015-01-01',
                        'description': 'desc',
                        'family': 'A_4',
                        'id': 'QWdncmVnYXRlTm9kZToxOA==',
                        'prefix': '192.0.0.0/12',
                        'rir': {
                            'id': 'UklSTm9kZToxMQ==',
                            'name': 'rir11'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['FieldsTestCase::test_ip_address 1'] = {
    'data': {
        'ipAddress': {
            'edges': [
            ]
        }
    }
}

snapshots['FieldsTestCase::test_rir 1'] = {
    'data': {
        'rirs': {
            'edges': [
                {
                    'node': {
                        'id': 'UklSTm9kZToxMQ==',
                        'isPrivate': True,
                        'name': 'rir11',
                        'slug': 'rir11'
                    }
                },
                {
                    'node': {
                        'id': 'UklSTm9kZToxMg==',
                        'isPrivate': True,
                        'name': 'rir12',
                        'slug': 'rir12'
                    }
                },
                {
                    'node': {
                        'id': 'UklSTm9kZToxMw==',
                        'isPrivate': True,
                        'name': 'rir13',
                        'slug': 'rir13'
                    }
                },
                {
                    'node': {
                        'id': 'UklSTm9kZToxNA==',
                        'isPrivate': True,
                        'name': 'rir14',
                        'slug': 'rir14'
                    }
                }
            ]
        }
    }
}

snapshots['FieldsTestCase::test_vlan 1'] = {
    'errors': [
        {
            'locations': [
                {
                    'column': 9,
                    'line': 24
                }
            ],
            'message': '''Syntax Error GraphQL request (24:9) Expected Name, found EOF

23:         }
24:         
            ^
'''
        }
    ]
}

snapshots['FieldsTestCase::test_vlan_groups 1'] = {
    'data': {
        'vlanGroups': {
            'edges': [
            ]
        }
    }
}

snapshots['FieldsTestCase::test_vlan_roles 1'] = {
    'data': {
        'vlanRoles': {
            'edges': [
            ]
        }
    }
}

snapshots['FieldsTestCase::test_vrf 1'] = {
    'data': {
        'vrfs': {
            'edges': [
            ]
        }
    }
}

snapshots['FieldsTestCase::test_prefix 1'] = {
    'data': {
        'prefixes': {
            'edges': [
            ]
        }
    }
}
