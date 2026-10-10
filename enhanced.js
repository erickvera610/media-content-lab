function randomGenerator(seed=42) {
    let state=seed>>>0;
    return ()=> {
        state=(1664525*state+1013904223)>>>0;
        return state/4294967296;
    }
    ;
}
function normal(random) {
    return Math.sqrt(-2*Math.log(Math.max(random(),1e-10)))*Math.cos(2*Math.PI*random());
}
function makeDataset(seed=42) {
    const random=randomGenerator(seed),rows=[];
    for(let id=1;id<=300;id++) {
        const duration=10+170*random(),hour=Math.floor(24*random()),video=Math.floor(2*random()),x=[1,duration/180,hour/24,video],y=Math.max(.001,.02+.025*video-.01*x[1]+.015*x[2]+.006*normal(random));
        rows.push( {
            id,x,y
        }
        );
    }
    for(let i=299;i>0;i--) {
        const j=Math.floor(random()*(i+1));
        [rows[i],rows[j]]=[rows[j],rows[i]];
    }
    return rows;
}
function fitModel(rows,ridge=0) {
    let w=[0,0,0,0];
    for(let epoch=0;epoch<600;epoch++) {
        const g=[0,0,0,0];
        for(const row of rows) {
            const error=w.reduce((s,v,j)=>s+v*row.x[j],0)-row.y;
            row.x.forEach((x,j)=>g[j]+=error*x/rows.length);
        }
        w=w.map((v,j)=>v-.1*(g[j]+(j?ridge*v:0)));
    }
    return w;
}
function prediction(w,x) {
    return Math.max(0,Math.min(1,w.reduce((s,v,j)=>s+v*x[j],0)));
}
function runEnhanced(p= {
}
) {
    const duration=Number(p.duration??60),hour=Number(p.hour??18),video=Number(p.video??1);
    if(!Number.isFinite(duration)||duration<10||duration>180||!Number.isInteger(hour)||hour<0||hour>23||![0,1].includes(video))throw Error('Duration 10–180, hour 0–23, video 0 or 1 required');
    const rows=makeDataset(p.seed??42),training=rows.slice(0,180),validation=rows.slice(180,240),test=rows.slice(240),mae=(rows,w)=>rows.reduce((s,r)=>s+Math.abs(prediction(w,r.x)-r.y),0)/rows.length,trials=[0,.01,.1].map(ridge=>( {
        ridge,validation_mae:mae(validation,fitModel(training,ridge))
    }
    )),chosen=trials.reduce((a,b)=>a.validation_mae<b.validation_mae?a:b),w=fitModel(rows.slice(0,240),chosen.ridge),base=rows.slice(0,240).reduce((s,r)=>s+r.y,0)/240;
    return  {
        train_samples:180,validation_samples:60,test_samples:60,selected_ridge:chosen.ridge,model_selection:trials,test_mae:mae(test,w),baseline_mae:test.reduce((s,r)=>s+Math.abs(r.y-base),0)/60,prediction:prediction(w,[1,duration/180,hour/24,video]),weights:Object.fromEntries(['intercept','duration_scaled','hour_scaled','video'].map((k,i)=>[k,w[i]])),examples:test.slice(0,10).map(r=>( {
            id:r.id,actual:r.y,predicted:prediction(w,r.x)
        }
        )),note:'Synthetic labels; not real FOX audience data. Browser and Python random generators differ.'
    }
    ;
}
if(typeof module!=='undefined')module.exports= {
    runEnhanced,makeDataset,fitModel
}
;
