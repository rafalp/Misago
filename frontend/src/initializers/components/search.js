import paths from "misago/components/search-route"
import misago from "misago"
import mount from "misago/utils/routed-component"

export default function initializer(context) {
  if (context.get("CURRENT_LINK") === "misago:search") {
    mount({
      paths: paths(misago.get("SEARCH_PROVIDERS")),
    })
  }
}

misago.addInitializer({
  name: "component:search",
  initializer: initializer,
  after: "store",
})
