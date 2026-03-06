# Guide pour URL Permanente

## L'URL actuelle (gratuite)
L'URL Cloudflare Tunnel gratuite **n'est pas permanente** - elle change à chaque redémarrage.

## Solutions pour URL Permanente

### Option 1: Cloudflare Tunnel Nommé (Gratuit)
1. Créez un compte sur cloudflare.com
2. Installez cloudflared:
   ```bash
   cloudflared tunnel create hotel-med
   ```
3. Créez le tunnel:
   ```bash
   cloudflared tunnel route dns hotel-med hotelmediterranee
   ```
4. Lancez avec:
   ```bash
   cloudflared tunnel --config config.yml run hotel-med
   ```

### Option 2: Service DNS Dynamique (Gratuit)
Utilisez No-IP ou DynDNS:
1. Créez un compte sur no-ip.com
2. Créez un hostname gratuit (ex: hotelmed.hopto.org)
3. Configurez votre routeur pour mettre à jour l'IP

### Option 3: Acheter un Nom de Domaine
- Achetez un .com ou .tn sur Hostinger, OVH, etc.
- Pointez vers votre IP publique

## Lancement Actuel
Pour lancer maintenant avec URL temporaire:
Double-cliquez sur start_internet.bat
