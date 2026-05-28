# Guide de Traduction de Livres avec Aphra

Pour que vos projets de traduction restent propres, que l'IA ne mélange pas les pinceaux entre deux livres différents et que vous puissiez suivre l'avancement chapitre par chapitre, voici la structure de répertoire idéale à mettre en place.

Le secret est de **séparer les livres à la racine**, puis de cloisonner les étapes de traduction à l'intérieur.

## 1. La Structure de Dossiers Idéale

Créez une arborescence claire, idéalement en dehors du code d'Aphra pour ne pas risquer de tout perdre lors d'une mise à jour du framework. Par exemple dans un dossier `Traduction_Livres` :

```text
Traduction_Livres/
│
├── Livre_1_NomDuLivre/
│   ├── 01_original/          # Vos chapitres bruts en anglais
│   │   ├── ch1.md
│   │   └── ch2.md
│   ├── 02_traduit/           # Les résultats générés par Aphra
│   │   ├── ch1_FR.md
│   │   └── ch2_FR.md
│   └── workspace/            # (OPTIONNEL) Dossier pour stocker vos notes/lorebook manuels
│       └── [Fichiers de mémoire, prompts customisés...]
│
└── Livre_2_AutreLivre/
    ├── 01_original/
    ├── 02_traduit/
    └── workspace/
```

---

## 2. Le Workflow Étape par Étape (Mode d'Emploi)

Voici la routine exacte à suivre pour traduire votre premier livre sans encombre.

### Étape 1 : Préparation du livre

Ne donnez pas un pavé de 400 pages d'un coup en local, découpez votre livre en fichiers Markdown séparés par chapitre dans le dossier `01_original`.

* *Astuce :* Nommez-les de manière séquentielle (`ch1.md`, `ch2.md`, `ch3.md`) pour que votre terminal s'y retrouve facilement.

### Étape 2 : Lancement du Chapitre 1

Ouvrez votre terminal dans votre dossier `aphra`, activez le `venv` et lancez la commande en pointant vers les dossiers du **Livre 1** :

```bash
python aphra_runner.py \
  -c config.toml \
  -w book_translation \
  -i ../Traduction_Livres/Livre_1_NomDuLivre/01_original/ch1.md \
  -o ../Traduction_Livres/Livre_1_NomDuLivre/02_traduit/ch1_FR.md \
  -s "English" \
  -t "French"
```

> **Note sur les modèles :** Les modèles (comme "dolphin3") ne se configurent pas en ligne de commande. Vous devez modifier le fichier `config.toml` à la racine d'Aphra pour définir vos modèles.
>
> **Ce qui se passe ici :** Aphra va analyser le `ch1.md` et générer la traduction en utilisant le workflow `book_translation`. Il lira automatiquement (ou créera) le fichier `workspace/lorebook.md` pour garantir la continuité entre les chapitres.

### Étape 3 : Traduction du Chapitre 2 (La Continuité)

Pour le chapitre suivant, vous changez **uniquement** les noms des fichiers d'entrée et de sortie :

```bash
python aphra_runner.py \
  -c config.toml \
  -w book_translation \
  -i ../Traduction_Livres/Livre_1_NomDuLivre/01_original/ch2.md \
  -o ../Traduction_Livres/Livre_1_NomDuLivre/02_traduit/ch2_FR.md \
  -s "English" \
  -t "French"
```

> **Ce qui se passe ici :** Le modèle lira le lorebook mis à jour lors du chapitre 1, traduira le chapitre 2 en respectant le style et les personnages, puis mettra à nouveau à jour le lorebook à la fin.

---

## 3. Configuration des modèles (config.toml)

Pour utiliser des modèles spécifiques comme Dolphin 3 en local via Ollama, vous devez éditer le fichier `config.toml` (créez-le à partir de `config.example.toml` si besoin) :

```toml
[openrouter]
base_url = "http://localhost:11434/v1"
api_key = "ollama"

[book_translation]
writer = "dolphin3"
searcher = "dolphin3"
critiquer = "dolphin3"
```

## 4. Les Règles d'Or pour la continuité

* **Règle n°1 : Vérifiez le lorebook.** Après chaque traduction, ouvrez `workspace/lorebook.md` pour vous assurer que l'IA a bien capturé les bonnes informations. Vous pouvez modifier ce fichier manuellement si besoin !
* **Règle n°2 : Les sauvegardes.** Faites toujours une copie de vos traductions validées et de votre lorebook. Ne comptez pas uniquement sur l'historique du terminal.
