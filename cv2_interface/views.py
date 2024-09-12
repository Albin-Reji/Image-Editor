from urllib.parse import urljoin

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
    value = 0
    if request.method == 'POST':
        value = request.POST.get('name')
        if value is not None:
            value = float(value)
        else:
            value = 0  # Default rotation value if none provided

        img = get_object_or_404(Images, name=imgname)
        new_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)

        image = Image.open(new_path)
        rotate_image = image.rotate(value, expand=True)

        rotated_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_rotate.png')
        os.makedirs(os.path.dirname(rotated_path), exist_ok=True)
        rotate_image.save(rotated_path)

        rotated_url = os.path.join(settings.MEDIA_URL, f'imageprocessed/{imgname}_rotate.png')

        content = {
            'new_path': img.upload_image.url,
            'rotate_image': rotated_url,
            'imgname': imgname
        }
        return render(request, 'editimg.html', content)
    else:

        return render(request, 'editimg.html', {})

def grayscale(request, imgname):
    img = Images.objects.get(name=imgname)
    new_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)

    image = Image.open(new_path)
    grayscale_img = image.convert('L')

    grayscale_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_grayscale.png')
    os.makedirs(os.path.dirname(grayscale_path), exist_ok=True)
    grayscale_img.save(grayscale_path)

    grayscle_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_grayscale.png')

    content = {
        'new_path': os.path.join(settings.MEDIA_URL, img.upload_image.name),
        'rotate_image': grayscle_url,
        'imgname': imgname

    }
    return render(request, 'editimg_form.html', content)


def blur(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=6
    # Retrieve the image object from the database
        img = Images.objects.get(name=imgname)

        new_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(new_path)
        blur_img = image.filter(ImageFilter.GaussianBlur(float(value)))

        blur_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_blur.png')
        os.makedirs(os.path.dirname(blur_path), exist_ok=True)

        blur_img.save(blur_path)
        blur_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_blur.png')

        content = {
            'new_path': os.path.join(settings.MEDIA_URL, img.upload_image.name),
            'rotate_image': blur_url,
            'imgname': imgname
        }
        return render(request, 'editimg.html', content)
    else:
        return render(request, 'editimg.html', {})


def adjust_contrast(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=3.6
        img = get_object_or_404(Images, name=imgname)
        img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(img_path)

        # Enhance the contrast of the image
        enhancer = ImageEnhance.Contrast(image)
        contrast_img = enhancer.enhance(float(value))
        contrast_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_contrast.png')
        os.makedirs(os.path.dirname(contrast_path), exist_ok=True)

        contrast_img.save(contrast_path)
        contrast_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_contrast.png')
        context = {
            'new_path': img.upload_image.url,
            'rotate_image': contrast_url,
            'imgname': imgname
        }

        # Render editimg.html with the context
        return render(request, 'editimg.html', context)
    else:
        return render(request, 'editimg.html', {})

def brightness(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=2.5
        img = get_object_or_404(Images, name=imgname)
        img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(img_path)
        enhancer = ImageEnhance.Brightness(image)
        brightness_img = enhancer.enhance(float(value))
        brightness_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_brightness.png')
        os.makedirs(os.path.dirname(brightness_path), exist_ok=True)
        brightness_img.save(brightness_path)
        brightness_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_brightness.png')
        context = {
            'new_path': img.upload_image.url,
            'rotate_image': brightness_url,
            'imgname': imgname
        }
        return render(request, 'editimg.html', context)
    else:
        return render(request, 'editimg.html', {})

def saturation(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=2.5
        img = get_object_or_404(Images, name=imgname)
        img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(img_path)
        enhancer = ImageEnhance.Color(image)
        saturated_img = enhancer.enhance(float(value))
        saturated_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_saturated.png')
        os.makedirs(os.path.dirname(saturated_path), exist_ok=True)
        saturated_img.save(saturated_path)
        saturated_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_saturated.png')
        context = {
            'new_path': img.upload_image.url,
            'rotate_image': saturated_url,
            'imgname': imgname
        }
        return render(request, 'editimg.html', context)
    else:
        return render(request, 'editimg.html', {})





def invert(request, imgname):
    img = get_object_or_404(Images, name=imgname)
    img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
    image = Image.open(img_path)

    # Invert the colors of the image
    if image.mode == 'RGBA':
        r, g, b, a = image.split()
        inverted_image = Image.merge('RGBA', (ImageOps.invert(r), ImageOps.invert(g), ImageOps.invert(b), a))
    else:
        inverted_image = ImageOps.invert(image)

    # Save the inverted image
    inverted_dir = os.path.join(settings.MEDIA_ROOT, 'imageprocessed')
    os.makedirs(inverted_dir, exist_ok=True)
    inverted_path = os.path.join(inverted_dir, f'{imgname}_inverted.png')
    inverted_image.save(inverted_path)

    inverted_url = os.path.join(settings.MEDIA_URL, f'imageprocessed/{imgname}_inverted.png')
    context = {
        'new_path': img.upload_image.url,
        'rotate_image': inverted_url,
        'imgname': imgname
    }
    return render(request, 'editimg_form.html', context)


def sharpness(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=1.5
        img = get_object_or_404(Images, name=imgname)
        img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(img_path)

        # Enhance the sharpness of the image
        enhancer = ImageEnhance.Sharpness(image)
        sharp_image = enhancer.enhance(float(value))

        # Save the sharpened image
        sharp_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_sharp.png')
        os.makedirs(os.path.dirname(sharp_path), exist_ok=True)
        sharp_image.save(sharp_path)

        sharp_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_sharp.png')
        context = {
            'new_path': img.upload_image.url,
            'rotate_image': sharp_url,
            'imgname':imgname
        }
        return render(request, 'editimg.html', context)
    else:
        return render(request, 'editimg.html', {})
#    _________________________________
def flipimage(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=2.5
        img = get_object_or_404(Images, name=imgname)
        img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(img_path)
        flip_image = ImageOps.flip(image)

        saturated_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_flipimage.png')
        os.makedirs(os.path.dirname(saturated_path), exist_ok=True)
        flip_image.save(saturated_path)
        saturated_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_flipimage.png')
        context = {
            'new_path': img.upload_image.url,
            'rotate_image': saturated_url,
            'imgname': imgname
        }
        return render(request, 'editimg.html', context)
    else:
        return render(request, 'editimg.html', {})
# _______________________________

def mirrorimage(request, imgname):
    if request.method=="POST":
        value=request.POST.get("name")

        if value is not None:
            value=value
        else:
            value=2.5
        img = get_object_or_404(Images, name=imgname)
        img_path = os.path.join(settings.MEDIA_ROOT, img.upload_image.name)
        image = Image.open(img_path)
        mirrorimage = ImageOps.mirror(image)

        saturated_path = os.path.join(settings.MEDIA_ROOT, 'imageprocessed', f'{imgname}_flipimage.png')
        os.makedirs(os.path.dirname(saturated_path), exist_ok=True)
        mirrorimage.save(saturated_path)
        saturated_url = os.path.join(settings.MEDIA_URL, 'imageprocessed', f'{imgname}_flipimage.png')
        context = {
            'new_path': img.upload_image.url,
            'rotate_image': saturated_url,
            'imgname': imgname
        }
        return render(request, 'editimg.html', context)
    else:
        return render(request, 'editimg.html', {})
#     ___________________________________
def recent_activity(request):
    folder_path = 'D:/cvDjango/ComputerVision_Django/media/imageprocessed'
    # Get a list of files in the folder
    files = os.listdir(folder_path)

    context={
        'fileList':files,
    }
    return render(request, 'activity.html', context)