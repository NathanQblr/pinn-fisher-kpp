# 🚀 Docker — Fiche pratique

## 🔧 Commandes de base

### 🏗️ Build (construction de l'image)
```bash
docker build -t mon_image:tag -f chemin/vers/Dockerfile .
```

### 🚀 Run (exécuter un conteneur)
```bash
docker run --rm mon_image:tag
```

### 🧑‍💻 Run interactif (accès terminal)
```bash
docker run -it --rm mon_image:tag bash
```

### 🔁 Run avec ton dossier monté (dev local)
```bash
docker run -it --rm -v $(pwd):/app -w /app mon_image:tag bash
```

---

## 📁 Fichiers recommandés

### 🐳 `Dockerfile`
- Définit l’environnement de développement reproductible

### 📄 `.dockerignore`
- Évite de copier les fichiers inutiles dans l’image

---

## 🛠️ Bonnes pratiques

| Action | Bon réflexe |
|--------|-------------|
| Développement | Monte ton code local avec `-v $(pwd):/app` |
| Test rapide | `docker run --rm image pytest` |
| Ajout de dépendance | Modifie `requirements.txt` puis rebuild |
| Test automatique | Utilise GitHub Actions (workflow `build.yml`) |
| Propreté | Utilise `--rm` pour ne pas laisser de conteneurs |

---

## 📦 Structure recommandée

```
pinn-fisher-kpp/
├── docker/
│   ├── Dockerfile
│   └── dev.sh
├── .dockerignore
├── requirements.txt
├── src/
├── tests/
└── .github/workflows/build.yml
```

---

## 🔗 Documentation utiles

- [Dockerfile reference](https://docs.docker.com/engine/reference/builder/)
- [Docker CLI cheat sheet](https://dockerlabs.collabnix.com/docker/cheatsheet/)
- [Docker for scientists](https://replicate.com/blog/docker-science)
