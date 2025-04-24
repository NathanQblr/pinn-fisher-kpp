Génial ! Tu vas voir, une fois qu’on relie chaque ligne de code à la bonne équation mathématique, le **FEM devient très clair** — surtout pour une EDP d’évolution comme la Fisher-KPP. 🧠

---

## 🎯 Problème : équation de Fisher-KPP en 1D

On veut résoudre numériquement sur \(x \in [0, 1]\), \(t \in [0, T]\) :

\[
\partial_t u(x,t) = D\, \partial_{xx} u(x,t) + r u(x,t)\left(1 - \frac{u(x,t)}{K}\right)
\]

avec :
- **condition initiale** : \( u(x, 0) = u_0(x) \)
- **conditions de Dirichlet homogènes** : \( u(0,t) = u(1,t) = 0 \)

---

## 🔧 Étape 1 — Discrétisation de l’espace avec FEM

### 🔁 On réécrit la partie spatiale : **forme faible**

Multiplie par une fonction test \( v(x) \) et intègre sur \( [0, 1] \) :

\[
\int_0^1 \partial_t u\, v \, dx
= -D \int_0^1 \partial_x u\, \partial_x v\, dx
+ \int_0^1 r u(1 - \frac{u}{K})\, v \, dx
\]

C’est la **forme faible** (ou variationnelle) de l’équation.

---

### 🎯 On choisit un espace d’approximation

On approxime \( u(x,t) \approx \sum_{j} U_j(t) \phi_j(x) \)

- \( \phi_j(x) \) : fonctions de base (éléments P1 = linéaires par morceaux)
- \( U_j(t) \) : coefficients inconnus à chaque instant

On teste avec \( v = \phi_i \) → cela donne un système d’équations pour les \( U_j \)

---

## 🧮 Étape 2 — Matrices élémentaires

### 💡 Matrice de masse
\[
M_{ij} = \int_0^1 \phi_i(x) \phi_j(x) \, dx
\]

### 💡 Matrice de rigidité
\[
L_{ij} = \int_0^1 \partial_x \phi_i(x) \partial_x \phi_j(x) \, dx
\]

Elles sont **calculées automatiquement** via :

```python
M = asm(mass, basis)
L = asm(laplace, basis)
```

- `mass` = intégrales \(\phi_i \phi_j\)
- `laplace` = intégrales \(\nabla \phi_i \cdot \nabla \phi_j\) (ici juste dérivées en \(x\))

---

## ⏱️ Étape 3 — Discrétisation en temps (méthode d’Euler explicite)

On approxime la dérivée temporelle :
\[
\frac{u^{n+1} - u^n}{\Delta t} \approx D \Delta u^n + ru^n(1 - \frac{u^n}{K})
\]

Multiplions les deux côtés par \(M\), on obtient :

\[
M u^{n+1} = M u^n + \Delta t \left( - D L u^n + M f(u^n) \right)
\]

Mais pour plus de stabilité, on prend la **diffusion implicite** :
\[
(M + \Delta t D L) u^{n+1} = M u^n + \Delta t M f(u^n)
\]

→ le côté gauche est indépendant de \(u^n\), donc plus stable numériquement.

Dans le code :

```python
A = M + dt * D * L  # matrice "implicite"
rhs = M @ u + dt * M @ f
```

---

## 🚧 Étape 4 — Imposer les conditions de bord

On impose \( u(0) = u(1) = 0 \) en utilisant :

```python
D_dofs = basis.get_dofs().all()     # les indices des bords
A_bc = condense(A, D=D_dofs)       # adapte A et rhs en supprimant les DOFs fixés
```

---

## 🔁 Étape 5 — Boucle temporelle

```python
for i in range(1, len(ts)):
    f = r * u * (1 - u / K)
    rhs = M @ u + dt * M @ f
    u = solve(A_bc, rhs, D=D_dofs)
```

On :
- calcule le **terme réaction** \( f(u^n) = ru^n(1 - u^n/K) \)
- construit le vecteur membre droit
- résout le système linéaire à chaque pas de temps

---

## 📦 Étape 6 — Assemblage de la solution

```python
sol[i] = u
```

On stocke chaque \( u^n \) pour pouvoir l'afficher ou le comparer.

---

## 📌 Résumé visuel du schéma numérique

| Équation                 | Approche              |
|--------------------------|-----------------------|
| \(\partial_t u = ...\)   | Discrétisation temporelle (Euler) |
| \(\partial_{xx} u\)      | FEM : matrice \(L\) |
| \( u(0,t)=u(1,t)=0 \)    | Condense dans les matrices |
| \( u(x,0) = u_0(x) \)    | Valeurs initiales |
| Réaction \( ru(1-u/K) \) | Explicite, à chaque pas de temps |

