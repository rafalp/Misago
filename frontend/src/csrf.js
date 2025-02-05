export const CSRF_FIELD_NAME = "csrfmiddlewaretoken"

export function getCSRFToken() {
  const element = document.querySelector(
    'input[name="' + CSRF_FIELD_NAME + '"]'
  )

  if (element) {
    return element.value
  }

  return null
}

export function appendCSRFTokenToForm(form) {
  form.append(CSRF_FIELD_NAME, getCSRFToken())
}
