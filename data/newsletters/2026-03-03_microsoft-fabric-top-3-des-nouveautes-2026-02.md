---
title: Microsoft Fabric : Top 3 des nouveautés de Février 2026 (+ Bonus)
url: https://antoinewang.substack.com/p/microsoft-fabric-top-3-des-nouveautes-2026-02
date: 2026-03-03
author: Antoine Wang
source: substack
---

# Microsoft Fabric : Top 3 des nouveautés de Février 2026 (+ Bonus)

Bienvenue dans cette 2ème édition des nouveautés de Microsoft Fabric.

Mon objectif aujourd’hui n’est donc pas de vous lister toutes les features du mois, mais de me concentrer sur 3 fonctionnalités qui vont avoir un impact immédiat sur la stabilité de vos déploiements. C’est parti !

---

### 1. Dataflow Gen2 : La fin du cauchemar CI/CD avec les Références Relatives

L’un des principes fondamentaux de **Fabric** et **Data Factory** est de proposer des solutions compatibles avec l’intégration continue et la livraison continue (CI/CD).

En septembre 2025, dans Dataflow Gen2, vous pouvez déjà utiliser des **paramètres publics** et les **bibliothèques de variables** Fabric pour rendre vos solutions dynamiques et compatibles avec les différents pipelines de déploiement.

Aujourd’hui, une nouvelle fonctionnalité permet de simplifier les scénarios CI/CD lors de l’utilisation des connecteurs **Fabric : les références relatives**.

**Pourquoi c’est un problème pour vos équipes ?**

* Historiquement, quand vous développiez un Dataflow Gen2 en environnement de “Dev”, l’ID du Lakehouse source était codé en dur dans le script M.
* Lors du déploiement via pipeline (CI/CD) vers “Test” ou “Prod”, le flux cassait car il cherchait l’ID de l’environnement de Dev.
* Il fallait alors bricoler avec des paramètres publics ou des bibliothèques de variables.

**Comment le résoudre :**

* Ce manque de portabilité freinait l’adoption de pratiques DevOps saines.
* La solution est immédiate : utiliser le **nœud** `(Current Workspace)` pour que le flux se connecte automatiquement au Lakehouse portant le même nom dans l’espace de travail cible, sans aucune modification de script.

**La réalité du terrain :**

* ✅ **Bénéfices :** Vos flux sont enfin “CI/CD-ready” nativement. Vous passez d’un environnement à l’autre sans toucher une ligne de code, ce qui sécurise massivement vos mises en production.
* ⚠️ **Limitation :** Cela exige une hygiène irréprochable sur le nommage de vos items. Si votre Lakehouse s’appelle “LH\_Dev” en développement et “LH\_Prod” en production, la référence relative ne trouvera pas sa cible. Le nom doit être identique partout.

**Mon conseil :** Standardisez vos conventions de nommage dès aujourd’hui (ex: “LH\_Sales\_Core”) et refactorez vos Dataflows Gen2 existants pour éliminer tous les IDs codés en dur.

---

### 2. Copy Job : Le couteau suisse de l’ingestion (Column Mapping & Stratégies Incrémentales)

Le **Copy Job**, c'est l'outil de déplacement de données brut de Data Factory.

Son but est de transférer de gros volumes (via full load, incrémental ou CDC) de manière robuste, sans avoir à monter des pipelines complexes

Deux évolutions majeures pour l’activité Copy Job :

* le support du ***Column Mapping*** (renommage et changement de type de données à la volée, y compris en CDC)

* et le choix explicite entre le ***CDF (Change Data Feed)*** et une méthode basée sur un ***Watermark*** (colonne incrémentale comme un RowVersion) pour les copies depuis un Lakehouse ou un SQL Fabric.

**Pourquoi c’est un problème pour vos équipes ?**

* Jusqu’ici, le Copy Job était puissant mais rigide. Si le nom d’une colonne source ne correspondait pas exactement à la destination, il fallait faire une copie brute (1:1), puis ajouter une étape de transformation coûteuse en aval.
* Pour l’incrémental, le manque d’options forçait parfois à redévelopper des logiques personnalisées si le CDF n’était pas activé ou adapté.

**Comment le résoudre :**

* L’ingestion doit être le plus “Push-down” possible pour économiser du compute. En utilisant le mapping natif du Copy Job, on gère les écarts de schéma dès l’extraction.
* Côté incrémental, on adapte la méthode (CDF ou Watermark) à la réalité technique de la source.

**La réalité du terrain :**

* ✅ **Bénéfices :** Une réduction drastique de la consommation de CUs en évitant des flux de transformation intermédiaires inutiles juste pour renommer des champs.
* ⚠️ **Limitation :** Si vous choisissez la méthode Watermark (ex: date de modification) au lieu du CDF, vous perdez la capacité de détecter les suppressions physiques (hard deletes) sur votre source.

**Mon conseil :** Pour une réplication fidèle (Insert/Update/Delete), privilégiez toujours le CDF. Ne rabattez vos choix sur le Watermark que si votre source ne supporte pas le CDF ou si vous gérez des tables strictement en ajout (append-only).

---

### 3. Real-Time (RTI) : Casser le mur de la sécurité avec les connecteurs Eventstream sur réseau privé

La nouveauté consiste en la possibilité d’injecter Eventstream dans des **réseaux virtuels privés** via le ***streaming virtual network data gateway***.

Cela permet de se connecter de manière sécurisée à des sources streaming on-premise ou sur des vNets Azure privés (via ExpressRoute, VPN, Private Endpoints).

**Pourquoi c’est un problème pour vos équipes ?**

