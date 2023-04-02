import * as React from "react"
import misago from "misago"
import SocialAuth from "../../components/social-auth"
import createRoot from "../../utils/createRoot"
import renderComponent from "../../utils/renderComponent"

export default function initializer(context) {
  if (context.get("CURRENT_LINK") === "misago:social-complete") {
    const props = context.get("SOCIAL_AUTH_FORM")
    const root = createRoot("page-mount")
    if (root) {
      renderComponent(<SocialAuth {...props} />, root)
    }
  }
}

misago.addInitializer({
  name: "component:social-auth",
  initializer: initializer,
  after: "store",
})
