from path import path
from PIL import Image
from zipfile import is_zipfile
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from misago import messages
from misago.apps.errors import error404
from misago.conf import settings
from misago.decorators import block_guest
from misago.messages import Message
from misago.shortcuts import render_to_response
from misago.utils.strings import random_string
from misago.utils.avatars import resizeimage
from misago.apps.usercp.template import RequestContext
from misago.apps.usercp.avatar.forms import UploadAvatarForm

def avatar_view(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if request.user.avatar_ban:
            return render_to_response('usercp/avatar_banned.html',
                                      context_instance=RequestContext(request, {
                                          'tab': 'avatar'}));
        return f(*args, **kwargs)
    return decorator


@block_guest
@avatar_view
def avatar(request):
    message = request.messages.get_message('usercp_avatar')
    return render_to_response('usercp/avatar.html',
                              context_instance=RequestContext(request, {
                                  'message': message,
                                  'tab': 'avatar'}));


@block_guest
@avatar_view
def gravatar(request):
    if not 'gravatar' in settings.avatars_types:
        return error404(request)
    if request.user.avatar_type != 'gravatar':
        if request.csrf.request_secure(request):
            request.user.delete_avatar()
            request.user.avatar_type = 'gravatar'
            request.user.save(force_update=True)
            messages.success(request, _("Your avatar has been changed to Gravatar."), 'usercp_avatar')
        else:
            messages.error(request, _("Request authorisation is invalid."), 'usercp_avatar')
    return redirect(reverse('usercp_avatar'))


@block_guest
@avatar_view
def gallery(request):
    if not 'gallery' in settings.avatars_types:
        return error404(request)

    allowed_avatars = []
    galleries = []
    for directory in path(settings.STATICFILES_DIRS[0]).joinpath('avatars').dirs():
        if directory[-7:] != '_locked' and directory[-8:] != '_default':
            gallery = {'name': directory[-7:], 'avatars': []}
            avatars = directory.files('*.gif')
            avatars += directory.files('*.jpg')
            avatars += directory.files('*.jpeg')
            avatars += directory.files('*.png')
            for item in avatars:
                gallery['avatars'].append('/'.join(path(item).splitall()[-2:]))
            galleries.append(gallery)
            allowed_avatars += gallery['avatars']

    if not allowed_avatars:
        messages.info(request, _("No avatar galleries are available at the moment."), 'usercp_avatar')
        return redirect(reverse('usercp_avatar'))

    message = request.messages.get_message('usercp_avatar')
    if request.method == 'POST':
        if request.csrf.request_secure(request):
            new_avatar = request.POST.get('avatar_image')
            if new_avatar in allowed_avatars:
                request.user.delete_avatar()
                request.user.avatar_type = 'gallery'
                request.user.avatar_image = new_avatar
                request.user.save(force_update=True)
                messages.success(request, _("Your avatar has been changed to one from gallery."), 'usercp_avatar')
                return redirect(reverse('usercp_avatar'))
            message = Message(_("Selected Avatar is incorrect."), messages.ERROR)
        else:
            message = Message(_("Request authorisation is invalid."), messages.ERROR)

    return render_to_response('usercp/avatar_gallery.html',
                              context_instance=RequestContext(request, {
                                  'message': message,
                                  'galleries': galleries,
                                  'tab': 'avatar'}));


@block_guest
@avatar_view
def upload(request):
    if not 'upload' in settings.avatars_types:
        return error404(request)
    message = request.messages.get_message('usercp_avatar')
    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            request.user.delete_avatar_temp()
            image = form.cleaned_data['avatar_upload']
            image_name, image_extension = path(smart_str(image.name.lower())).splitext()
            image_name = '%s_tmp_%s%s' % (request.user.pk, random_string(8), image_extension)
            image_path = settings.MEDIA_ROOT + 'avatars/' + image_name
            request.user.avatar_temp = image_name

            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            request.user.save()
            try:
                if is_zipfile(image_path):
                    # Composite file upload
                    raise ValidationError()
                image = Image.open(image_path)
                if not image.format in ['GIF', 'PNG', 'JPEG']:
                    raise ValidationError()
                image.seek(0)
                image.save(image_path)
                if request.POST.get('js_check'):
                    return redirect(reverse('usercp_avatar_upload_crop'))
                # Redirect to crop page didnt happen, handle avatar with old school hollywood way
                image_path = settings.MEDIA_ROOT + 'avatars/'
                source = Image.open(image_path + request.user.avatar_temp)
                image_name, image_extension = path(request.user.avatar_temp).splitext()
                image_name = '%s_%s%s' % (request.user.pk, random_string(8), image_extension)
                resizeimage(source, settings.AVATAR_SIZES[0], image_path + image_name, info=source.info, format=source.format)
                for size in settings.AVATAR_SIZES[1:]:
                    resizeimage(source, size, image_path + str(size) + '_' + image_name, info=source.info, format=source.format)
                # Update user model one more time
                request.user.delete_avatar_image()
                request.user.delete_avatar_original()
                request.user.avatar_type = 'upload'
                request.user.avatar_original = '%s_org_%s%s' % (request.user.pk, random_string(8), image_extension)
                source.save(image_path + request.user.avatar_original)
                request.user.delete_avatar_temp()
                request.user.avatar_image = image_name
                request.user.save(force_update=True)
                # Set message and adios!
                messages.success(request, _("Your avatar has changed."), 'usercp_avatar')
                return redirect(reverse('usercp_avatar'))
            except ValidationError:
                request.user.delete_avatar()
                request.user.default_avatar()
                message = Message(_("Only gif, jpeg and png files are allowed for member avatars."), messages.ERROR)
        else:
            message = Message(form.non_field_errors()[0], messages.ERROR)
    else:
        form = UploadAvatarForm(request=request)

    return render_to_response('usercp/avatar_upload.html',
                              context_instance=RequestContext(request, {
                                  'message': message,
                                  'form': form,
                                  'tab': 'avatar'}));


@block_guest
@avatar_view
def crop(request, upload=False):
    if upload and (not request.user.avatar_temp or not 'upload' in settings.avatars_types):
        return error404(request)

    if not upload and request.user.avatar_type != 'upload':
        messages.error(request, _("Crop Avatar option is avaiable only when you use uploaded image as your avatar."), 'usercp_avatar')
        return redirect(reverse('usercp_avatar'))

    message = request.messages.get_message('usercp_avatar')
    if request.method == 'POST':
        if request.csrf.request_secure(request):
            try:
                image_path = settings.MEDIA_ROOT + 'avatars/'
                if upload:
                    source = Image.open(image_path + request.user.avatar_temp)
                else:
                    source = Image.open(image_path + request.user.avatar_original)
                width, height = source.size

                aspect = float(width) / float(request.POST['crop_b'])
                crop_x = int(aspect * float(request.POST['crop_x']))
                crop_y = int(aspect * float(request.POST['crop_y']))
                crop_w = int(aspect * float(request.POST['crop_w']))
                crop = source.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_w))

                if upload:
                    image_name, image_extension = path(request.user.avatar_temp).splitext()
                else:
                    image_name, image_extension = path(request.user.avatar_original).splitext()
                image_name = '%s_%s%s' % (request.user.pk, random_string(8), image_extension)
                resizeimage(crop, settings.AVATAR_SIZES[0], image_path + image_name, info=source.info, format=source.format)
                for size in settings.AVATAR_SIZES[1:]:
                    resizeimage(crop, size, image_path + str(size) + '_' + image_name, info=source.info, format=source.format)

                request.user.delete_avatar_image()
                if upload:
                    request.user.delete_avatar_original()
                    request.user.avatar_type = 'upload'
                    request.user.avatar_original = '%s_org_%s%s' % (request.user.pk, random_string(8), image_extension)
                    source.save(image_path + request.user.avatar_original)
                request.user.delete_avatar_temp()
                request.user.avatar_image = image_name
                request.user.save(force_update=True)
                messages.success(request, _("Your avatar has been cropped."), 'usercp_avatar')
                return redirect(reverse('usercp_avatar'))
            except Exception:
                message = Message(_("Form contains errors."), messages.ERROR)
        else:
            message = Message(_("Request authorisation is invalid."), messages.ERROR)


    return render_to_response('usercp/avatar_crop.html',
                              context_instance=RequestContext(request, {
                                  'message': message,
                                  'after_upload': upload,
                                  'avatar_size': settings.AVATAR_SIZES[0],
                                  'source': 'avatars/%s' % (request.user.avatar_temp if upload else request.user.avatar_original),
                                  'tab': 'avatar'}));
