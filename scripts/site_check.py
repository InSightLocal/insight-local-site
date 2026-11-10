#!/usr/bin/env python3
"""Static quality and security checks for insight-local.fr."""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
HTMLS = sorted(ROOT.glob("*.html"))
INDEXABLE = {
    "index.html",
    "services.html",
    "missions.html",
    "methode.html",
    "a-propos.html",
    "secteurs.html",
    "audits-commerciaux.html",
    "collecte-terrain.html",
    "etudes-marche.html",
    "e-reputation.html",
    "contact.html",
    "mentions-legales.html",
    "faq.html",
}
NOINDEX = {"404.html", "confidentialite.html"}
failures: list[str] = []

# This is intentionally a static GitHub Pages site.
for path in [*ROOT.rglob("*.php"), ROOT / "composer.json", ROOT / "composer.lock"]:
    if path.exists():
        failures.append(f"Fichier serveur inattendu : {path.relative_to(ROOT)}")
if (ROOT / "vendor").exists():
    failures.append("Dossier vendor inattendu sur un site statique")
if (ROOT / "Net-Elo").exists():
    failures.append("Ancienne copie Net-Elo encore présente")
if (ROOT / ".github/workflows/optimize-logo.yml").exists():
    failures.append("Ancien workflow de génération d’images encore présent")

dangerous_js = {
    r"\beval\s*\(": "eval()",
    r"\bnew\s+Function\s*\(": "new Function()",
    r"document\.write\s*\(": "document.write()",
    r"\.innerHTML\s*=": "affectation innerHTML",
}
for js_path in ROOT.glob("*.js"):
    source = js_path.read_text(encoding="utf-8")
    for pattern, label in dangerous_js.items():
        if re.search(pattern, source, re.I):
            failures.append(f"{js_path.name}: construction JavaScript interdite ({label})")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1 = 0
        self.main = 0
        self.ids: set[str] = set()
        self.hrefs: list[tuple[str, dict[str, str | None]]] = []
        self.images: list[dict[str, str | None]] = []
        self.links: list[dict[str, str | None]] = []
        self.robots = ""
        self.jsonld: list[object] = []
        self._json = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
        if data.get("id"):
            self.ids.add(str(data["id"]))
        if tag == "a" and data.get("href"):
            self.hrefs.append((str(data["href"]), data))
        if tag == "img":
            self.images.append(data)
        if tag == "link":
            self.links.append(data)
        if tag == "meta" and data.get("name") == "robots":
            self.robots = str(data.get("content", ""))
        if tag == "script" and data.get("type") == "application/ld+json":
            self._json = True
            self._buffer = []

    def handle_data(self, data):
        if self._json:
            self._buffer.append(data)

    def handle_endtag(self, tag):
        if tag == "script" and self._json:
            try:
                self.jsonld.append(json.loads("".join(self._buffer)))
            except Exception as exc:
                failures.append(f"JSON-LD invalide : {exc}")
            self._json = False


parsed: dict[str, Page] = {}
raw: dict[str, str] = {}
for path in HTMLS:
    html = path.read_text(encoding="utf-8")
    raw[path.name] = html
    page = Page()
    page.feed(html)
    parsed[path.name] = page

for path in HTMLS:
    page = parsed[path.name]
    html = raw[path.name]

    if re.search(r"javascript\s*:", html, re.I):
        failures.append(f"{path.name}: URL javascript: interdite")
    if re.search(r"\son[a-z]+\s*=", html, re.I):
        failures.append(f"{path.name}: gestionnaire d’événement inline interdit")
    if re.search(r"""(?:src|href)=["']http://""", html, re.I):
        failures.append(f"{path.name}: ressource HTTP non chiffrée")

    if page.h1 != 1:
        failures.append(f"{path.name}: {page.h1} H1")
    if page.main != 1:
        failures.append(f"{path.name}: {page.main} élément main")

    for attrs in page.images:
        if not attrs.get("alt"):
            failures.append(f"{path.name}: image sans texte alternatif")
        if not attrs.get("width") or not attrs.get("height"):
            failures.append(f"{path.name}: image sans dimensions")
        src = str(attrs.get("src", ""))
        parsed_src = urlsplit(src)
        if parsed_src.scheme or parsed_src.netloc or src.startswith("data:"):
            continue
        target = ROOT / parsed_src.path.lstrip("/")
        if parsed_src.path and not target.is_file():
            failures.append(f"{path.name}: image inexistante {src}")

    for href, attrs in page.hrefs:
        if attrs.get("target") == "_blank":
            rel = set(str(attrs.get("rel", "")).split())
            if "noopener" not in rel:
                failures.append(f"{path.name}: lien _blank sans noopener ({href})")
        parsed_url = urlsplit(href)
        if parsed_url.scheme or parsed_url.netloc or href.startswith(("mailto:", "tel:")):
            continue
        local_path = parsed_url.path.lstrip("/")
        target_name = "index.html" if local_path in ("", ".", "./") else local_path
        target = ROOT / target_name
        if not target.is_file():
            failures.append(f"{path.name}: lien local absent {href}")
            continue
        if parsed_url.fragment and target_name in parsed:
            if parsed_url.fragment not in parsed[target_name].ids:
                failures.append(f"{path.name}: ancre absente {href}")

    if path.name in INDEXABLE:
        expected = "https://insight-local.fr/" + ("" if path.name == "index.html" else path.name)
        if "noindex" in page.robots:
            failures.append(f"{path.name}: noindex inattendu")
        if not any(link.get("rel") == "canonical" and link.get("href") == expected for link in page.links):
            failures.append(f"{path.name}: canonical absent ou erroné")
        if not page.jsonld:
            failures.append(f"{path.name}: données structurées absentes")

    if path.name in NOINDEX and "noindex" not in page.robots:
        failures.append(f"{path.name}: doit être noindex")

sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
locations = [node.text for node in sitemap.findall(f".//{ns}loc")]
expected_locations = {
    "https://insight-local.fr/" + ("" if name == "index.html" else name)
    for name in INDEXABLE
}
if set(locations) != expected_locations:
    failures.append(f"Sitemap différent des pages indexables : {set(locations) ^ expected_locations}")
if len(locations) != len(set(locations)):
    failures.append("Sitemap : URL dupliquée")

cname = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
if cname != "insight-local.fr":
    failures.append(f"CNAME inattendu : {cname}")

robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
if "Sitemap: https://insight-local.fr/sitemap.xml" not in robots:
    failures.append("robots.txt : sitemap absent")
if "Disallow: /Net-Elo/" in robots:
    failures.append("robots.txt : ancienne règle Net-Elo encore présente")

if failures:
    print("\n".join("ERREUR — " + item for item in failures))
    sys.exit(1)

print(
    f"InSight Local validé : {len(HTMLS)} pages HTML, "
    f"{len(locations)} URL indexables, liens, images, JSON-LD et sécurité statique."
)
