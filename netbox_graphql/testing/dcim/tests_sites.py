import pytest
from graphene.test import Client
from snapshottest import TestCase
from netbox_graphql.testing.data import *
from netbox_graphql.schema import schema
from circuits.models import CircuitType, Circuit, Provider, CircuitTermination

pytestmark = pytest.mark.django_db


class SiteTestCase(TestCase):
    def test_creating_new_site(self):
        initialize_region('18')
        initialize_tenant('18')
        query = '''
        mutation{
          newSite(input: { name:"Site 3", slug: "site3", region:"UmVnaW9uTm9kZToxOA==", tenant: "VGVuYW50Tm9kZToxOA==",
           facility: "A", asn: 12, physicalAddress:"A1", shippingAddress: "A2", contactName: "Name",
           contactPhone: "123",  contactEmail:"a@gmail.com", comments: "comments"}) {
            site {
            id
            name
            slug
            region {
              name
            }
            tenant {
              name
            }
            facility
            asn
            physicalAddress
            shippingAddress
            contactName
            contactPhone
            contactEmail
            comments
            }
          }
        }
        '''
        expected = {'newSite': {
            'site': {'id': 'U2l0ZU5vZGU6MQ==', 'name': 'Site 3', 'slug': 'site3', 'region': {'name': 'Region18'},
                     'tenant': {'name': 'Tenant 18'}, 'facility': 'A', 'asn': 12.0, 'physicalAddress': 'A1',
                     'shippingAddress': 'A2', 'contactName': 'Name', 'contactPhone': '123',
                     'contactEmail': 'a@gmail.com', 'comments': 'comments'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_site(self):
        initialize_site('16')
        query = '''
        {
          sites(id: "U2l0ZU5vZGU6MTY=") {
            edges {
              node {
                id
                name
                slug
                region {
                  name
                }
                tenant {
                  name
                }
                facility
                asn
                physicalAddress
                shippingAddress
                contactName
                contactPhone
                contactEmail
                comments
              }
            }
          }
        }
        '''
        expected = {'sites': {'edges': [{'node': {'id': 'U2l0ZU5vZGU6MTY=', 'name': 'Site Name 16', 'slug': 'site-name 16',
                                                  'region': {'name': 'Region16'}, 'tenant': {'name': 'Tenant 16'},
                                                  'facility': 'fac', 'asn': 12.0, 'physicalAddress': 'A1',
                                                  'shippingAddress': 'A2', 'contactName': 'Name', 'contactPhone': '123',
                                                  'contactEmail': 'a@gmail.com', 'comments': 'comment'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_site(self):
        initialize_site('17')
        query = '''
        mutation{
          updateSite(input: { id: "U2l0ZU5vZGU6MTc=" name:"Site 5", slug: "site6", facility: "A", asn: 12,
          physicalAddress:"A1", shippingAddress: "A2",
          contactName: "Name", contactPhone: "456",  contactEmail:"a@gmail.com", comments: "comments"}) {
            site {
            id
            name
            slug
            region {
              name
            }
            tenant {
              name
            }
            facility
            asn
            physicalAddress
            shippingAddress
            contactName
            contactPhone
            contactEmail
            comments
            }
          }
        }
        '''
        expected = {'updateSite': {
            'site': {'id': 'U2l0ZU5vZGU6MTc=', 'name': 'Site 5', 'slug': 'site6', 'region': {'name': 'Region17'},
                     'tenant': {'name': 'Tenant 17'}, 'facility': 'A', 'asn': 12.0, 'physicalAddress': 'A1',
                     'shippingAddress': 'A2', 'contactName': 'Name', 'contactPhone': '456',
                     'contactEmail': 'a@gmail.com', 'comments': 'comments'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_site(self):
        initialize_site('15')
        query = '''
        mutation{
         deleteSite(input: { id:"U2l0ZU5vZGU6MTU=" }) {
            site {
            id
            name
            slug
            region {
              name
            }
            tenant {
              name
            }
            facility
            asn
            physicalAddress
            shippingAddress
            contactName
            contactPhone
            contactEmail
            comments
            }
          }
        }
        '''
        expected = {'deleteSite': {
            'site': {'id': 'U2l0ZU5vZGU6Tm9uZQ==', 'name': 'Site Name 15', 'slug': 'site-name 15', 'region': {'name': 'Region15'},
                     'tenant': {'name': 'Tenant 15'}, 'facility': 'fac', 'asn': 12.0, 'physicalAddress': 'A1',
                     'shippingAddress': 'A2', 'contactName': 'Name', 'contactPhone': '123',
                     'contactEmail': 'a@gmail.com', 'comments': 'comment'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected
