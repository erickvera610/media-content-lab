const assert=require('node:assert/strict');
const {runEnhanced}=require('./enhanced.js');const r=runEnhanced();assert.ok(r.test_mae<r.baseline_mae);assert.equal(r.test_samples,60);assert.deepEqual(r,runEnhanced());assert.throws(()=>runEnhanced({duration:0}));
console.log('Enhanced behavior tests passed');
