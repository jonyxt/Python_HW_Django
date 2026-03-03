from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def recipe(request):
    dish = request.GET.get('dish', 'omlet')
    servings = int(request.GET.get('servings', 1))
    recipe_for_servings = {
        key: round(value * servings, 2) for key, value in DATA[dish].items()
    }
    context = {
        'recipe': recipe_for_servings,
    }
    return render(request, 'calculator/index.html', context)

