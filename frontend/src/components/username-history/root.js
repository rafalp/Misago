import React from "react"
import ListEmpty from "misago/components/username-history/list-empty"
import ListReady from "misago/components/username-history/list-ready"
import ListPreview from "misago/components/username-history/list-preview"

export default class extends React.Component {
  render() {
    if (this.props.isLoaded) {
      if (this.props.changes.length) {
        return <ListReady changes={this.props.changes} />
      } else {
        return <ListEmpty emptyMessage={this.props.emptyMessage} />
      }
    } else {
      return <ListPreview />
    }
  }
}
