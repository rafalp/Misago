import misago from "misago/index"
import RequestActivationLink from "misago/components/request-activation-link"
import mount from "misago/utils/mount-component"

export default function initializer() {
  if (document.getElementById("request-activation-link-mount")) {
    mount(RequestActivationLink, "request-activation-link-mount", false)
  }
}

misago.addInitializer({
  name: "component:request-activation-link",
  initializer: initializer,
  after: "store",
})
