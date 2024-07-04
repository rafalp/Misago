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

htmx.onLoad(renderSnackbars)
