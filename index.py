import pandas as pd
import numpy as np
import os
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')
plt.style.use('default')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10
from adjustText import adjust_text

attrakdiff_path = Path('attrakdiff')
scm_path = Path('scm')

attrakdiff_dfs = {}
scm_dfs = {}

for csv_file in attrakdiff_path.glob('*.csv'):

    app_name = csv_file.stem.replace('attrakdiff', '')
    try:
        df = pd.read_csv(csv_file)
        attrakdiff_dfs[app_name] = df
        print(f"Loaded attrakdiff data for: {app_name} - Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
              
for csv_file in scm_path.glob('*.csv'):
    app_name = csv_file.stem.replace('scm', '')
    try:
        df = pd.read_csv(csv_file)
        scm_dfs[app_name] = df
        print(f"Loaded SCM data for: {app_name} - Shape: {df.shape}")
    except Exception as e:
        print(f"Error loading {csv_file}: {e}")
          
print("Available applications in attrakdiff data:")
for app_name in sorted(attrakdiff_dfs.keys()):
    print(f"  - {app_name}")

print("\nAvailable applications in SCM data:")
for app_name in sorted(scm_dfs.keys()):
    print(f"  - {app_name}")
    
from mapper import map_attrakdiff_df, map_scm_df

attrakdiff_dfs_mapped = {}
scm_dfs_mapped = {}

for app_name, df in attrakdiff_dfs.items():
    attrakdiff_dfs_mapped[app_name] = map_attrakdiff_df(df)

for app_name, df in scm_dfs.items():
    scm_dfs_mapped[app_name] = map_scm_df(df)

if 'youtube' in attrakdiff_dfs_mapped:
    print("\nMapped Attrakdiff data for YouTube:")
    print(attrakdiff_dfs_mapped['youtube'].head())

if 'youtube' in scm_dfs_mapped:
    print("\nMapped SCM data for YouTube:")
    print(scm_dfs_mapped['youtube'].head())

common_apps = ['atm', 'campusprinterterminal', 'chatgpt', 'dbnavigator', 'excel', 'facebook', 'gemini', 'gmail', 'googlemaps', 'instagram', 'moodlelms', 'nintendoswitch', 'snapchat', 'spotify', 'supermarket', 'youtube']

print("Data summary for common applications:")
print("=" * 50)

for app in common_apps:
    if app in attrakdiff_dfs and app in scm_dfs:
        print(f"\n{app.upper()}:")
        print(f"  Attrakdiff data shape: {attrakdiff_dfs[app].shape}")
        print(f"  SCM data shape: {scm_dfs[app].shape}")
        
        print(f"  Attrakdiff columns: {list(attrakdiff_dfs[app].columns)}")
        print(f"  SCM columns: {list(scm_dfs[app].columns)}")
    else:
        print(f"\n{app.upper()}: Data not found in one or both datasets")

output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

summary_data = []

apps_to_process = [app for app in common_apps if app in attrakdiff_dfs_mapped and app in scm_dfs_mapped]
n_apps = len(apps_to_process)

n_cols = 2
n_rows = (n_apps + n_cols - 1) // n_cols 
fig, axes = plt.subplots(n_rows, n_cols, figsize=(10 * n_cols, 8 * n_rows))
axes = axes.flatten() 

for i, app in enumerate(apps_to_process):
    attrakdiff_df = attrakdiff_dfs_mapped[app]
    scm_df = scm_dfs_mapped[app]

    if len(attrakdiff_df) != len(scm_df):
        print(f"Skipping {app} due to mismatched row counts.")
        axes[i].set_visible(False)
        continue

    combined_df = pd.concat([attrakdiff_df, scm_df], axis=1)

    full_correlation_matrix = combined_df.corr()

    correlation_slice = full_correlation_matrix.loc[scm_df.columns, attrakdiff_df.columns]

    sns.heatmap(correlation_slice, annot=True, cmap='coolwarm', fmt=".2f", ax=axes[i])
    axes[i].set_title(f'SCM vs Attrakdiff Correlation for {app.upper()}')

    correlation_values = correlation_slice.values.flatten()

    summary_stats = {
        'service': app,
        'min_correlation': np.min(correlation_values),
        'max_correlation': np.max(correlation_values),
        'mean_correlation': np.mean(correlation_values),
        'median_correlation': np.median(correlation_values),
        'abs_mean_correlation': np.mean(np.abs(correlation_values))
    }
    summary_data.append(summary_stats)

for j in range(n_apps, len(axes)):
    axes[j].set_visible(False)

plt.tight_layout()
plt.savefig(output_dir / 'all_services_correlation_heatmaps.png')
plt.close()

summary_df = pd.DataFrame(summary_data)

summary_df.to_csv(output_dir / 'correlation_summary_stats.csv', index=False)

print("\nCorrelation analysis complete. Combined heatmap and summary CSV are saved in the 'output' directory.")

output_dir = Path('output')
output_dir.mkdir(exist_ok=True)

attrak_means = []
for app, df in attrakdiff_dfs_mapped.items():
    if app in common_apps:
        pq = df[['impractical - practical', 'complicated - simple']].mean(axis=1).mean()
        hq_s = df[['dull - creative', 'boring - exciting']].mean(axis=1).mean()
        hq_i = df[['tacky - stylish', 'amateurish - professional']].mean(axis=1).mean()
        hq = np.mean([hq_s, hq_i])
        attrak_means.append({'app': app, 'PQ': pq, 'HQ': hq})

attrak_means_df = pd.DataFrame(attrak_means)

plt.figure(figsize=(8,6))
sns.scatterplot(data=attrak_means_df, x='PQ', y='HQ', s=80)

texts = []
for i, row in attrak_means_df.iterrows():
    texts.append(plt.text(row['PQ'], row['HQ'], row['app'], fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))
plt.title("AttrakDiff: Mean Pragmatic vs Hedonic Quality (per app)")
plt.xlabel("Pragmatic Quality (PQ)")
plt.ylabel("Hedonic Quality (HQ)")
plt.tight_layout()
plt.savefig(output_dir / 'attrakdiff_mean_PQ_vs_HQ.png', dpi=150)
plt.close()

scm_means = []
for app, df in scm_dfs_mapped.items():
    if app in common_apps:
        warmth = df[['warm', 'user-intentioned', 'trustworthy']].mean(axis=1).mean()
        competence = df[['competent', 'capable']].mean(axis=1).mean()
        scm_means.append({'app': app, 'Warmth': warmth, 'Competence': competence})

scm_means_df = pd.DataFrame(scm_means)

plt.figure(figsize=(8,6))
sns.scatterplot(data=scm_means_df, x='Warmth', y='Competence', s=80, color='orange')

texts = []
for i, row in scm_means_df.iterrows():
    texts.append(plt.text(row['Warmth'], row['Competence'], row['app'], fontsize=9))

adjust_text(texts, arrowprops=dict(arrowstyle="->", color='gray', lw=0.5))
plt.title("SCM: Mean Warmth vs Competence (per app)")
plt.xlabel("Warmth")
plt.ylabel("Competence")
plt.tight_layout()
plt.savefig(output_dir / 'scm_mean_Warmth_vs_Competence.png', dpi=150)
plt.close()

print("\nAdditional scatter plots saved to 'output':")
print(" - attrakdiff_mean_PQ_vs_HQ.png")
print(" - scm_mean_Warmth_vs_Competence.png")

