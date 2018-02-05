# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['FieldsTestCase::test_regions 1'] = {
    'data': {
        'regions': {
            'edges': [
                {
                    'node': {
                        'id': 'UmVnaW9uTm9kZTo0MzQ=',
                        'name': 'Region434',
                        'parent': None,
                        'slug': 'region-434'
                    }
                },
                {
                    'node': {
                        'id': 'UmVnaW9uTm9kZTo3NTY=',
                        'name': 'Region756',
                        'parent': None,
                        'slug': 'region-756'
                    }
                },
                {
                    'node': {
                        'id': 'UmVnaW9uTm9kZTo3ODk=',
                        'name': 'Region789',
                        'parent': None,
                        'slug': 'region-789'
                    }
                },
                {
                    'node': {
                        'id': 'UmVnaW9uTm9kZTo3OTE=',
                        'name': 'Region791',
                        'parent': None,
                        'slug': 'region-791'
                    }
                }
            ]
        }
    }
}

snapshots['FieldsTestCase::test_sites 1'] = {
    'data': {
        'sites': {
            'edges': [
                {
                    'node': {
                        'asn': 12.0,
                        'comments': 'comment',
                        'contactEmail': 'a@gmail.com',
                        'contactName': 'Name',
                        'contactPhone': '123',
                        'facility': 'fac',
                        'id': 'U2l0ZU5vZGU6NDM0',
                        'name': 'Site Name 434',
                        'physicalAddress': 'A1',
                        'region': {
                            'name': 'Region434'
                        },
                        'shippingAddress': 'A2',
                        'slug': 'site-name 434',
                        'tenant': {
                            'name': 'Tenant 434'
                        }
                    }
                },
                {
                    'node': {
                        'asn': 12.0,
                        'comments': 'comment',
                        'contactEmail': 'a@gmail.com',
                        'contactName': 'Name',
                        'contactPhone': '123',
                        'facility': 'fac',
                        'id': 'U2l0ZU5vZGU6NzU2',
                        'name': 'Site Name 756',
                        'physicalAddress': 'A1',
                        'region': {
                            'name': 'Region756'
                        },
                        'shippingAddress': 'A2',
                        'slug': 'site-name 756',
                        'tenant': {
                            'name': 'Tenant 756'
                        }
                    }
                },
                {
                    'node': {
                        'asn': 12.0,
                        'comments': 'comment',
                        'contactEmail': 'a@gmail.com',
                        'contactName': 'Name',
                        'contactPhone': '123',
                        'facility': 'fac',
                        'id': 'U2l0ZU5vZGU6Nzg5',
                        'name': 'Site Name 789',
                        'physicalAddress': 'A1',
                        'region': {
                            'name': 'Region789'
                        },
                        'shippingAddress': 'A2',
                        'slug': 'site-name 789',
                        'tenant': {
                            'name': 'Tenant 789'
                        }
                    }
                },
                {
                    'node': {
                        'asn': 12.0,
                        'comments': 'comment',
                        'contactEmail': 'a@gmail.com',
                        'contactName': 'Name',
                        'contactPhone': '123',
                        'facility': 'fac',
                        'id': 'U2l0ZU5vZGU6Nzkx',
                        'name': 'Site Name 791',
                        'physicalAddress': 'A1',
                        'region': {
                            'name': 'Region791'
                        },
                        'shippingAddress': 'A2',
                        'slug': 'site-name 791',
                        'tenant': {
                            'name': 'Tenant 791'
                        }
                    }
                }
            ]
        }
    }
}
