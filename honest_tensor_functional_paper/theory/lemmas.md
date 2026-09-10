# Lemma index

All listed lemmas are PROVED in proofs.md or the linked diagonal benchmark derivation.

| Lemma | Statement | Proof location | Role |
|---|---|---|---|
| L1 | Tucker expansion with at most min_k product_(l!=k)r_l terms and sum squared CP weights equal to the squared Frobenius norm | P1 | Controls the rank factor without singular-value denominators |
| L2 | Left-canonical TT path expansion has sum squared weights equal to the squared Frobenius norm | P1 | Establishes the TT analogue despite nonorthogonal paths |
| L3 | Orthogonal diagonal contraction of each CP term has l_(2/K) quasi-norm power <= its CP weight^(2/K) | P2 | Holder and Bessel reduction |
| L4 | On abs(e)<=lambda, soft threshold error <=min(abs(x),2lambda) | P3 | Finite deterministic coverage envelope |
| L5 | An interval covering zero and a mixture-common target has expected length >=target distance times (1-2alpha-TV) | P6 | Both lower bounds |
| L6 | E exp(a S_p^2/p)<=(1-2a)^(-1/2), a<1/2, for a sum of p Rademachers | P7 | Dimension-independent mixture proximity |

Holder, Bessel, Gaussian tail bounds, Gaussian likelihood ratios, and the sparse-mixture argument are established tools. The project-specific content is their use to quantify the difference between joint tensor constraints and a single-unfolding honesty class.

L7 — PROVED: the rank-one diagonal image is exactly an ell_(2/K) ball; see P2b and manuscript Lemma 2.

L8 — PROVED: if H is the overlap of two uniform size-s subsets of p coordinates, then E exp(rho^2 H) <= exp{s^2(exp(rho^2)-1)/p}. The factorial-moment proof is in [diagonal_minimax.md](diagonal_minimax.md), step 3. This is a classical mixture bound and is not asserted for H^K.
