import random, math

def rank(posts, min_views=100):
    if min_views < 1:
        raise ValueError('Minimum views must be positive')
    output = []
    for post in posts:
        v = post['views']
        l = post['likes']
        s = post['shares']
        c = post['comments']
        if any((not isinstance(x, int) or x < 0 for x in [v, l, s, c])):
            raise ValueError('Nonnegative integer counts required')
        if v < min_views:
            continue
        rate = (l + c + s) / v
        score = (l + 2 * c + 3 * s) / v
        output.append({**post, 'engagement_rate': rate, 'editorial_score': score})
    return sorted(output, key=lambda x: -x['editorial_score'])

def run(p):
    rng = random.Random(int(p.get('seed', 42)))
    posts = []
    for i in range(30):
        views = rng.randint(100, 15000)
        posts.append({'title': f'Fictional post {i + 1}', 'format': ['Video', 'Article', 'Clip'][i % 3], 'views': views, 'likes': rng.randint(0, views // 8), 'shares': rng.randint(0, views // 40), 'comments': rng.randint(0, views // 60)})
    ranked = rank(posts, int(p.get('min_views', 100)))
    return {'ranked_posts': ranked, 'eligible_posts': len(ranked), 'note': 'Independent educational project inspired by media workflows; no affiliation or private FOX data. Rankings are descriptive, not causal.'}
_rank_run = run

def run(p):
    if p.get('mode') == 'model':
        from model import run_model
        return run_model(p)
    return _rank_run(p)
