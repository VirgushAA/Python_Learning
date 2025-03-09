import random


def turrets_generator():
    cuts = sorted(random.sample(range(101), 4))
    traits = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, 4)] + [100 - cuts[-1]]
    return type('Turret', (object,), {
        'personality_traits': {k: v for k, v in
                               zip(['neuroticism', 'openness', 'conscientiousness', 'extraversion', 'agreeableness'],
                                   traits)},
        'shoot': lambda self: print('Shooting'),
        'search': lambda self: print('Searching'),
        'talk': lambda self: print('Talking')})()
