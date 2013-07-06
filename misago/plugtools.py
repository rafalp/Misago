from django.template.loader import render_to_string as django_render_to_string

def render_to_string(template_name, dictionary=None, context_instance=None):
    from misago.template.theme import prefix_templates
    template_name = prefix_templates(template_name)
    return django_render_to_string(template_name,
                                   dictionary,
                                   context_instance=context_instance)
