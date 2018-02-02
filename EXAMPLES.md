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

### Vlan Role

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
 
 ### VLAN Group
 
 Get all
```
{
  vlanGroups {
    edges {
      node {
        id
        name
        slug
        site {
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
  newVlanGroup(input: { name: "VlanRole 1", slug: "vlanrole-1", site: "U2l0ZU5vZGU6MQ=="}) {
    vlanGroup{
      id
      name
      slug
      site {
        name
      }
    }
  }
}
```
 
 Update
```
mutation{
  updateVlanGroup(input: { id:"VkxBTkdyb3VwTm9kZToy", name: "VlanRole A", slug: "vlanrole-A", site: "U2l0ZU5vZGU6MQ=="}) {
    vlanGroup{
      id
      name
      slug
      site {
        name
      }
    }
  }
}
```
 
 Delete
```
mutation{
  deleteVlanGroup(input: { id:"VkxBTkdyb3VwTm9kZToy"}) {
    vlanGroup{
      id
      name
      slug
      site {
        name
      }
    }
  }
}
```

 ### VLAN
 
 Get all
```
 { vlans {
    edges {
      node {
        id
        name
        description
        vid
        site{
          name
        }
        group{
          name
        }
        tenant{
          name
        }
        role{
          name
        }
      }
    }
  }
```
 
 Create 
```
mutation{
  newVlan(input: {  site: "U2l0ZU5vZGU6MQ==", group: "VkxBTkdyb3VwTm9kZTox", tenant: "VGVuYW50Tm9kZToy", role: "Um9sZU5vZGU6NA==", vid: 2, name: "vlan2", description: "test"}) {
    vlan{
      id
      name
      site {
        name
      }
      group{
        name
      } 
      tenant{
        name
      }
      role{
        name
      }
      vid
      name
      description
    }
  }
}
```
 
 Update
```
mutation{
  updateVlan(input: { id:"VkxBTk5vZGU6Mg==", site: "U2l0ZU5vZGU6MQ==", group: "VkxBTkdyb3VwTm9kZTox", tenant: "VGVuYW50Tm9kZToy", role: "Um9sZU5vZGU6NA==", vid: 3, name: "vlanA", description: "desc"}) {
    vlan{
      id
      name
      site {
        name
      }
      group{
        name
      } 
      tenant{
        name
      }
      role{
        name
      }
      vid
      name
      description
    }
  }
}
```
 
 Delete
```
mutation{
  deleteVlan(input: { id:"VkxBTk5vZGU6Mg=="}) {
    vlan{
      id      
    }
  }
}
```

### VRF
 Get all
```
{
  vrfs {
    edges {
      node {
        id
        name
        rd    
        description
        enforceUnique
        tenant {
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
  newVrf(input: { tenant: "VGVuYW50Tm9kZToy",  name: "vrf", rd: "rd", enforceUnique: true, description: "desc" }) {
    vrf{
        id
        name
        rd    
        description
        enforceUnique
        tenant {
        name
      }      
    }
  }
}
```
 
 Update
```
mutation{
  updateVrf(input: { id: "VlJGTm9kZToy", tenant: "VGVuYW50Tm9kZToy",  name: "vrfA", rd: "rd", enforceUnique: true, description: "desc" }) {
    vrf{
        id
        name
        rd    
        description
        enforceUnique
        tenant {
        name
      }      
    }
  }
}
```
 
 Delete
```
mutation{
  deleteVrf(input: { id: "VlJGTm9kZTox" }) {
    vrf{
       id    
    }
  }
}
```

### RIR
 Get all
```
{
  rirs {
    edges {
      node {
        id
        name
        slug
        isPrivate
      }
    }
  }
}
```
 
 Create 
```
mutation{
  newRir(input: { name: "rir",  slug: "rir", isPrivate: true }) {
    rir{
        id
        name
        slug
        isPrivate     
    }
  }
}
```
 
 Update
```
mutation{
  updateRir(input: { id:"UklSTm9kZTo3", name: "rirA",  slug: "rira", isPrivate: true }) {
    rir{
        id
        name
        slug
        isPrivate     
    }
  }
}
```
 
 Delete
```
mutation{
  deleteRir(input: { id:"UklSTm9kZTo3" }) {
    rir{
        id
        name
        slug
        isPrivate     
    }
  }
}
```

### Aggregate
 Get all
```
{
  aggregates {
    edges {
      node {
        id
        family
        prefix
        rir {
          id
          name
        }
        dateAdded
       description
      }
    }
  }
}
```
 
 Create 
