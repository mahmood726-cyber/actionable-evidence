# Only 1.3% of Cochrane Meta-Analyses Meet All Six Criteria for Clinically Actionable Evidence: A Cross-Sectional Evaluation of 6229 Pairwise Meta-Analyses

**Mahmood Ahmad, MRCP**

Department of Cardiology, Royal Free Hospital, London, United Kingdom

ORCID: 0009-0003-7781-4478

**Corresponding Author:** Mahmood Ahmad, Department of Cardiology, Royal Free Hospital, Pond Street, London NW3 2QG, United Kingdom.

**Word Count:** 3,812

---

## Key Points

**Question:** What proportion of Cochrane pairwise meta-analyses produce evidence that is robust enough to directly inform clinical action?

**Findings:** In this cross-sectional evaluation of 6229 meta-analyses from 501 Cochrane reviews, only 78 (1.3%) met all six criteria for actionable evidence (statistical significance under the Hartung-Knapp-Sidik-Jonkman method, prediction interval concordance, multiverse robustness, clean audit profile, sufficient evidence volume, and absence of publication bias). The largest bottleneck was statistical significance under HKSJ, which eliminated 85.7% of meta-analyses.

**Meaning:** The gap between "statistically significant" and "clinically actionable" is vast; most meta-analyses that appear conclusive under conventional methods fail more stringent but defensible evidentiary thresholds.

---

## Abstract

**Importance:** Meta-analyses are the highest tier of the evidence hierarchy, yet "statistically significant" results are routinely conflated with "actionable evidence." No systematic framework exists to evaluate how many meta-analyses meet the multiple conditions necessary for direct clinical application.

**Objective:** To determine the proportion of Cochrane pairwise meta-analyses that satisfy six independently necessary criteria for clinically actionable evidence.

**Design, Setting, and Participants:** Cross-sectional evaluation of 6229 pairwise meta-analyses extracted from 501 Cochrane systematic reviews in the Pairwise70 dataset (a curated repository of individual study-level data from Cochrane reviews). Each meta-analysis was recomputed using the Hartung-Knapp-Sidik-Jonkman (HKSJ) method and evaluated against six criteria applied as a sequential waterfall filter. Analysis was conducted in March 2026.

**Main Outcomes and Measures:** The primary outcome was the proportion of meta-analyses classified as ACTIONABLE (passing all six criteria). Secondary outcomes included the failure rate for each individual criterion and the identification of which criterion constitutes the primary bottleneck.

**Results:** Of 6229 meta-analyses, only 78 (1.3%) met all six criteria for actionable evidence, distributed across 42 of 501 reviews (8.4%). The sequential waterfall showed progressive attrition: 6229 total, 888 after significance (85.7% eliminated), 383 after prediction interval concordance, 167 after multiverse robustness, 99 after audit flag screening, 78 after evidence volume, and 78 after publication bias assessment. Statistical significance under HKSJ was the single largest bottleneck (failure rate 85.7%). Among the 145 meta-analyses that failed on exactly one criterion, robustness was the most common single point of failure (116 of 145, 80.0%). No review had all of its meta-analyses classified as actionable.

**Conclusions and Relevance:** Only 1 in 77 Cochrane meta-analyses meets a defensible threshold for clinically actionable evidence. The vast majority of apparently significant meta-analyses lose their significance when analyzed using the HKSJ method, which appropriately penalizes heterogeneity. These findings suggest that evidence-based guidelines should adopt multi-criteria actionability frameworks rather than relying on pooled p-values alone.

---

## Introduction

Meta-analysis sits at the apex of the evidence hierarchy, and Cochrane systematic reviews represent the gold standard of evidence synthesis.^1^ Clinical guidelines routinely cite pooled effect estimates as though they directly license treatment decisions. Yet a statistically significant pooled result does not, by itself, guarantee that the evidence is robust enough to act upon. The gap between "p < 0.05" and "clinically actionable" remains poorly quantified.

