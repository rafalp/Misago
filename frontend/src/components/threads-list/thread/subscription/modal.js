import React from 'react';
import Options from 'misago/components/threads-list/thread/subscription/options'; // jshint ignore:line

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog modal-sm"
                role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Change subscription")}</h4>
        </div>

        <Options className="modal-menu" thread={this.props.thread}/>

      </div>
    </div>;
    /* jshint ignore:end */
  }
}