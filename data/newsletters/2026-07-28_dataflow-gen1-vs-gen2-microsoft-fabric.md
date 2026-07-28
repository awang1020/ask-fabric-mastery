---
title: Dataflow Gen1 vs Gen2 : faut-il migrer maintenant ?
url: https://blog.antoinewang-tech.com/p/dataflow-gen1-vs-gen2-microsoft-fabric
date: 2026-07-28
author: Antoine Wang
source: substack
---

# Dataflow Gen1 vs Gen2 : faut-il migrer maintenant ?

Bonjour à tous, je suis Antoine Wang.

J’aide les profils techniques à maîtriser l’architecture de Microsoft Fabric, et j’aide les décideurs à comprendre l’impact réel de cette technologie.

Mon objectif ? Vulgariser le complexe et vous donner les clés pour maîtriser Microsoft Fabric, une plateforme de données SaaS unifiée et alimentée par l’IA pour simplifier la gestion des données et l’analyse.

🆕 **Nouveauté pour les lecteurs** : j’ai créé **Ask Fabric Mastery**, un assistant IA qui répond à vos questions sur Microsoft Fabric & Power BI en s’appuyant uniquement sur les 30 éditions de cette newsletter. Réponses sourcées, sans hallucination, avec un lien direct vers l’édition d’origine.

