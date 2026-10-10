"""Train on user-owned chronological CSV; save auditable JSON model/report."""
import argparse, csv, json, math
from pathlib import Path
from model import train, mae, predict

def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as stream:
        for raw in csv.DictReader(stream):
            d, h, v, y = [float(raw[k]) for k in ["duration_seconds", "hour", "video", "engagement_rate"]]
            if not all(map(math.isfinite, [d,h,v,y])) or not (10 <= d <= 180 and h.is_integer() and 0 <= h <= 23 and v in (0,1) and 0 <= y <= 1):
                raise ValueError("Invalid pre-publication features or engagement label")
            rows.append({"timestamp": raw["timestamp"], "x": [1,d/180,h/24,v], "engagement_rate": y})
    from datetime import datetime
    rows.sort(key=lambda r: datetime.fromisoformat(r["timestamp"]))
    if len(rows) < 50:
        raise ValueError("At least 50 dated records required")
    if len({r["timestamp"] for r in rows}) != len(rows):
        raise ValueError("Unique timestamps required to avoid splitting simultaneous records")
    return rows

def fit_csv(path):
    rows = load(path)
    a,b = int(len(rows)*.6), int(len(rows)*.8)
    training, validation, test = rows[:a],rows[a:b],rows[b:]
    trials = [{"ridge": r, "validation_mae": mae(validation, train(training,r))} for r in [0,.01,.1]]
    chosen = min(trials, key=lambda r:r["validation_mae"])
    weights = train(training+validation, chosen["ridge"])
    baseline = sum(r["engagement_rate"] for r in training+validation)/b
    errors = [abs(predict(weights,r["x"])-r["engagement_rate"]) for r in test]
    return {"weights": weights, "feature_order": ["intercept","duration/180","hour/24","video"],
            "split": {"train":a,"validation":b-a,"test":len(test)},
            "boundaries": {"last_train":training[-1]["timestamp"],"first_validation":validation[0]["timestamp"],"last_validation":validation[-1]["timestamp"],"first_test":test[0]["timestamp"]},
            "selection":trials,"selected_ridge":chosen["ridge"], "test_mae":sum(errors)/len(errors),
            "test_rmse":math.sqrt(sum(e*e for e in errors)/len(errors)),
            "baseline_mae":sum(abs(r["engagement_rate"]-baseline) for r in test)/len(test),
            "note":"Chronological holdout. Labels must use the same observation window. No outcome counts are features. Performance depends on supplied data; this is not a causal model."}
if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("--output",default="trained-model.json")
    args=parser.parse_args()
    report=fit_csv(args.csv_path)
    Path(args.output).write_text(json.dumps(report,indent=2,allow_nan=False))
    print(json.dumps(report))
