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

