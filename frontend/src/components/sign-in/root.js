import React from 'react';

export default class SignInModal extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 className="modal-title">{gettext("Sign in")}</h4>
        </div>
        <div className="modal-body">
          <p>This will be sign in form!</p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}
