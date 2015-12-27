import React from 'react';
import snackbar from 'misago/services/snackbar';

export default class SignInModal extends React.Component {
  info() {
    snackbar.info('Lorem ipsum dolor met');
  }

  success() {
    snackbar.success('Lorem ipsum dolor met');
  }

  warning() {
    snackbar.warning('Lorem ipsum dolor met');
  }

  error() {
    snackbar.error('Lorem ipsum dolor met');
  }

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
          <button type="button"
                  className="btn btn-primary"
                  onClick={this.info}>
            Test info alert
          </button>

          <br />

          <button type="button"
                  className="btn btn-success"
                  onClick={this.success}>
            Test success alert
          </button>

          <br />

          <button type="button"
                  className="btn btn-warning"
                  onClick={this.warning}>
            Test warning alert
          </button>

          <br />

          <button type="button"
                  className="btn btn-danger"
                  onClick={this.error}>
            Test error alert
          </button>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}
