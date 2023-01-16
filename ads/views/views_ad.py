import json

from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Ad, User, Category
from levito import settings


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by("-price").select_related("author")

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse(
            {"total": page_obj.paginator.count,
             "num_pages": page_obj.paginator.num_pages,
             "items": [
                 {"id": ad.id,
                  "name": ad.name,
                  "author_id": ad.author_id,
                  "author": ad.author.first_name,
                  "price": ad.price,
                  "description": ad.description,
                  "is_published": ad.is_published,
                  "category_id": ad.category_id,
                  "images": ad.image.url if ad.image else None
                  } for ad in page_obj]}, safe=False, json_dumps_params={"ensure_ascii": False})


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        ad = self.get_object()

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.first_name,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "images": ad.image.url if ad.image else None}, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        ad_data = json.loads(request.body)

        author = get_object_or_404(User, username=ad_data["username"])
        category = get_object_or_404(Category, name=ad_data["category"])

        ad = Ad.objects.create(
            name=ad_data["name"],
            # author_id=ad_data["author_id"],
            author=author,
            price=ad_data["price"],
            description=ad_data["description"],
            is_published=ad_data["is_published"],
            # category_id=ad_data["category_id"],
            category=category
        )

        return JsonResponse({
            "id": ad.id,
            "name": ad.name,
            "author_id": ad.author_id,
            "author": ad.author.username,
            "price": ad.price,
            "description": ad.description,
            "is_published": ad.is_published,
            "category_id": ad.category_id,
            "category": ad.category.name,
            "images": ad.image.url if ad.image else None}, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = "__all__"

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.author = get_object_or_404(User, username=ad_data["username"])
        self.object.category = get_object_or_404(Category, name=ad_data["category"])
        self.object.name = ad_data["name"]
        # self.object.author_id = int(ad_data["author_id"])
        self.object.price = int(ad_data["price"])
        self.object.description = ad_data["description"]
        self.object.is_published = ad_data["is_published"]
        # self.object.category_id = int(ad_data["category_id"])

        self.object.save()
        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": self.object.author.username,
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published,
            "category": self.object.category.name
        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUploadView(UpdateView):
    model = Ad
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse({"name": self.object.name, "image": self.object.image.url})
