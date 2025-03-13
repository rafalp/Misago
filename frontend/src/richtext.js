import htmx from "htmx.org"
import * as snackbars from "./snackbars"

export function activateRichText() {
  document
    .querySelectorAll("[misago-rich-text-code] button")
    .forEach((element) => {
      element.addEventListener("click", copyCode)
    })
}

async function copyCode(event) {
  const element = event.target.closest("[misago-rich-text-code]")
  if (!!element) {
    event.preventDefault()
    const code = element.querySelector("code").textContent
    if (code.trim()) {
      await navigator.clipboard.writeText(code)
      snackbars.info(pgettext("code copied", "Code copied"))
    }
  }
}

htmx.onLoad(activateRichText)
