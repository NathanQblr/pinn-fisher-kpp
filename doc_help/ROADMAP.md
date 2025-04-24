### Semaine 1 — Plan d’action détaillé  
**PINNs pour équation de diffusion-réaction biologique (ex. Fisher-KPP 1-D ou 2-D)**  

---

#### 0. Pré-requis à préparer avant de commencer la semaine  
| Outils | Actions |
|--------|---------|
| **Repo GitHub** | Crée un dépôt `pinn-fisher-kpp` (branch `main` + branch `dev`). |
| **Condensé Docker** | Démarre `Dockerfile` minimal : `python:3.11-slim`, installe `pytorch`, `torchdiffeq`, `numpy`, `scipy`, `matplotlib`, `pytest`, `fenicsx` **ou** `scikit-fem` (baseline FEM). |
| **CI** | Ajoute un _workflow_ GitHub Actions « build-and-test » : build de l’image + lancement des tests unitaires sur CPU (≈ 5 min). |

---

#### J-1 / J-2  • Choix, cadrage & base-line numérique
1. **Sélection de la PDE**  
   - Formulation 1-D Fisher-KPP :  
     \[
       \partial_t u = D\,\partial_{xx}u + ru\!\left(1-\tfrac{u}{K}\right)
     \]  
     où `D, r, K` constants (>0).  
   - BC/IC : domaine \(x\in[0,1]\) avec \(u(0,t)=u(1,t)=0\), IC gaussienne centrée.

2. **Résolution *classique***  
   - Choisis **FEM** 1-D (scikit-fem) ou **FVM** fait-maison.  
   - Discrétisation temporelle : RK4 ou Crank-Nicolson.  
   - Sauvegarde de la solution de référence → `baseline_solution.npy`.  
   - **Test unitaire** : conservation de la positivité + ∥err∥ ≤ 1e-2.

---

#### J-3  • Conception du PINN
| Élément | Décision |
|---------|----------|
| **Entrées réseau** | \((x,t)\) (normalisés à \([-1,1]\)). |
| **Sortie** | \(\hat u(x,t)\). |
| **Architecture** | MLP : `4–8` couches fully-connected, `tanh` activations, ~ 2 000–10 000 paramètres. |
| **Loss globale** | \(\mathcal L = w_\text{PDE}\;\| \partial_t\hat u - D\,\partial_{xx}\hat u - r\hat u\!(1-\hat u/K) \|_2^2 \;+\; w_{\text{IC/BC}}\) … |
| **Collocation grid** | Latin-Hypercube : 5 000 points (intérieur) + 1 000 (frontières) + 500 (t=0). |
| **Optimiseur** | Adam (lr = 1e-3) + LBFGS en phase de raffinement. |

💡 **Astuce** : démarre avec `w_PDE = 1, w_IC = w_BC = 100` puis ajuste dynamiquement (`nn.Parameter` ou scheduler).

---

#### J-4  • Implémentation, entraînement & suivi
1. **Back-prop** avec autograd PyTorch.  
2. **Logging** : `tensorboard` → losses + L2-error vs baseline courbes.  
3. **Critères d’arrêt** : L2-error test < 1e-3 ou plateau 2 000 itérations.  
4. **Plots** : profils \(u(x,t)\) aux temps clés \(t=0,0.25,0.5,1\).

---

#### J-5  • Data-assimilation (bonus)  
- Traite **\(D\)** comme variable trainable :`D = torch.nn.Parameter(torch.tensor(0.2))`.  
- Ajoute petite quantité d’**observations bruitées** de \(u\) (5–10 points spatio-temporels).  
- Loss supplémentaire \(\mathcal L_\text{obs}\).  
- Mesure **erreur relative** sur \(D\), trace histogrammes quand ré-entraîné 10 fois (incertitude).  

---

#### J-6  • Industrialisation & reproductibilité
| Étape | Vérif. |
|-------|--------|
| **Docker build** | `docker build . && docker run pytest` doit passer. |
| **Tag** | `v0.1-baseline`, `v0.2-pinn`, `v0.3-pinn-estimation`. |
| **README** | Principe PINN ; dataset ; comment exécuter ; résultats (figures). |

---

#### J-7  • Polish, diffusion & valorisation
1. **Refactor** code → modules `pinn`, `utils`, `fem_baseline`.  
2. **Upload notebook de démonstration** + GIF animé convergence.  
3. **Post LinkedIn** : visuels + lessons learned (≈ 300 mots).  
4. **Argumentaire entretien** :  
   - *Hybrid solver* (FEM vs PINN) → choix selon régime (non-linéarité, coût mémoire).  
   - *Reproductibilité* (Docker + CI) → transfert facile équipe / cloud.  

---

#### Ressources ciblées (lecture rapide)
| Type | Lien |
|------|------|
| **Paper** | Raissi et al., *JCP 2019* « Physics-Informed Neural Networks ». |
| **Code** | `github.com/maziarraissi/PINNs` • `github.com/lululxvi/deepxde`. |
| **Tutos** | PyTorch Pinocchio / medQuadrics “PINN crash course” (vidéos courtes). |

---

#### Structure de dépôt indicative
```
pinn-fisher-kpp/
│
├── docker/
│   └── Dockerfile
├── src/
│   ├── pinn/
│   │   ├── model.py
│   │   └── train.py
│   ├── fem_baseline/
│   │   └── fem_solver.py
│   └── utils/
│       └── sampling.py
├── tests/
│   ├── test_fem.py
│   └── test_pinn.py
├── notebooks/
│   └── demo.ipynb
├── ci/
│   └── build.yml
└── README.md
```

---

### Bilan attendu fin de semaine
- **Comparatif chiffré** : L2-error FEM vs PINN ± incertitude paramètre \(D\).  
- **Image Docker** prête à l’emploi (`ghcr.io/<user>/pinn-fisher-kpp:latest`).  
- **Communication claire** (README + article LinkedIn) pour prouver :  
  1) compréhension math/physique,  
  2) implémentation ML,  
  3) bonnes pratiques d’ingénierie logicielle.  

➡️ En une semaine, tu produis un **prototype