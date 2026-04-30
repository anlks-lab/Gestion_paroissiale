# TODO.MD

## New modifications(tasks to accomplish)

### Architecture globale du système

Ton système est organisé en trois couches distinctes, ce qui est important à présenter clairement dans ton mémoire.

```text
┌─────────────────────────────────────────┐
│           CLIENTS (Couche présentation) │
│  Interface web admin  │  App mobile     │
└─────────────────┬───────────────────────┘
                  │ Requêtes HTTP/HTTPS
                  │ (JSON)
┌─────────────────▼───────────────────────┐
│         API REST (Couche métier)        │
│         Django REST Framework           │
│  Authentification │ Routage │ Logique   │
└─────────────────┬───────────────────────┘
                  │ ORM Django
┌─────────────────▼───────────────────────┐
│       Base de données (Couche données)  │
│              MySQL                 │
└─────────────────────────────────────────┘
```

### Modèle de données

C'est le cœur de ta conception. Chaque entité ci-dessous correspond à une table dans ta base de données et à un ensemble d'endpoints dans ton API.

#### Entité 1 — Utilisateur (User)

```text
User
├── id (UUID, clé primaire)
├── nom
├── prenom
├── email (unique)
├── mot_de_passe (haché)
├── role (admin / pretre / secretaire / tresorier / responsable / fidele)
├── telephone
├── date_creation
└── est_actif (booléen)
```

#### Entité 2 — Membre / Fidèle

```Membre
   ├── id (UUID, clé primaire)
   ├── user (clé étrangère → User, nullable)
   ├── nom
   ├── prenom
   ├── date_naissance
   ├── sexe
   ├── telephone
   ├── email
   ├── quartier
   ├── date_inscription
   ├── est_baptise (booléen)
   ├── est_confirme (booléen)
   └── groupe (clé étrangère → Groupe)
```

#### Entité 3 — Groupe / Mouvement

```text
Groupe
├── id
├── nom (ex : Chorale, Jeunes, Catéchisme)
├── description
├── responsable (clé étrangère → User)
└── date_creation
```

#### Entité 4 — Événement

```text
Evenement
├── id
├── titre
├── type (messe / fete_liturgique / reunion / kermesse / reservation)
├── description
├── date_debut
├── date_fin
├── lieu
├── est_inscription_requise (booléen)
└── createur (clé étrangère → User)
```

#### Entité 5 — Participation

```text
Participation
├── id
├── evenement (clé étrangère → Evenement)
├── membre (clé étrangère → Membre)
└── date_inscription
```

#### Entité 6 — Transaction financière

```text
Transaction
├── id
├── type (recette / depense)
├── categorie (quete / don / location / librairie / autre)
├── montant
├── description
├── date
├── membre (clé étrangère → Membre, nullable — si don nominatif)
└── enregistre_par (clé étrangère → User)
```

#### Entité 7 — Article (Librairie)

```text
Article
├── id
├── nom
├── description
├── categorie (livre / bougie / chapelet / vetement / autre)
├── prix_unitaire
├── stock_disponible
├── seuil_alerte (stock minimum avant alerte)
└── date_ajout
```

#### Entité 8 — Vente (Librairie)

```text
Vente
├── id
├── article (clé étrangère → Article)
├── quantite
├── prix_total
├── date
├── membre (clé étrangère → Membre, nullable)
└── enregistre_par (clé étrangère → User)
```

#### Entité 9 — Sacrement

```text
Sacrement
├── id
├── type (bapteme / mariage / confirmation / communion / funerailles)
├── membre (clé étrangère → Membre)
├── date
├── officiant (clé étrangère → User)
└── observations
```

### Conception des endpoints

Un endpoint est une URL de l'API associée à une méthode HTTP. Voici l'ensemble des endpoints organisés par module, en suivant les conventions REST.
Convention utilisée :

#### Module Authentification — préfixe /api/auth/

