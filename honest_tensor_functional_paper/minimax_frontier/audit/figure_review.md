# Figure and PDF audit

The figure-designer guidance was applied to four scientific results figures.
All figures are generated with matplotlib from retained numerical results and
saved as vector PDF/SVG, with PNG previews. Nominal legend and annotation sizes
are at least 9 points; the figures are designed at the report's 6.8-inch width
so the report does not shrink a 10-inch plot into unreadable labels.

- `statistical_frontiers`: analytic comparisons are explicitly labelled. The
  profiles are annotated directly, and one-cap versus simultaneous-cap curves
  are distinguished as different parameter spaces. No solver output is implied.
- `spectral_performance`: paired direct and proposed lengths use solid/dashed
  lines, consistent colors, and common ordinate limits. Error bars are Monte
  Carlo uncertainty; modest or absent gains remain visible.
- `coordinate_hierarchy`: every Hamming distance is shown; common logarithmic
  axes and a shared legend avoid overlapping labels. Dotted segments are
  explicitly anchored theoretical exponents, not additional data.
- `computation`: preprocessing and subsequent evaluation are separated. The
  caption states three calls, one thread, four shapes, and no general minimax
  optimizer interpretation.

All four final figure previews were visually inspected. Earlier layout problems
with compressed three-panel legends were corrected. Representative pages from
both PDFs were inspected, and all pages were checked programmatically for
readable text, replacement glyphs, and content outside the page bounds. The
build logs contain no missing-character or undefined-command errors. PDF hashes
and page counts are recorded by the final validator.

The plots are evidence summaries, not substitutes for the supplied proofs.
