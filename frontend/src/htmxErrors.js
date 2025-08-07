import { error, httpResponseError } from "./snackbars"

function handleResponseError(event) {
  if (isEventVisible(event)) {
    httpResponseError(event.detail.xhr)
  }
}

function handleSendError(event) {
  if (isEventVisible(event)) {
    const message = pgettext("htmx response error", "Site could not be reached")
    error(message)
  }
}

function handleTimeoutError(event) {
  if (isEventVisible(event)) {
    const message = pgettext(
      "htmx response error",
      "Site took too long to reply"
    )
    error(message)
  }
}

function isEventVisible({ detail }) {
  const silent = getEventTargetSilentAttr(detail.target)
  return !(silent === "true" && detail.requestConfig.verb === "get")
}

function getEventTargetSilentAttr(target) {
  const element = target.closest("[hx-silent]")
  if (element) {
    return element.getAttribute("hx-silent")
  }
  return null
}

export function setupHtmxErrors() {
  document.addEventListener("htmx:responseError", handleResponseError)
  document.addEventListener("htmx:sendError", handleSendError)
  document.addEventListener("htmx:timeout", handleTimeoutError)
}

setupHtmxErrors()
