import htmx from "htmx.org"
import { getClosestAttribute } from "./closest-attribute"

function onEvent(name, event) {
  if (
    name === "htmx:beforeRequest" &&
    event.target &&
    event.detail &&
    event.detail.target
  ) {
    const template = getLoaderTemplate(event.target)
    if (template) {
      event.detail.target.replaceChildren(template.content.cloneNode(true))
    }
  }
}

function getLoaderTemplate(target) {
  const selector = getClosestAttribute(target, "mg-loader")
  if (!selector || selector === "true" || selector === "false") {
    return null
  }

  const template = document.querySelector(selector)
  if (!template) {
    console.warn(
      "Could not resolve the '" +
        selector +
        "' element specified in the 'mg-loader' attribute."
    )
  }

  return template
}

htmx.defineExtension("mg-loader", { onEvent })
