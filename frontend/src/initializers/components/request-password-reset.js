import misago from "misago/index"
import RequestPasswordReset from "misago/components/request-password-reset"
import mount from "misago/utils/mount-component"

export default function initializer() {
  if (document.getElementById("request-password-reset-mount")) {
    mount(RequestPasswordReset, "request-password-reset-mount", false)
  }
}

misago.addInitializer({
  name: "component:request-password-reset",
  initializer: initializer,
  after: "store",
})
