import pytest
from graphene.test import Client
from snapshottest import TestCase
from .data import initialize_region
from ..schema import schema
from dcim.models import Tenant
from dcim.models import Device, Interface, Site, Region

pytestmark = pytest.mark.django_db

class FieldsTestCase(TestCase):
    def test_regions(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          regions {
            edges {
              node {
                id
                name
                slug
                parent {
                  name
                }
              }
            }
          }
        }
        '''))

    def test_sites(self):
        client = Client(schema)
        self.assertMatchSnapshot(client.execute('''
        {
          sites {
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
        '''))

class RegionTestCase(TestCase):
    def test_creating_new_region(self):
        initialize_region('11')
        query = '''
        mutation{
          newRegion(input: { parent:"UmVnaW9uTm9kZToxMQ==", name: "Region 1", slug: "region-1"}) {
            region{
              id
              name
              slug
              parent{
                name
              }
            }
          }
        }
        '''
        expected = {'newRegion': {'region': {'id': 'UmVnaW9uTm9kZTox', 'name': 'Region 1', 'slug': 'region-1',
                                             'parent': {'name': 'Region11'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_correct_fetch_of_region(self):
        initialize_region('12')
        query = '''
        {
          regions(id: "UmVnaW9uTm9kZToxMg==") {
            edges {
              node {
                name
                slug
              }
            }
          }
        }
        '''
        expected = {'regions': {
            'edges': [{'node': {'name': 'Region12', 'slug': 'region-12'}}]}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_update_region(self):
        initialize_region('13')
        initialize_region('14')
        query = '''
        mutation{
          updateRegion(input: { id:"UmVnaW9uTm9kZToxMw==", parent:"UmVnaW9uTm9kZToxNA==", name: "Region C", slug: "region-c"}) {
            region{
              id
              name
              slug
              parent{
                name
              }
            }
          }
        }
        '''
        expected = {'updateRegion': {'region': {'id': 'UmVnaW9uTm9kZToxMw==', 'name': 'Region C', 'slug': 'region-c',
                                                'parent': {'name': 'Region14'}}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

    def test_delete_region(self):
        initialize_region('14')
        query = '''
        mutation{
          deleteRegion(input: { id:"UmVnaW9uTm9kZToxNA=="}) {
            region{
              id
              name
              slug
            }
          }
        }
        '''
        expected = {'deleteRegion': {'region': {'id': 'UmVnaW9uTm9kZTpOb25l', 'name': 'Region14', 'slug': 'region-14'}}}

        result = schema.execute(query)
        assert not result.errors
        assert result.data == expected

