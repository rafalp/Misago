import htmx from "htmx.org"

class QuickSearch {
  constructor(element) {
    this.element = element

    // Search on submit
    this.element.addEventListener("submit", this.search)

    // Search on scope change
    this.element.querySelectorAll('input[name="action"]').forEach((choice) => {
      choice.addEventListener("change", this.search)
    })
  }

  search = (event) => {
    event.preventDefault()

    const data = new FormData(this.element)
    const action = (data.get("action") || "").trim()
    const query = (data.get("query") || "").trim()

    if (action && query) {
      htmx.ajax("get", action, { event, source: this.element })
    }
  }
}

export default QuickSearch
