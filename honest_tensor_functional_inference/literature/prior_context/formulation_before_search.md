# Initial formulation before literature search

This is a research assessment, not an extension of the existing manuscript. The existing project treats conditional-generator KL risk on compact, rank-separated TT strata; its fixed-stratum risk results and stability certificate do not establish uniform inference over rank boundaries.

Primary benchmark: observe iid (X_i,Y_i), with X_i in R^{p_1 x ... x p_K}, vec(X_i)~N(0,I_D), Y_i=<X_i,A>+epsilon_i, epsilon_i~N(0,sigma^2) independent, D=product p_k. Tensor A is the identifiable parameter; Tucker/TT factors are nonunique coordinates, not additional observed random variables. Fix K initially and permit dimensions and rank caps to grow. Use squared loss, population R(B)=sigma^2+||B-A||_F^2, empirical R_n(B)=n^{-1}sum(Y_i-<X_i,B>)^2. A rank-penalized constrained least-squares estimator is a pilot, not a required innovation.

Parameter space: ||A||_F<=M and Tucker mode ranks <=r_max or TT cut ranks <=r_max, including every lower-rank stratum and zero. Do not combine Tucker and TT as if their rank vectors and tangent spaces were interchangeable. No positive minimum unfolding singular-value assumption. First study known sigma and design law, no contamination or dependence; extend only if needed.

Target 1: prespecified linear functional psi_L(A)=<L,A>, ||L||_F=1. Seek liminf_n inf_A P_A{psi_L(A) in C_n}>=1-alpha. Define optimal interval length relative to the SAME rank-union honesty class and local alternatives; do not assume the known-rank oracle variance remains achievable at singular points. Weak singular values, ambient information degeneracy, and factor gauge nonidentifiability are different phenomena.

Diagnostic experiment: Z=A+(sigma/sqrt(n))G, iid standard Gaussian tensor G. The direct interval <L,Z> +/- z_(1-alpha/2)sigma||L||_F/sqrt(n) is exact across all ranks. Consequently existence of honest intervals alone cannot be the novelty claim. The question is whether rank-sensitive length adaptation can be characterized sharply, including an impossibility result and a useful attainable envelope.

Secondary target 2: quadratic functional q(A)=||A||_F^2 or model-based KL to a fixed reference; first derivative may vanish, requiring a separate nonregular analysis. Target 3: risk R(hat A) of a data-trained model, conditional on training, often has direct independent-validation inference; do not conflate with target 1 or 2.

Optional conditional-generator extension: iid prompt-response clusters (E_i,X_i,Y_i), Y_i~p_A(.|X_i,E_i), with frozen map p_A=softmax(g_A(X,E)), A a Tucker/TT weight block. Functional psi(A)=E_{X~Q}f(p_A(.|X)); fix Q and f. Full stochastic responses, exact probability queries and observed teacher weights are different statistical experiments. A response, not each dependent token, is one sample unit. This extension is secondary until the Gaussian benchmark survives the novelty audit.