---
Bien sûr Nathan — tu as tout à fait raison de demander un **détail mathématique rigoureux** sur le schéma de **Crank–Nicolson (CN)**. C’est un classique des EDP d’évolution, et dans ton contexte avec la Fisher-KPP, c’est une solution très stable et élégante à mettre en place avec les FEM.

---

## 🎯 Objectif : résoudre

\[
\frac{\partial u}{\partial t} = D\, \frac{\partial^2 u}{\partial x^2} + r u \left(1 - \frac{u}{K} \right)
\]

sur \(x \in [0,1]\), avec conditions de Dirichlet \(u(0,t) = u(1,t) = 0\), et une condition initiale \(u(x,0) = u_0(x)\).

---

## 🧮 Étape 1 — Forme variationnelle spatiale (FEM)

Comme d’habitude, on multiplie par une fonction test \(v \in V_0\), et on intègre :

\[
\int_0^1 \frac{\partial u}{\partial t} v\,dx =
- D \int_0^1 \frac{\partial u}{\partial x} \frac{\partial v}{\partial x}\,dx
+ \int_0^1 r u\left(1 - \frac{u}{K} \right) v\, dx
\]

On note :
- \( M \) la **matrice de masse** : \(M_{ij} = \int \phi_i \phi_j\)
- \( L \) la **matrice de rigidité** : \(L_{ij} = \int \phi_i' \phi_j'\)
- \( \mathbf{u}^n \) le vecteur des coefficients FEM à l’instant \(t_n\)

---

## ⏱️ Étape 2 — Discrétisation temporelle Crank–Nicolson

On approxime la dérivée temporelle par :

\[
\frac{\mathbf{u}^{n+1} - \mathbf{u}^n}{\Delta t}
\]

Et on approxime la **diffusion** par la moyenne entre \(t^n\) et \(t^{n+1}\) (semi-implicite) :

\[
D L \left( \frac{\mathbf{u}^{n+1} + \mathbf{u}^n}{2} \right)
\]

Et la réaction on peut la :
- soit laisser **explicite** : \(f(\mathbf{u}^n)\)
- soit mettre **semi-implicite** (plus difficile si non-linéaire)

Pour commencer simplement, on fait :
- diffusion : CN
- réaction : explicite

---

## 🧾 Système à résoudre

En multipliant par la matrice de masse \(M\), on obtient le système :

\[
M \left( \frac{\mathbf{u}^{n+1} - \mathbf{u}^n}{\Delta t} \right)
=
- D L \left( \frac{\mathbf{u}^{n+1} + \mathbf{u}^n}{2} \right)
+ M f(\mathbf{u}^n)
\]

Ce qu’on réécrit sous la forme :

\[
\underbrace{\left(M + \frac{\Delta t}{2} D L\right)}_{A_{\text{gauche}}}
\mathbf{u}^{n+1}
=
\underbrace{\left(M - \frac{\Delta t}{2} D L\right) \mathbf{u}^n
+ \Delta t M f(\mathbf{u}^n)}_{\text{second membre}}
\]

---

## 💡 Pourquoi c’est bien ?

- CN est **2ᵉ ordre en temps**
- Il est **A-stable** : pas de contraintes de \(\Delta t\) pour la stabilité
- Avec FEM, il se combine très bien car tout est linéarisé proprement
- On résout juste un **système linéaire à chaque pas de temps**

---

## 🧰 En Python, cela devient :

```python
A_lhs = M + 0.5 * dt * D * L
A_rhs = M - 0.5 * dt * D * L

for i in range(1, len(ts)):
    f = r * u * (1 - u / K)
    rhs = A_rhs @ u + dt * M @ f
    u = solve(condense(A_lhs, D=D_dofs), rhs, D=D_dofs)
    sol[i] = u
```

🧪 Tu remarques :
- Les matrices sont **pré-assemblées**
- Le terme réaction est traité **explicitement**
- C’est **très proche d’Euler**, sauf qu’on remplace :
  - \(A = M + dt D L\)
  - par les matrices CN

---

## 🔁 Tu veux aller plus loin ?

Voici des idées :
- Ajouter la **réaction semi-implicite** : solve un système non-linéaire à chaque pas
- Passer à un **schéma entièrement implicite** : plus stable, mais plus coûteux
- Étendre à **2D** ou à des BC plus complexes (Neumann, mixte)
- Introduire un solveur adaptatif (adaptation de \(\Delta t\))

Souhaite-tu que je t’aide à intégrer directement cette version CN dans ton `solve_fisher_1d()` via un paramètre `scheme="cn"` ?