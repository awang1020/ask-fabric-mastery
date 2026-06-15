using './main.bicep'

param location = 'eastus2'
param resourceGroupName = 'rg-ask-fabric-mastery'

param chatDeployment = 'gpt-4o-mini'
param chatModel = 'gpt-4o-mini'
param chatModelVersion = '2024-07-18'
param chatSkuName = 'GlobalStandard'
param chatCapacity = 50

param embeddingDeployment = 'text-embedding-3-small'
param embeddingModel = 'text-embedding-3-small'
param embeddingModelVersion = '1'
param embeddingSkuName = 'GlobalStandard'
param embeddingCapacity = 50
