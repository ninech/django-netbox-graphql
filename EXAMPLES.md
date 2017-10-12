## Circuits

### CircuitType

Get all
```
{
  circuitTypes {
    edges {
      node {
        id
        name
        slug
      }
    }
  }
}
```

Create 
```
mutation {
  newCircuitType(input: {name: "Type", slug: "type"}) {
    circuitType {
      name
      slug
    }
  }
}
```

Update
```
mutation {
  updateCircuitType(input: {id:"Q2lyY3VpdFR5cGVOb2RlOjE2", name: "Type1", slug: "type1"}) {
    circuitType {
     id	
      name
      slug
    }
  }
}
```

Delete
```
mutation {
  deleteCircuitType(input: {id: "Q2lyY3VpdFR5cGVOb2RlOjg="}) {
    circuitType {
      name
      slug
    }
  }
}
```

### Provider

Get all
```
{
  providers {
    edges {
      node {
        id
        slug
        name
        asn
        account
        portalUrl
        nocContact
        comments
      }
    }
  }
}
```

Create 
```
mutation {
  newProvider(input: {name: "Provider123", slug: "provider123", asn: 256, account: "account", portalUrl: "http://github.com/", nocContact:"noc", comments: "my comment"}) {
    provider {
      id
      slug
      name
      asn
      account
      portalUrl
      nocContact
      comments
    }
  }
}
```

Update
```
mutation {
  updateProvider(input: {id:"UHJvdmlkZXJOb2RlOjY0", name: "Provider1", slug: "provider1231", asn: 512, account: "account", portalUrl: "http://github.com/", nocContact:"noc", comments: "my comment"}) {
    provider {
      id
      slug
      name
      asn
      account
      portalUrl
      nocContact
      comments
    }
  }
}
```

Delete
```
mutation {
  deleteProvider(input: {id:"UHJvdmlkZXJOb2RlOjY0"}) {
    provider {
      id
      slug
      name
      asn
      account
      portalUrl
      nocContact
      comments
    }
  }
}
```


### Circuit

Get all
```
{
  circuits {
    edges {
      node {
        id
        cid
        provider {
          id
          name
        }
        type {
          id
          name
        }
        tenant {
          id
          name
        }
        installDate
        commitRate
        description
      }
    }
  }
}
```

Create 
```
mutation {
  newCircuit(input: {cid: "cid", provider: "UHJvdmlkZXJOb2RlOjU4", type:"Q2lyY3VpdFR5cGVOb2RlOjMx", installDate:"2017-10-12", commitRate: 12, description:"desc", comments:"dsadsa" }) {
    circuit {
      id
      cid
      provider {
        id
        name
      }
      type {
        id
        name
      }
      installDate
      commitRate
      description
      comments
    }
  }
}
```

Update
```
mutation {
  updateCircuit(input: {id: "Q2lyY3VpdE5vZGU6NA==", cid: "ci3d", provider: "UHJvdmlkZXJOb2RlOjU4", type:"Q2lyY3VpdFR5cGVOb2RlOjQ=", installDate:"2017-11-12", commitRate: 12, description:"someting", comments:"dsadsa" }) {
    circuit {
         id
        cid
        provider {
          id
          name
        }
        type {
          id
          name
        }
        tenant {
          id
          name
        }
        installDate
        commitRate
        description
       comments
    }
  }
}
```

Delete
```
mutation {
  deleteCircuit(input: {id: "Q2lyY3VpdE5vZGU6Mg=="}) {
    circuit {
      id
       cid
        provider {
          id
          name
        }
        type {
          id
          name
        }
        tenant {
          id
          name
        }
        installDate
        commitRate
        description
       comments
    }
  }
}
```

### CircuitTermination

Get all
```
{
  circuitTerminations {
    edges {
      node {
        id
        termSide
        portSpeed
        ppInfo
        upstreamSpeed
        xconnectId
        interface {
          id
          name
        }
        site {
          id
          name
        }
        circuit {
          id
          cid
        }
      }
    }
  }
}
```

Create 
```
mutation {
  newCircuitTermination(input: {circuit: "Q2lyY3VpdE5vZGU6MQ==", portSpeed:128, termSide:"A", upstreamSpeed:128, site:"U2l0ZU5vZGU6MQ==", interface:"SW50ZXJmYWNlTm9kZToz", ppInfo:"ppInfo",xconnectId:"xconnectId" }) {
    circuitTermination {
      id
      termSide
      portSpeed
      ppInfo
      upstreamSpeed
      xconnectId
      interface {
        id
        name
      }
      site {
        id
        name
      }
      circuit {
        id
        cid
      }
    }
  }
}
```

Update
```
mutation {
  updateCircuitTermination(input: {id: "Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTox", portSpeed:512, termSide:"Z", upstreamSpeed:512, ppInfo:"ppInfo123",xconnectId:"xconnectId123" }) {
    circuitTermination {
      id
      termSide
      portSpeed
      ppInfo
      upstreamSpeed
      xconnectId
      interface {
        id
        name
      }
      site {
        id
        name
      }
      circuit {
        id
        cid
      }
    }
  }
}
```

