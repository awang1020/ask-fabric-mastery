// Azure OpenAI account + chat/embedding deployments.
@description('Cognitive Services account name (also used as the custom subdomain).')
param name string

@description('Azure region.')
param location string

param chatDeployment string
param chatModel string
param chatModelVersion string
param chatSkuName string
param chatCapacity int

param embeddingDeployment string
param embeddingModel string
param embeddingModelVersion string
param embeddingSkuName string
param embeddingCapacity int

param tags object = {}

resource account 'Microsoft.CognitiveServices/accounts@2024-10-01' = {
  name: name
  location: location
  kind: 'OpenAI'
  sku: {
    name: 'S0'
  }
  tags: tags
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    customSubDomainName: name
    publicNetworkAccess: 'Enabled'
    disableLocalAuth: false
    networkAcls: {
      defaultAction: 'Allow'
    }
  }
}

resource chatDeploy 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: account
  name: chatDeployment
  sku: {
    name: chatSkuName
    capacity: chatCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: chatModel
      version: chatModelVersion
    }
    raiPolicyName: 'Microsoft.DefaultV2'
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
}

resource embeddingDeploy 'Microsoft.CognitiveServices/accounts/deployments@2024-10-01' = {
  parent: account
  name: embeddingDeployment
  sku: {
    name: embeddingSkuName
    capacity: embeddingCapacity
  }
  properties: {
    model: {
      format: 'OpenAI'
      name: embeddingModel
      version: embeddingModelVersion
    }
    versionUpgradeOption: 'OnceNewDefaultVersionAvailable'
  }
  // Azure throttles parallel deployment creation under the same account; serialize them.
  dependsOn: [
    chatDeploy
  ]
}

output name string = account.name
output endpoint string = account.properties.endpoint
