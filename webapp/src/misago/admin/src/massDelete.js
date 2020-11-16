const initMassDelete = confirmation => {
  const tables = document.querySelectorAll(".card-admin-table")
  tables.forEach(table => initTableMassDelete(table, confirmation))
}

const initTableMassDelete = (table, confirmation) => {
  const form = table.querySelector("form")
  if (form === null) return

  const submit = form.querySelector("button")
  const toggle = table.querySelector("th input[type=checkbox]")
  const checkbox = table.querySelectorAll("td input[type=checkbox]")

  const updateState = () => {
    const checked = table.querySelectorAll("td input:checked")
    toggle.checked = checkbox.length === checked.length
    submit.disabled = checked.length === 0
  }

  updateState()

  toggle.addEventListener("change", event => {
    checkbox.forEach(element => (element.checked = event.target.checked))
    updateState()
  })

  checkbox.forEach(element => {
    element.addEventListener("change", updateState)
  })

  form.addEventListener("submit", event => {
    const checked = table.querySelectorAll("td input:checked")
    if (checked.length === 0 || !window.confirm(confirmation)) {
      event.preventDefault()
      return false
    }
  })
}

export default initMassDelete
