# InSight Local — site vitrine

Site statique de **InSight Local**, publié sur GitHub Pages depuis la branche `main`.

## Organisation et référencement

Pages indexables : `index.html`, `services.html`, `audits-commerciaux.html`, `collecte-terrain.html`, `etudes-marche.html`, `e-reputation.html`, `missions.html`, `methode.html`, `a-propos.html`, `secteurs.html`, `faq.html`, `contact.html` et `mentions-legales.html`.

Pages utilitaires hors index : `confidentialite.html` et `404.html`, conservées en `noindex,follow`.

Le sitemap contient uniquement les pages réellement destinées à l’indexation. `robots.txt` autorise l’exploration générale et référence `sitemap.xml`. `llms.txt` résume l’identité, les prestations et les pages importantes pour les systèmes qui choisissent de le consulter.

Lors d’une modification significative d’une page, mettre à jour son `lastmod` dans le sitemap. Ne pas modifier artificiellement toutes les dates.

## Images et performances

- Source de marque conservée : `logo-insight-local.png`.
- Logo public : `logo-insight-local.webp`.
- Icônes : `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png`.
- Visuels terrain et analyse : sources WebP et variantes `-768.webp` utilisées pour l’affichage adaptatif.

Les anciens visuels et cartes non référencés ont été supprimés. Les ressources publiques sont désormais stockées directement dans le dépôt ; aucun workflow n’a besoin de les régénérer automatiquement.

## Formulaire et données

Le formulaire `contact.html` prépare un message via `mailto:` ou copie le contenu localement. **Aucune donnée n’est envoyée à un serveur du site lui-même.** Le visiteur doit valider l’envoi depuis sa messagerie.

La politique de confidentialité reste accessible depuis le pied de page mais n’est pas destinée à apparaître dans les résultats de recherche.

## Sécurité et maintenance

Le site est volontairement **100 % statique**. Aucun PHP, Composer, dossier `vendor` ou backend serveur n’est nécessaire.

La GitHub Action `.github/workflows/quality.yml` contrôle notamment :

- syntaxe JavaScript ;
- liens locaux et ancres ;
- images, textes alternatifs et dimensions ;
- canoniques, robots et sitemap ;
- validité JSON-LD ;
- absence de PHP/Composer/vendor ;
- absence de constructions JavaScript à risque inutiles à ce site ;
- absence de ressources HTTP non chiffrées ;
- disparition de l’ancienne copie `Net-Elo/`.

Les GitHub Actions sont exécutées avec des permissions minimales et `actions/checkout` est épinglé au SHA de la version validée. Dependabot surveille chaque semaine les mises à jour de GitHub Actions.

## Indexation

`.github/workflows/indexnow.yml` informe IndexNow lorsqu’une page publique ou le sitemap est modifié. La clé de vérification IndexNow est publiée à la racine, comme prévu par ce protocole.

IndexNow facilite la notification aux moteurs compatibles mais ne garantit jamais l’indexation.

## Publication

Après une modification :

1. vérifier le succès de **InSight Local — qualité et sécurité** ;
2. vérifier le déploiement **pages build and deployment** ;
3. si le contenu public a changé, contrôler le passage d’IndexNow ;
4. conserver des `lastmod` correspondant à de vraies modifications.

Le design actuel doit être préservé sauf demande explicite de refonte.
