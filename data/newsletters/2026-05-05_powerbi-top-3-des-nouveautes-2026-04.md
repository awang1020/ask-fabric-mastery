---
title: Power BI : Top 3 des nouveautés d'Avril 2026
url: https://antoinewang.substack.com/p/powerbi-top-3-des-nouveautes-2026-04
date: 2026-05-05
author: Antoine Wang
source: substack
---

# Power BI : Top 3 des nouveautés d'Avril 2026

Bonjour à tous, je suis Antoine Wang.

J’aide les profils techniques à maîtriser l’architecture de Microsoft Fabric, et j’aide les décideurs à comprendre l’impact réel de cette technologie.

Mon objectif ? Vulgariser le complexe et vous donner les clés pour maîtriser Microsoft Fabric, une plateforme de données SaaS unifiée et alimentée par l’IA pour simplifier la gestion des données et l’analyse.

Cette newsletter est 100% gratuite. En vous abonnant maintenant, vous recevrez en exclusivité mon “One-Pager” pour cartographier l’ensemble de la solution Fabric en un coup d’œil.

Merci à celles et ceux qui me suivent depuis le début. Sans plus attendre, entrons dans le vif du sujet !

---

Combien de temps passez-vous à reformater vos rapports Power BI chaque fois que vous créez un nouveau projet ? Ajuster les couleurs, recaler les tailles de canvas, reconfigurer les styles de tables… La réalité du terrain, c’est que beaucoup de créateurs de rapports perdent un temps considérable sur du formatage au lieu de se concentrer sur la valorisation de la donnée.

Ce mois d’avril 2026, Microsoft s’attaque frontalement à ce problème avec des améliorations qui vont changer la façon dont vous construisez vos rapports au quotidien.

Mon objectif aujourd’hui n’est pas de vous lister toutes les features du mois, mais de me concentrer sur **3 fonctionnalités “Reporting”** qui vont avoir un impact immédiat sur votre productivité dans Power BI Desktop. C’est parti !

---

## 1. Card Visual : L’interactivité que vous attendiez

Je vois souvent des rapports où le Card visual, devenu GA depuis novembre 2025, est utilisé comme un simple afficheur de KPIs statiques. Vous posez vos métriques clés en haut de page, et c’est tout. Le potentiel interactif du visuel est complètement sous-exploité.

### Ce qui change

Microsoft enrichit le Card visual avec des mises à jour qui le transforment en un véritable composant interactif :

* **Feedback visuel sur la sélection de catégorie** : lorsque vous cliquez sur un header de catégorie, la carte sélectionnée s’illumine tandis que les autres s’estompent. Fini l’ambiguïté sur “qu’est-ce que je suis en train de filtrer ?”
* **Concaténation automatique** : si vous ajoutez plusieurs colonnes de données dans le champ catégorie, les valeurs se concatènent proprement dans le header. Plus besoin de créer une colonne calculée pour combiner `Ville` et `Région`.
* **Edit Interactions** : vous pouvez désormais contrôler précisément quels visuels de la page sont filtrés quand l’utilisateur clique sur une carte. C’est le même mécanisme que sur les graphiques, enfin disponible sur les Cards.
* **Support images base64** : les images encodées en base64 s’affichent correctement au niveau supérieur. Si vous alimentez vos cartes avec des images stockées dans vos données (logos produits, photos d’articles), elles apparaissent sans conversion supplémentaire.

#### La réalité du terrain

✅ **Le scénario qui change tout** : imaginez un dashboard exécutif avec 5 cartes affichant le CA par région. L’utilisateur clique sur “Nord-Est” : la carte se met en surbrillance, les 4 autres s’estompent, et tous les graphiques de la page se filtrent automatiquement. C’est de la navigation contextuelle native, sans boutons, sans slicers, sans bookmarks.

✅ **Edit Interactions** est un game-changer discret. Jusqu’ici, un clic sur une carte filtrait systématiquement tous les visuels de la page. Maintenant, vous pouvez décider que le clic ne filtre que le graphique de tendance et la table de détails, sans toucher au KPI global en haut de page.

⚠️ **Point de vigilance** : La fonctionnalité Edit Interactions sur le Card n’est pas rétroactive. Si vous avez des rapports existants avec des Cards, les interactions par défaut restent à “tout filtrer”. Passez en revue vos dashboards existants pour configurer les interactions visuelles souhaitées, surtout si certains KPIs de synthèse ne doivent jamais être filtrés.

---

## 2. Modern Visual Defaults & Theme Switcher (Preview) : La fin du formatage artisanal

La réalité du terrain, c’est que la majorité des créateurs de rapports Power BI partent d’une page blanche et reformatent chaque visuel manuellement. Les couleurs par défaut ne correspondent pas à la charte, les tailles de canvas sont approximatives, et les tables n’ont ni banded rows ni boutons d’expansion.

Résultat ? Des heures perdues en formatage, et des rapports visuellement incohérents d’un projet à l’autre.

### Ce qui change

Microsoft introduit le thème de base **Fluent 2(en Preview)** et enrichit considérablement le dialogue **Customize current theme** :

- **Base theme switcher** : directement dans le dialogue Customize current theme (View > Themes), vous pouvez maintenant basculer entre trois thèmes de base : **Fluent 2 (Preview)**, Classic 2026 et Classic 2018. Si votre thème personnalisé ne fonctionne pas encore avec les nouveaux defaults, vous revenez au précédent le temps de l’ajuster.

- **Preset canvas sizes** : des tailles de canvas prédéfinies par ratio d’aspect. Pour le 16:9, vous choisissez directement entre HD (1280×720), Full HD (1920×1080), QHD (2560×1440) et 4K UHD (3840×2160). Plus besoin de deviner les bonnes dimensions.

