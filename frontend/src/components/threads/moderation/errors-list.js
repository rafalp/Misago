import React from 'react';

export default class extends React.Component {
  render() {
    /* jshint ignore:start */
    return (
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              aria-label={gettext("Close")}
              className="close"
              data-dismiss="modal"
              type="button"
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">{gettext("Threads moderation")}</h4>
          </div>
          <div className="modal-body">

            <p className="lead">
              {gettext("One or more threads could not be deleted:")}
            </p>

            <ul className="list-unstyled list-errored-items">
              {this.props.errors.map((item) => {
                return (
                  <ThreadErrors
                    errors={item.errors}
                    key={item.thread.id}
                    thread={item.thread}
                  />
                );
              })}
            </ul>

          </div>
        </div>
      </div>
    );
    /* jshint ignore:end */
  }
}

/* jshint ignore:start */
export function ThreadErrors({ errors, thread }) {
  return (
    <li>
      <h5>{thread.title}</h5>
      {errors.map((message, i) => {
        return (
          <p>{message}</p>
        );
      })}
    </li>
  );
}
/* jshint ignore:end */