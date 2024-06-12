const indicator = document.getElementById("misago-ajax-indicator")

let requests = 0
let timeout = null

function updateIndicator(visible) {
  if (timeout) {
    window.clearTimeout(timeout)
  }

  if (visible) {
    indicator.classList.add("busy")
    indicator.classList.remove("complete")
  } else {
    indicator.classList.remove("busy")
    indicator.classList.add("complete")

    timeout = setTimeout(() => {
      indicator.classList.remove("complete")
    }, 1500)
  }
}

document.addEventListener("htmx:beforeSend", () => {
  requests += 1
  updateIndicator(requests !== 0)
})

document.addEventListener("htmx:afterOnLoad", () => {
  requests -= 1
  updateIndicator(requests !== 0)
})

document.addEventListener("htmx:sendError", () => {
  requests -= 1
  updateIndicator(requests !== 0)
})