```
mutation{
  newAggregate(input: { family: 4, prefix: "173.16.0.0/12", rir: "UklSTm9kZTo1", dateAdded: "2015-01-01", description: "desc" }) {
    aggregate{
        id
        family
        prefix
        rir {
          id
          name
        }
        dateAdded
        description   
    }
  }
}
```
 
 Update
```
mutation{
  updateAggregate(input: { id: "QWdncmVnYXRlTm9kZTox", rir: "UklSTm9kZTo1", dateAdded: "2017-01-01", description: "desc", prefix: "14.0.0.0/8"}) {
    aggregate{
        id
        family
        prefix
        rir {
          id
          name
        }
    	dateAdded
        description 
    }
  }
}
```
 
 Delete
```
mutation{
  deleteAggregate(input: { id: "QWdncmVnYXRlTm9kZTox"}) {
    aggregate{
        id
        family
        prefix
        rir {
          id
          name
        }
        dateAdded
        description 
    }
  }
}
```

### IPAddress
Get all
```
{
  ipAddress {
    edges {
      node {
        id
        family
        address
        vrf {
          name
        }
        tenant {
          name
        }
        interface {
          name
        }
        natInside {
          id
        }
        natOutside {
          id
        }
        description
        status        
      }
    }
  }
}
```
 
 Create 
```
mutation{
  newIpAddress(input: { address: "173.16.0.0/12", vrf: "VlJGTm9kZToz", tenant: "VGVuYW50Tm9kZToy", interface: "SW50ZXJmYWNlTm9kZTox", natInside: "SVBBZGRyZXNzTm9kZTox", description: "desc", status: 1}) {
    ipAddress{
     	id
        family
        address
        vrf {
          name
        }
        tenant {
          name
        }
        interface {
          name
        }
        natInside {
          id
        }
        natOutside {
          id
        }
        description
        status  
    }
  }
}
```
 
 Update
```
mutation{
  updateIpAddress(input: { id:"SVBBZGRyZXNzTm9kZTox", address: "177.12.0.0/24", vrf: "VlJGTm9kZToz", tenant: "VGVuYW50Tm9kZToy", interface: "SW50ZXJmYWNlTm9kZTox", description: "txt", status: 1}) {
    ipAddress{
     	id
        family
        address
        vrf {
          name
        }
        tenant {
          name
        }
        interface {
          name
        }
        natInside {
          id
        }
        natOutside {
          id
        }
        description
        status  
    }
  }
}
```
 
 Delete
```
mutation{
  deleteIpAddress(input: { id:"SVBBZGRyZXNzTm9kZTox"}) {
    ipAddress{
        id
        family
        address
    }
  }
}
```

### Prefix
Get all
```
{
  prefixes {
    edges {
      node {
        id
        family
        prefix
        site {
          id
        }
        vrf {
          id
        }
        tenant {
          id
        }
        vlan {
          id
        }
        status
        role {
          id
        }
        isPool
        description
      }
    }
  }
}
```
 
 Create 
```
mutation{
  newPrefix(input: { prefix: "173.16.0.0/12", description: "desc", site: "U2l0ZU5vZGU6MQ==", vrf: "VlJGTm9kZToz", tenant: "VGVuYW50Tm9kZToy", status: 1, role: "Um9sZU5vZGU6NA==", isPool: false}) {
    prefix{
        id
      	description
        family
        prefix
        site {
          id
        }
        vrf {
          id
        }
        tenant {
          id
        }
        vlan {
          id
        }
        status
        role {
          id
        }
        isPool        
    }
  }
}
```
 
 Update
```
mutation{
  updatePrefix(input: { id: "UHJlZml4Tm9kZToxMQ==", prefix: "173.16.0.0/24", description: "txt", site: "U2l0ZU5vZGU6MQ==", vrf: "VlJGTm9kZToz", tenant: "VGVuYW50Tm9kZToy", status: 2, role: "Um9sZU5vZGU6NA==", isPool: true}) {
    prefix{
        id
      	description
        family
        prefix
        site {
          id
        }
        vrf {
          id
        }
        tenant {
          id
        }
        vlan {
          id
        }
        status
        role {
          id
        }
        isPool        
    }
  }
}
```
 
 Delete
```
mutation{
  deletePrefix(input: {id: "UHJlZml4Tm9kZToxMQ=="}) {
    prefix{
        id
        description
        family
        prefix
        site {
          id
        }
        vrf {
          id
        }
        tenant {
          id
        }
        vlan {
          id
        }
        status
        role {
          id
        }
        isPool        
    }
  }
}
```