Delete
```
mutation {
  deleteCircuitTermination(input: {id: "Q2lyY3VpdFRlcm1pbmF0aW9uTm9kZTox" }) {
    circuitTermination {
      id
      termSide
      portSpeed
      ppInfo
      upstreamSpeed
      xconnectId
      interface {
        id
        name
      }
      site {
        id
        name
      }
      circuit {
        id
        cid
      }
    }
  }
}
```

# Tenancies

### TenantGroup

Get all
```
{
  tenantGroups {
    edges {
      node {
        id
        name
        slug
      }
    }
  }
}
```

Create 
```
mutation{
  newTenantGroup(input: {name: "TenantGroupA", slug: "tenant-group-A"}) {
    tenantGroup{
      id
      name
      slug
    }
  }
}
```

Update
```
mutation{
  updateTenantGroup(input: {id: "VGVuYW50R3JvdXBOb2RlOjQ=", name: "TenantGroup1", slug: "tenant-group-1"}) {
    tenantGroup{
      id
      name
      slug
    }
  }
}
```

Delete
```
mutation{
  deleteTenantGroup(input: {id: "VGVuYW50R3JvdXBOb2RlOjM="}) {
    tenantGroup{
      id
      name
      slug
    }
  }
}
```

### Tenant

Get all
```
{
  tenants {
    edges {
      node {
        id
        name
        slug
        group {
          id
        }
        description
        comments
      }
    }
  }
}
```

Create 
```
mutation {
  newTenant(input: {name: "Tenant 1", slug: "tenant-1", group: "VGVuYW50R3JvdXBOb2RlOjE=", description: "desc", comments: "comments"}) {
    tenant {
      id
      name
      slug
            group {
        	id
      	} 
      description
      comments
    }
  }
}
```

Update
```
mutation {
  updateTenant(input: {id: "VGVuYW50Tm9kZTox", name: "Tenant A", slug: "tenant-A", group: "VGVuYW50R3JvdXBOb2RlOjE=", description: "descA", comments: "commentsA"}) {
    tenant {
      id
      name
      slug
      group {
        id
      } 
      description
      comments
    }
  }
}
```

Delete
```
mutation {
  deleteTenant(input: {id: "VGVuYW50Tm9kZTox"}) {
    tenant {
      id
      name
      slug
      group {
        id
      } 
      description
      comments
    }
  }
}
```

# DCIM

### Region

Get all
```
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
```

Create 
```
mutation{
  newRegion(input: { parent:"UmVnaW9uTm9kZTo0", name: "Region 1", slug: "region-1"}) {
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
```

Update
```
mutation{
  updateRegion(input: { id:"UmVnaW9uTm9kZTo1", parent:"UmVnaW9uTm9kZTo0", name: "Region C", slug: "region-c"}) {
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
```

Delete
```
mutation{
  deleteRegion(input: { id:"UmVnaW9uTm9kZTo1"}) {
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
```

### Site

Get all
```
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
```

Create 
```
mutation{
  newSite(input: { name:"Site 3", slug: "site3", region:"UmVnaW9uTm9kZTo0", tenant: "VGVuYW50Tm9kZToy", facility: "A", 
    asn: 12, physicalAddress:"A1", shippingAddress: "A2", contactName: "Name", contactPhone: "123",  contactEmail:"a@gmail.com", comments: "comments"}) {
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
```

Update
```
mutation{
  updateSite(input: { id: "U2l0ZU5vZGU6Ng==" name:"Site 5", slug: "site6", region:"UmVnaW9uTm9kZTo0", tenant: "VGVuYW50Tm9kZToy", facility: "A", asn: 12, physicalAddress:"A1", shippingAddress: "A2", contactName: "Name", contactPhone: "456",  contactEmail:"a@gmail.com", comments: "comments"}) {
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
```

Delete
```
mutation{
 deleteSite(input: { id:"U2l0ZU5vZGU6Ng==" }) {
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
```

# IPAM

### Role

Get all
```
{
  vlanRoles {
    edges {
      node {
        id
        slug
        name
        weight        
      }
    }
  }
}
```

Create 
```
mutation{
  newVlanRole(input: { name: "VlanRole 1", slug: "vlanrole-1", weight: 1001}) {
    vlanRole{
      id
      name
      slug
      weight
    }
  }
}
```

Update
```
mutation{
  updateVlanRole(input: { id: "Um9sZU5vZGU6Ng==", name: "VlanRole A", slug: "vlanrole-a", weight: 1002}) {
    vlanRole{
      id
      name
      slug
      weight
    }
  }
}
```

Delete
```
mutation{
  deleteVlanRole(input: { id: "Um9sZU5vZGU6Ng==" }) {
    vlanRole{
      id
      name
      slug
      weight
    }
  }
}
```