- **Reset to default repensé** : le tile “Reset to default” est désormais visuellement distinct dans la galerie de thèmes. Fini la confusion entre “appliquer un thème” et “réinitialiser toute la mise en forme”.

### La réalité du terrain

✅ **Fluent 2 change le point de départ**. Avec ce nouveau thème de base, les nouvelles pages démarrent en 1920×1080 (au lieu de 1280×720), le fond est gris clair pour un meilleur contraste, et tous les visuels partagent des polices, paddings et bordures uniformes. Vous partez d’une base visuellement propre sans rien configurer.

✅ **L’impact sur les rapports existants** : vos rapports actuels ne changent pas automatiquement. La mise à jour est volontaire : ouvrez le dialogue Customize current theme, un bandeau vous invite à “Update theme”. Vous décidez quand migrer.

✅ **Les style presets** par type de visuel sont un gain de temps considérable. Les graphiques offrent des presets (Default, Data Labels) et les line charts utilisent des courbes lissées par défaut avec des variations en un clic.

💡 **Tips**: Activez la Preview dans Power BI Desktop (Options > Preview features > Modern visual defaults). Créez un rapport test avec vos visuels habituels pour évaluer le rendu Fluent 2 avant de migrer vos rapports de production. Exportez ensuite votre thème personnalisé en JSON pour le réutiliser sur tous vos projets, c’est la meilleure façon de standardiser l’apparence de vos rapports à l’échelle de l’équipe.

---

## 3. Narrative Visual : Copilot par défaut et 10 000 caractères

Avez-vous déjà ajouté un visuel Narrative (Smart Narrative) dans un rapport, pour être accueilli par un choix entre “Copilot” et “Custom” sans trop savoir lequel prendre ? L’erreur classique sur le terrain : les créateurs de rapports choisissent “Custom”, écrivent manuellement leur résumé, et passent à côté de la puissance de l’IA générative.

### Ce qui change

Deux améliorations qui simplifient radicalement l’expérience :

* **Copilot mode par défaut** : si l’utilisateur dispose d’une licence Copilot, le visuel Narrative s’ouvre désormais directement en mode Copilot. Plus besoin de choisir, l’IA prend la main immédiatement pour générer un résumé contextuel de votre rapport.
* **Limite de caractères augmentée à 10 000** : la précédente limite était un frein pour les rapports complexes nécessitant des narratifs détaillés. Avec 10 000 caractères, vous pouvez rédiger des prompts plus riches et obtenir des résumés plus complets.
* Les créateurs peuvent toujours basculer entre les modes Copilot et Custom à tout moment. Aucune fonctionnalité n’est retirée, c’est le comportement par défaut qui devient plus intelligent.

### La réalité du terrain

✅ **L’impact sur l’adoption** : en mettant Copilot par défaut, Microsoft élimine la friction initiale. Je vois souvent des équipes qui n’utilisent pas le Narrative Visual simplement parce qu’elles ne savaient pas qu’un mode IA existait. Maintenant, c’est le premier écran qu’elles voient.

✅ **Les 10 000 caractères changent la donne pour les prompts avancés**. Vous pouvez désormais écrire des instructions détaillées : “Résume les tendances de vente par région, mets en avant les écarts supérieurs à 10% par rapport au mois précédent, et identifie les 3 produits avec la plus forte croissance.” Ce niveau de détail était impossible avec l’ancienne limite.

⚠️ **Point de vigilance** : Le mode Copilot par défaut nécessite une licence Copilot active. Sans licence, le visuel s’ouvrira en mode Custom comme avant. Vérifiez la couverture de licences dans votre tenant avant de former vos équipes sur cette fonctionnalité, vous éviterez la frustration du “ça ne marche pas chez moi”.

---

## Conclusion

Si tu dois retenir une chose : Power BI Desktop n’est plus un outil où l’on passe la moitié de son temps à formater et l’autre moitié à modéliser.

Avec Fluent 2, les Card interactifs, le Narrative Copilot par défaut et les colonnes calculées Direct Lake, Microsoft rapproche Power BI de ce qu’il devrait être depuis le début, une plateforme où vous vous concentrez sur la valorisation de la donnée, pas sur la mise en forme.

> Et vous, quelle fonctionnalité allez-vous activer en premier ? Le thème Fluent 2 pour standardiser tous vos rapports, ou les Cards interactifs pour repenser la navigation de vos dashboards ? Répondez simplement à cet email ou ce post, je lis tous vos messages.

À la semaine prochaine pour continuer à explorer ensemble les entrailles de Fabric !

---

## 📚 Ressources pour aller plus loin

Pour approfondir le sujet et passer à la pratique, je vous recommande ces lectures essentielles issues de la documentation officielle :

- [[Nouveautés Power BI — Avril 2026](https://powerbi.microsoft.com/en-us/blog/power-bi-april-2026-feature-summary/)]

- [[Create a card visual in Power BI](https://learn.microsoft.com/power-bi/visuals/power-bi-visualization-card)]

- [[Visual defaults in Power BI reports (Fluent 2)](https://learn.microsoft.com/power-bi/create-reports/power-bi-reports-visual-defaults)]

- [[Use report themes in Power BI Desktop](https://learn.microsoft.com/power-bi/create-reports/desktop-report-themes)]

- [[Create Smart Narrative Summaries](https://learn.microsoft.com/fr-fr/power-bi/visuals/power-bi-visualization-smart-narrative)]

- [[Direct Lake overview](https://learn.microsoft.com/fabric/fundamentals/direct-lake-overview)]