## Virtualization

### ClusterType

Get all
```
{
  clusterGroups {
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
  newClusterGroup(input: { name: "clusterGroup1", slug: "clusterGroup1"}) {
    clusterGroup{
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
  updateClusterGroup(input: { id: "Q2x1c3Rlckdyb3VwTm9kZTox", name: "clusterGroupA", slug: "clusterGroupA"}) {
    clusterGroup{
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
  deleteClusterGroup(input: { id: "Q2x1c3Rlckdyb3VwTm9kZTox"}) {
    clusterGroup{
      id
      name
      slug
    }
  }
}
```

### ClusterGroup

Get all
```
{
  clusterTypes {
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
  newClusterType(input: { name: "clusterType1", slug: "clustertype1"}) {
    clusterType{
      id
      name
      slug
    }
  }
}
```

Update
```
mutation{
  updateClusterType(input: { id: "Q2x1c3RlclR5cGVOb2RlOjI=", name: "clusterTypeA", slug: "clustertypeA"}) {
    clusterType{
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
  deleteClusterType(input: { id: "Q2x1c3RlclR5cGVOb2RlOjI="}) {
    clusterType{
      id
      name
      slug
    }
  }
}
```


### Cluster

Get all
```
{
  clusters {
    edges {
      node {
        id
        name
        type {
          id
        }
        group {
          id
        }
        site {
          id
        }
      }
    }
  }
}
```

Create 
```
mutation{
  newCluster(input: { name: "clusterA", type: "Q2x1c3Rlck5vZGU6MQ=="}) {
    cluster{
      id
      name
      type {
        id
      }
      group {
        id
      }
      site {
        id
      }
    }
  }
}
```

Update
```
mutation{
  updateCluster(input: { id:"Q2x1c3Rlck5vZGU6Mg==", name: "clusterB", type: "Q2x1c3Rlck5vZGU6MQ=="}) {
    cluster{
      id
      name
      type {
        id
      }
      group {
        id
      }
      site {
        id
      }
    }
  }
}
```

Delete
```
mutation{
  deleteCluster(input: { id:"Q2x1c3Rlck5vZGU6Mg=="}) {
    cluster{
      id
      name
      type {
        id
      }
      group {
        id
      }
      site {
        id
      }
    }
  }
}
```

### Virtual Machine

Get all
```
{
  virtualMachines {
    edges {
      node {
        id
        cluster {
          id
        }
        tenant {
          id
        }
        platform {
          id
        }
        name
        status
        role {
          id
        }
        primaryIp4 {
          id
        }
        primaryIp6 {
          id
        }
        vcpus
        memory
        disk
        comments
        }
      }
    }
}
```

Create 
```
mutation{
  newVirtualMachine(input: { cluster:"Q2x1c3Rlck5vZGU6MQ==", name: "virtual machine", status: 1, primaryIp4: "SVBBZGRyZXNzTm9kZTox", primaryIp6:"SVBBZGRyZXNzTm9kZToy", vcpus: 12, memory:126, disk: 256, comments: "test" }) {
    virtualMachine{
        id
        cluster {
          id
        }
        tenant {
          id
        }
        platform {
          id
        }
        name
        status
        role {
          id
        }
        primaryIp4 {
          id
        }
        primaryIp6 {
          id
        }
        vcpus
        memory
        disk
        comments
    }
  }
}

```

Update
```
mutation{
  updateVirtualMachine(input: { id: "VmlydHVhbE1hY2hpbmVOb2RlOjI=", cluster:"Q2x1c3Rlck5vZGU6MQ==", name: "virtual machine", status: 1, primaryIp4: "SVBBZGRyZXNzTm9kZTox", vcpus: 12, memory:256, disk: 512, comments: "test" }) {
    virtualMachine{
				id
        cluster {
          id
        }
        tenant {
          id
        }
        platform {
          id
        }
        name
        status
        role {
          id
        }
        primaryIp4 {
          id
        }
        primaryIp6 {
          id
        }
        vcpus
        memory
        disk
        comments
    }
  }
}
```

Delete
```
mutation{
  deleteVirtualMachine(input: { id: "VmlydHVhbE1hY2hpbmVOb2RlOjI=" }) {
    virtualMachine{
         id
        cluster {
          id
        }
        tenant {
          id
        }
        platform {
          id
        }
        name
        status
        role {
          id
        }
        primaryIp4 {
          id
        }
        primaryIp6 {
          id
        }
        vcpus
        memory
        disk
        comments
    }
  }
}
```
