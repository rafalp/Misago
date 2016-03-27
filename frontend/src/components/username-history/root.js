import React from 'react';
import ListEmpty from 'misago/components/username-history/list-empty'; // jshint ignore:line
import ListReady from 'misago/components/username-history/list-ready'; // jshint ignore:line
import ListPreview from 'misago/components/username-history/list-preview'; // jshint ignore:line

export default class extends React.Component {
  render() {
    if (this.props.isLoaded) {
      if (this.props.changes.length) {
        /* jshint ignore:start */
        return <ListReady changes={this.props.changes} />;
        /* jshint ignore:end */
      } else {
        /* jshint ignore:start */
        return <ListEmpty emptyMessage={this.props.emptyMessage} />;
        /* jshint ignore:end */
      }
    } else {
      /* jshint ignore:start */
      return <ListPreview />;
      /* jshint ignore:end */
    }
  }
}