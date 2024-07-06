import cv2
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .imageform import ImageForm
from .models import Images
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
from django.conf import settings
import os


def main(request):
    content = {}
    return render(request, 'main.html', content)
def homepage(request):
    images = Images.objects.all()
    content = {
        'images': images,
    }
    return render(request, 'homepage.html', content)


def successpage(request):
    return render(request, 'image.html', {})

def feature(request):
    return render(request, 'feature.html', {})

def about(request):
    return render(request, 'about.html', {})

def uploadimg(request):
    form = ImageForm()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/successpage/')

    content = {
        'form': form,
    }
    return render(request, 'interface.html', content)


def imageView(request, imgname):
    img = Images.objects.get(name=imgname)
    new_path = os.path.join(settings.MEDIA_URL, img.upload_image.name)
    content = {
        'new_path': new_path,
    }
    return render(request, 'viewimg.html', content)

def editlist(request, imgpath):
    content={
        'imgpath':imgpath,
    }
    return render(request, 'editlist.html', content)
def rotate(request, imgname):

    img = Images.objects.get(name=imgname)
    new_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)

    image = Image.open(new_path)
    rotate_image = image.rotate(90)

    rotated_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}.png')
    os.makedirs(os.path.dirname(rotated_path), exist_ok=True)
    rotate_image.save(rotated_path)

    rotated_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}.png')

    content = {
        'new_path': os.path.join(settings.MEDIA_URL, img.upload_image.name),
        'rotate_image': rotated_url,
    }
    return render(request, 'editimg.html', content)

def grayscale(request, imgname):
    img = Images.objects.get(name=imgname)
    new_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)

    image = Image.open(new_path)
    grayscale_img = image.convert('L')

    grayscale_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}.png')
    os.makedirs(os.path.dirname(grayscale_path), exist_ok=True)
    grayscale_img.save(grayscale_path)

    grayscle_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}.png')

    content = {
        'new_path': os.path.join(settings.MEDIA_URL, img.upload_image.name),
        'rotate_image': grayscle_url,

    }
    return render(request, 'editimg.html', content)


def blur(request, imgname):
    # Retrieve the image object from the database
    img = Images.objects.get(name=imgname)

    new_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(new_path)
    blur_img = image.filter(ImageFilter.GaussianBlur(6))

    blur_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}.png')
    os.makedirs(os.path.dirname(blur_path), exist_ok=True)

    blur_img.save(blur_path)
    blur_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}.png')

    content = {
        'new_path': os.path.join(settings.MEDIA_URL, img.upload_image.name),
        'rotate_image': blur_url,
    }
    return render(request, 'editimg.html', content)


def adjust_contrast(request, imgname):

    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path)

    # Enhance the contrast of the image
    enhancer = ImageEnhance.Contrast(image)
    contrast_img = enhancer.enhance(3.5)
    contrast_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_contrast.png')
    os.makedirs(os.path.dirname(contrast_path), exist_ok=True)

    contrast_img.save(contrast_path)
    contrast_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_contrast.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': contrast_url,
    }

    # Render editimg.html with the context
    return render(request, 'editimg.html', context)

def brightness(request, imgname, factor=2.5):
    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path)
    enhancer = ImageEnhance.Brightness(image)
    brightness_img = enhancer.enhance(factor)
    brightness_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_brightness.png')
    os.makedirs(os.path.dirname(brightness_path), exist_ok=True)
    brightness_img.save(brightness_path)
    brightness_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_brightness.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': brightness_url,
    }
    return render(request, 'editimg.html', context)

def saturation(request, imgname, factor=2.5):
    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path)
    enhancer = ImageEnhance.Color(image)
    saturated_img = enhancer.enhance(factor)
    saturated_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_saturated.png')
    os.makedirs(os.path.dirname(saturated_path), exist_ok=True)
    saturated_img.save(saturated_path)
    saturated_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_saturated.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': saturated_url,
    }
    return render(request, 'editimg.html', context)


def opacity(request, imgname, opacity=0.5):
    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path).convert("RGBA")

    # Create an alpha layer with the specified opacity
    alpha = image.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)

    # Add the new alpha layer to the image
    image.putalpha(alpha)

    # Save the modified image
    opacity_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_opacity.png')
    os.makedirs(os.path.dirname(opacity_path), exist_ok=True)
    image.save(opacity_path)

    opacity_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_opacity.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': opacity_url,
    }
    return render(request, 'editimg.html', context)


def invert (request, imgname):
    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path)

    # Invert the colors of the image
    inverted_image = ImageOps.invert(image)

    # Save the inverted image
    inverted_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_inverted.png')
    os.makedirs(os.path.dirname(inverted_path), exist_ok=True)
    inverted_image.save(inverted_path)

    inverted_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_inverted.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': inverted_url,
    }
    return render(request, 'editimg.html', context)


def sharpness(request, imgname, factor=60):
    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path)

    # Enhance the sharpness of the image
    enhancer = ImageEnhance.Sharpness(image)
    sharp_image = enhancer.enhance(factor)

    # Save the sharpened image
    sharp_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_sharp.png')
    os.makedirs(os.path.dirname(sharp_path), exist_ok=True)
    sharp_image.save(sharp_path)

    sharp_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_sharp.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': sharp_url,
    }
    return render(request, 'editimg.html', context)

def recent_activity(request):
    folder_path = 'D:/cvDjango/ComputerVision_Django/media/imageprocessed'
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    context={
        'fileList':files,
    }
    return render(request, 'activity.html', context)