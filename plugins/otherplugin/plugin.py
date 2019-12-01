from typing import Optional

from misago.hooks import graphql_context_hook, register_input_hook

print("PLUGIN!", __file__)


@graphql_context_hook.append
async def add_plugin_data_to_graphql_context(action, request, context):
    context = await action(request, context)
    context["plugin"] = "YES!"
    return context


@register_input_hook.append
async def add_plugin_field_to_registration_input(action, context):
    return await action(context)
    
    class NewModel(model):
        captcha: Optional[str]
    
    return NewModel