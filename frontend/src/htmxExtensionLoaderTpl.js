import htmx from "htmx.org"

const templates = {}

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

function getLoaderTemplate(element) {
  const selector = getClosestAttribute(element, "tpl-loader")
  if (!selector) {
    return null
  }

  if (typeof templates[selector] === "undefined") {
    const template = document.querySelector(selector)
    templates[selector] = template || null
  }

  return templates[selector]
}

function getClosestAttribute(element, attr) {
  const el = element.closest("[" + attr + "]")
  return el ? el.getAttribute(attr) : null
}

htmx.defineExtension("loader-tpl", {
  onEvent,
})
