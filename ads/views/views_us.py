import json

from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Ad, User, Category, Location
from levito import settings


class UserListView(ListView):
    model = User
    queryset = User.objects.annotate(total_ads=Count("ad", filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse(
            [{"id": user.pk,
              "first_name": user.first_name,
              "last_name": user.last_name,
              "username": user.username,
              "role": user.role,
              "age": user.age,
              "total_ads": user.total_ads,
              "location": [loc.name for loc in user.location.all()]
               } for user in self.object_list], safe=False, json_dumps_params={"ensure_ascii": False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()]}, safe=False, json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            username=user_data.get("username"),
            password=user_data.get("password"),
            role=user_data.get("role"),
            age=user_data.get("age"),
            )
        locations = user_data.get("location")
        if locations:
            for location in locations:
                loc, created = Location.objects.get_or_create(name=location)
                user.location.add(loc)

        return JsonResponse({
            "id": user.pk,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "username": user.username,
            "role": user.role,
            "age": user.age,
            "location": [loc.name for loc in user.location.all()]}, safe=False,
            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = "__all__"

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        if user_data.get("first_name"):
            self.object.first_name = user_data.get("first_name")
        if user_data.get("last_name"):
            self.object.last_name = user_data.get("last_name")
        if user_data.get("username"):
            self.object.username = user_data.get("username")
        if user_data.get("age"):
            self.object.age = user_data.get("age")

        locations = user_data.get("location")
        if locations:
            self.object.location.all().delete()
            for location in locations:
                loc, created = Location.objects.get_or_create(name=location)
                self.object.location.add(loc)

        self.object.save()
        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "location": [loc.name for loc in self.object.location.all()]}, safe=False,
            json_dumps_params={"ensure_ascii": False})

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.first_name = user_data.get("first_name")
        self.object.last_name = user_data.get("last_name")
        self.object.username = user_data.get("username")
        self.object.password = user_data.get("password")
        self.object.age = user_data.get("age")

        locations = user_data.get("location")
        if locations:
            self.object.location.all().delete()
            for location in locations:
                loc, created = Location.objects.get_or_create(name=location)
                self.object.location.add(loc)

        self.object.save()
        return JsonResponse({
            "id": self.object.pk,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "username": self.object.username,
            "role": self.object.role,
            "age": self.object.age,
            "location": [loc.name for loc in self.object.location.all()]}, safe=False,
            json_dumps_params={"ensure_ascii": False})


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)
