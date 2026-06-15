---
title: FabCon & SQLCon 2026 : l’événement à ne pas rater !
url: https://antoinewang.substack.com/p/fabcon-and-sqlcon-2026
date: 2026-03-20
author: Antoine Wang
source: substack
---

# FabCon & SQLCon 2026 : l’événement à ne pas rater !

Bonjour à tous, je suis **Antoine Wang**.

J’aide les profils techniques à maîtriser l’architecture de Microsoft Fabric, et j’aide les décideurs à comprendre l’impact réel de cette technologie, sans le jargon inutile.

Mon objectif ? Vulgariser le complexe et vous donner les clés pour maîtriser Microsoft Fabric, une plateforme de données SaaS unifiée et alimentée par l’IA pour simplifier la gestion des données et l’analyse.

Cette newsletter est 100% gratuite. En vous abonnant maintenant, vous recevrez en exclusivité mon “One-Pager” pour cartographier l’ensemble de la solution Fabric en un coup d’œil.

Merci à celles et ceux qui me suivent depuis le début. Sans plus attendre, entrons dans le vif du sujet !

---

## Annonce : FabCon & SQLCon 2026 !

FabCon et SQLCon 2026 se sont tenus cette semaine à Atlanta ! Avec 8 000 participants, 300 sessions et de nombreux ateliers, l’événement a fait le plein de nouveautés que j’ai hâte de vous partager.

### Le rendez-vous mondial de l’écosystème Data

Il s’agit du plus grand rassemblement mondial dédié à **Microsoft Fabric**. Organisée chaque année, cette conférence en est à sa troisième édition, elle réunit passionnés de technologie, innovateurs et leaders du secteur pour explorer l’avenir des données, de l’analytique, de la Business Intelligence et de l’intégration de l’IA.

Cet événement dynamique permet de découvrir les dernières innovations de la plateforme, d’assister à des sessions d’experts, de suivre les interventions clés de Microsoft et de networker avec des pairs du monde entier.

### Une vision unifiée : La convergence SQL & Fabric

Cette année marque un tournant : pour la première fois, SQLCon rejoint FabCon. Cette union illustre une stratégie claire : unifier le monde des bases de données opérationnelles et celui de l’analytique au sein d’une plateforme unique.

Les chiffres parlent d’eux-mêmes :

* **Microsoft Fabric** compte désormais plus de 31 000 clients actifs, devenant la plateforme data à la croissance la plus rapide de l’histoire de Microsoft.
* **SQL Server 2025** progresse déjà deux fois plus vite que la version précédente.

Je vous propose de résumer les points essentiels annoncés sur le blog officiel de Microsoft par **Arun Ulag**, Vice-Président Corporatif, Azure Data.

---

## 1. Le Database Hub : une console pour toutes vos bases de données

À mesure que les ensembles de données s’étoffent, la complexité opérationnelle augmente également. La plupart des organisations gèrent un mélange de bases de données relationnelles et NoSQL dans des environnements edge, PaaS et SaaS, souvent via des outils, des portails et des expériences de gestion fragmentés.

Microsoft vient d’annoncer le **Database Hub dans Microsoft Fabric**, disponible en early access.

L’idée est simple : il s’agit d’un véritable plan de contrôle (control plane), un seul endroit pour observer, gouverner et optimiser l’ensemble de votre patrimoine de bases de données (Azure SQL, Cosmos DB, PostgreSQL, …).

Ce qui change concrètement :

* **Observabilité centralisée** : vous voyez l’état de toutes vos bases depuis un seul écran, le Hub montre les problèmes urgents et les opportunités d'optimisation (sécurité, conformité, utilisation de votre moteur de calcul) pour faciliter la prise de décision.
* **Agents assistés par Copilot** : l'agent corrèle les signaux à travers tout le parc (requêtes, temps d'attente, verrous de schémas) pour identifier la cause racine exacte d'un blocage et proposer une résolution ciblée.
* **Le maintien strict du contrôle humain** : L'agent opère dans des limites de sécurité (RBAC) strictes. Il propose une action et explique son raisonnement avec des alertes claires, mais l'administrateur garde le contrôle absolu pour valider ou ajuster avant exécution

> 💡 **Astuce :** Utilisez le Database Hub pour repérer instantanément vos bases sous-utilisées ou les requêtes mal optimisées avant même de penser à augmenter le *Capacity* (CU) de votre workspace Fabric. L’agent fera le travail d’analyse complexe à votre place.

---

## 2. Unifiez votre patrimoine de données avec Microsoft OneLake

Le Mirroring dans Fabric, c’est la brique qui permet de répliquer vos données opérationnelles dans OneLake sans pipeline ETL customisé. Ce qui était déjà un gain énorme devient encore plus large.

Ce qui vient d’être annoncé :

* **Disponibilité Générale (GA) :** SAP Datasphere et Oracle.
* **Preview** : SharePoint Lists et Dremio.
* **À venir** : Azure Monitor.

De plus, les Shortcut Transformations passent en GA, et la conversion Excel en tables Delta spécifiquement est encore en Preview.

