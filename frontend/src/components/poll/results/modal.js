import React from "react"
import moment from "moment"
import Message from "misago/components/modal-message"
import Loader from "misago/components/modal-loader"
import ajax from "misago/services/ajax"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: true,
      error: null,
      data: [],
    }
  }

  componentDidMount() {
    ajax.get(this.props.poll.api.votes).then(
      (data) => {
        const hydratedData = data.map((choice) => {
          return Object.assign({}, choice, {
            voters: choice.voters.map((voter) => {
              return Object.assign({}, voter, {
                voted_on: moment(voter.voted_on),
              })
            }),
          })
        })

        this.setState({
          isLoading: false,
          data: hydratedData,
        })
      },
      (rejection) => {
        this.setState({
          isLoading: false,
          error: rejection.detail,
        })
      }
    )
  }

  render() {
    return (
      <div
        className={
          "modal-dialog" + (this.state.error ? " modal-message" : " modal-sm")
        }
        role="document"
      >
        <div className="modal-content">
          <div className="modal-header">
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label={pgettext("modal", "Close")}
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">
              {pgettext("thread poll", "Poll votes")}
            </h4>
          </div>

          <ModalBody
            data={this.state.data}
            error={this.state.error}
            isLoading={this.state.isLoading}
          />
        </div>
      </div>
    )
  }
}

export function ModalBody(props) {
  if (props.isLoading) {
    return <Loader />
  } else if (props.error) {
    return <Message icon="error_outline" message={props.error} />
  }

  return <ChoicesList data={props.data} />
}

export function ChoicesList(props) {
  return (
    <div className="modal-body modal-poll-votes">
      <ul className="list-unstyled votes-details">
        {props.data.map((choice) => {
          return <ChoiceDetails key={choice.hash} {...choice} />
        })}
      </ul>
    </div>
  )
}

export function ChoiceDetails(props) {
  return (
    <li>
      <h4>{props.label}</h4>
      <VotesCount votes={props.votes} />
      <VotesList voters={props.voters} />
      <hr />
    </li>
  )
}

export function VotesCount(props) {
  const message = npgettext(
    "thread poll",
    "%(votes)s user has voted for this choice.",
    "%(votes)s users have voted for this choice.",
    props.votes
  )

  const label = interpolate(
    message,
    {
      votes: props.votes,
    },
    true
  )

  return <p>{label}</p>
}

export function VotesList(props) {
  if (!props.voters.length) return null

  return (
    <ul className="list-unstyled">
      {props.voters.map((user) => {
        return <Voter key={user.username} {...user} />
      })}
    </ul>
  )
}

export function Voter(props) {
  if (props.url) {
    return (
      <li>
        <a className="item-title" href={props.url}>
          {props.username}
        </a>{" "}
        <VoteDate voted_on={props.voted_on} />
      </li>
    )
  }

  return (
    <li>
      <strong>{props.username}</strong> <VoteDate voted_on={props.voted_on} />
    </li>
  )
}

export function VoteDate(props) {
  return (
    <abbr className="text-muted" title={props.voted_on.format("LLL")}>
      {props.voted_on.fromNow()}
    </abbr>
  )
}
