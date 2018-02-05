# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['FieldsTestCase::test_circuit_terminations 1'] = {
    'data': {
        'circuitTerminations': {
            'edges': [
                {
                    'node': {
                        'circuit': {
                            'cid': 'cid',
                            'id': 'Q2lyY3VpdE5vZGU6NDM0'
                        },
                        'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZToxNw==',
                        'interface': None,
                        'portSpeed': 128,
                        'ppInfo': 'ppInfo',
                        'site': {
                            'id': 'U2l0ZU5vZGU6NDM0',
                            'name': 'Site Name 434'
                        },
                        'termSide': 'A',
                        'upstreamSpeed': 128,
                        'xconnectId': 'xconnectId'
                    }
                },
                {
                    'node': {
                        'circuit': {
                            'cid': 'cid',
                            'id': 'Q2lyY3VpdE5vZGU6Nzg5'
                        },
                        'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3ODk=',
                        'interface': None,
                        'portSpeed': 512,
                        'ppInfo': 'ppInfo123',
                        'site': {
                            'id': 'U2l0ZU5vZGU6Nzg5',
                            'name': 'Site Name 789'
                        },
                        'termSide': 'Z',
                        'upstreamSpeed': 512,
                        'xconnectId': 'xconnectId123'
                    }
                },
                {
                    'node': {
                        'circuit': {
                            'cid': 'cid',
                            'id': 'Q2lyY3VpdE5vZGU6Nzkx'
                        },
                        'id': 'Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTo3OTE=',
                        'interface': None,
                        'portSpeed': 256,
                        'ppInfo': 'pp_info',
                        'site': {
                            'id': 'U2l0ZU5vZGU6Nzkx',
                            'name': 'Site Name 791'
                        },
                        'termSide': 'A',
                        'upstreamSpeed': 512,
                        'xconnectId': 'xconnect_id'
                    }
                }
            ]
        }
    }
}

snapshots['FieldsTestCase::test_circuit_types 1'] = {
    'data': {
        'circuitTypes': {
            'edges': [
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjMy',
                        'name': 'Type',
                        'slug': 'type'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjEyMw==',
                        'name': 'Type 123',
                        'slug': 'type123'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjExMg==',
                        'name': 'Type112',
                        'slug': 'type112'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjExNQ==',
                        'name': 'Type115',
                        'slug': 'type115'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjExNw==',
                        'name': 'Type117',
                        'slug': 'type117'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjQzNA==',
                        'name': 'Type434',
                        'slug': 'type434'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjc1Ng==',
                        'name': 'Type756',
                        'slug': 'type756'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjc4OQ==',
                        'name': 'Type789',
                        'slug': 'type789'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjc5MQ==',
                        'name': 'Type791',
                        'slug': 'type791'
                    }
                },
                {
                    'node': {
                        'id': 'Q2lyY3VpdFR5cGVOb2RlOjExMQ==',
                        'name': 'TypeX',
                        'slug': 'typex'
                    }
                }
            ]
        }
    }
}

snapshots['FieldsTestCase::test_circuits 1'] = {
    'data': {
        'circuits': {
            'edges': [
                {
                    'node': {
                        'cid': 'cid112',
                        'commitRate': 12,
                        'description': 'desc',
                        'id': 'Q2lyY3VpdE5vZGU6MzI=',
                        'installDate': '2017-10-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjEyNA==',
                            'name': 'Provider 124'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjEyMw==',
                            'name': 'Type 123'
                        }
                    }
                },
                {
                    'node': {
                        'cid': 'ci3d',
                        'commitRate': 12,
                        'description': 'someting',
                        'id': 'Q2lyY3VpdE5vZGU6MTEy',
                        'installDate': '2017-11-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjExMg==',
                            'name': 'Provider112'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjExMg==',
                            'name': 'Type112'
                        }
                    }
                },
                {
                    'node': {
                        'cid': 'cid',
                        'commitRate': 12,
                        'description': 'desc',
                        'id': 'Q2lyY3VpdE5vZGU6MTE3',
                        'installDate': '2017-10-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjExNw==',
                            'name': 'Provider117'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjExNw==',
                            'name': 'Type117'
                        }
                    }
                },
                {
                    'node': {
                        'cid': 'cid',
                        'commitRate': 12,
                        'description': 'desc',
                        'id': 'Q2lyY3VpdE5vZGU6NDM0',
                        'installDate': '2017-10-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjQzNA==',
                            'name': 'Provider434'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjQzNA==',
                            'name': 'Type434'
                        }
                    }
                },
                {
                    'node': {
                        'cid': 'cid',
                        'commitRate': 12,
                        'description': 'desc',
                        'id': 'Q2lyY3VpdE5vZGU6NzU2',
                        'installDate': '2017-10-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjc1Ng==',
                            'name': 'Provider756'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjc1Ng==',
                            'name': 'Type756'
                        }
                    }
                },
                {
                    'node': {
                        'cid': 'cid',
                        'commitRate': 12,
                        'description': 'desc',
                        'id': 'Q2lyY3VpdE5vZGU6Nzg5',
                        'installDate': '2017-10-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjc4OQ==',
                            'name': 'Provider789'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjc4OQ==',
                            'name': 'Type789'
                        }
                    }
                },
                {
                    'node': {
                        'cid': 'cid',
                        'commitRate': 12,
                        'description': 'desc',
                        'id': 'Q2lyY3VpdE5vZGU6Nzkx',
                        'installDate': '2017-10-12',
                        'provider': {
                            'id': 'UHJvdmlkZXJOb2RlOjc5MQ==',
                            'name': 'Provider791'
                        },
                        'tenant': None,
                        'type': {
                            'id': 'Q2lyY3VpdFR5cGVOb2RlOjc5MQ==',
                            'name': 'Type791'
                        }
                    }
                }
            ]
        }
    }
}

snapshots['FieldsTestCase::test_providers 1'] = {
    'data': {
        'providers': {
            'edges': [
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjEyNA==',
                        'name': 'Provider 124',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider124'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjExMg==',
                        'name': 'Provider112',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider112'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjExNQ==',
                        'name': 'Provider115',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider115'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjExNw==',
                        'name': 'Provider117',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider117'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjQzNA==',
                        'name': 'Provider434',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider434'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjc1Ng==',
                        'name': 'Provider756',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider756'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjc4OQ==',
                        'name': 'Provider789',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider789'
                    }
                },
                {
                    'node': {
                        'account': '12345',
                        'asn': 256.0,
                        'comments': 'comments',
                        'id': 'UHJvdmlkZXJOb2RlOjc5MQ==',
                        'name': 'Provider791',
                        'nocContact': 'noc_contact',
                        'portalUrl': 'https://www.nine.ch',
                        'slug': 'provider791'
                    }
                }
            ]
        }
    }
}
