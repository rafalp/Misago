import React from "react"
import Register from "./register"
import Complete from "./complete"

export default class SocialAuth extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      step: props.step,

      activation: props.activation || "",
      email: props.email || "",
      username: props.username || "",
    }
  }

  handleRegistrationComplete = ({ activation, email, step, username }) => {
    this.setState({ activation, email, step, username })
  }

  render() {
    const { backend_name, url } = this.props
    const { activation, email, step, username } = this.state

    if (step === "register") {
      return (
        <Register
          backend_name={backend_name}
          email={email}
          url={url}
          username={username}
          onRegistrationComplete={this.handleRegistrationComplete}
        />
      )
    }

    return (
      <Complete
        activation={activation}
        backend_name={backend_name}
        email={email}
        url={url}
        username={username}
      />
    )
  }
}
