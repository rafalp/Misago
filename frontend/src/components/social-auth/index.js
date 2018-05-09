/* jshint ignore:start */
import React from 'react';
import Register from './register';

export default class SocialAuth extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      step: props.step,
      email: props.email || '',
      username: props.username || ''
    };
  }

  handleRegistrationComplete = (step, username, email) => {
    this.setState({
      step,
      email,
      username
    });
  };

  render() {
    const { backend_name, url } = this.props
    const { email, username, step} = this.state

    if (step === 'register') {
      return (
        <Register
          backend_name={backend_name}
          email={email}
          url={url}
          username={username}
          onRegistrationComplete={this.handleRegistrationComplete}
        />
      );
    }
  }
}