from path import path
from PIL import Image
from django.conf import settings
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils.translation import ugettext as _
from misago.authn.decorators import block_guest
from misago.forms import FormLayout
from misago.messages import Message
from misago.usercp.template import RequestContext
from misago.usercp.avatar.forms import UploadAvatarForm
from misago.views import error404
from misago.utils import get_random_string

def avatar_view(f):
    def decorator(*args, **kwargs):
        request = args[0]
        if request.user.avatar_ban:
            return request.theme.render_to_response('usercp/avatar_banned.html',
                                                    context_instance=RequestContext(request, {
                                                        'tab': 'avatar',
                                                    }));
        return f(*args, **kwargs)
    return decorator


@block_guest
@avatar_view
def avatar(request):
    message = request.messages.get_message('usercp_avatar')
    return request.theme.render_to_response('usercp/avatar.html',
                                            context_instance=RequestContext(request, {
                                              'message': message,
                                              'tab': 'avatar',
                                             }));


@block_guest
@avatar_view
def gravatar(request):
    if not 'gravatar' in request.settings.avatars_types:
        return error404(request)
    if request.user.avatar_type != 'gravatar':
        if request.csrf.request_secure(request):
            request.user.delete_avatar()
            request.user.avatar_type = 'gravatar'
            request.user.save(force_update=True)
            request.messages.set_flash(Message(_("Your avatar has been changed to Gravatar.")), 'success', 'usercp_avatar')
        else:
            request.messages.set_flash(Message(_("Request authorisation is invalid.")), 'error', 'usercp_avatar')
    return redirect(reverse('usercp_avatar'))


@block_guest
@avatar_view
def gallery(request):
    if not 'gallery' in request.settings.avatars_types:
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
        request.messages.set_flash(Message(_("No avatars are avaiable.")), 'info', 'usercp_avatar')
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
                request.messages.set_flash(Message(_("Your avatar has been changed to one from gallery.")), 'success', 'usercp_avatar')
                return redirect(reverse('usercp_avatar'))
            message = Message(_("Selected Avatar is incorrect."), 'error')
        else:
            message = Message(_("Request authorisation is invalid."), 'error')
    
    return request.theme.render_to_response('usercp/avatar_gallery.html',
                                            context_instance=RequestContext(request, {
                                              'message': message,
                                              'galleries': galleries,
                                              'tab': 'avatar',
                                             }));


@block_guest
@avatar_view
def upload(request):
    if not 'upload' in request.settings.avatars_types:
        return error404(request)
    
    message = request.messages.get_message('usercp_avatar')
    if request.method == 'POST':
        form = UploadAvatarForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            request.user.delete_avatar_temp()
            image = form.cleaned_data['avatar_upload']
            image_name, image_extension = path(image.name.lower()).splitext()
            image_name = '%s_tmp_%s%s' % (request.user.pk, get_random_string(8), image_extension)
            image_path = settings.MEDIA_ROOT + 'avatars/' + image_name
            request.user.avatar_temp = image_name

            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            request.user.save()
            image = Image.open(image_path)
            image.seek(0)
            image.save(image_path)
            
            return redirect(reverse('usercp_avatar_upload_crop'))
        else:
            message = Message(form.non_field_errors()[0], 'error')          
    else:
        form = UploadAvatarForm(request=request)
        
    return request.theme.render_to_response('usercp/avatar_upload.html',
                                            context_instance=RequestContext(request, {
                                              'message': message,
                                              'form': FormLayout(form),
                                              'tab': 'avatar',
                                            }));


@block_guest
@avatar_view
def crop(request, upload=False):
    if upload and (not request.user.avatar_temp or not 'upload' in request.settings.avatars_types):
        return error404(request)
    
    if not upload and request.user.avatar_type != 'upload':
        request.messages.set_flash(Message(_("Crop Avatar option is avaiable only when you use uploaded image as your avatar.")), 'error', 'usercp_avatar')
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
                avatar = source.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_w))
                avatar.thumbnail((125, 125), Image.ANTIALIAS)
                
                if upload:
                    image_name, image_extension = path(request.user.avatar_temp).splitext()
                else:
                    image_name, image_extension = path(request.user.avatar_original).splitext()
                image_name = '%s_%s%s' % (request.user.pk, get_random_string(8), image_extension)
                avatar.save(image_path + image_name)
                
                request.user.delete_avatar_image()
                if upload:
                    request.user.delete_avatar_original()
                    request.user.avatar_type = 'upload'
                    request.user.avatar_original = '%s_org_%s%s' % (request.user.pk, get_random_string(8), image_extension)
                    source.save(image_path + request.user.avatar_original)
                request.user.delete_avatar_temp()
                request.user.avatar_image = image_name
                request.user.save(force_update=True)
                
                request.messages.set_flash(Message(_("Your avatar has been cropped.")), 'success', 'usercp_avatar')
                return redirect(reverse('usercp_avatar'))
            except Exception:
                message = Message(_("Form contains errors."), 'error')
        else:
            message = Message(_("Request authorisation is invalid."), 'error')
    
    
    return request.theme.render_to_response('usercp/avatar_crop.html',
                                            context_instance=RequestContext(request, {
                                              'message': message,
                                              'after_upload': upload,
                                              'source': 'avatars/%s' % (request.user.avatar_temp if upload else request.user.avatar_original),
                                              'tab': 'avatar',
                                            }));