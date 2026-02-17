---
title: "eduroam Netwerkinstallatie"
weight: 23
---


Sommige gebruikers kunnen problemen ondervinden met het verbinden met eduroam op moderne Linux-systemen met NetworkManager 1.50+ (getest op Fedora 43), waarbij de verbinding blijft hangen tijdens de TLS-handshake. In deze handleiding wordt de technische achtergrond uitgelegd en een oplossing geboden die betrouwbaar werkt op recente Linux-distributies.

## Wat niet werkt


Verschillende beschikbare tools en installers werken mogelijk niet direct op de nieuwste Linux-distributies door wijzigingen in NetworkManager. Hieronder een overzicht van veelgebruikte opties en hun gedrag op Fedora 43:


{{% details title="cat.eduroam.org installer (officieel)" closed="true" %}}
De Python-installer van [cat.eduroam.org](https://cat.eduroam.org/) biedt een grafische interface en maakt een verbindingsprofiel aan. Op sommige recente Linux-distributies (zoals Fedora 43) kan de verbinding blijven hangen tijdens de TLS-handshake door wijzigingen in NetworkManager. Zie [Technische vergelijking](#technische-vergelijking) hieronder voor meer details.

![cat.eduroam.org downloadportaal voor Saxion](/images/eduroam-cat-portal.avif)
{{% /details %}}

{{% details title="geteduroam Linux app (officieel)" closed="true" %}}

De [geteduroam Linux app](https://github.com/geteduroam/linux-app) (CLI en GUI RPM) kan op sommige recente distributies ook verbindingsproblemen ondervinden.
{{% /details %}}

{{% details title="easyroam-linux (community)" closed="true" %}}
[easyroam-linux](https://github.com/jahtz/easyroam-linux) van jahtz werkt mogelijk niet op alle distributies.
{{% /details %}}

{{% details title="UvA/HvA Linux eduroam handleiding" closed="true" %}}
De handleiding op [linux.datanose.nl](https://linux.datanose.nl/linux/eduroam/) (UvA/HvA) levert mogelijk niet op alle recente systemen een werkende verbinding op.
{{% /details %}}

## Wat wel werkt

De werkende configuratie gebruikt PEAP/MSCHAPv2 met CA-validatie via de systeem-truststore en `domain-suffix-match` — de moderne vervanging voor het verouderde `altsubject-matches` dat niet werkt op Fedora 43.

**Vereisten:**
- Python 3.10+
- NetworkManager 1.8+ (`nmcli`)

### Verbindingsinstellingen

| Instelling | Waarde |
|------------|--------|
| Beveiliging | WPA & WPA2 Enterprise |
| Authenticatie | Protected EAP (PEAP) |
| PEAP-versie | Automatisch |
| Interne authenticatie | MSCHAPv2 |
| CA-certificaat | Systeem-CA-bundel (`/etc/pki/tls/certs/ca-bundle.crt`) |
| Domeinvalidatie | `domain-suffix-match: ise.infra.saxion.net` |
| Fase2 domeinvalidatie | `phase2-domain-suffix-match: ise.infra.saxion.net` |
| Anonieme identiteit | `anonymous@saxion.nl` |
| Identiteit | `gebruiker@instelling.nl` |

{{< callout type="info" >}}
Deze configuratie valideert het RADIUS-servercertificaat via de systeem-CA-truststore en zowel `domain-suffix-match` als `phase2-domain-suffix-match` voor `ise.infra.saxion.net`. De anonieme identiteit (`anonymous@saxion.nl`) beschermt je gebruikersnaam tijdens de initiële handshake. Dit is een aanbevolen methode voor Linux-gebruikers die een veilige en geautomatiseerde setup willen. Android en Windows hebben hun eigen officiële workflows, die kunnen verschillen in certificaatvalidatie.
{{< /callout >}}

### Geautomatiseerde installatie (aanbevolen)

Een modern Python-script met GUI-ondersteuning automatiseert de hele `nmcli`-verbindingsconfiguratie voor Saxion:

```bash
curl -LO https://zephyrus-linux.stentijhuis.nl/scripts/saxion-eduroam.py
python3 saxion-eduroam.py
```

Het script doet het volgende:
1. Detecteert beschikbare GUI-tools (zenity, kdialog of yad) of valt terug naar terminal-invoer
2. Controleren of NetworkManager (`nmcli`) beschikbaar is
3. Een eventueel bestaand eduroam-verbindingsprofiel verwijderen
4. Een vriendelijke GUI-dialoog tonen voor het invoeren van je inloggegevens (gebruikersnaam + wachtwoord)
5. Een PEAP/MSCHAPv2-verbindingsprofiel aanmaken met:
   - CA-validatie via de systeem-truststore
   - Domeinvalidatie tegen `ise.infra.saxion.net`
   - Fase2 domeinsuffix-matching
   - Anonieme identiteit (`anonymous@saxion.nl`)
6. De verbinding automatisch activeren

Dit script is **Saxion-specifiek** en valideert tegen het Saxion RADIUS-serverdomein (`ise.infra.saxion.net`). Voor andere instellingen: download het officiële CAT-script via [cat.eduroam.org](https://cat.eduroam.org/) en pas het serverdomein en realm aan.

{{< callout type="info" >}}
Na afloop van het script wordt de verbinding automatisch geactiveerd — je zou binnen enkele seconden verbonden moeten zijn. Als je inloggegevens of het RADIUS-servercertificaat niet kloppen, kan NetworkManager een GUI-prompt tonen om je gegevens opnieuw in te voeren.
{{< /callout >}}

{{< callout type="warning" >}}
Je downloadt en voert een script uit vanaf het internet. Wil je extra veilig zijn, verifieer dan de bron (of checksum) voordat je het uitvoert.
{{< /callout >}}

Als alles goed gaat, zie je zoiets als dit:

![eduroam installer toont installatie geslaagd](/images/eduroam-installer-success.avif)

**Bron:** [saxion-eduroam.py](/scripts/saxion-eduroam.py)

### Handmatige setup via nmcli

```bash
nmcli connection add \
  type wifi \
  con-name "eduroam" \
  ssid "eduroam" \
  wifi-sec.key-mgmt wpa-eap \
  802-1x.eap peap \
  802-1x.phase2-auth mschapv2 \
  802-1x.identity "gebruiker@instelling.nl" \
  802-1x.password "je-wachtwoord" \
  802-1x.anonymous-identity "anonymous@saxion.nl" \
  802-1x.ca-cert file:///etc/pki/tls/certs/ca-bundle.crt \
  802-1x.domain-suffix-match "ise.infra.saxion.net" \
  802-1x.phase2-domain-suffix-match "ise.infra.saxion.net"
```

Maak daarna verbinding:

```bash
nmcli connection up eduroam
```

### Handmatige setup via GNOME Instellingen

1. Open **Instellingen → Wi-Fi**
2. Selecteer **eduroam**
3. Ga naar het **Beveiliging**-tabblad en vul de instellingen in uit de tabel hierboven
4. Voer je instellingsgegevens in
5. Klik op **Toepassen**

Zo hoort het Beveiliging-tabblad eruit te zien:

![GNOME Instellingen eduroam Beveiliging-tabblad](/images/eduroam-gnome-settings.avif)

### Verwijderen

```bash
nmcli connection delete eduroam
```

## Technische vergelijking

De officiele CAT-installer (van [cat.eduroam.org](https://cat.eduroam.org/)) en dit script verschillen op drie belangrijke punten:

| | Officieel CAT-script | Dit script |
|---|---|---|
| **CA-certificaat** | USERTrust RSA → GEANT OV RSA CA 4 (ingebouwd) | Systeem-CA-bundel (`/etc/pki/tls/certs/ca-bundle.crt`) |
| **Servervalidatie** | `altsubject-matches: DNS:ise.infra.saxion.net` (verouderd) | `domain-suffix-match: ise.infra.saxion.net` + phase2 |
| **Anonieme identiteit** | Niet ingesteld | `anonymous@saxion.nl` |
| **`password-flags`** | `1` (agent-owned — vereist secret agent zoals GNOME Keyring) | `1` (agent-owned — wachtwoord veilig opgeslagen in GNOME Keyring, niet in verbindingsbestand) |
| **Gebruikersinterface** | GUI en terminal-dialogen | GUI-ondersteuning (zenity/kdialog/yad) + terminal-fallback |
| **Resultaat op moderne NM (1.50+)** | Blijft hangen tijdens TLS-handshake | Verbindt direct |

### Hoe het officiele script verbindt


De officiele CAT-installer gebruikt een configuratie die mogelijk niet volledig compatibel is met de nieuwste NetworkManager-versies op sommige Linux-distributies:

1. **Sluit een CA-certificaatketen in** (USERTrust RSA root + GEANT OV RSA CA 4 intermediate) en instrueert NetworkManager om de RADIUS-server hiertegen te valideren.

2. **Stelt `altsubject-matches` in** op `DNS:ise.infra.saxion.net`. Deze property bestaat nog in NetworkManager, maar `domain-suffix-match` is de aanbevolen vervanging sinds NM 1.8 (2017). Op sommige recente systemen kan de combinatie van CA-validatie met `altsubject-matches` ervoor zorgen dat de TLS-handshake blijft hangen.

3. **Stelt `password-flags` in op `1`** (agent-owned), wat betekent dat NetworkManager verwacht dat een secret agent (bijv. GNOME Keyring) het wachtwoord levert bij het verbinden, in plaats van het uit het verbindingsbestand te lezen. Zonder een actieve, ontgrendelde keyring agent kan dit extra problemen veroorzaken.

### Hoe dit script verbindt


Dit script past de configuratie aan voor moderne Linux-systemen en voegt enkele functies toe:

- **Systeem-CA-bundel** — NetworkManager valideert het RADIUS-servercertificaat tegen de systeem-truststore, die USERTrust RSA bevat.
- **`domain-suffix-match` en `phase2-domain-suffix-match`** — gebruikt de moderne aanbevolen eigenschappen voor servervalidatie.
- **Anonieme identiteit** — beschermt je gebruikersnaam tijdens de initiële RADIUS-handshake door eerst `anonymous@saxion.nl` te verzenden.
- **`password-flags` op `1`** — het wachtwoord wordt veilig opgeslagen in je GNOME Keyring (of compatibele secret agent), niet in het verbindingsbestand.
- **GUI-ondersteuning** — detecteert en gebruikt automatisch zenity, kdialog of yad voor een gebruiksvriendelijke installatie-ervaring, met terminal-fallback.


Deze methode is ontworpen voor moderne Linux-systemen en kan een soepelere ervaring bieden op recente distributies. Android en Windows hebben hun eigen officiële workflows, die kunnen verschillen in certificaatvalidatie. Dit script is bedoeld als een aanbevolen methode voor Linux-gebruikers die een veilige en geautomatiseerde setup willen.


### Wachtwoordopslag

{{< callout type="info" >}}
Je eduroam-wachtwoord wordt **niet in platte tekst** op schijf opgeslagen. In plaats daarvan wordt het veilig opgeslagen in je GNOME Keyring (of compatibele secret agent). NetworkManager haalt het wachtwoord op uit de keyring bij het verbinden, dus zelfs gebruikers met root-toegang kunnen het niet zomaar uit een bestand lezen. Je kunt gevraagd worden je keyring te ontgrendelen bij het verbinden met eduroam.
{{< /callout >}}

{{< callout type="info" >}}
Dit script is geschreven door Sten Tijhuis ([Stensel8](https://github.com/Stensel8)) op basis van onderzoek naar hoe eduroam verbindt op Android en Windows, en een vergelijking van de officiele CAT-installer met wat moderne NetworkManager-versies ondersteunen. Het is niet verbonden aan of goedgekeurd door enige instelling of het eduroam-consortium.
{{< /callout >}}
