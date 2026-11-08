# InSight Local — site vitrine

Site statique de [InSight Local](https://insight-local.fr/), publié sur GitHub Pages depuis la branche `main`.

## Organisation et référencement

- Pages de prestations : `services.html`, `audits-commerciaux.html`, `collecte-terrain.html`, `etudes-marche.html` et `e-reputation.html`
- Autres pages : `index.html`, `missions.html`, `methode.html`, `a-propos.html`, `secteurs.html`, `faq.html`, `contact.html`
- Informations légales et RGPD : `mentions-legales.html`, `confidentialite.html`
- Page d'erreur : `404.html` (hors sitemap, `noindex`)
- Découverte : `sitemap.xml` (14 pages), `robots.txt`, `llms.txt`

Chaque page indexable conserve ses balises `title`, `description`, `canonical`, Open Graph et JSON-LD. Lors d'une modification significative de contenu, vérifier le sitemap et les métadonnées. Ne pas publier de rapport ou d'identité de client sans autorisation.

## Images optimisées

- Source de marque : `logo-insight-local.png`, conservée.
- Affichage du logo : `logo-insight-local.webp` (500 × 250).
- Icônes : `favicon.ico`, `favicon-32.png`, `apple-touch-icon.png`, `icon-192.png`.
- Illustrations adaptées : `assets/terrain-768.webp`, `assets/analyse-768.webp` et sources WebP existantes.

La tâche GitHub Actions `.github/workflows/optimize-logo.yml` régénère ces ressources lorsque les sources originales sont modifiées. Son commit automatique doit être terminé avant qu'une nouvelle ressource soit référencée dans le HTML.

## Formulaire et données

Le formulaire `contact.html` prépare un message via `mailto:` ou copie le contenu localement. **Aucune donnée n'est envoyée à un serveur du site lui-même**. Le visiteur doit valider l'envoi depuis sa messagerie. Préserver ce fonctionnement tant qu'il n'est pas expressément modifié.

## Vérifications de publication

1. Les liens internes et le menu fonctionnent sur petit écran.
2. Une balise `h1` par page ; images avec `alt`, dimensions et chargement adapté.
3. JSON-LD valide et URL canonique identique à la page.
4. Action GitHub Pages `pages build and deployment` terminée avec succès.
5. Test manuel mobile et ordinateur, puis mesure via PageSpeed Insights. **Ne pas annoncer de score Lighthouse sans exécution réelle**.

## Séparation des activités

Le répertoire `Net-Elo/` correspond à une activité distincte. **Ne pas modifier ni supprimer son contenu au cours des changements du site InSight Local sans demande explicite.** Ne pas supprimer les anciennes illustrations ou cartes de visite sans vérification préalable de leurs usages.
