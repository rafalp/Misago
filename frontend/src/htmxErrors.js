import { error } from "./snackbars"

function handleResponseError(event) {
  if (isEventVisible(event)) {
    const message = getResponseErrorMessage(event.detail.xhr)
    error(message)
  }
}

function getResponseErrorMessage(xhr) {
  if (xhr.getResponseHeader("content-type") === "application/json") {
    const data = JSON.parse(xhr.response)
    if (data.error) {
      return data.error
    }
  }

  if (xhr.status === 404) {
    return pgettext("htmx response error", "Page not found")
  }

  if (xhr.status === 403) {
    return pgettext("htmx response error", "Permission denied")
  }

  return pgettext("htmx response error", "Unexpected error")
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
