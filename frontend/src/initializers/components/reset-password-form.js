import misago from "misago"
import ResetPasswordForm from "misago/components/reset-password-form"
import mount from "misago/utils/mount-component"

export default function initializer() {
  if (document.getElementById("reset-password-form-mount")) {
    mount(ResetPasswordForm, "reset-password-form-mount", false)
  }
}

misago.addInitializer({
  name: "component:reset-password-form",
  initializer: initializer,
  after: "store",
})
