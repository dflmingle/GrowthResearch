"""Synthetic installations and finite-window cashflows; ground truth separate from features."""
import math,random
from .common import BASE,DAY
def generate(seed,world,protocol):
    rng=random.Random(seed);n=protocol['samples_per_world_seed'];rows=[];cashflows=[]
    for i in range(n):
        split='train' if i<180 else 'validation' if i<270 else 'test'
        pos=i if split=='train' else i-(180 if split=='validation' else 270)
        count=180 if split=='train' else 90;lo,hi=protocol['install_days'][split]
        install=BASE+int((lo+(hi-lo)*pos/max(1,count-1))*DAY);pred=install+6*3600
        z=rng.gauss(0,1);context=rng.gauss(0,1);engagement=rng.gauss(0,1)
        country=rng.randrange(4);platform=rng.randrange(2);sessions=max(0,round(4+1.7*engagement+rng.gauss(0,1)))
        history=round(1e6*80*math.exp(.95*z+.2*rng.gauss(0,1)));refund_history=round(history*.10) if rng.random()<.2 else 0
        shared=rng.random()<.1
        # The same random draws are consumed in both worlds. Only the structural
        # coefficient of independent history latent z changes, never test selection.
        log_rate=(.9*z if world=='history_informative' else 0)+.5*context+.65*engagement-.4
        sid=f'syn:{world}:{seed}:install-{i:04d}';events=[]
        for j,d in enumerate([.5,2,6,14,29]):
            purchase_draw=rng.random();noise=rng.gauss(0,.55);refund_draw=rng.random()
            occurs=purchase_draw<.70
            amount=max(1,round(1e6*18*math.exp(log_rate+noise))) if occurs else 0
            if amount:
                event=dict(sample_id=sid,event_id=f'syn:purchase-{j}',kind='IAP',occurred_at=install+int(d*DAY),
                    available_at=install+int(d*DAY)+DAY,amount_micros=amount,currency='USD')
                events.append(event)
                if refund_draw<.2:
                    events.append(dict(sample_id=sid,event_id=f'syn:refund-{j}',kind='REFUND',occurred_at=install+int((d+4)*DAY),
                        available_at=install+int((d+4)*DAY)+DAY,amount_micros=-round(amount*.30),currency='USD'))
        row=dict(sample_id=sid,owner_unit=f'syn:owner:{seed}:{i}',world=world,seed=seed,split=split,country=country,platform=platform,
            context_score=context,early_sessions=sessions,early_engagement=engagement,install_at=install,prediction_at=pred,
            early_observed_at=pred-3600,early_available_at=pred,history_gross_micros=history,history_refund_micros=refund_history,
            shared_device=shared,history_latent=z)
        for horizon in [1,7,30]:
            end=install+horizon*DAY
            row[f'label_D{horizon}']=sum(e['amount_micros'] for e in events if install<=e['occurred_at']<end)/1e6
            row[f'mature_D{horizon}']=end+2*DAY
        rows.append(row);cashflows.extend(events)
    return rows,cashflows
