---
name: cold-email-french
description: >-
  Write French-language B2B cold emails with native phrasing, vouvoiement and lowercase
  subject lines, avoiding the formulas that read as spam in French. Use when the user
  writes in French, targets French-speaking prospects, or mentions email de prospection,
  cold email en français, prospection B2B, or relance en français.
---

# Cold email en français

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Écrire le premier email de la campagne <CAMPAIGN_ID> en français, pour des prospects francophones. Structure identique au skill "Cold email first touch", mais les règles de langue ci-dessous priment. Tu rédiges, je valide et j'active dans l'app.

## Steps
1. `list_sender_accounts` puis `get_campaign_authoring_context` — lis le dossier de signaux de chaque lead.
2. Rédige lead par lead : **objet** (2-4 mots, minuscules, sans point final) · **accroche** (1 phrase sur eux, le signal daté) · **lien** (1-2 phrases : pourquoi ce signal rend mon offre pertinente) · **preuve** (1 phrase, un chiffre ou un client nommé — sinon supprime la ligne) · **demande** (1 question, faible friction).
3. Pousse avec `write_campaign_drafts`, relis via `list_campaign_actions`, corrige avec `update_campaign_action_draft`.

## Règles de langue (non négociables)
- **Vouvoiement par défaut.** Tutoiement seulement si je le demande explicitement (écosystème startup/tech).
- **Objets en minuscules**, pas de title case à l'anglaise ("question rapide" et non "Question Rapide"). Pas de prénom dans l'objet.
- **Moins de 130 mots.** Le français est plus long que l'anglais à contenu égal : coupe plus fort, ne traduis pas.
- Pas de conditionnel de politesse en cascade ("je me permettrais de vous proposer de bien vouloir…"). Phrases courtes, verbes actifs.
- Une seule question à la fin, pas de "dans l'attente de votre retour".

## Marqueurs de texte généré (les plus coûteux)
- **Jamais de tiret cadratin ni demi-cadratin (— –) dans le message.** Le français ne les utilise pas : c'est le signal "écrit par une IA" le plus immédiat. Virgule, deux-points ou parenthèses.
- **Apostrophes typographiques (')**, pas droites (').
- **Aucun Markdown** : `**gras**`, `*italique*`, `#` arrivent en caractères bruts chez le destinataire.
- **Aération obligatoire** : retour à la ligne après chaque phrase, ligne vide entre deux blocs d'idées. Jamais un pavé.

## Mise en forme de l'email
- Propose un créneau. Le lien de prise de rendez-vous vit dans la signature, pas dans le corps.
- Signature : "Bien à vous," puis une ligne vide, puis le bloc signature.

## Formules interdites (marqueurs de spam en français)
"J'espère que vous allez bien" · "Je me permets de vous contacter" · "Suite à ma précédente relance" · "Je reviens vers vous" · "Sauf erreur de ma part" · "Nous sommes une société spécialisée dans…" · "Nous accompagnons les entreprises comme la vôtre" · "N'hésitez pas à revenir vers moi" · "Cet exemple pourrait vous parler" · "Une chose me saute aux yeux" · toute traduction littérale de "I hope this finds you well".

## Contrôle final
- L'email passe le test de substitution : sous un autre nom, il ne tient plus.
- Aucune phrase ne commence par "Je" ou "Nous".
- Relis à voix haute : si ça ne se dit pas, ça ne s'écrit pas.

## Hard rules
- Jamais de signal, de client ou de chiffre inventé.
- Brouillons uniquement. L'activation se fait dans Lead Scorer, par moi.
