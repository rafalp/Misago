import React from "react"
import modal from "../services/modal"
import SignInModal from "./sign-in"

class SignInModalAutoOpen extends React.Component {
  componentDidMount() {
    const query = window.document.location.search
    if (query === "?modal=login") {
      window.setTimeout(() => modal.show(<SignInModal />), 300)
    }
  }

  render() {
    return null
  }
}

export default SignInModalAutoOpen
