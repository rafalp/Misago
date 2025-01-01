import htmx from "htmx.org"

export function activatePageSelectForms() {
  document.querySelectorAll("[misago-page-form]").forEach((element) => {
    if (element.getAttribute("misago-page-form") === "") {
      activatePageSelectForm(element)
    }
  })
}

export function activatePageSelectForm(form) {
  form.setAttribute("misago-page-form", "true")
  form.addEventListener("submit", (event) => {
    const page = form.getAttribute("misago-page")
    const input = event.target.querySelector("input")
    const value = input.value
    if (value >= input.min && value <= input.max && value != page) {
      let url = form.getAttribute("misago-page-url")
      if (value > 1) {
        url += value + "/"
      }

      window.history.pushState({}, "", url)
      document.getElementById("misago-page-scroll-target").scrollIntoView()

      htmx.ajax("GET", url, {
        target: "#misago-htmx-root",
        swap: "outerHTML",
      })
    }

    const toggle = form.closest(".dropdown").querySelector("[data-toggle]")
    if (toggle) {
      $().dropdown("toggle")
    }

    event.preventDefault()
    return false
  })
}

htmx.onLoad(activatePageSelectForms)
