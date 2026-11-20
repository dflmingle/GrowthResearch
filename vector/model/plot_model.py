from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent
x=json.loads((R/'output/results.json').read_text(encoding='utf-8'))
fig,axes=plt.subplots(1,3,figsize=(15,4.5),layout='constrained')
for i,a in enumerate(x['arms']):
 axes[0].plot(range(29),[v/a['cpi_usd']*100 for v in a['cumulative_ltv']],label=a['arm'],linestyle='-' if i==0 else '--',linewidth=2.5 if i==0 else 1.5)
axes[0].axhline(100,color='#888888',linestyle=':');axes[0].set(title='Matched synthetic cohort: identical outcomes',xlabel='Install age (day)',ylabel='Cumulative net ad ROAS (%)');axes[0].legend(fontsize=8)
s=x['supply_segments'];vol=[a['cumulative_installs'] for a in s]
axes[1].plot(vol,[a['average_roas_d28']*100 for a in s],marker='o',label='Blended ROAS')
axes[1].plot(vol,[a['marginal_roas_d28']*100 for a in s],marker='s',label='Marginal ROAS')
axes[1].axhline(100,color='#888888',linestyle=':');axes[1].set(title='Scaling: averages can conceal losses',xlabel='Cumulative expected installs',ylabel='D28 net ad ROAS (%)');axes[1].legend(fontsize=8)
b=x['prediction_bias_sensitivity'];axes[2].plot([a['assumed_relative_bias']*100 for a in b],[a['realized_roas_if_price_equals_ceiling']*100 for a in b],marker='o',color='#a54837')
axes[2].axhline(100,color='#888888',linestyle=':');axes[2].set(title='Sensitivity only; no measured model accuracy',xlabel='Assumed LTV prediction bias (%)',ylabel='ROAS at illustrative CPI ceiling (%)')
for ax in axes:ax.grid(alpha=.2)
fig.suptitle('OFFLINE ILLUSTRATION — NOT Unity / AppLovin measured performance',fontsize=13)
fig.savefig(R/'output/economics.png',dpi=170)
print(R/'output/economics.png')
