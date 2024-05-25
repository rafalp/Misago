import { error } from "./snackbars"

function handleResponseError({ detail }) {
  const message = getResponseErrorMessage(detail.xhr)
  error(message)
}

function getResponseErrorMessage(xhr) {
  if (xhr.getResponseHeader('content-type') === "application/json") {
    const data = JSON.parse(xhr.response)
    if (data.error) {
      return data.error
    }
  }

  if (xhr.status === 404) {
    return pgettext("htmx response error", "Not found")
  }

  if (xhr.status === 403) {
    return pgettext("htmx response error", "Permission denied")
  }

  return pgettext("htmx response error", "Unexpected error")
}

function handleSendError() {
  const message = pgettext("htmx response error", "Site could not be reached")
  error(message)
}

function handleTimeoutError() {
  const message = pgettext("htmx response error", "Site took too long to reply")
  error(message)
}

export function setupHtmxErrors() {
  document.addEventListener("htmx:responseError", handleResponseError)
  document.addEventListener("htmx:sendError", handleSendError)
  document.addEventListener("htmx:timeout", handleTimeoutError)
}