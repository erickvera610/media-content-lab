const assert=require('node:assert/strict');const {run}=require('./docs/demo.js');const p={"min_views": 100};assert.deepEqual(run(p),run(p));assert.ok(JSON.stringify(run(p)).length>100);console.log('Browser exercise passed');
assert.ok(run({min_views:100}).ranked_posts.every(x=>Number.isFinite(x.engagement_rate)));
