import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import os

# Set style for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

# Define color palette
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff9800',
    'info': '#17a2b8',
    'purple': '#9467bd',
    'pink': '#e377c2',
    'brown': '#8c564b',
    'gray': '#7f7f7f'
}

GRADIENT_COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#43e97b', '#fa709a', '#fee140']

# --- Main Script ---

# Load the dataset, checking for common paths
file_path = 'deliveries.csv'
if not os.path.exists(file_path):
    file_path = 'content/deliveries.csv'

try:
    ipl = pd.read_csv(file_path)
    print(f"Dataset loaded successfully with {len(ipl)} records")
except FileNotFoundError:
    print(f"Error: '{file_path}' not found. Please ensure the dataset is available.")
    exit()
 
# Create a PDF object to save the plots
with PdfPages('report.pdf') as pdf:
    
    # --- Page 1: Enhanced Title Page ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    ax = fig.add_subplot(111)
    ax.axis('off')
    
    # Add gradient background effect
    gradient = np.linspace(0, 1, 256).reshape(256, 1)
    ax.imshow(gradient, extent=[0, 1, 0, 1], aspect='auto', cmap='Blues', alpha=0.3)
    
    # Title and subtitle
    fig.text(0.5, 0.65, "IPL DATA ANALYSIS", ha='center', va='center', 
             fontsize=42, weight='bold', color=COLORS['primary'], family='sans-serif')
    fig.text(0.5, 0.58, "REPORT", ha='center', va='center', 
             fontsize=42, weight='bold', color=COLORS['primary'], family='sans-serif')
    
    # Decorative line
    fig.add_artist(plt.Line2D([0.25, 0.75], [0.53, 0.53], linewidth=3, color=COLORS['secondary']))
    
    # Subtitle
    fig.text(0.5, 0.47, "A Comprehensive Visual Analysis", ha='center', va='center', 
             fontsize=18, style='italic', color=COLORS['gray'])
    fig.text(0.5, 0.43, "of Batting Performance & Statistics", ha='center', va='center', 
             fontsize=18, style='italic', color=COLORS['gray'])
    
    # Statistics summary box
    total_matches = ipl['match_id'].nunique()
    total_runs = ipl['batsman_runs'].sum()
    total_batsmen = ipl['batsman'].nunique()
    
    fig.text(0.5, 0.32, f"Total Matches: {total_matches:,}", ha='center', va='center', 
             fontsize=14, weight='bold', color=COLORS['info'])
    fig.text(0.5, 0.28, f"Total Runs Scored: {total_runs:,}", ha='center', va='center', 
             fontsize=14, weight='bold', color=COLORS['success'])
    fig.text(0.5, 0.24, f"Unique Batsmen: {total_batsmen:,}", ha='center', va='center', 
             fontsize=14, weight='bold', color=COLORS['purple'])
    
    # Footer
    fig.text(0.5, 0.1, "Generated using Python, Pandas & Matplotlib", ha='center', va='center', 
             fontsize=10, color=COLORS['gray'], style='italic')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # --- Data Analysis ---
    # 1. Top 10 Batsman by Runs
    top_batsman = ipl.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10)

    # 2. Top 5 Batsmen with Most Sixes
    sixes = ipl[ipl['batsman_runs'] == 6]
    max_sixes_batsman = sixes.groupby('batsman').size().sort_values(ascending=False).head(5)
    
    # 2b. Top 5 Batsmen with Most Fours
    fours = ipl[ipl['batsman_runs'] == 4]
    max_fours_batsman = fours.groupby('batsman').size().sort_values(ascending=False).head(5)

    # 3. Top 5 Death Over Hitters (Boundaries in overs 16-20)
    death_overs = ipl[ipl['over'] > 15]
    death_over_boundaries = death_overs[(death_overs['batsman_runs'] == 4) | (death_overs['batsman_runs'] == 6)]
    death_over_hitters = death_over_boundaries.groupby('batsman').size().sort_values(ascending=False).head(5)

    # 4. V Kohli's run distribution against different teams
    vk_df = ipl[ipl['batsman'] == 'V Kohli']
    vk_record = vk_df.groupby('bowling_team')['batsman_runs'].sum().sort_values(ascending=False)

    # 5. Top 5 Highest Individual Scores in a match
    highest_scores = ipl.groupby(['match_id', 'batsman'])['batsman_runs'].sum().sort_values(ascending=False).head(5)
    
    # 6. Run distribution by type (0, 1, 2, 3, 4, 6)
    run_distribution = ipl['batsman_runs'].value_counts().sort_index()
    
    # 7. Strike rate analysis for top batsmen (min 500 runs)
    batsman_stats = ipl.groupby('batsman').agg({
        'batsman_runs': 'sum',
        'ball': 'count'
    }).reset_index()
    batsman_stats.columns = ['batsman', 'total_runs', 'balls_faced']
    batsman_stats['strike_rate'] = (batsman_stats['total_runs'] / batsman_stats['balls_faced']) * 100
    batsman_stats = batsman_stats[batsman_stats['total_runs'] >= 500].sort_values('strike_rate', ascending=False).head(10)

    # --- Page 2: Top Run Scorers (Horizontal Bar Chart) ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.suptitle('🏏 IPL BATTING LEGENDS', fontsize=24, weight='bold', y=0.96, color=COLORS['primary'])
    
    ax = plt.subplot(111)
    
    # Create gradient colors for bars
    colors_gradient = plt.cm.viridis(np.linspace(0.3, 0.9, len(top_batsman)))
    
    bars = ax.barh(range(len(top_batsman)), top_batsman.values, color=colors_gradient, edgecolor='black', linewidth=1.5)
    ax.set_yticks(range(len(top_batsman)))
    ax.set_yticklabels(top_batsman.index, fontsize=12, weight='bold')
    ax.set_xlabel('Total Runs Scored', fontsize=14, weight='bold')
    ax.set_title('Top 10 Run Scorers in IPL History', fontsize=16, pad=20, weight='bold')
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Add value labels on bars
    for i, (bar, value) in enumerate(zip(bars, top_batsman.values)):
        ax.text(value + 100, i, f'{value:,}', va='center', fontsize=11, weight='bold', color=COLORS['primary'])
    
    # Add rank badges
    for i in range(min(3, len(top_batsman))):
        medal = ['🥇', '🥈', '🥉'][i]
        ax.text(-200, i, medal, va='center', ha='center', fontsize=16)
    
    # Description box
    description = ("These batsmen have demonstrated exceptional consistency and skill throughout IPL history.\n"
                   "The chart showcases the cumulative runs scored by the top 10 performers.")
    fig.text(0.5, 0.08, description, ha='center', va='center', fontsize=11, 
             bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.3), wrap=True)
    
    plt.tight_layout(rect=[0, 0.12, 1, 0.94])
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # --- Page 3: Power Hitters - Sixes & Fours (Dual Bar Chart) ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.suptitle('⚡ POWER HITTERS ANALYSIS', fontsize=24, weight='bold', y=0.96, color=COLORS['danger'])
    
    # Plot 1: Most Sixes
    ax1 = plt.subplot(2, 1, 1)
    bars1 = ax1.bar(range(len(max_sixes_batsman)), max_sixes_batsman.values, 
                    color=COLORS['danger'], edgecolor='black', linewidth=1.5, alpha=0.8)
    ax1.set_xticks(range(len(max_sixes_batsman)))
    ax1.set_xticklabels(max_sixes_batsman.index, rotation=45, ha='right', fontsize=11, weight='bold')
    ax1.set_ylabel('Number of Sixes', fontsize=12, weight='bold')
    ax1.set_title('🚀 Top 5 Batsmen with Most Sixes', fontsize=16, pad=15, weight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars1, max_sixes_batsman.values)):
        ax1.text(i, value + 5, str(value), ha='center', fontsize=12, weight='bold', color=COLORS['danger'])
    
    # Plot 2: Most Fours
    ax2 = plt.subplot(2, 1, 2)
    bars2 = ax2.bar(range(len(max_fours_batsman)), max_fours_batsman.values, 
                    color=COLORS['success'], edgecolor='black', linewidth=1.5, alpha=0.8)
    ax2.set_xticks(range(len(max_fours_batsman)))
    ax2.set_xticklabels(max_fours_batsman.index, rotation=45, ha='right', fontsize=11, weight='bold')
    ax2.set_ylabel('Number of Fours', fontsize=12, weight='bold')
    ax2.set_title('🎯 Top 5 Batsmen with Most Fours', fontsize=16, pad=15, weight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars2, max_fours_batsman.values)):
        ax2.text(i, value + 10, str(value), ha='center', fontsize=12, weight='bold', color=COLORS['success'])
    
    # Description
    description = ("Power hitters are the game-changers in T20 cricket. Sixes demonstrate raw power,\n"
                   "while fours showcase timing and placement. These batsmen excel at boundary hitting.")
    fig.text(0.5, 0.06, description, ha='center', va='center', fontsize=11,
             bbox=dict(boxstyle='round,pad=1', facecolor='lightyellow', alpha=0.3), wrap=True)
    
    plt.tight_layout(rect=[0, 0.10, 1, 0.94])
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

    # --- Page 4: Run Distribution (Pie Chart & Histogram) ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.suptitle('📊 RUN DISTRIBUTION ANALYSIS', fontsize=24, weight='bold', y=0.96, color=COLORS['purple'])
    
    # Plot 1: Pie Chart - Run Types Distribution
    ax1 = plt.subplot(2, 1, 1)
    colors_pie = [COLORS['gray'], COLORS['info'], COLORS['success'], COLORS['warning'], 
                  COLORS['primary'], COLORS['danger']]
    
    wedges, texts, autotexts = ax1.pie(run_distribution.values, labels=run_distribution.index,
                                        autopct='%1.1f%%', startangle=90, colors=colors_pie,
                                        explode=[0.05 if x in [4, 6] else 0 for x in run_distribution.index],
                                        shadow=True, textprops={'fontsize': 11, 'weight': 'bold'})
    
    plt.setp(autotexts, color='white', weight='bold', size=10)
    ax1.set_title('🎯 Distribution of Runs by Type (0, 1, 2, 3, 4, 6)', fontsize=14, pad=20, weight='bold')
    
    # Add legend with counts
    legend_labels = [f'{run} runs: {count:,} balls' for run, count in zip(run_distribution.index, run_distribution.values)]
    ax1.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=9)
    
    # Plot 2: Histogram - Runs per Ball
    ax2 = plt.subplot(2, 1, 2)
    bars = ax2.bar(run_distribution.index, run_distribution.values, color=colors_pie, 
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    ax2.set_xlabel('Runs Scored', fontsize=12, weight='bold')
    ax2.set_ylabel('Frequency (Number of Balls)', fontsize=12, weight='bold')
    ax2.set_title('📈 Histogram: Frequency of Each Run Type', fontsize=14, pad=15, weight='bold')
    ax2.grid(axis='y', alpha=0.3, linestyle='--')
    
    # Add value labels
    for bar, value in zip(bars, run_distribution.values):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + max(run_distribution.values)*0.01,
                f'{value:,}', ha='center', va='bottom', fontsize=10, weight='bold')
    
    # Description
    description = ("This analysis shows how runs are distributed across different scoring types.\n"
                   "Boundaries (4s & 6s) are highlighted, showing their impact on the game.")
    fig.text(0.5, 0.06, description, ha='center', va='center', fontsize=11,
             bbox=dict(boxstyle='round,pad=1', facecolor='lavender', alpha=0.3), wrap=True)
    
    plt.tight_layout(rect=[0, 0.10, 1, 0.94])
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # --- Page 5: Death Over Specialists & Strike Rate ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.suptitle('🔥 DEATH OVERS & STRIKE RATE ANALYSIS', fontsize=22, weight='bold', y=0.96, color=COLORS['danger'])
    
    # Plot 1: Death Over Hitters
    ax1 = plt.subplot(2, 1, 1)
    colors_death = plt.cm.Reds(np.linspace(0.5, 0.9, len(death_over_hitters)))
    bars1 = ax1.bar(range(len(death_over_hitters)), death_over_hitters.values, 
                    color=colors_death, edgecolor='black', linewidth=1.5)
    ax1.set_xticks(range(len(death_over_hitters)))
    ax1.set_xticklabels(death_over_hitters.index, rotation=45, ha='right', fontsize=11, weight='bold')
    ax1.set_ylabel('Number of Boundaries', fontsize=12, weight='bold')
    ax1.set_title('💥 Top 5 Death Over Specialists (Overs 16-20)', fontsize=15, pad=15, weight='bold')
    ax1.grid(axis='y', alpha=0.3, linestyle='--')
    
    for i, (bar, value) in enumerate(zip(bars1, death_over_hitters.values)):
        ax1.text(i, value + 5, str(value), ha='center', fontsize=11, weight='bold', color=COLORS['danger'])
    
    # Plot 2: Strike Rate of Top Batsmen
    ax2 = plt.subplot(2, 1, 2)
    colors_sr = plt.cm.Greens(np.linspace(0.4, 0.9, len(batsman_stats)))
    bars2 = ax2.barh(range(len(batsman_stats)), batsman_stats['strike_rate'].values, 
                     color=colors_sr, edgecolor='black', linewidth=1.5)
    ax2.set_yticks(range(len(batsman_stats)))
    ax2.set_yticklabels(batsman_stats['batsman'].values, fontsize=10, weight='bold')
    ax2.set_xlabel('Strike Rate', fontsize=12, weight='bold')
    ax2.set_title('⚡ Top 10 Batsmen by Strike Rate (Min 500 runs)', fontsize=15, pad=15, weight='bold')
    ax2.invert_yaxis()
    ax2.grid(axis='x', alpha=0.3, linestyle='--')
    
    for i, (bar, value) in enumerate(zip(bars2, batsman_stats['strike_rate'].values)):
        ax2.text(value + 1, i, f'{value:.1f}', va='center', fontsize=10, weight='bold', color=COLORS['success'])
    
    # Description
    description = ("Death overs (16-20) are crucial in T20 cricket. Strike rate measures scoring efficiency.\n"
                   "These metrics identify the most impactful batsmen in pressure situations.")
    fig.text(0.5, 0.06, description, ha='center', va='center', fontsize=11,
             bbox=dict(boxstyle='round,pad=1', facecolor='lightcoral', alpha=0.2), wrap=True)
    
    plt.tight_layout(rect=[0, 0.10, 1, 0.94])
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # --- Page 6: Virat Kohli Analysis (Pie Chart) ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.suptitle("👑 VIRAT KOHLI - PERFORMANCE BREAKDOWN", fontsize=22, weight='bold', y=0.96, color=COLORS['primary'])
    
    ax = plt.subplot(111)
    
    # Prepare data - group smaller slices
    if len(vk_record) > 7:
        others = vk_record[6:].sum()
        vk_record = vk_record[:6]
        vk_record['Others'] = others
    
    # Create exploded pie chart
    explode = [0.1 if i == 0 else 0.02 for i in range(len(vk_record))]
    colors_vk = plt.cm.Set3(np.linspace(0, 1, len(vk_record)))
    
    wedges, texts, autotexts = ax.pie(vk_record.values, labels=vk_record.index,
                                       autopct='%1.1f%%', startangle=45, colors=colors_vk,
                                       explode=explode, shadow=True, 
                                       textprops={'fontsize': 11, 'weight': 'bold'})
    
    plt.setp(autotexts, color='white', weight='bold', size=11)
    ax.set_title("🏏 Runs Distribution Against Different Teams", fontsize=16, pad=30, weight='bold')
    
    # Add legend with run counts
    legend_labels = [f'{team}: {runs:,} runs' for team, runs in zip(vk_record.index, vk_record.values)]
    ax.legend(legend_labels, loc='center left', bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
    
    # Add statistics box
    total_vk_runs = vk_record.sum()
    fig.text(0.5, 0.25, f"Total Runs: {total_vk_runs:,}", ha='center', va='center',
             fontsize=14, weight='bold', color=COLORS['primary'],
             bbox=dict(boxstyle='round,pad=0.8', facecolor='yellow', alpha=0.3))
    
    # Description
    description = ("Virat Kohli is one of IPL's most consistent performers. This pie chart shows\n"
                   "the distribution of his runs against various teams, highlighting his dominance.")
    fig.text(0.5, 0.15, description, ha='center', va='center', fontsize=11,
             bbox=dict(boxstyle='round,pad=1', facecolor='lightblue', alpha=0.2), wrap=True)
    
    plt.tight_layout(rect=[0, 0.18, 1, 0.94])
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # --- Page 7: Top Individual Performances (Table) ---
    fig = plt.figure(figsize=(8.5, 11), facecolor='white')
    fig.suptitle('🌟 RECORD-BREAKING PERFORMANCES', fontsize=24, weight='bold', y=0.94, color=COLORS['warning'])
    
    ax = fig.add_subplot(111)
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare table data
    table_data = highest_scores.reset_index()
    table_data.columns = ['Match ID', 'Batsman', 'Runs']
    table_data['Rank'] = ['🥇', '🥈', '🥉', '4️⃣', '5️⃣']
    
    # Create table
    table = ax.table(cellText=table_data[['Rank', 'Batsman', 'Runs']].values,
                     colLabels=['Rank', 'Batsman', 'Runs Scored'],
                     loc='center',
                     cellLoc='center',
                     colWidths=[0.15, 0.5, 0.25])
    
    table.auto_set_font_size(False)
    table.set_fontsize(13)
    table.scale(1, 3.5)
    
    # Style the table
    for i in range(len(table_data) + 1):
        for j in range(3):
            cell = table[(i, j)]
            if i == 0:  # Header row
                cell.set_facecolor(COLORS['primary'])
                cell.set_text_props(weight='bold', color='white', size=14)
            else:  # Data rows
                if i % 2 == 0:
                    cell.set_facecolor('#f0f0f0')
                else:
                    cell.set_facecolor('white')
                cell.set_text_props(weight='bold', size=13)
                
                # Highlight runs column
                if j == 2:
                    cell.set_facecolor('#ffffcc')
    
    # Add title and description
    fig.text(0.5, 0.75, "Top 5 Highest Individual Scores in a Single Match", 
             ha='center', va='center', fontsize=18, weight='bold', color=COLORS['primary'])
    
    description = ("These extraordinary innings represent the pinnacle of individual batting performances in IPL.\n"
                   "Each score showcases exceptional skill, concentration, and match-winning ability.\n"
                   "These batsmen dominated their respective matches with remarkable consistency and power.")
    fig.text(0.5, 0.20, description, ha='center', va='center', fontsize=12,
             bbox=dict(boxstyle='round,pad=1.5', facecolor='lightyellow', alpha=0.4), wrap=True)
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()


print("=" * 60)
print("✅ SUCCESS! IPL Analysis Report Generated")
print("=" * 60)
print(f"📄 File: report.pdf")
print(f"📊 Pages: 7 comprehensive analysis pages")
print(f"🎨 Visualizations: Bar charts, Pie charts, Histograms, Tables")
print(f"📈 Insights: Top performers, Power hitters, Strike rates, and more")
print("=" * 60)
print("Report includes:")
print("  1. Title Page with Statistics")
print("  2. Top 10 Run Scorers")
print("  3. Power Hitters (Sixes & Fours)")
print("  4. Run Distribution Analysis")
print("  5. Death Overs & Strike Rate")
print("  6. Virat Kohli Performance")
print("  7. Record-Breaking Performances")
print("=" * 60)