Enfin, côté interopérabilité, la lecture native depuis OneLake via Azure Databricks Unity Catalog est en public preview, et l’interopérabilité avec Snowflake est désormais GA.

---

## 3. L’analytique Fabric s’industrialise : Runtime 2.0 et Materialized Lake Views

Deux annonces qui vont changer concrètement le quotidien des data engineers :

**Runtime 2.0 (Preview)**

* Apache Spark 4.x + Delta Lake 4.x + Scala 2.13
* Conçu pour les charges de calcul à grande échelle
* Nouvelle expérience Copilot dans les notebooks : plus contextuelle, qui raisonne sur votre Workspace, génère du code avec plus de précision

**Materialized Lake Views (Disponibilité Générale)**

Dans une Architecture Medallion, vous écrivez du SQL ou du PySpark pour transformer Bronze → Silver → Gold, puis vous orchestrez tout ça manuellement avec des pipelines.

Les Materialized Lake Views (MLV) permettent de définir ces transformations de manière déclarative, elles s’actualisent automatiquement, sans orchestration manuelle.

**Nouveautés :**

* Les MLV prennent désormais en charge plusieurs planifications par lakehouse.

* Prise en charge de PySpark pour les MLV (Preview) : cela permet aux ingénieurs de données de créer, d’actualiser et de remplacer des MLV à partir de notebooks Fabric à l’aide de l’API DataFrameWriter.

C’est la fin du “j’ai oublié de relancer le pipeline Silver ce matin”.

> ⚠️ **Ne confondez pas Materialized Lake Views et vues SQL classiques.** Les vues SQL du SQL Endpoint sont read-only et recalculées à la requête. Les Materialized Lake Views matérialisent physiquement le résultat dans OneLake. Ce sont deux briques très différentes pour des usages différents.

---

## 4. Fabric IQ : la couche sémantique devient le carburant de vos agents

L’annonce la plus structurante de cette FabCon 2026 !

Fabric IQ est une couche sémantique qui unifie données analytiques et données opérationnelles dans un cadre de concepts métier : entités, relations, propriétés, règles, actions. Concrètement : au lieu que vos agents IA raisonnent sur des tables SQL et des schémas techniques, ils raisonnent sur des concepts que votre équipe métier reconnaît, comme “client”, “commande”, “territoire de vente”.

Les annonces clés :

* **Ontologies via MCP Server (Preview)** : vos agents externes peuvent découvrir et interroger la couche sémantique Fabric IQ via le protocole MCP
* **Direct Lake on OneLake (GA**) : les semantic models lisent directement depuis OneLake avec enforcement de la sécurité natif, sans déplacement de données, performances proches de l’import
* **Graph in Fabric (GA dans les prochaines semaines)** : requêtez les relations complexes entre clients, partenaires, chaîne d’approvisionnement
* **Planning in Fabric IQ** (voir la démo!) : une nouvelle fonctionnalité de planification d’entreprise qui permet aux organisations de créer des plans, des budgets, des prévisions et des modèles de scénarios directement sur les modèles sémantiques de Fabric.

---

## 5. Deux agents complémentaires : Data & Operations

**Fabric Data Agents (GA) !**

Ce n’est plus une preview. Vous pouvez les déployer en production, les connecter à vos Lakehouses, Warehouses, KQL databases, et semantic models. Vos agents peuvent être exposés dans Microsoft Foundry, Copilot Studio, ou Microsoft 365 Copilot.

De plus, les **Operations Agents** sont la nouveauté complémentaire : là où les Data Agents sont des “analystes virtuels” qui répondent à des questions, les Operations Agents surveillent les données en temps réel, détectent des patterns, et prennent des actions proactives. Regardons la démonstration ci-dessous !

---

## Conclusion

Si tu dois retenir une chose : FabCon 2026 marque le moment où Microsoft a officiellement fusionné le monde des bases de données opérationnelles et le monde de l’analytique dans une seule plateforme cohérente. Le Database Hub, Fabric IQ, les Data Agents en GA, ce ne sont pas des features additionnelles. Ce sont les fondations d’une architecture où vos agents IA raisonnent sur la réalité de votre entreprise, pas seulement sur des tables SQL.

Ces annonces ne sont pas toutes à déployer demain en production. La valeur de cette veille, c’est de savoir ce qui est mûr pour vos projets actuels et ce qui mérite d’être mis en pilote dans les prochains mois. Un arbitrage éclairé vaut mieux qu’une adoption précipitée.

> **Et vous, quelle nouveauté va le plus impacter votre quotidien ?** Répondez simplement à cet email ou ce post, je lis tous vos messages.

À la semaine prochaine pour continuer à explorer ensemble les entrailles de Fabric !

---

## 📚 Ressources pour aller plus loin

🔗 [Blog officiel FabCon & SQLCon 2026 — Arun Ulag](https://azure.microsoft.com/en-us/blog/fabcon-and-sqlcon-2026-unifying-databases-and-fabric-on-a-single-data-platform/)
