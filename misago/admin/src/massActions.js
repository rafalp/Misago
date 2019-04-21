import { addEventListenerToAll } from "./utils"

const initMassActions = (emptySelectionLabel, selectionLabel) => {
  const dropdownToggle = document.querySelector("#mass-action .dropdown-toggle")
  const dropdownLabel = dropdownToggle.querySelector("span:last-child")

  const updateDropdownState = () => {
    const checked = document.querySelectorAll(".row-select input:checked")
    dropdownToggle.disabled = checked.length === 0
    if (checked.length) {
      dropdownLabel.textContent = selectionLabel.replace("0", checked.length)
    } else {
      dropdownLabel.textContent = emptySelectionLabel
    }
  }

  updateDropdownState()

  addEventListenerToAll(".row-select input", "change", () => {
    updateDropdownState()
  })

  addEventListenerToAll("#mass-action [data-confirmation]", "click", event => {
    if (!window.confirm(event.target.dataset.confirmation)) {
      event.preventDefault()
      return false
    }
  })
}

export default initMassActions
