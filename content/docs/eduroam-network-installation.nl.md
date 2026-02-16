---
title: "eduroam Netwerkinstallatie"
weight: 23
---

De officiele eduroam-installers en community-scripts werken niet op Fedora 43 (NetworkManager 1.50+). De verbinding blijft hangen tijdens de TLS-handshake — geen foutmelding, geen timeout, helemaal niks. In deze handleiding leg ik uit waarom, en geef ik je een setup die wel gewoon werkt.

## Wat niet werkt

Ik heb alle tools geprobeerd die ik kon vinden. Geen enkele leverde een werkende verbinding op onder Fedora 43:

{{% details title="cat.eduroam.org installer (officieel)" closed="true" %}}
De Python-installer van [cat.eduroam.org](https://cat.eduroam.org/) maakt wel een verbindingsprofiel aan, maar maakt nooit daadwerkelijk verbinding — hij blijft hangen tijdens de TLS-handshake. Je kunt hem zelf downloaden via [cat.eduroam.org](https://cat.eduroam.org/) en proberen, maar op Fedora 43 werkt het niet. Zie [Technische vergelijking](#technische-vergelijking) hieronder voor de reden.

![cat.eduroam.org downloadportaal voor Saxion](/images/eduroam-cat-portal.png)
{{% /details %}}

{{% details title="geteduroam Linux app (officieel)" closed="true" %}}
De [geteduroam Linux app](https://github.com/geteduroam/linux-app) (CLI en GUI RPM) heeft hetzelfde probleem: hij blijft eindeloos verbinden zonder ooit te slagen.
{{% /details %}}

{{% details title="easyroam-linux (community)" closed="true" %}}
[easyroam-linux](https://github.com/jahtz/easyroam-linux) van jahtz werkte ook niet.
{{% /details %}}

{{% details title="UvA/HvA Linux eduroam handleiding" closed="true" %}}
De handleiding op [linux.datanose.nl](https://linux.datanose.nl/linux/eduroam/) (UvA/HvA) leverde ook geen werkende verbinding op.
{{% /details %}}

## Wat wel werkt

De werkende configuratie gebruikt PEAP/MSCHAPv2 zonder CA-certificaatvalidatie — precies zoals Android en Windows in de praktijk ook verbinden met eduroam.

### Verbindingsinstellingen

| Instelling | Waarde |
|------------|--------|
| Beveiliging | WPA & WPA2 Enterprise |
| Authenticatie | Protected EAP (PEAP) |
| PEAP-versie | Automatisch |
| Interne authenticatie | MSCHAPv2 |
| CA-certificaat | Geen |
| Identiteit | `gebruiker@instelling.nl` |

{{< callout type="warning" >}}
Deze configuratie valideert het CA-certificaat van de server **niet**. Dit komt overeen met hoe Android en Windows zich gedragen, en voorkomt de validatieproblemen waardoor de officiele tools falen. Wees je bewust van de beveiligings-afweging.
{{< /callout >}}

### Geautomatiseerde installatie (aanbevolen)

Een Python-script automatiseert de hele `nmcli`-verbindingsconfiguratie:

```bash
curl -LO https://zephyrus-linux.stentijhuis.nl/scripts/eduroam-linux.py
python eduroam-linux.py
```

Het script doet het volgende:
1. Controleren of NetworkManager (`nmcli`) beschikbaar is
2. Een eventueel bestaand eduroam-verbindingsprofiel verwijderen
3. Om je inloggegevens vragen (gebruikersnaam + wachtwoord)
4. Een PEAP/MSCHAPv2-verbindingsprofiel aanmaken zonder CA-certificaatvalidatie
5. Proberen de verbinding te activeren

Als alles goed gaat, zie je zoiets als dit:

![eduroam installer toont installatie geslaagd](/images/eduroam-installer-success.png)

**Bron:** [eduroam-linux.py](/scripts/eduroam-linux.py)

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
  802-1x.password "je-wachtwoord"
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

![GNOME Instellingen eduroam Beveiliging-tabblad](/images/eduroam-gnome-settings.png)

### Verwijderen

```bash
nmcli connection delete eduroam
```

## Technische vergelijking

De officiele CAT-installer (van [cat.eduroam.org](https://cat.eduroam.org/)) en dit script verschillen op drie belangrijke punten:

| | Officieel CAT-script | Dit script |
|---|---|---|
| **CA-certificaat** | USERTrust RSA → GEANT OV RSA CA 4 (ingebouwd) | Geen |
| **Servervalidatie** | `altsubject-matches: DNS:ise.infra.saxion.net` | Geen |
| **`password-flags`** | `1` (agent-owned — vereist secret agent zoals GNOME Keyring) | `0` (opgeslagen in verbindingsbestand) |
| **Resultaat op Fedora 43** | Blijft hangen tijdens TLS-handshake | Verbindt direct |

### Hoe het officiele script verbindt

De officiele CAT-installer doet drie dingen die problemen veroorzaken op modern Fedora:

1. **Sluit een CA-certificaatketen in** (USERTrust RSA root + GEANT OV RSA CA 4 intermediate) en instrueert NetworkManager om de RADIUS-server hiertegen te valideren.

2. **Stelt `altsubject-matches` in** op `DNS:ise.infra.saxion.net`. Deze property bestaat nog in NetworkManager, maar `domain-suffix-match` is de aanbevolen vervanging sinds NM 1.8 (2017). Op Fedora 43 met NM 1.50+ zorgt de combinatie van CA-validatie met `altsubject-matches` ervoor dat de TLS-handshake vastloopt — geen foutmelding, geen timeout, alleen eindeloos laden.

3. **Stelt `password-flags` in op `1`** (agent-owned), wat betekent dat NetworkManager verwacht dat een secret agent (bijv. GNOME Keyring) het wachtwoord levert bij het verbinden, in plaats van het uit het verbindingsbestand te lezen. Zonder een actieve, ontgrendelde keyring agent kan dit extra problemen veroorzaken.

### Hoe dit script verbindt

Dit script verwijdert alle drie die instellingen:

- **Geen CA-certificaat** — NetworkManager slaat servercertificaatvalidatie over en gaat direct naar de PEAP-tunnel.
- **Geen `altsubject-matches`** — vermijdt het kapotte validatiepad volledig.
- **`password-flags` op `0`** — het wachtwoord wordt direct in het verbindingsbestand opgeslagen, zodat NetworkManager kan verbinden zonder afhankelijk te zijn van een externe secret agent.

Dit is functioneel hetzelfde als wat Android en Windows doen:

- **Windows** vraagt bij de eerste verbinding "Vertrouwt u dit certificaat?" — op OK klikken slaat verdere validatie over.
- **Android** — institutionele setup-handleidingen (inclusief die van Saxion zelf) instrueren gebruikers om certificaatvalidatie in te stellen op "Niet valideren".

De RADIUS-server van de instelling (`ise.infra.saxion.net`, Cisco ISE) werkt prima. Het probleem zit volledig aan de clientkant.

### Wachtwoordopslag

{{< callout type="warning" >}}
Je eduroam-wachtwoord wordt in **platte tekst** opgeslagen in het NetworkManager-verbindingsbestand:

```bash
sudo cat /etc/NetworkManager/system-connections/eduroam.nmconnection
```

Het bestand is alleen leesbaar door root (`chmod 600`). Houd hier rekening mee als je iemand `sudo`-toegang geeft of systeemback-ups extern kopieert.
{{< /callout >}}

{{< callout type="info" >}}
Dit script is geschreven door Sten Tijhuis ([Stensel8](https://github.com/Stensel8)) op basis van onderzoek naar hoe eduroam verbindt op Android en Windows, en een vergelijking van de officiele CAT-installer met wat moderne NetworkManager-versies ondersteunen. Het is niet verbonden aan of goedgekeurd door enige instelling of het eduroam-consortium.
{{< /callout >}}
