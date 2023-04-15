import React from "react"

export default class ApiMutation extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      data: null,
      loading: false,
      error: null,
    }
  }

  mutate = (options) => {
    this.setState({ loading: true })

    fetch(this.props.url, {
      method: this.props.method || "POST",
      credentials: "include",
      headers: headers(options),
      body: body(options),
    }).then(
      async (response) => {
        if (response.status == 200) {
          const data = await response.json()
          this.setState({ loading: false, data })
          if (options.onSuccess) {
            await options.onSuccess(data)
          }
        } else if (response.status == 204) {
          this.setState({ loading: false })
          if (options.onSuccess) {
            await options.onSuccess()
          }
        } else {
          const error = { status: response.status }
          if (response.headers.get("Content-Type") === "application/json") {
            error.data = await response.json()
          }
          this.setState({ loading: false, error })
          if (options.onError) {
            await options.onError(error)
          }
        }
      },
      async (rejection) => {
        const error = { status: 0, rejection }
        this.setState({ loading: false, error })
        if (options.onError) {
          await options.onError(error)
        }
      }
    )
  }

  render() {
    return this.props.children(this.mutate, this.state)
  }
}

function headers(options) {
  if (!!options.json) {
    return {
      "Content-Type": "application/json; charset=utf-8",
      "X-CSRFToken": csrfToken(),
    }
  }

  return {
    "X-CSRFToken": csrfToken(),
  }
}

function body(options) {
  if (!!options.json) {
    return JSON.stringify(options.json)
  }

  return undefined
}

function csrfToken() {
  const cookieName = window.misago_csrf

  if (document.cookie.indexOf(cookieName) !== -1) {
    const cookieRegex = new RegExp(cookieName + "=([^;]*)")
    const cookie = document.cookie.match(cookieRegex)[0]
    return cookie ? cookie.split("=")[1] : null
  } else {
    return null
  }
}
