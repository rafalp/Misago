import {
  getClosestAttribute,
  getClosestBoolAttribute,
} from "./closest-attribute"
import loader from "./loader"
import { mountTemplate } from "./template"

function beforeRequest(event) {
  const config = getClosestAttribute(event.target, "mg-loader")
  if (!config || config === "true") {
    loader.show()
  } else if (config !== "false" && event.detail && event.detail.target) {
    const template = document.querySelector(config)
    if (!template) {
      console.error(
        "Could not resolve the '" +
          config +
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
