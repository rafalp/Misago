const initValidation = () => {
  // js workaround for validation states
  const controls = document.querySelectorAll(".form-group.has-error")
  controls.forEach(control => {
    const inputs = control.querySelectorAll(".form-control")
    inputs.forEach(input => {
      input.classList.add("is-invalid")
    })
  })
}

export default initValidation
