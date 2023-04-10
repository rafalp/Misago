import React from "react"
import ajax from "../../services/ajax"

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

    ajax.get(url).then(
      (data) => {
        if (url === this.props.url) {
          this.setState({ loading: false, data })
        }
      },
      (rejection) => {
        if (url === this.props.url) {
          this.setState({ loading: false, error: rejection })
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
