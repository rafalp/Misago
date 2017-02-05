import React from 'react';
import Loader from 'misago/components/loader'; // jshint ignore:line
import RegisterModal from 'misago/components/register.js'; // jshint ignore:line
import captcha from 'misago/services/captcha'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      isLoaded: false
    };
  }

  /* jshint ignore:start */
  showRegisterModal = () => {
    if (misago.get('SETTINGS').account_activation === 'closed') {
      snackbar.info(gettext("New registrations are currently disabled."));
    } else if (this.state.isLoaded) {
      modal.show(RegisterModal);
    } else {
      this.setState({ isLoading: true });

      Promise.all([
        captcha.load()
      ]).then(() => {
        this.setState({ isLoading: false });
        modal.show(RegisterModal);
      }, () => {
        this.setState({ isLoading: false });

        snackbar.error(gettext("Registration is currently unavailable due to an error."));
      });
    }
  };
  /* jshint ignore:end */

  getClassName() {
    return this.props.className + (this.state.isLoading ? ' btn-loading' : '');
  }

  render() {
    /* jshint ignore:start */
    return (
      <button
        className={'btn ' + this.getClassName()}
        disabled={this.state.isLoading}
        onClick={this.showRegisterModal}
        type="button"
      >
        {gettext("Register")}
        {this.state.isLoading ? <Loader /> : null }
      </button>
    );
    /* jshint ignore:end */
  }
}
