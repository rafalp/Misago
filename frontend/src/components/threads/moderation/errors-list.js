import React from 'react';

/* jshint ignore:start */
export function ThreadErrors(props) {
  return <li>
    <h5>{props.thread.title}</h5>
    <ul className="list-unstyled list-item-errors">
      {props.errors.map((item, i) => {
        return <li key={i}>{item}</li>
      })}
    </ul>
  </li>;
}
/* jshint ignore:end */

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog"
                role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal"
                  aria-label={gettext("Close")}>
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{gettext("Threads moderation")}</h4>
        </div>
        <div className="modal-body">

          <p className="lead">
            {gettext("Errors were encountered when performing moderation action on one or more threads:")}
          </p>

          <ul className="list-unstyled list-errored-items">
            {this.props.errors.map((item) => {
              return <ThreadErrors
                errors={item.errors}
                key={item.thread.id}
                thread={item.thread}
              />;
            })}
          </ul>

        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}