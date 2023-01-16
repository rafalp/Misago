import misago from "misago/index"
import showBannedPage from "misago/utils/banned-page"

export default function initializer(context) {
  if (context.has("BAN_MESSAGE")) {
    showBannedPage(context.get("BAN_MESSAGE"), false)
  }
}

misago.addInitializer({
  name: "component:banmed-page",
  initializer: initializer,
  after: "store",
})
