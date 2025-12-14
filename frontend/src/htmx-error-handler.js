import { getClosestAttribute } from "./closest-attribute"
import { mountTemplate } from "./template"
import * as toast from "./snackbars"

function createErrorHandler(getErrorMessage) {
  async function handler(event) {
    const error = await getErrorMessage(event)
    const config = getClosestAttribute(event.target, "mg-error")

    if (!config || config === "true") {
      toast.error(error.message)
    } else if (config !== "false" && event.detail && event.detail.target) {
      const template = document.querySelector(config)
      if (!template) {
        console.error(
          "Could not resolve the '" +
            config +
            "' element specified in the 'mg-error' attribute."
        )
        return
      }

      if (template) {
        mountTemplate(event.detail.target, template, error)
      }
    }
  }

  return handler
}

async function getResponseError(event) {
  const response = event.detail.xhr

  let status = response.status

  if (
    typeof response.getResponseHeader !== "undefined" &&
    response.getResponseHeader("content-type") === "application/json"
  ) {
    const data = JSON.parse(response.response)
    if (data.error) {
      return { status, error: data.error }
    }
  } else if (response.headers.get("content-type") === "application/json") {
    const data = await response.json()
    if (data.error) {
      return { status, error: data.error }
    }
  }

  return {
    status,
    error: getDefaultErrorForStatus(status),
  }
}

function getDefaultErrorForStatus(status) {
  if (status === 404) {
    return pgettext("htmx response error", "Page not found")
  }

  if (status === 403) {
    return pgettext("htmx response error", "Permission denied")
  }

  if (status === 0) {
    return pgettext("htmx response error", "Site could not be reached")
  }

  return pgettext("htmx response error", "Unexpected error")
}

function getSendError() {
  return {
    status: 0,
    error: pgettext("htmx response error", "Site could not be reached"),
  }
}

function getTimeoutError() {
  return {
    status: 408,
    error: pgettext("htmx response error", "Site took too long to respond"),
  }
}

export { createErrorHandler, getResponseError, getSendError, getTimeoutError }

document.addEventListener(
  "htmx:responseError",
  createErrorHandler(getResponseError)
)
document.addEventListener("htmx:sendError", createErrorHandler(getSendError))
document.addEventListener("htmx:timeout", createErrorHandler(getTimeoutError))
