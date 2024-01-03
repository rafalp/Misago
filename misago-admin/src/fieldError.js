export function setFieldError(input, error) {
  input.classList.add("is-invalid")

  const feedback = document.createElement("div")
  feedback.id = input.id + "_invalid_feedback"
  feedback.classList.add("invalid-feedback")
  feedback.innerText = error

  if (input.parentNode.classList.contains("admin-user-select")) {
    feedback.classList.add("d-block")
    input.parentNode.after(feedback)
  } else {
    input.after(feedback)
  }
}

export function clearFieldError(input) {
  input.classList.remove("is-invalid")
  const feedback = document.getElementById(input.id + "_invalid_feedback")
  if (feedback) {
    feedback.remove()
  }
}

export function hasFieldError(input) {
  return input.classList.contains("invalid-feedback")
}