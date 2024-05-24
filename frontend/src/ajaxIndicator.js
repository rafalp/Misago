const indicator = document.getElementById("misago-ajax-indicator")

let stack = 0
let timeout = null

function updateIndicator(show) {
  if (timeout) {
    window.clearTimeout(timeout)
  }

  if (show) {
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
  stack += 1
  updateIndicator(stack !== 0)
})

document.addEventListener("htmx:afterOnLoad", () => {
  stack -= 1
  updateIndicator(stack !== 0)
})