👉 **Testez-le maintenant** : [ask-fabric-mastery](http://awang1020.github.io/ask-fabric-mastery)

🔑 **Code d’accès (ce code est réservé aux abonnés Fabric Mastery) :**

Cette newsletter est 100% gratuite. En vous abonnant maintenant, vous recevrez en exclusivité mon “One-Pager” pour cartographier l’ensemble de la solution Fabric en un coup d’œil.

Merci à celles et ceux qui me suivent depuis le début. Sans plus attendre, entrons dans le vif du sujet !

---

## ⚡ En 30 secondes

Ce qu’il faut retenir :

* Dataflow Gen1 est officiellement en état \*\*Legacy\*\* : pas de retrait immédiat, mais zéro nouvelle feature à venir. Les Premium bénéficient d’un préavis ≥ 12 mois avant tout retrait.
* Gen2 garde l’expérience Power Query, mais ajoute 4 leviers (Staging, Fast Copy, Modern Evaluator, Partitioned Compute) et une tarification CU découplée, sur les benchmarks officiels, l’écart va jusqu’à ~**20× plus rapide** sur les patterns ELT.
* Pour un nouveau projet, démarrez direct en Dataflow Gen Gen2 (CI/CD) avec destination Lakehouse. Pour l’existant, migrez par lot avec “Save As” et l’API associée.

---

Combien de Dataflow Gen1 tournent encore dans votre tenant Power BI ? Et surtout : combien de Data Engineers de votre équipe savent vraiment ce qui change quand on passe en Gen2, quelles sont les prérequis et est-ce vraiment nécessaire ?

La réalité du terrain, c’est que la majorité des organisations que je vois en mission ont accumulé des dizaines, parfois des centaines, de Dataflow Gen1 sur 8 ans d’historique Power BI. Et quand Microsoft annonce que Gen1 entre en état Legacy, deux réflexes apparaissent : la panique migration ”on doit tout refaire pour hier” ou “"on ne voit pas l’intérêt donc on attend”.

Aujourd’hui, on tranche. Ni panique, ni déni : on regarde ce que dit Microsoft, ce que disent les benchmarks officiels, et ce qui se passe vraiment quand on bascule un Dataflow en production.

---

## C’est quoi, Dataflow Gen1 et Dataflow Gen2 ?

Les deux sont des artefacts de préparation de données low-code, basés sur **Power Query** et le **langage M**. Ils permettent d’ingérer, nettoyer et publier des tables réutilisables sans écrire de code Spark ou SQL. Trois différences fondamentales :

1. **Gen1 (**aussi connu sous le nom de **Flux de données Power BI)** vit dans **Power BI**, écrit dans un stockage Power BI interne, et son moteur de calcul est lié à la capacité Premium.
2. Gen2 vit dans **Fabric** (du workload Data Factory), peut écrire dans n’importe quelle destination Fabric ou externe (Lakehouse, Warehouse, ADLS Gen2, Azure SQL DB, Snowflake, SharePoint…), et son compute est facturé au **Capacity Unit (CU** selon la consommation réelle.
3. **Gen2 (CI/CD)** est la variante “moderne” de Gen2 : elle embarque par défaut le **Modern Query Evaluator** (le nouveau moteur d’évaluation M) et débloque les leviers de scalabilité (Fast Copy, Partitioned Compute, Staging).

Le statut officiel depuis avril 2026 : **Gen1 = Legacy** ! (existant supporté, plus d’innovation), le but : **Gen2** **= la cible**.

---

## La réalité du terrain

#### ✅ 1. Gen1 n’est pas retiré demain, mais l’innovation est stoppée

Microsoft a été clair : les Dataflow Gen1 existants continueront de tourner, et pour les capacités Premium, un préavis d’au moins 12 mois sera donné avant tout retrait. Aucune date butoir publiée à ce jour.

En revanche :

* Plus aucune feature ne sera ajoutée à Gen1.
* Les artefacts Gen1 sont désormais marqués “**Legacy**” dans le menu \*\*New Artifact\*\*.
* Le support se limite aux correctifs critiques implémentables sans changer l’architecture.

#### ✅ 2. Gen2 garde Power Query, le code est transférable

L’expérience d’authoring est identique, les connecteurs sont là, vos transformations existantes se rejouent telles quelles dans Gen2 via la fonction **Save as Dataflow Gen2**.

Ce qui change, c’est **l’environnement d’exécution** :

* Moteur de calcul Fabric élastique (auto-scaling sans tuning manuel).
* Exécution parallélisée des partitions et des étapes.
* Diagnostics enrichis (timing par étape, foldability, comportements connecteurs).

#### ✅ 3. Les 4 leviers Gen2, et quand les utiliser

* **Staging** : Matérialiser une fois pour réutiliser plusieurs fois en aval pour des Patterns ELT, requêtes dérivées multiples
* **Fast Copy** : Ingestion haut-débit vers OneLake (Lakehouse) pour du Bulk-load Parquet/CSV depuis ADLS, peu ou pas de transformations
* **Modern Evaluator** : Nouveau moteur M, par défaut sur Gen2 (CI/CD) pour des transformations lourdes, non-foldables, row-by-row

* **Partitioned Compute (preview)** : Évaluation parallèle des partitions pour des sources fichiers partitionnables (Combine Files)

Les benchmarks officiels Microsoft (avril 2026), sur des scénarios canoniques exécutés sur Gen1 vs Gen2 (CI/CD) donnent les ordres de grandeur suivants :

#### ✅ 4. La tarification : CU à la consommation, plus capacité Premium “always-on”

C’est le changement structurel le plus mal compris.

* **Gen1** : votre compute est inclus dans la capacité Premium achetée, vous payez la capacité même quand les Dataflow ne tournent pas.
* **Gen2** : la consommation est facturée en **CU (Capacity Units)**, alignée sur le runtime Fabric. Vous payez ce que vous consommez réellement, avec un scaling élastique pour les bursts.

Le point que Microsoft a explicitement clarifié à FabCon Europe en septembre 2025 (avec les Dataflow Gen2 pricing improvements) : **les gains de performance se traduisent directement en gains de coût**. Sur Gen2, plus une transformation s’exécute vite, moins elle consomme de CU. Le ratio n’est plus “compute payé d’avance, performance subie”, c’est “**compute facturé à l’usage, performance qui réduit la facture**”.

Par exemple, sur les patterns du benchmark Microsoft :

* Sur un ELT qui passe de 2h42 (Gen1) à 5m53 (Gen2 avec Staging + Fast Copy), vous ne gagnez pas seulement ~27× sur le temps, vous réduisez **dans des proportions équivalentes** la consommation CU de ce workload sur votre capacité.
* Sur un bulk-load Parquet Lakehouse qui passe de 1h42 à 7m43, la même logique s’applique : Fast Copy fait le travail plus vite, donc utilise moins de CU sur la durée.

Conséquence côté FinOps :

* **Workloads intermittents ou saisonniers** : Gen2 peut baisser nettement la facture, car vous ne payez plus une capacité Premium dormante 24/7.
* Workloads très denses : dimensionnez finement votre SKU pour éviter le throttling, mais les gains de perf compensent une partie significative de la consommation.

**💡Mon conseil** : avant de migrer en bulk, faites tourner **un échantillon représentatif** (≈ 10 % de vos Gen1) en Gen2 pendant 1 cycle de facturation. Mesurez deux choses, pas une seule : le **temps de refresh** ET la **consommation CU** via la ***Fabric Capacity Metrics App***. C’est la combinaison des deux qui vous dit si vous gagnez vraiment, pas le temps d’exécution seul !

---

## Points de vigilance / Pièges à Éviter

⚠️ **Pro et PPU : pas encore de chemin Gen2 clair**

Le blog Microsoft est explicite : pour les licences **Pro et Premium Per User (PPU)**, des “paths Gen2” sont annoncés mais pas encore livrés au moment où j’écris. Si votre tenant est en Pro/PPU sans Fabric, Gen1 reste votre option par défaut, et Microsoft a confirmé qu’il continuera de tourner. Surveillez les annonces, mais ne vous mettez pas la pression pour migrer ce qui n’a pas encore de destination.

⚠️ **Partitioned Compute est en preview**

Très puissant (gain ~20× sur Combine Files), mais **preview** donc pas encore couvert par les SLA de production. Pour vos workloads critiques, attendez la GA ou prévoyez un fallback Modern Evaluator. Vérifiez l’état dans la [Data Factory Roadmap](https://roadmap.fabric.microsoft.com/?product=datafactory).

⚠️ “**Save as Dataflow Gen2” ne migre pas tout**

La fonction couvre la majorité des transformations courantes, mais certains scénarios anciens (connecteurs custom, paramètres particuliers) peuvent nécessiter un ajustement manuel. Testez chaque Dataflow migré contre son équivalent Gen1 pendant 1-2 cycles avant de débrancher Gen1. Ne supprimez jamais le Gen1 source tant que le Gen2 n’a pas tourné en parallèle.

⚠️ **Connecteur “Dataflows” en aval : la limitation qui piège les migrations**

Quand vous migrez un Gen1 vers Gen2 et que des items en aval (modèles sémantiques, autres Dataflow) consomment votre Gen2 via le connecteur **Dataflow**, la donnée transite par une **API interne**. Cette API peut subir des timeouts intermittents, ce qui se traduit par des ***échecs de refresh côté items consommateurs***, souvent avec un message d’erreur trompeur du type *”The key didn’t match any rows in the table.”.* Ce n’est pas un problème de données, c’est le backend qui n’a pas pu retourner les résultats à temps.

La parade officielle Microsoft : \*\***configurez une destination**\*\* (Lakehouse ou Warehouse) sur chaque Gen2 source, puis modifiez les items en aval pour qu’ils lisent \*\***via le connecteur Lakehouse / Warehouse**\*\*, pas via le connecteur Dataflows. Vous court-circuitez l’API interne et la fiabilité du refresh remonte significativement. Détail dans la [doc Data Factory limitations](https://learn.microsoft.com/fabric/data-factory/data-factory-limitations).

---

## 🥇 La Règle d’Or

**Si tu dois retenir une chose** : Dataflow Gen1 n’est pas mort, mais il est gelé. Tout nouveau Dataflow doit naître en Gen2 (CI/CD), pas pour suivre la tendance, mais parce que les 4 leviers de scalabilité et le modèle CU vous évitent de payer pour une capacité dormante. Pour l’existant, migrez par vagues, en commençant par geler les créations Gen1 et en validant chaque Dataflow critique en parallèle avant cutover.

L’impact terrain : vous arrêtez d’empiler de la dette technique sur une plateforme legacy, vous valorisez vos refresh sans surconsommer de CU, et vous ouvrez la porte à Direct Lake sur Lakehouse, qui est la combinaison naturelle de Gen2 pour les rapports Power BI à grande échelle.

> Et vous, où en êtes-vous dans l’inventaire de vos Dataflow Gen1 ? Répondez simplement à cet email ou ce post, je lis tous vos messages.

À la semaine prochaine pour continuer à explorer ensemble les entrailles de Fabric !

---

## 🔗 À lire dans Fabric Mastery

* [Ingestion Microsoft Fabric : Dataflow, Pipeline ou Notebook ? Guide complet 2026](https://blog.antoinewang-tech.com/p/microsoft-fabric-data-ingestion-tools)
* [Microsoft Fabric : Explorer tout le potentiel de Copilot dans Dataflow Gen2](https://blog.antoinewang-tech.com/p/copilot-dataflow-gen2-microsoft-fabric)

---

## 📚 Ressources pour aller plus loin

Pour approfondir le sujet et affiner vos choix d’architecture, je vous recommande ces lectures essentielles issues de la documentation officielle :

* [Choisir la bonne stratégie Dataflow Gen2 — Decision guide](https://learn.microsoft.com/fabric/data-factory/decision-guide-data-transformation)
* [Créer votre premier Dataflow Gen2](https://learn.microsoft.com/fabric/data-factory/create-first-dataflow-gen2)]
* [Migrer un Dataflow Gen1 vers Gen2 avec “Save As”](https://learn.microsoft.com/fabric/data-factory/migrate-to-dataflow-gen2-using-save-as)
* [Migration Gen1 → Gen2 (CI/CD) — Scénarios programmatiques](https://learn.microsoft.com/fabric/data-factory/dataflow-gen2-migrate-from-dataflow-gen1-scenarios)
* [Tarification Dataflow Gen2 — Standard / High Scale / Fast Copy](https://learn.microsoft.com/fabric/data-factory/pricing-dataflows-gen2)