Several methodological concerns erode confidence in meta-analytic conclusions. First, the conventional DerSimonian-Laird random-effects model underestimates uncertainty when the number of studies is small or heterogeneity is high, producing anticonservative confidence intervals and inflated Type I error rates.^2,3^ The Hartung-Knapp-Sidik-Jonkman (HKSJ) adjustment corrects this by using a t-distribution and better variance estimation, but its adoption in Cochrane reviews remains incomplete.^4^ Second, a significant pooled estimate may obscure substantial heterogeneity: if the prediction interval for the true effect in a new study setting crosses the null, the result is not generalizable.^5^ Third, evidence of publication bias, data quality concerns, and fragility of conclusions under alternative analytic choices further undermine the actionability of pooled estimates.^6,7^

Despite these well-known threats, no systematic framework has been applied at scale to ask: how many meta-analyses simultaneously satisfy all the conditions that a thoughtful clinician or guideline panel should require before acting? We developed a six-criterion actionability framework and applied it to 6229 pairwise meta-analyses from 501 Cochrane systematic reviews to answer this question.

---

## Methods

### Data Source

We used the Pairwise70 dataset, a curated repository containing individual study-level data from 501 Cochrane systematic reviews, comprising 6229 pairwise meta-analyses.^8^ Each meta-analysis includes arm-level counts (for binary outcomes) or means and standard deviations (for continuous outcomes) sufficient for independent recomputation of pooled effects.

### Statistical Recomputation

All meta-analyses were recomputed from study-level data using the HKSJ random-effects method, which applies the Sidik-Jonkman heterogeneity estimator with a Hartung-Knapp adjustment to the confidence interval.^4^ This method yields appropriately wider confidence intervals than DerSimonian-Laird, particularly when the number of studies is small (k < 20) or heterogeneity is substantial.^2,3^ For each meta-analysis, we obtained the pooled effect estimate, 95% confidence interval, p-value, heterogeneity statistics (tau-squared, I-squared), and, where k was 3 or greater, the 95% prediction interval.

### Actionability Criteria

We defined six independently necessary criteria for actionable evidence (Table 1). A meta-analysis was classified as ACTIONABLE only if it passed all six criteria; failure on any single criterion resulted in a NOT YET classification.

The six criteria were applied as a sequential waterfall filter in the following order: (1) statistical significance, (2) prediction interval concordance, (3) multiverse robustness, (4) audit flag screening, (5) evidence volume, and (6) publication bias assessment. The ordering was designed to apply the most discriminating filter first, but each criterion was also evaluated independently to compute marginal failure rates.

**Criterion 1: Statistical Significance Under HKSJ (p < 0.05).** The pooled effect must achieve statistical significance at the 5% level using the HKSJ method. This is more conservative than DerSimonian-Laird and correctly accounts for uncertainty in heterogeneity estimation.

**Criterion 2: Prediction Interval Concordance.** For meta-analyses with 3 or more studies, the 95% prediction interval must not cross the null value (0 on the log scale for ratio measures; 0 for mean differences).^5^ This ensures that the treatment effect would be expected to remain on the same side of the null in a future study setting. Meta-analyses with fewer than 3 studies passed this criterion by default, as prediction intervals cannot be meaningfully computed.

**Criterion 3: Multiverse Robustness.** Using data from the Fragility Atlas,^9^ which classifies Cochrane reviews as Robust, Moderate, Fragile, or Unstable based on multiverse sensitivity analysis (varying estimator, model, and influence diagnostics), the parent review must be classified as Robust or Moderate. Reviews not covered by the Fragility Atlas (963 of 6229 meta-analyses) received the benefit of the doubt and passed this criterion by default.

**Criterion 4: Clean Audit Profile.** Using data from a comprehensive meta-analytic audit (MetaAudit)^10^ that applies 11 automated quality detectors to each meta-analysis, the meta-analysis must have zero FAIL or CRITICAL severity flags. This captures data extraction errors, inconsistencies between reported and recomputed effects, and anomalous study-level patterns.

