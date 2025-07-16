import htmx from "htmx.org"

function activatePollChoicesControl(element) {
  element.setAttribute("poll-choices-control", "true")

  const maxChoices = Number(element.getAttribute("max-choices") || 0)

  element.addEventListener("keyup", function (event) {
    const input = event.target.closest("input")
    const newChoices = element.querySelectorAll("[poll-new-choice]").length

    if (input && input.value.trim() && (!maxChoices || newChoices < maxChoices)) {
      const listItem = event.target.closest("li")
      if (!listItem.nextElementSibling) {
        const newListItem = listItem.cloneNode(true)
        const newInput = newListItem.querySelector("input")

        newInput.value = ""
        newInput.name = input.name

        listItem.after(newListItem)
      }
    }
  })
}

export default activatePollChoicesControl

htmx.onLoad(function () {
  document
    .querySelectorAll("[poll-choices-control]")
    .forEach(function (element) {
      if (!element.getAttribute("poll-choices-control")) {
        activatePollChoicesControl(element)
      }
    })
})
