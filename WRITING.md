# Writing rules

Conventions for reports, notes and slides made from these templates. Sources: the TU/e EE course
document guidelines (*Some Document Guidelines* v2.3), the IEEE editorial style, and the TU/e
visual identity manual. Where they disagree, the stricter rule is given.

## Before sending

- Spell-check (`make spell`, or LTeX in VS Code). American spelling throughout (`en-US`): color, analyze, modeling, center.
- The build finishes without warnings or undefined references; fonts are embedded (they are).
- Version in `\reportversion`; release with `make release` (`snapshots/YYYY-MM-DD_title_vX-Y.pdf`) and commit
  the PDF you hand in.
  Reviewed copies get your initials appended, not a new version number.
- Next versions differ visibly; apply a correction everywhere it occurs, not just where marked.
- Mark reused text, figures and data from other documents (including your own).

## Structure (paper or report)

| Part | Contains |
|---|---|
| Title | What it is about |
| Abstract | Problem, what is new, main result with numbers. No citations |
| Introduction | Context, problem, claims, approach, how the report is organized |
| Related work | How this work differs from others, not a list |
| Approach / setup | Why each experiment is done (to prove a claim), then how; reproducible |
| Results | Explain, do not only describe; show the claims are proven |
| Conclusions | Problem, solution, results that prove the claims. No citations |

Each section starts with a short link to the previous one and ends with a link to the next.

## English

- One sentence per line in the source (git diffs then show the changed sentence).
- Comments and package code: at most 80 characters per line (dividers exactly 80).
  Prose has no limit: a sentence is one line, the editor wraps it.
- Active, short sentences. "To", not "in order to"; "to verb", not "for verb-ing".
- No "obviously", "as is well known"; no contractions (it's, can't); no ellipses;
  commas, not dashes, around asides.
- "That" defines (no comma), ", which" adds. Oxford comma: A, B, and C.
  Fewer (count) vs less (amount). "Either" goes with one "or".
- Define every term once and keep using it; no synonyms for the same thing.
- Introduce each abbreviation at first use, full form first: "analog-to-digital converter (ADC)".
  `\ac{ADC}` does it. Again in the body even if the abstract did. Plural "ADCs".
- Hyphenate compound adjectives before a noun: "a high-frequency signal".
- Do not start a sentence with a symbol or a digit: "Twenty samples", "Equation (3) shows".
- Discuss items in the order they were introduced.
- Emphasis with `\emph{}`, bold very sparingly, never underline. Quotes with `\enquote{}`.

## Paragraphs and line breaks

- New paragraph: a blank line. One newline in the source is a space.
- `\\` only where lines matter: table rows, `align`, title pages. Never between paragraphs.
- `\clearpage` before major parts; `\vspace`, `\noindent`, `\linebreak` only as final touches.

## References and labels

- Labels: `type:short-name`, lowercase, hyphens, no spaces. Describe what it is, never a
  number or a position (`fig:spring-force`, not `fig:3` or `fig:below`); keep labels when
  titles change; unique in the whole document.

  | Prefix | For | Example | Where `\label` goes |
  |---|---|---|---|
  | `sec:` | section, subsection, subsubsection | `sec:related-work` | right after `\section{}` |
  | `fig:` | figure, subfigure | `fig:spring-force`, `fig:steps-a` | after `\caption` |
  | `tab:` | table | `tab:setup` | after `\caption` |
  | `eq:` | equation | `eq:hooke` | inside the equation environment |
  | `app:` | appendix | `app:calculations` | right after `\section{}` |
  | `lst:` | code listing | `lst:adc-init` | in the listing options or after `\caption` |
  | `item:` | numbered list item | `item:req-range` | right after `\item` |
  | `ch:` | chapter (book/report class only) | `ch:design` | right after `\chapter{}` |
- `\cref{fig:x}` writes "Figure 3.1" with the non-breaking space; `\Cref` at a sentence start;
  `\cref{fig:a,fig:b}` for several. `\eqref{eq:x}` writes "(3.1)". Subsections are called
  "Section", appendices "Appendix". Never "the figure below".
- Citations: `text~\autocite{key}` (or `\cite`), the number as a name: "as shown in [3]",
  "[2]–[5]", "Smith *et al.* [3]". Citation before the full stop.
- Every figure and table is referred to and explained: why it is there, what to learn from it.

## Figures, tables, graphs

- Figure captions below the figure, table captions above the table.
- Tables: `booktabs` rules, no vertical lines.
- Graphs: axis labels with quantity and unit, "Frequency (Hz)"; same markers, colors and legend
  order for the same experiment across figures; same axis ranges when compared; readable in
  black and white; vector graphics (PDF), not screenshots; never exaggerate.

## Numbers, units and maths

- Units with `siunitx`: `\SI{250}{\newton\per\metre}` gives "250 N/m", `N·m` for products.
  Space between number and unit (`10 mm`), except `°`, `%`. Units upright, never italic.
  At most one solidus: `m/s²`, `J/(kg·K)`. No made-up units ("Mbps", "sec").
- × between numbers (`2.5 × 10³`, dimensions `300 × 100 × 50 mm`), · or a thin space between
  units, nothing between variables (`F = k δ`).
- Decimal point, never a comma; leading zero (`0.5`); ranges with an en dash
  (`10--20~Hz`, `\SIrange{10}{20}{\hertz}`).
- Variables italic, vectors bold, functions upright (sin, exp). Word subscripts upright:
  `V_\mathrm{out}`. (The document guidelines write `\textit`; both avoid `$eff$` looking like e f f.)
- Equations are part of the sentence: punctuate them.

## Bibliography

- One `.bib`, keys `AuthorYear` (`knuth1986`), sorted by key.
- Protect capitals in titles: `{SOC}`, `{MEMS}`.
- Web sources: `@online` with `url` and `urldate`. IEEE style is set in the templates.

## Slides

- Slide numbers on every slide (the theme does it); one consistent style.
- One message per slide; every figure explained; graphs as above.
- Extra material after `\appendix` as backup slides (not counted in the total).

## TU/e brand

- Color TU/e Scarlet (`Tue-red`, #C81919) for logo, headers, color areas; text black.
- Official logo files only, with their bounding box; never recolored, never on photos.

## Email

- A subject that says what the email is about; "Dear …" when in doubt; attach documents rather
  than linking them; check the attachment is there.
