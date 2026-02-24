from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Artwork, Favorite
import os

def index(request):
    artworks = Artwork.objects.all()
    return render(request, "gallery/index.html", {"artworks": artworks})

def add(request):
    if request.method == "POST":
        image = request.FILES.get("image")
        prompt = request.POST.get("prompt", "").strip()
        parameters = request.POST.get("parameters", "").strip()

        if not image or not prompt or not parameters:
            messages.error(request, "图片、Prompt 和 Parameters 都必须填写")
            return redirect("gallery:index")

        # Save image
        fs = FileSystemStorage(location=settings.MEDIA_ROOT / "gallery_images")
        filename = fs.save(image.name, image)
        
        Artwork.objects.create(
            image_path=filename,
            prompt=prompt,
            parameters=parameters
        )
        messages.success(request, "作品添加成功！")
        return redirect("gallery:index")
    
    return redirect("gallery:index")

def view(request, art_id):
    artwork = get_object_or_404(Artwork, id=art_id)
    return render(request, "gallery/view.html", {"artwork": artwork})

def edit(request, art_id):
    artwork = get_object_or_404(Artwork, id=art_id)
    if request.method == "POST":
        prompt = request.POST.get("prompt", "").strip()
        parameters = request.POST.get("parameters", "").strip()
        if prompt and parameters:
            artwork.prompt = prompt
            artwork.parameters = parameters
            artwork.save()
            messages.success(request, "修改成功")
            return redirect("gallery:view", art_id=artwork.id)
        messages.error(request, "内容不能为空")
    
    return render(request, "gallery/edit.html", {"artwork": artwork})

def delete(request, art_id):
    artwork = get_object_or_404(Artwork, id=art_id)
    # Delete file
    fs = FileSystemStorage(location=settings.MEDIA_ROOT / "gallery_images")
    if fs.exists(artwork.image_path):
        fs.delete(artwork.image_path)
    
    artwork.delete()
    messages.success(request, "删除成功")
    return redirect("gallery:index")

@csrf_exempt
def toggle_favorite(request, artwork_id):
    if request.method == "POST":
        try:
            artwork = Artwork.objects.get(id=artwork_id)
        except Artwork.DoesNotExist:
             return JsonResponse({"success": False, "error": "作品不存在"}, status=404)

        fav, created = Favorite.objects.get_or_create(artwork=artwork)
        if not created:
            fav.delete()
            return JsonResponse({"success": True, "action": "removed", "message": "已取消收藏"})
        else:
            return JsonResponse({"success": True, "action": "added", "message": "已添加到收藏"})
            
    return JsonResponse({"success": False, "error": "Invalid method"}, status=405)

def favorites(request):
    favorites = Favorite.objects.select_related('artwork').all()
    # Template expects artworks list
    artworks = [f.artwork for f in favorites]
    return render(request, "gallery/favorites.html", {"artworks": artworks})

def favorite_status(request, artwork_id):
    """API to get status"""
    is_fav = Favorite.objects.filter(artwork_id=artwork_id).exists()
    return JsonResponse({"is_favorited": is_fav})
