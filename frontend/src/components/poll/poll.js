import React from "react"
import moment from "moment"
import Results from "./results"
import Voting from "./voting"

export default class extends React.Component {
  constructor(props) {
    super(props)

    let showResults = true
    if (props.user.id && !props.poll.hasSelectedChoices) {
      showResults = false
    }

    this.state = {
      showResults,
    }
  }

  showResults = () => {
    this.setState({
      showResults: true,
    })
  }

  showVoting = () => {
    this.setState({
      showResults: false,
    })
  }

  render() {
    if (!this.props.thread.poll) return null

    const isPollOver = getIsPollOver(this.props.poll)

    if (
      !isPollOver &&
      this.props.poll.acl.can_vote &&
      !this.state.showResults
    ) {
      return <Voting showResults={this.showResults} {...this.props} />
    } else {
      return (
        <Results
          isPollOver={isPollOver}
          showVoting={this.showVoting}
          {...this.props}
        />
      )
    }
  }
}

export function getIsPollOver(poll) {
  if (poll.length) {
    return moment().isAfter(poll.endsOn)
  }
  return false
}
