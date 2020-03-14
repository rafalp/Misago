from misago.hooks import graphql_context_hook

print("PLUGIN!", __file__)


@graphql_context_hook.append
async def add_plugin_data_to_graphql_context(action, request):
    context = await action(request)
    context["plugin"] = "YES!"
    return context
