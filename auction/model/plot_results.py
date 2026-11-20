from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R=Path(__file__).resolve().parent/'output'
data=json.loads((R/'results.json').read_text())['arms']
fig,axs=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for profile,label in [('applovin','AL-like fixture (500 ms)'),('unity','Unity-like fixture (200 ms)')]:
 a=[r for r in data if r['profile']==profile]
 x=[r['ltv_prediction_multiplier'] for r in a]
 axs[0].plot(x,[r['CPI_usd'] for r in a],marker='o',label=label)
 axs[1].plot(x,[r['D28_ROAS'] for r in a],marker='o',label=label)
axs[0].set_ylabel('Synthetic CPI (USD)');axs[1].set_ylabel('Synthetic D28 ROAS')
axs[1].axhline(1,color='gray',linestyle='--',linewidth=1)
for ax in axs:
 ax.set_xlabel('Assumed LTV prediction multiplier');ax.set_xticks([.6,1,1.4]);ax.grid(alpha=.2)
axs[0].legend(fontsize=8)
fig.suptitle('Synthetic offline illustration - NOT vendor performance or model accuracy',fontsize=11)
fig.savefig(R/'synthetic_economics.png',dpi=170)
print(R/'synthetic_economics.png')
