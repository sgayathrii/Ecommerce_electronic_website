from .models import Category

def catgories(request):
    return {
        "categories": Category.objects.all()
    }