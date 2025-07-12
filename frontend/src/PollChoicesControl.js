import htmx from "htmx.org"

function activatePollChoicesControl(element) {
  element.setAttribute("misago-poll-choices-control", "true")

  const maxChoices = Number(element.getAttribute("max-choices") || 0)

  element.addEventListener("keyup", function (event) {
    const input = event.target.closest("input")
    const choices = element.querySelectorAll("li").length

    if (input && input.value.trim() && (!maxChoices || choices < maxChoices)) {
      const listItem = event.target.closest("li")
      if (!listItem.nextElementSibling) {
        const newListItem = listItem.cloneNode(true)
        const newInput = newListItem.querySelector("input")

        newInput.value = ""
        newInput.name = cleanInputName(input.name)

        listItem.after(newListItem)
      }
    }
  })
}

function cleanInputName(name) {
  return name.substring(0, name.indexOf("[")) + "[]"
}

export default activatePollChoicesControl

htmx.onLoad(function () {
  document
    .querySelectorAll("[misago-poll-choices-control]")
    .forEach(function (element) {
      if (!element.getAttribute("misago-poll-choices-control")) {
        activatePollChoicesControl(element)
      }
    })
})
