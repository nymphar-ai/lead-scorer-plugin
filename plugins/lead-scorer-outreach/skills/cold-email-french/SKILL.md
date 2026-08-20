---
name: cold-email-french
description: >-
  Write French-language B2B cold emails with native phrasing, vouvoiement and French
  sentence-case subject lines, avoiding the formulas that read as spam in French. Use when
  the user writes in French, targets French-speaking prospects, or mentions email de
  prospection, cold email en français, prospection B2B, or relance en français.
---

# Cold email en français

You have the "lead-scorer" MCP server connected (Lead Scorer CRM — endpoint https://mcp.lead-scorer.com/mcp, authenticated with Lead Scorer OAuth). Use its tools for every read and write. Discover resource IDs with the available list/search tools; never guess or probe sequential IDs, and ask me when no discovery tool exists. Never invent data: if a tool result is empty, say so. An API key is only a manual fallback for clients without OAuth support.

> **Context first.** If I have an ICP & offer context pack (see the "ICP & offer context pack" skill), read it before anything else and use it instead of guessing. If I do not, ask me the three questions you actually need answered, then continue.

## Goal
Écrire le premier email de la campagne <CAMPAIGN_ID> en français, pour des prospects francophones. Structure identique au skill "Cold email first touch", mais les règles de langue ci-dessous priment. Tu rédiges, je valide et j'active dans l'app.

## Steps
1. `list_sender_accounts`, puis résous la campagne avec `list_campaigns` si son ID est inconnu avant `get_campaign_authoring_context` — lis le dossier de signaux de chaque lead. Pour l'email, arrête-toi si `signature_configured` est faux : demande-moi la signature exacte puis enregistre-la une fois avec `update_sender_account`, sans jamais inventer l'identité de l'expéditeur.
2. Rédige lead par lead : **objet** (2-6 mots, casse française, sans point final) · **angle métier** (1-2 phrases sur un problème crédible de sa fonction) · **cas client concret** (3-5 phrases : contexte, solution construite, usage dans le travail et changement obtenu) · **lien avec son rôle** (1 phrase) · **demande** (1 question, faible friction).
3. Pousse avec `write_campaign_drafts`, relis via `list_campaign_actions`, corrige avec `update_campaign_action_draft`.

## Règles de langue (non négociables)
- **Vouvoiement par défaut.** Tutoiement seulement si je le demande explicitement (écosystème startup/tech).
- **Objets avec une majuscule initiale**, puis casse française : noms propres et acronymes conservent leurs majuscules, sans Title Case à l'anglaise. Exemples : "Projets IA pour les opérations", "Activation CRM prédictive". Pas de prénom dans l'objet.
- **Moins de 160 mots.** Réserve assez de place au cas client pour rendre le déroulement et l'usage imaginables, puis coupe tout le reste.
- Pas de conditionnel de politesse en cascade ("je me permettrais de vous proposer de bien vouloir…"). Phrases courtes, verbes actifs.
- Une seule question à la fin, pas de "dans l'attente de votre retour".

## Personnalisation honnête
- Ne force jamais une actualité ou un signal en accroche pour feindre un intérêt personnel. Écarte les formulations comme "votre actualité m'a intéressé" ou "j'ai vu que vous…" si elles ne changent pas réellement l'hypothèse commerciale.
- Personnalise d'abord par le poste, le département, le modèle opérationnel et le problème probable. Un signal public ne sert que s'il rend cette hypothèse plus précise.
- Énonce l'hypothèse comme telle. Ne prétends pas connaître un problème interne qui n'a pas été vérifié.

## Cas client concret
- Le cas client doit permettre au destinataire de visualiser l'expérience, pas seulement prouver qu'un projet existe.
- Décris successivement : **qui a porté le besoin** · **quel problème métier était traité** · **ce qui a été construit** · **comment l'équipe l'utilise** · **quel résultat ou quelle décision cela améliore**.
- Si plusieurs projets illustrent l'accompagnement continu, relie-les chronologiquement : premier département, première livraison, puis extension aux autres équipes.
- N'invente jamais un résultat chiffré. Sans métrique vérifiée, décris le changement opérationnel observable, par exemple un ciblage plus fin, une production de contenu accélérée ou une décision d'ouverture mieux étayée.
- Évite les listes de trois cas réduits à leurs intitulés. Développe un cas principal, puis cite brièvement les extensions seulement si elles renforcent la projection.

## Marqueurs de texte généré (les plus coûteux)
- **Jamais de tiret cadratin ni demi-cadratin (— –) dans le message.** Le français ne les utilise pas : c'est le signal "écrit par une IA" le plus immédiat. Virgule, deux-points ou parenthèses.
- **Apostrophes typographiques (’)**, pas droites (').
- **Aucun Markdown** : `**gras**`, `*italique*`, `#` arrivent en caractères bruts chez le destinataire.
- **Aération obligatoire** : retour à la ligne après chaque phrase, ligne vide entre deux blocs d'idées. Jamais un pavé.

## Mise en forme de l'email
- Dans `write_campaign_drafts`, enregistre le corps des étapes email en HTML minimal : un bloc `<p>` par idée, sans CSS, tableau, titre ni Markdown. Échappe tout contenu dynamique susceptible de contenir `<`, `>` ou `&`.
- Garde les étapes LinkedIn en texte brut. Ne mets jamais de balises HTML dans une invitation ou un message LinkedIn.
- Propose un créneau. Le lien de prise de rendez-vous vit dans la signature, pas dans le corps.
- Signature email HTML : `<p>Bien à vous,<br><br>LE_BLOC_SIGNATURE</p>`.

## Formules interdites (marqueurs de spam en français)
"J'espère que vous allez bien" · "Je me permets de vous contacter" · "Suite à ma précédente relance" · "Je reviens vers vous" · "Sauf erreur de ma part" · "Nous sommes une société spécialisée dans…" · "Nous accompagnons les entreprises comme la vôtre" · "N'hésitez pas à revenir vers moi" · "Cet exemple pourrait vous parler" · "Une chose me saute aux yeux" · toute traduction littérale de "I hope this finds you well".

## Contrôle final
- L'email passe le test de substitution : sous un autre nom, il ne tient plus.
- L'accroche reste honnête même si le prospect sait exactement pourquoi il a été ciblé.
- Le cas client répond sans jargon aux questions : qui, quel problème, quoi, comment et pour quelle amélioration concrète ?
- Aucune phrase ne commence par "Je" ou "Nous".
- Relis à voix haute : si ça ne se dit pas, ça ne s'écrit pas.

## Hard rules
- Jamais de signal, de client ou de chiffre inventé.
- Brouillons uniquement. L'activation se fait dans Lead Scorer, par moi.