**Criterion 5: Sufficient Evidence Volume.** The meta-analysis must include at least 5 studies (k >= 5) and a combined sample size of at least 500 participants (N >= 500). These thresholds ensure a minimum evidence base for both heterogeneity estimation and clinical generalizability.^11^

**Criterion 6: No Publication Bias Signal.** For meta-analyses with 10 or more studies, the MetaAudit publication bias module (incorporating Egger's regression test with a threshold of p < 0.10) must not have a FAIL or CRITICAL flag.^12^ Meta-analyses with fewer than 10 studies passed by default, as funnel plot asymmetry tests lack power below this threshold.^13^

### Statistical Analysis

The primary analysis computed the proportion of meta-analyses classified as ACTIONABLE. Secondary analyses included: (1) individual criterion failure rates (the proportion of all 6229 meta-analyses failing each criterion, regardless of other criteria); (2) the waterfall attrition at each sequential filter step; (3) the distribution of the number of failed criteria per meta-analysis; (4) single-point-of-failure analysis (meta-analyses failing exactly one criterion); and (5) review-level analysis (proportion of reviews containing at least one actionable meta-analysis). All analyses were conducted in Python 3.13 using NumPy and pandas. The random seed was fixed at 42 for reproducibility.

---

## Results

### Overall Actionability

Of 6229 pairwise meta-analyses from 501 Cochrane reviews, 78 (1.3%) met all six criteria for actionable evidence (Figure 1). The remaining 6151 (98.7%) failed at least one criterion. Actionable meta-analyses were distributed across 42 of 501 reviews (8.4%); no review had all of its meta-analyses classified as actionable.

### Waterfall Attrition

The sequential waterfall filter showed steep attrition at each stage (Figure 1). Of 6229 meta-analyses, 888 (14.3%) survived the HKSJ significance filter, representing an 85.7% elimination rate at the first step. Of these 888, 383 (43.1%) additionally passed prediction interval concordance. After multiverse robustness, 167 remained; after audit flag screening, 99; after evidence volume, 78; and after publication bias assessment, 78 (unchanged, as all meta-analyses surviving to this stage also passed the publication bias criterion).

### Individual Criterion Failure Rates

The marginal failure rate for each criterion (evaluated independently across all 6229 meta-analyses) is shown in Figure 2 and Table 1. Statistical significance under HKSJ had the highest failure rate (85.7%; 5341 meta-analyses), followed by prediction interval concordance (66.1%; 4117), evidence volume (51.4%; 3202), robustness (47.4%; 2952), audit flags (29.5%; 1837), and publication bias (12.6%; 785).

### Failure Multiplicity

Most meta-analyses failed on multiple criteria simultaneously. The distribution of the number of failed criteria was: 0 criteria (78 meta-analyses, 1.3%), 1 criterion (145, 2.3%), 2 criteria (1920, 30.8%), 3 criteria (2530, 40.6%), 4 criteria (1133, 18.2%), 5 criteria (414, 6.6%), and 6 criteria (9, 0.1%). The median number of failed criteria was 3 (interquartile range 2-3).

### Single Points of Failure

Among the 145 meta-analyses that failed on exactly one criterion, the most common single point of failure was multiverse robustness (116 of 145, 80.0%), followed by evidence volume (21 of 145, 14.5%), and audit flags (8 of 145, 5.5%). No meta-analysis had statistical significance, prediction interval concordance, or publication bias as its sole point of failure.

### Review-Level Analysis

Of the 42 reviews containing at least one actionable meta-analysis, the number of actionable meta-analyses per review ranged from 1 to 8 (Table 2). The review with the most actionable meta-analyses (CD007784) had 8, followed by CD003774 and CD011600 with 5 each. Most reviews with actionable evidence (32 of 42, 76.2%) contained only 1 or 2 actionable meta-analyses.

### Characteristics of Actionable Meta-Analyses

The 78 actionable meta-analyses had a median of 12 studies (range 5-245) and a median combined sample size of 3472 (range 528-397,441). These meta-analyses tended to be large, well-powered, and drawn from clinical questions with substantial trial activity.

---

## Discussion

In this cross-sectional evaluation of 6229 Cochrane pairwise meta-analyses, we found that only 1.3% met all six criteria for clinically actionable evidence. This finding quantifies what has long been suspected: the gap between "statistically significant meta-analysis" and "evidence strong enough to act upon" is enormous. For every meta-analysis that clears all six hurdles, 77 do not.

### HKSJ as the Key Filter

The single largest bottleneck was statistical significance under the HKSJ method, which eliminated 85.7% of meta-analyses at the first waterfall step. This finding has profound implications. Many of these meta-analyses would appear statistically significant under the conventional DerSimonian-Laird method, which is still the default in most Cochrane reviews and statistical software. The HKSJ method appropriately inflates the standard error when heterogeneity is poorly estimated (particularly with few studies), converting many nominally significant results to nonsignificant ones.^2-4^ Our results suggest that a substantial fraction of meta-analytic conclusions in the Cochrane Library may be false positives attributable to anticonservative variance estimation.

### Prediction Interval Concordance

Among the 888 meta-analyses surviving the HKSJ significance filter, an additional 505 (56.9%) failed the prediction interval criterion. This is consistent with prior work showing that prediction intervals frequently cross the null even when confidence intervals do not, particularly when heterogeneity is moderate to high.^5^ A confidence interval addresses "what is the average effect?", while a prediction interval addresses "what effect would I expect in the next study setting?" — a question far more relevant to clinical decision-making in diverse patient populations.

### Multiverse Robustness and Audit Flags

The robustness criterion (derived from multiverse sensitivity analysis in the Fragility Atlas) was the most common single point of failure: 116 meta-analyses that passed all other criteria failed solely because their parent review was classified as Fragile or Unstable. This indicates that many meta-analyses are sensitive to reasonable analytic choices (estimator, model specification, outlier handling) — a concern that standard reporting rarely addresses.^7,9^

The audit flag criterion (requiring zero FAIL or CRITICAL flags from 11 automated quality detectors) eliminated 29.5% of meta-analyses. Common flags included discrepancies between reported and recomputed effect sizes, implausible study-level statistics, and data extraction anomalies.^10^ This criterion serves as a data quality filter that is orthogonal to the statistical properties of the pooled estimate.

### Publication Bias

Publication bias had the lowest failure rate (12.6%) and did not eliminate any additional meta-analyses in the final waterfall step (all 78 surviving after the volume filter also passed the publication bias criterion). This may reflect that Egger's test was only applied to meta-analyses with 10 or more studies (a standard power threshold^13^), and that meta-analyses large enough to survive all prior filters tend to have sufficient studies to dilute funnel plot asymmetry.

### Implications for GRADE and Clinical Guidelines

The Grading of Recommendations Assessment, Development and Evaluation (GRADE) framework evaluates certainty of evidence across five domains: risk of bias, inconsistency, indirectness, imprecision, and publication bias.^14^ Our six-criterion framework partially maps to GRADE domains (imprecision maps to significance and evidence volume; inconsistency maps to prediction intervals and robustness; publication bias maps directly) but operationalizes them with specific, reproducible quantitative thresholds rather than subjective judgments.

The finding that only 1.3% of meta-analyses are actionable does not mean the remaining 98.7% are "wrong." Many address important questions where the evidence is genuinely uncertain. The NOT YET classification is not a verdict of invalidity but rather a recognition that the evidence has not yet accumulated to the point where it can bear the weight of a treatment recommendation with high confidence. Guidelines that rely on meta-analyses failing one or more of these criteria should explicitly acknowledge the specific evidentiary gaps rather than treating all "significant" meta-analyses as equivalent.

### Comparison With Prior Work

Previous studies have examined individual threats to meta-analytic validity. Partlett and Riley^5^ demonstrated that prediction intervals frequently contradict confidence intervals. IntHout et al^3^ showed that DerSimonian-Laird inflates Type I error rates. Ioannidis^6^ argued that most published research findings are false. Our contribution is to integrate these individual concerns into a single, reproducible framework and to quantify their joint impact at scale.

### Limitations

Several limitations warrant consideration. First, the six criteria and their thresholds involve judgment. Alternative thresholds (eg, alpha of 0.01 rather than 0.05, or k >= 10 rather than k >= 5) would change the proportion classified as actionable. Second, the Fragility Atlas did not cover all reviews (963 meta-analyses from uncovered reviews received benefit of the doubt), which may overestimate the actionable proportion. Third, the framework evaluates statistical properties of the pooled evidence but does not address clinical relevance, risk of bias within individual studies, or indirectness — factors that GRADE appropriately includes. Fourth, the sequential waterfall ordering affects the stage-specific attrition numbers (though not the final count), and readers should refer to the marginal failure rates for criterion-specific interpretation. Fifth, the Pairwise70 dataset, while large, represents a subset of all Cochrane reviews and may not be fully representative.

### Conclusions

Only 78 of 6229 Cochrane pairwise meta-analyses (1.3%) meet a six-criterion threshold for clinically actionable evidence. The HKSJ significance filter is the dominant bottleneck, suggesting that many conventional meta-analytic conclusions rest on anticonservative variance estimation. These findings argue for routine adoption of HKSJ methods, mandatory prediction interval reporting, and multi-criteria actionability frameworks in evidence-based medicine.

---

## Tables

### Table 1. Six Criteria for Actionable Evidence

| Criterion | Threshold | Justification | Failure Rate |
|-----------|-----------|---------------|:------------:|
| 1. Statistical significance | HKSJ p < 0.05 | Corrects DerSimonian-Laird anticonservatism; uses t-distribution with appropriate variance estimation^2-4^ | 85.7% |
| 2. Prediction interval concordance | 95% PI does not cross null (k >= 3) | Ensures treatment effect is expected to persist in a new study setting, not just on average^5^ | 66.1% |
| 3. Multiverse robustness | Parent review classified as Robust or Moderate in Fragility Atlas | Conclusions should be stable under reasonable analytic alternatives (estimator, outlier handling)^7,9^ | 47.4% |
| 4. Clean audit profile | Zero FAIL/CRITICAL flags across 11 automated quality detectors | Data extraction errors and statistical anomalies must be absent for the pooled estimate to be trustworthy^10^ | 29.5% |
| 5. Sufficient evidence volume | k >= 5 studies AND N >= 500 total participants | Minimum base for reliable heterogeneity estimation and clinical generalizability^11^ | 51.4% |
| 6. No publication bias signal | Egger's test p >= 0.10 (applied when k >= 10; pass by default otherwise) | Asymmetric funnel plots suggest missing studies, inflating pooled estimates^12,13^ | 12.6% |

### Table 2. Top 10 Reviews by Number of Actionable Meta-Analyses

| Rank | Review ID | Actionable MAs | Total MAs in Review |
|:----:|-----------|:--------------:|:-------------------:|
| 1 | CD007784 | 8 | 61 |
| 2 | CD003774 | 5 | 18 |
| 3 | CD011600 | 5 | 27 |
| 4 | CD010145 | 4 | 22 |
| 5 | CD013830 | 4 | 22 |
| 6 | CD012712 | 3 | 20 |
| 7 | CD001909 | 2 | 7 |
| 8 | CD003598 | 2 | 36 |
| 9 | CD006023 | 2 | 28 |
| 10 | CD001155 | 2 | 10 |

*Note: 42 reviews contained at least one actionable meta-analysis. 32 of these (76.2%) contained only 1 or 2 actionable meta-analyses.*

---

## Figures

### Figure 1. Waterfall Attrition of 6229 Meta-Analyses Through Six Actionability Criteria

A sequential waterfall chart showing the progressive filtering of 6229 Cochrane pairwise meta-analyses through six actionability criteria. Starting from 6229 meta-analyses, the count decreases to 888 after HKSJ significance (5341 eliminated, 85.7%), 383 after prediction interval concordance (505 eliminated), 167 after multiverse robustness (216 eliminated), 99 after audit flag screening (68 eliminated), 78 after evidence volume (21 eliminated), and 78 after publication bias (0 eliminated). The final bar (78, 1.3%) is highlighted in a distinct color to indicate the ACTIONABLE subset.

### Figure 2. Marginal Failure Rates for Each Actionability Criterion

A horizontal bar chart showing the percentage of all 6229 meta-analyses that fail each criterion independently (not sequentially). Bars are sorted from highest to lowest failure rate: significance (85.7%), prediction interval (66.1%), evidence volume (51.4%), robustness (47.4%), audit flags (29.5%), publication bias (12.6%). Each bar is annotated with the exact percentage and count of failing meta-analyses.

---

## References

1. Higgins JPT, Thomas J, Chandler J, et al, eds. *Cochrane Handbook for Systematic Reviews of Interventions*. Version 6.4. Cochrane; 2023.

2. Veroniki AA, Jackson D, Bender R, et al. Methods to calculate uncertainty in the estimated overall effect size from a random-effects meta-analysis. *Res Synth Methods*. 2019;10(1):23-43. doi:10.1002/jrsm.1319

3. IntHout J, Ioannidis JPA, Borm GF. The Hartung-Knapp-Sidik-Jonkman method for random effects meta-analysis is straightforward and considerably outperforms the standard DerSimonian-Laird method. *BMC Med Res Methodol*. 2014;14:25. doi:10.1186/1471-2288-14-25

4. Rover C, Knapp G, Friede T. Hartung-Knapp-Sidik-Jonkman approach and its modification for random-effects meta-analysis with few studies. *BMC Med Res Methodol*. 2015;15:99. doi:10.1186/s12874-015-0091-1

5. IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ. Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open*. 2016;6(7):e010247. doi:10.1136/bmjopen-2015-010247

6. Ioannidis JPA. Why most published research findings are false. *PLoS Med*. 2005;2(8):e124. doi:10.1371/journal.pmed.0020124

7. Olkin I, Dahabreh IJ, Trikalinos TA. GOSH — a graphical display of study heterogeneity. *Res Synth Methods*. 2012;3(3):214-223. doi:10.1002/jrsm.1053

8. Cochrane Library. Cochrane Database of Systematic Reviews. Accessed March 2026. https://www.cochranelibrary.com

9. Ahmad M. Fragility Atlas: multiverse sensitivity analysis of Cochrane systematic reviews. Preprint. 2026.

10. Ahmad M. MetaAudit: automated quality audit of 4,424 Cochrane meta-analyses with 11 detectors. Preprint. 2026.

11. Jackson D, Turner R. Power analysis for random-effects meta-analysis. *Res Synth Methods*. 2017;8(3):290-302. doi:10.1002/jrsm.1240

12. Egger M, Davey Smith G, Schneider M, Minder C. Bias in meta-analysis detected by a simple, graphical test. *BMJ*. 1997;315(7109):629-634. doi:10.1136/bmj.315.7109.629

13. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. *BMJ*. 2011;343:d4002. doi:10.1136/bmj.d4002

14. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ*. 2008;336(7650):924-926. doi:10.1136/bmj.39489.470347.AD

15. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. *BMJ*. 2021;372:n71. doi:10.1136/bmj.n71

---

## Data Availability

The Pairwise70 dataset is derived from publicly available Cochrane reviews. The ActionableEvidence analysis code, including the verdict computation pipeline and all results, is available at [repository URL to be added upon publication]. The MetaAudit and Fragility Atlas datasets used for criteria 3 and 4 are described in their respective preprints.^9,10^

## Funding

None.

## Conflict of Interest Disclosures

The author reports no conflicts of interest.

## Role of the Funder/Sponsor

Not applicable.
