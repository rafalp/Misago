import React from "react"

export default class ApiClientGet extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      data: null,
      loading: false,
      error: null,
    }
  }

  componentDidMount() {
    if (this.props.url && !this.props.disabled) {
      this.request(this.props.url)
    }
  }

  componentDidUpdate(prevProps) {
    const urlDidUpdate = this.props.url && this.props.url !== prevProps.url
    const disabledDidUpdate =
      !this.props.disabled && this.props.disabled != prevProps.disabled

    if (urlDidUpdate || disabledDidUpdate) {
      this.request(this.props.url)
    }
  }

  request = (url) => {
    this.setState({ loading: true })

    fetch(url, {
      method: "GET",
      credentials: "include",
    }).then(
      async (response) => {
        if (url === this.props.url) {
          if (response.status == 200) {
            const data = await response.json()
            this.setState({ loading: false, data })
          } else {
            const error = { status: response.status }
            if (response.headers.get("Content-Type") === "application/json") {
              error.data = await response.json()
            }
            this.setState({ loading: false, error })
          }
        }
      },
      (rejection) => {
        if (url === this.props.url) {
          this.setState({ loading: false, error: { status: 0, rejection } })
        }
      }
    )
  }

  refetch = () => {
    this.request(this.props.url)
  }

  update = (mutation) => {
    this.setState((state) => {
      return { data: mutation(state.data) }
    })
  }

  render() {
    return this.props.children(
      Object.assign({ refetch: this.refetch, update: this.update }, this.state)
    )
  }
}
