import htmx from "htmx.org"

const DEBOUNCE = 1000

const cache = {}

export function registerElementValidator(element) {
  const active = element.getAttribute("misago-validate-active")
  if (active) {
    return
  }

  const url = element.getAttribute("misago-validate")
  const user = element.getAttribute("misago-validate-user")
  const strip =
    element.getAttribute("misago-validate-strip") == "false" ? false : true
  const input = element.querySelector("input")
  const csrf = input.closest("form").querySelector("input[type=hidden]")

  if (!url || !input) {
    return
  }

  if (!cache[url]) {
    cache[url] = {}
  }

  element.setAttribute("misago-validate-active", "true")

  let timeout = null

  input.addEventListener("keyup", (event) => {
    let value = event.target.value
    if (strip) {
      value = value.trim()
    }

    if (value.trim().length === 0) {
      clearFormControlValidationState(element)
      return
    }

    if (cache[url][value]) {
      setFormControlValidationState(element, input, cache[url][value])
    } else {
      if (timeout) {
        window.clearTimeout(timeout)
      }

      timeout = window.setTimeout(async () => {
        const { errors } = await callValidationUrl(url, csrf, value, user)
        cache[url][value] = errors
        setFormControlValidationState(element, input, errors)
      }, DEBOUNCE)
    }
  })
}

function setFormControlValidationState(element, input, errors) {
  if (errors.length) {
    setFormControlErrorValidationState(element, input, errors)
  } else {
    setFormControlSuccessValidationState(element)
  }
}

function setFormControlErrorValidationState(element, input, errors) {
  element.classList.remove("has-success")
  element.classList.add("has-error")

  clearFormControlValidationMessages(element)

  errors.forEach((error) => {
    const message = document.createElement("p")
    message.className = "help-block"
    message.setAttribute("misago-dynamic-message", "true")
    message.innerText = error
    input.after(message)
  })
}

function setFormControlSuccessValidationState(element) {
  element.classList.remove("has-error")
  element.classList.add("has-success")

  clearFormControlValidationMessages(element)
}

function clearFormControlValidationState(element) {
  element.classList.remove("has-error")
  element.classList.remove("has-success")

  clearFormControlValidationMessages(element)
}

function clearFormControlValidationMessages(element) {
  element
    .querySelectorAll("[misago-dynamic-message]")
    .forEach((i) => i.remove())
}

async function callValidationUrl(url, csrf, value, user) {
  const data = new FormData()
  data.set(csrf.name, csrf.value)
  data.set("value", value)
  if (user) {
    data.set("user", user)
  }

  const response = await fetch(url, {
    method: "POST",
    mode: "cors",
    credentials: "same-origin",
    body: data,
  })
  return await response.json()
}

export function registerValidators(element) {
  const target = element || document
  target.querySelectorAll("[misago-validate]").forEach(registerElementValidator)
}

htmx.onLoad(registerValidators)
