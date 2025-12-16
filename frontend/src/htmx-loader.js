import {
  getClosestAttribute,
  getClosestBoolAttribute,
} from "./closest-attribute"
import loader from "./loader"
import { mountTemplate } from "./template"

function beforeRequest(event) {
  const loader = getClosestAttribute(event.target, "mg-loader")
  if (!loader || loader === "true") {
    loader.show()
  } else if (loader !== "false" && event.detail && event.detail.target) {
    const template = document.querySelector(loader)
    if (!template) {
      console.error(
        "Could not resolve the '" +
          loader +
          "' element specified in the 'mg-loader' attribute."
      )
      return
    }

    if (template) {
      mountTemplate(event.detail.target, template)
    }
  }
}

function afterRequest({ target }) {
  if (getClosestBoolAttribute(target, "mg-loader", true)) {
    loader.hide()
  }
}

document.addEventListener("htmx:beforeRequest", beforeRequest)
document.addEventListener("htmx:afterRequest", afterRequest)
