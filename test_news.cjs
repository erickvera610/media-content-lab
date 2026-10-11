const fs=require('fs'),assert=require('node:assert/strict'),{predictNews}=require('./docs/news.js');const artifact=JSON.parse(fs.readFileSync('artifacts/news-model.json')),report=JSON.parse(fs.readFileSync('artifacts/news-results.json'));
for(const row of report.examples){const r=predictNews(artifact,row.features);assert.ok(Math.abs(r.predicted_log1p_shares-row.predicted_log1p_shares)<1e-9);}
assert.throws(()=>predictNews(artifact,{shares:100}));console.log('Python-trained news model matches browser predictions on reserved examples');
