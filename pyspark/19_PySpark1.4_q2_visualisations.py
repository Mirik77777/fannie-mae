import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
servicer_pd = servicer_results.toPandas()
speed_pd = cure_speed.toPandas()
# ---- Chart 1: Cure vs Roll side by side ----
fig, axes = plt.subplots(1, 2, figsize=(16, 8))
top_cure = servicer_pd.nlargest(10, 'cure_rate_pct')
axes[0].barh(top_cure['servicer'], top_cure['cure_rate_pct'], color='#2ecc71')
axes[0].set_xlabel('Cure Rate (%)')
axes[0].set_title('Top 10 Servicers - Highest Cure Rate')
axes[0].invert_yaxis()
for i, (v, n) in enumerate(zip(top_cure['cure_rate_pct'], top_cure['delinquent_months'])):
    axes[0].text(v+0.2, i, f'{v:.1f}% (n={int(n):,})', va='center', fontsize=8)
top_roll = servicer_pd.dropna(subset=['roll_rate_pct']).nlargest(10, 'roll_rate_pct')
axes[1].barh(top_roll['servicer'], top_roll['roll_rate_pct'], color='#e74c3c')
axes[1].set_xlabel('Roll Rate to Serious Delinquency (%)')
axes[1].set_title('Top 10 Servicers - Highest Roll Rate')
axes[1].invert_yaxis()
for i, (v, n) in enumerate(zip(top_roll['roll_rate_pct'], top_roll['early_delinq_months'])):
    axes[1].text(v+0.1, i, f'{v:.1f}% (n={int(n):,})', va='center', fontsize=8)
plt.suptitle('Servicer Performance: Cure vs Roll Rates', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/tmp/q2_cure_roll.png', dpi=150)
plt.show()
print('Saved: /tmp/q2_cure_roll.png')
# ---- Chart 2: Scatter - Cure vs Roll ----
fig, ax = plt.subplots(figsize=(10, 8))
sdata = servicer_pd.dropna(subset=['cure_rate_pct', 'roll_rate_pct'])
sizes = sdata['delinquent_months'] / sdata['delinquent_months'].max() * 500
ax.scatter(sdata['cure_rate_pct'], sdata['roll_rate_pct'],
           s=sizes, alpha=0.6, edgecolors='black', linewidth=0.5)
for _, row in sdata.iterrows():
    if row['delinquent_months'] > sdata['delinquent_months'].quantile(0.75):
        ax.annotate(str(row['servicer'])[:25],
                    (row['cure_rate_pct'], row['roll_rate_pct']),
                    fontsize=7, ha='center', va='bottom')
ax.set_xlabel('Cure Rate (%)')
ax.set_ylabel('Roll Rate (%)')
ax.set_title('Servicer Performance Map (bubble size = delinquent volume)')
plt.tight_layout()
plt.savefig('/tmp/q2_scatter.png', dpi=150)
plt.show()
print('Saved: /tmp/q2_scatter.png')
# ---- Chart 3: Cure Speed ----
top_speed = speed_pd.nsmallest(15, 'avg_months_to_cure')
fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(top_speed['servicer_name'], top_speed['avg_months_to_cure'], color='#3498db')
ax.set_xlabel('Average Months to Cure')
ax.set_title('Fastest Servicers: Average Time to Cure Delinquency')
ax.invert_yaxis()
for b, med in zip(bars, top_speed['median_months_to_cure']):
    ax.text(b.get_width()+0.05, b.get_y()+b.get_height()/2,
            f'median: {med:.1f}mo', va='center', fontsize=9, color='gray')
plt.tight_layout()
plt.savefig('/tmp/q2_speed.png', dpi=150)
plt.show()