| Méthode | Endpoint | Description | Rôle requis |
| --- | --- | --- | --- |
| POST | api/auth/register/ | Créer un compte | Admin |
| POST | api/auth/login/ | Obtenir un token JWT | Public |
| POST | api/auth/token/refresh/ | Rafraîchir le token | Authentifié |
| POST | api/auth/logout/ | Invalider le token | Authentifié |
| GET | api/auth/me/ | Profil de l'utilisateur connecté | Authentifié |

#### Module Membres — préfixe /api/membres/

| Méthode | Endpoint | Description | Rôle requis |
| --- | --- | --- | --- |
| GET | api/membres/ | Lister tous les membres | Secrétaire+ |
| POST | api/membres/ | Créer un membre | Secrétaire+ |
| GET | api/membres/{id}/ | Détails d'un membre | Secrétaire+ |
| PATCH | api/membres/{id}/ | Modifier un membre | Secrétaire+ |
| DELETE | api/membres/{id}/ | Supprimer un membre | Admin |
| GET | api/membres/{id}/sacrements/ | Sacrements d'un membre | Secrétaire+ |

#### Module Groupes — préfixe /api/groupes/

| Méthode | Endpoint | Description | Rôle requis |
| --- | --- | --- | --- |
| GET | api/groupes/ | Lister les groupes | Authentifié |
| POST | api/groupes/ | Créer un groupe | Admin |
| GET | api/groupes/{id}/ | Détails d'un groupe | Authentifié |
| PATCH | api/groupes/{id}/ | Modifier un groupe | Admin |
| DELETE | api/groupes/{id}/ | Supprimer un groupe | Admin |
| GET | api/groupes/{id}/membres/ | Membres d'un groupe | Authentifié |

#### Module Événements — préfixe /api/evenements/

| Méthode | Endpoint | Description | Rôle requis |
| --- | --- | --- | --- |
| GET | api/evenements/ | Lister les événements | Authentifié |
| POST | api/evenements/ | Créer un événement | Secrétaire+ |
| GET | api/evenements/{id}/ | Détails d'un événement | Authentifié |
| PATCH | api/evenements/{id}/ | Modifier un événement | Secrétaire+ |
| DELETE | api/evenements/{id}/ | Supprimer un événement | Admin |
| POST | api/evenements/{id}/inscrire/ | Inscrire un membre | Secrétaire+ |
| GET | api/evenements/{id}/participants/ | Liste des participants | Secrétaire+ |

#### Module Finances — préfixe /api/finances/

| Méthode | Endpoint | Description | Rôle requis |
| --- | --- | --- | --- |
| GET | /api/finances/transactions/ | Lister les transactions | Trésorier+ |
| POST | api/finances/transactions/ | Enregistrer une transaction | Trésorier+ |
| GET | api/finances/transactions/{id}/ | Détails d'une transaction | Trésorier+ |
| DELETE | api/finances/transactions/{id}/ | Supprimer une transaction | Admin |
| GET | api/finances/rapport/ | Rapport financier par période | Trésorier+ |
| GET | api/finances/membre/{id}/dons/ | Historique des dons d'un membre | Trésorier+ |

#### Module Librairie — préfixe /api/librairie/

| Méthode | Endpoint | Description | Rôle requis |
| --- | --- | --- | --- |
| GET | api/librairie/articles/ | Lister les articles | Authentifié |
| POST | api/librairie/articles/ | Ajouter un article | Secrétaire+ |
| GET | api/librairie/articles/{id}/ | Détails d'un article | Authentifié |
| PATCH | api/librairie/articles/{id}/ | Modifier un article | Secrétaire+ |
| DELETE | api/librairie/articles/{id}/ | Supprimer un article | Admin |
| POST | api/librairie/ventes/ | Enregistrer une vente | Secrétaire+ |
| GET | api/librairie/ventes/ | Historique des ventes | Secrétaire+ |
| GET | api/librairie/alertes/ | Articles en stock critique | Secrétaire+ |
