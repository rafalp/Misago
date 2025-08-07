import htmx from "htmx.org"

const SNACKBAR_TTL = 6

const container = document.getElementById("misago-snackbars")
let timeout = null

export function removeSnackbars() {
  container.replaceChildren()
}

function renderSnackbars() {
  if (timeout) {
    window.clearTimeout(timeout)
  }

  container.querySelectorAll(".snackbar").forEach((element) => {
    element.classList.add("in")
  })

  timeout = window.setTimeout(() => {
    container.querySelectorAll(".snackbar").forEach((element) => {
      element.classList.add("out")
      timeout = window.setTimeout(removeSnackbars, 1000)
    })
  }, SNACKBAR_TTL * 1000)
}

export function snackbar(type, message) {
  removeSnackbars()

  if (timeout) {
    window.clearTimeout(timeout)
  }

  const element = document.createElement("div")
  element.classList.add("snackbar")
  element.classList.add("snackbar-" + type)
  element.innerText = message
  element.role = "alert"
  container.appendChild(element)

  timeout = window.setTimeout(renderSnackbars, 100)
}

export function info(message) {
  snackbar("info", message)
}

export function success(message) {
  snackbar("success", message)
}

export function warning(message) {
  snackbar("warning", message)
}

export function error(message) {
  snackbar("danger", message)
}

export async function httpResponseError(response) {
  snackbar("danger", await getHttpResponseErrorMessage(response))
}

export async function getHttpResponseErrorMessage(response) {
  if (
    typeof response.getResponseHeader !== "undefined" &&
    response.getResponseHeader("content-type") === "application/json"
  ) {
    const data = JSON.parse(response.response)
    if (data.error) {
      return data.error
    }
  } else if (response.headers.get("content-type") === "application/json") {
    const data = await response.json()
    if (data.error) {
      return data.error
    }
  }

  if (response.status === 404) {
    return pgettext("htmx response error", "Page not found")
  }

  if (response.status === 403) {
    return pgettext("htmx response error", "Permission denied")
  }

  if (response.status === 0) {
    return pgettext("htmx response error", "Site could not be reached")
  }

  return pgettext("htmx response error", "Unexpected error")
}

htmx.onLoad(renderSnackbars)
