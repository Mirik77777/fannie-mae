import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
national_pd = result_national.toPandas()
rates = {}
for _, row in national_pd.iterrows():
    rates[row['risk_group']] = row['delinquency_rate_pct']
baseline = rates.get('Low DTI & Low CLTV', 0)
dti_only = rates.get('High DTI & Low CLTV', 0)
cltv_only = rates.get('Low DTI & High CLTV', 0)
combined = rates.get('High DTI & High CLTV', 0)
matrix = np.array([[baseline, cltv_only],[dti_only, combined]])
fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(matrix, cmap='YlOrRd', aspect='auto')
ax.set_xticks([0, 1]); ax.set_xticklabels(['CLTV <= 80%', 'CLTV > 80%'])
ax.set_yticks([0, 1]); ax.set_yticklabels(['DTI <= 43%', 'DTI > 43%'])
for i in range(2):
    for j in range(2):
        color = 'white' if matrix[i,j] > matrix.max()*0.6 else 'black'
        ax.text(j, i, f'{matrix[i,j]:.3f}%', ha='center', va='center', fontsize=14, fontweight='bold', color=color)
ax.set_title('90+ Day Delinquency Rate by Risk Layer (National)')
plt.colorbar(im, label='Delinquency Rate (%)')
plt.tight_layout(); plt.savefig('/tmp/q1_heatmap.png', dpi=150); plt.show()
print('Saved: /tmp/q1_heatmap.png')
labels = ['Low DTI &\nLow CLTV','High DTI\nonly','High CLTV\nonly','High DTI &\nHigh CLTV']
vals = [baseline, dti_only, cltv_only, combined]
colors = ['#2ecc71','#f39c12','#e67e22','#e74c3c']
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(labels, vals, color=colors, edgecolor='black', linewidth=0.5)
for b, v in zip(bars, vals):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.001, f'{v:.3f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')
ax.set_ylabel('90+ Day Delinquency Rate (%)'); ax.set_title('Risk Layering Effect: 90+ Day Delinquency by DTI x CLTV')
plt.tight_layout(); plt.savefig('/tmp/q1_bar.png', dpi=150); plt.show()
print('Saved: /tmp/q1_bar.png')
state_pd = state_multipliers.toPandas()
top15 = state_pd.nlargest(15, 'multiplier')
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(top15['property_state'], top15['multiplier'], color='steelblue')
ax.set_xlabel('Risk Multiplier (Combined / Baseline)'); ax.set_title('Top 15 States: Risk Layering Multiplier Effect')
ax.axvline(x=1, color='red', linestyle='--', alpha=0.7, label='No amplification'); ax.invert_yaxis()
for b, v in zip(bars, top15['multiplier']):
    ax.text(b.get_width()+0.1, b.get_y()+b.get_height()/2, f'{v:.1f}x', va='center', fontsize=10)
ax.legend(); plt.tight_layout(); plt.savefig('/tmp/q1_states.png', dpi=150); plt.show()
