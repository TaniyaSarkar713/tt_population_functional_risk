# Figure design and integrity plan

Experimental-results line plots suit parameter sweeps; error-bar point plots suit paired coverage/width comparisons; log-log plots suit rates and costs. Grouped bars would obscure continuous scales; radar diagrams have no useful role.

Use Matplotlib with reusable plot_utils.py, vector PDF and SVG exports. Rate figures have two adjacent 3.3-by-2.6-inch panels (observed length or RMSE; rate-normalized quantity). Coverage figures place coverage and length side by side, with nominal references and Wilson/mean-standard-error bars. Solver figures show gap versus runtime with separate symbols for completed and unresolved certificates. Gaussian diagnostics use a QQ panel and a moment/coverage table; nonlinear centers have no asserted CLT.

Use serif fonts at least 9pt at final 6.8-inch figure width, Okabe–Ito colors, paired line/marker encodings, a light grid, explicit log-scale labels and no decorative effects. Captions are generated only after results exist; first sentence states an observed finding, followed by DGM, repetitions, uncertainty and limitations. All plotted values come from checked result files. Visual inspection of rendered figures plus PDF font/image checks completes the integrity gate. No motivated-example or conceptual diagram is needed for this task.

The first actual-data preview showed crowded logarithmic x ticks and legends obscuring curves. The final two-panel canvas is enlarged to 6.8 by 3.8 inches, with explicit tested x values when there are at most six and no minor x tick labels. Legends use 8pt text below the panels, preserving 9–10pt base axes text. Small mathematical superscripts are a normal typographic exception. These layout changes affect no numerical result or analysis choice.
