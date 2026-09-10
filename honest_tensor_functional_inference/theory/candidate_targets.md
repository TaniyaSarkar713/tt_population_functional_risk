# Candidate targets before manuscript claims

The prior survey left optimal general-loading rank adaptation unresolved. This project narrows to orthogonal tensor contrasts and tests the following chain.

1. A Tucker/TT rank cap and Frobenius bound imply an l_(2/K) bound on orthogonal diagonal contractions.
2. Coordinate soft thresholding gives a finite-sample honest interval with a radius determined by that bound, without estimating actual rank or nonzero singular values.
3. Every fixed-radius affine interval has a larger worst-case required radius in a specified growing-dimensional regime.
4. Every interval honest on a model retaining only one unfolding rank constraint must remain long at zero, even though the joint tensor model permits a uniformly shorter interval.
5. A coordinate-spike mixture gives a lower bound within the joint model. Matching it with an upper bound is a separate target, not assumed.

These targets deliberately distinguish existence, separation from a restricted method class, separation between honesty classes, and unrestricted minimax optimality. Only the first four and a nonmatching lower bound are established below. The general adaptive-length problem remains PARTIAL.