* Dans le monde de l’usine, de l’OT (Operational Technology) ou des environnements critiques, les règles sont strictes : aucune donnée ne transite par l’internet public.
* Demander aux équipes réseaux (SecOps) d’ouvrir un flux public pour alimenter un Eventstream cloud se soldait généralement par un “non” définitif.

**Comment le résoudre :**

1. **Le pont réseau :** Vous configurez un VNet Azure relié à votre réseau privé source (via ExpressRoute, VPN, ou Private Endpoint pour les services Azure).
2. **L’injection :** Fabric utilise l’injection SWIFT pour placer son connecteur Eventstream dans un sous-réseau (subnet) dédié de ce VNet.
3. **Le portail :** Dans Fabric, vous n’avez plus qu’à déclarer un *“Streaming virtual network data gateway”* (Passerelle de réseau virtuel de diffusion en continu) dans le menu “Gérer les connexions et les passerelles”.

**La réalité du terrain :**

* ✅ **Bénéfices :** C’est le feu vert tant attendu pour les projets IoT industriels sur Fabric. Vous respectez les contraintes réseau strictes, et bonus : ce nouveau type de gateway streaming ne nécessite pas de provisionner une capacité (CU) supplémentaire sur votre tenant.
* ⚠️ **Limitation :** La configuration (peering, ExpressRoute) ne se fait pas en trois clics. Elle nécessite de s’asseoir à la table des ingénieurs réseaux Azure de votre entreprise.

**Mon conseil :** Arrêtez d’essayer de contourner vos équipes sécurité. Utilisez cette fonctionnalité native pour monter un PoV avec eux et prouver que l’intégration temps réel dans Fabric répond aux standards industriels les plus stricts.

---

### 🎁 Bonus : Fin du code spaghetti et pilotage Power BI par le code

On avait dit 3 nouveautés, mais je ne pouvais pas vous laisser partir sans parler de deux pépites qui viennent nettoyer notre dette technique ce mois-ci :

**A. L’arrivée du** `%run` **dans les Notebooks Python**

* **Pourquoi c’est un problème :** Copier-coller la même fonction de nettoyage de données dans 15 notebooks différents est le meilleur moyen de créer une dette technique incontrôlable.
* **La réalité du terrain :**

  + ✅ **Bénéfices :** Avec `%run`, vous pouvez enfin appeler et exécuter un notebook “utilitaire” depuis un autre. Vous structurez un code modulaire et DRY (Don’t Repeat Yourself).
  + ⚠️ **Limitation :** Pour l’instant, la commande supporte uniquement l’appel de Notebooks, pas encore l’exécution directe de simples fichiers `.py` stockés dans vos dossiers.
* **Mon conseil :** Créez immédiatement un dossier “Core” contenant vos notebooks de fonctions communes (connexions, logs, nettoyage standard) pour que toute votre équipe les appelle dynamiquement.

**B. Semantic Link 0.13.0 & Power BI Automation**

**Semantic Link** (via la librairie Python `Sempy`), c'est le pont natif entre le monde de l'ingénierie/Data Science (Python/Spark) et la BI (Power BI). La nouveauté majeure de la version 0.13.0, c'est l'ajout de nouveaux modules complets qui permettent de piloter tout votre espace de travail par le code : gestion des Lakehouses, clonage et re-binding de rapports, ou encore administration des paramètres SQL et Spark.

* **Pourquoi c’est un problème :** Administrer des dizaines de modèles sémantiques Power BI à la main, remapper des rapports un par un ou gérer des espaces de travail via l’interface graphique est un travail de titan et un nid à erreurs humaines lors des mises en production.
* **La réalité du terrain :**

  + ✅ **Bénéfices :** L’automatisation “End-to-End” devient enfin une réalité. Vous pouvez désormais scripter directement dans un notebook Spark la création de vos tables, le clonage de vos rapports Power BI, et le monitoring de vos modèles, le tout avec une authentification par Service Principal enfin fiabilisée.
  + ⚠️ **Limitation :** Il faut faire sortir les développeurs BI de leur zone de confort (l’interface graphique) et les acculturer aux bases de Python et des Notebooks Spark pour en tirer profit.
* **Mon conseil :** Jetez un œil aux modules expérimentaux de *Semantic Link Labs*. Scripter vos opérations de maintenance Power BI n’est plus un luxe, c’est une nécessité pour passer à l’échelle.

---

### Conclusion

L’impact terrain de cette mise à jour est massif : c’est bâtir un socle gouverné pour qu’ils puissent enfin se concentrer sur la valorisation de la donnée, sans se soucier de la tuyauterie.

Entre les déploiements enfin automatisables sans retouche de code, l’économie de CUs sur l’ingestion, et le déblocage des cas d’usage industriels bridés par la sécurité réseau, on passe clairement un cap de maturité.

**Si tu dois retenir une chose :** La réussite d’un projet data d’entreprise ne se joue pas sur le volume de données traité, mais sur l’industrialisation de vos flux (CI/CD natif) et votre capacité à vous intégrer de manière transparente aux règles de sécurité réseau existantes.

**Et vous, quelle fonctionnalité va le plus impacter votre quotidien ce mois-ci ?** Répondez simplement en commentaire (ou par email) pour me le dire, je lis toutes vos réponses ! 👋

À très vite pour explorer ensemble le futur de la Data.

---

### 📚 Ressources pour aller plus loin :

* 🔗 [Nouveautés de Microsoft Fabric (Février 2026)](https://blog.fabric.microsoft.com/fr-fr/blog/fabric-february-2026-feature-summary?ft=All)
