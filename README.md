# Motortheorie oefenen

Statische oefensite voor het Nederlandse theorie-examen motor (rijbewijs A/A1/A2).
Geen build-stap, geen dependencies — puur HTML, CSS en JavaScript.

## Wat zit erin

- **Examensimulatie**: 50 vragen, 30 minuten, geslaagd vanaf 41 goed. Met timer, vraagoverzicht, markeren en nabespreking.
- **Oefenmodus**: per categorie (gevaarherkenning / kennis / inzicht) of per onderwerp, met direct antwoord en uitleg.
- **Voortgang**: scores per categorie en examengeschiedenis, opgeslagen in `localStorage` van de browser.
- **Foute vragen opnieuw oefenen**.
- 60 oefenvragen met eigen SVG-illustraties van borden en verkeerssituaties.

## Bestanden

```
index.html          de hele site (single page, hash-routing)
css/style.css       styling, met licht- en donkerthema
js/app.js           alle logica
data/questions.json de vragenbank
img/*.svg           borden en verkeerssituaties
make_svgs.py        script waarmee de SVG's gegenereerd zijn (niet nodig voor de site)
```

## Publiceren op GitHub Pages

1. Maak een nieuwe repository op GitHub, bijvoorbeeld `motortheorie`.
2. Zet de inhoud van deze map in de repository:

   ```bash
   git init
   git add .
   git commit -m "Motortheorie oefensite"
   git branch -M main
   git remote add origin https://github.com/<jouw-gebruikersnaam>/motortheorie.git
   git push -u origin main
   ```

3. Ga in de repository naar **Settings → Pages**.
4. Kies bij *Source*: **Deploy from a branch**, branch `main`, map `/ (root)`. Opslaan.
5. Na een minuut staat de site op `https://<jouw-gebruikersnaam>.github.io/motortheorie/`.

Het bestand `.nojekyll` staat er al in, zodat GitHub Pages de bestanden ongewijzigd serveert.

## Lokaal bekijken

De vragen worden met `fetch` geladen, dus dubbelklikken op `index.html` werkt niet.
Start een lokale server:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Vragen toevoegen of aanpassen

Alles staat in `data/questions.json`. Een vraag ziet er zo uit:

```json
{
  "id": "k21",
  "categorie": "kennis",
  "onderwerp": "Borden",
  "vraag": "Wat betekent dit bord?",
  "afbeelding": "img/bord-b7.svg",
  "opties": ["Stoppen is verplicht", "Verleen voorrang", "Voorrangsweg"],
  "antwoord": 0,
  "uitleg": "Bord B7: je moet stoppen en daarna voorrang verlenen."
}
```

- `categorie` is `gevaarherkenning`, `kennis` of `inzicht`.
- `onderwerp` is vrij te kiezen; nieuwe onderwerpen verschijnen automatisch in het oefenmenu.
- `antwoord` is de index van het juiste antwoord (0 = eerste optie). De site schudt de antwoorden bij elke vraag, dus de volgorde in het bestand maakt niet uit.
- `afbeelding` is optioneel.

In `examen` bovenin het bestand stel je het aantal vragen, de tijd, de slaagnorm en de verdeling over de categorieën in. Zorg dat je van elke categorie minstens zoveel vragen hebt als de verdeling vraagt.

## Disclaimer

Dit is oefenmateriaal en geen officieel CBR-product. Alle vragen zijn zelf geschreven.
De examenopzet (50 vragen, 30 minuten, 41 goed om te slagen) is gebaseerd op de informatie van het CBR.
