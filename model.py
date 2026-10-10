"""Train a pre-publication regression model without using outcome counts as features."""
import random, math

def dataset(seed=42, n=300):
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        duration = rng.uniform(10, 180)
        hour = rng.randrange(24)
        video = rng.randrange(2)
        x = [1, duration / 180, hour / 24, video]
        target = max(0.001, 0.02 + 0.025 * video - 0.01 * x[1] + 0.015 * x[2] + rng.gauss(0, 0.006))
        rows.append({'id': i + 1, 'duration_seconds': duration, 'hour': hour, 'video': video, 'x': x, 'engagement_rate': target})
    rng.shuffle(rows)
    return rows

def train(rows, ridge=0, epochs=600):
    w = [0.0] * 4
    for _ in range(epochs):
        gradient = [0.0] * 4
        for row in rows:
            error = sum((a * b for a, b in zip(w, row['x']))) - row['engagement_rate']
            for j, x in enumerate(row['x']):
                gradient[j] += error * x / len(rows)
        w = [a - 0.1 * (gradient[j] + (ridge * a if j else 0)) for j, a in enumerate(w)]
    return w

def predict(w, x):
    return max(0, min(1, sum((a * b for a, b in zip(w, x)))))

def mae(rows, w):
    return sum((abs(predict(w, r['x']) - r['engagement_rate']) for r in rows)) / len(rows)

def run_model(p):
    duration = float(p.get('duration', 60))
    hour = int(p.get('hour', 18))
    video = int(p.get('video', 1))
    if not math.isfinite(duration) or not 10 <= duration <= 180 or (not 0 <= hour <= 23) or (video not in [0, 1]):
        raise ValueError('Duration 10–180, hour 0–23, video 0 or 1 required')
    seed = int(p.get('seed', 42))
    rows = dataset(seed)
    training, validation, test = (rows[:180], rows[180:240], rows[240:])
    trials = [{'ridge': r, 'validation_mae': mae(validation, train(training, r))} for r in [0, 0.01, 0.1]]
    chosen = min(trials, key=lambda x: x['validation_mae'])
    weights = train(training + validation, chosen['ridge'])
    baseline = sum((r['engagement_rate'] for r in training + validation)) / 240
    prediction = predict(weights, [1, duration / 180, hour / 24, video])
    return {'train_samples': 180, 'validation_samples': 60, 'test_samples': 60, 'selected_ridge': chosen['ridge'], 'model_selection': trials, 'test_mae': mae(test, weights), 'baseline_mae': sum((abs(r['engagement_rate'] - baseline) for r in test)) / 60, 'prediction': prediction, 'weights': dict(zip(['intercept', 'duration_scaled', 'hour_scaled', 'video'], weights)), 'examples': [{'id': r['id'], 'actual': r['engagement_rate'], 'predicted': predict(weights, r['x'])} for r in test[:10]], 'note': 'Synthetic engagement labels. Pre-publication features only; tuning uses validation, test is held out. No FOX affiliation or real audience performance claim.'}
