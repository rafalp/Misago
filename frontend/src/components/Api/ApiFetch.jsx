import React from "react"

export default class ApiFetch extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      data: null,
      loading: false,
      error: null,
    }

    this.controller = new AbortController()
    this.signal = this.controller.signal
  }

  componentDidMount() {
    if (this.props.url && !this.props.disabled) {
      this.request(this.props.url)
    }
  }

  componentDidUpdate(prevProps) {
    const url = this.props.url
    const urlChanged = url && url !== prevProps.url
    const disabledChanged = this.props.disabled != prevProps.disabled

    if (urlChanged || disabledChanged) {
      if (!this.props.disabled) {
        if (this.hasCache(url)) {
          this.getCache(url)
        } else {
          this.controller.abort()

          this.controller = new AbortController()
          this.signal = this.controller.signal
          this.request(url)
        }
      } else {
        this.controller.abort()
      }
    }
  }

  componentWillUnmount() {
    this.controller.abort()
  }

  hasCache = (url) => {
    return this.props.cache && this.props.cache[url]
  }

  getCache = async (url) => {
    const data = this.props.cache[url]
    this.setState({ loading: false, error: null, data })
    if (this.props.onData) {
      await this.props.onData(data)
    }
  }

  setCache = (url, data) => {
    if (this.props.cache) {
      this.props.cache[url] = data
    }
  }

  request = (url) => {
    this.setState({ loading: true })

    fetch(url, {
      method: "GET",
      credentials: "include",
      signal: this.signal,
    }).then(
      async (response) => {
        if (url === this.props.url) {
          if (response.status == 200) {
            const data = await response.json()
            this.setState({ loading: false, error: null, data })
            this.setCache(url, data)
            if (this.props.onData) {
              await this.props.onData(data)
            }
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
