import React from "react"
import Blankslate from "./blankslate"
import Loader from "./loader"
import Form from "./form"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      loading: true,
      groups: null,
    }
  }

  componentDidMount() {
    ajax.get(this.props.api).then(
      (groups) => {
        this.setState({
          loading: false,

          groups,
        })
      },
      (rejection) => {
        snackbar.apiError(rejection)
        if (this.props.cancel) {
          this.props.cancel()
        }
      }
    )
  }

  render() {
    const { groups, loading } = this.state

    return (
      <div className="panel panel-default panel-form">
        <div className="panel-heading">
          <h3 className="panel-title">
            {pgettext("user profile details form title", "Edit details")}
          </h3>
        </div>
        <Loader display={loading} />
        <Blankslate display={!loading && !groups.length} />
        <FormDisplay
          api={this.props.api}
          display={!loading && groups.length}
          groups={groups}
          onCancel={this.props.onCancel}
          onSuccess={this.props.onSuccess}
        />
      </div>
    )
  }
}

export function FormDisplay({ api, display, groups, onCancel, onSuccess }) {
  if (!display) return null

  return (
    <Form api={api} groups={groups} onCancel={onCancel} onSuccess={onSuccess} />
  )
}
