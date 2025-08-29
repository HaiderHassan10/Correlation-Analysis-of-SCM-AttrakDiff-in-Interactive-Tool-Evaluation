How It Works
1. Data Loading
>index.py loads all CSV files from attrakdiff/ and scm/ folders.
>File names determine which application they belong to.
2. Data Mapping
>mapper.py converts textual survey responses into numeric values.
>AttrakDiff is mapped to –2 … +2.
>SCM is mapped to –1 … +2.
3. Analysis
>Per-application correlations between SCM and AttrakDiff are calculated.
>Heatmaps are generated for each app to show correlation strengths.
>A summary CSV with min, max, mean correlations per app is saved.
4. Global Scatter Plots
>Mean Pragmatic vs Hedonic Quality (AttrakDiff).
>Mean Warmth vs Competence (SCM).
>Each dot represents one app; labels are adjusted to avoid overlap.

Outputs; after running index.py, check the output/ folder:
>Heatmaps per app (in a combined PNG).
>correlation_summary_stats.csv: summary of correlations for all apps.
>attrakdiff_mean_PQ_vs_HQ.png: scatter plot of mean Pragmatic vs Hedonic quality.
>scm_mean_Warmth_vs_Competence.png: scatter plot of mean Warmth vs Competence.

How to Run
1. Install required packages:
pip install pandas numpy matplotlib seaborn scipy adjustText
2. Make sure you have the attrakdiff/ and scm/ folders with per-app CSVs.
3. Run the main script:
python index.py
4. Check the output/ folder for results.