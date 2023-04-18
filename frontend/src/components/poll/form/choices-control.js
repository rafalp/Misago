import React from "react"
import getRandomString from "../../../utils/getRandomString"

const HASH_LENGTH = 12

export default class extends React.Component {
  onAdd = () => {
    let choices = this.props.choices.slice()
    choices.push({
      hash: getRandomString(HASH_LENGTH),
      label: "",
    })

    this.props.setChoices(choices)
  }

  onChange = (hash, label) => {
    const choices = this.props.choices.map((choice) => {
      if (choice.hash === hash) {
        choice.label = label
      }

      return choice
    })
    this.props.setChoices(choices)
  }

  onDelete = (hash) => {
    const choices = this.props.choices.filter((choice) => {
      return choice.hash !== hash
    })
    this.props.setChoices(choices)
  }

  render() {
    return (
      <div className="poll-choices-control">
        <ul className="list-group">
          {this.props.choices.map((choice) => {
            return (
              <PollChoice
                canDelete={this.props.choices.length > 2}
                choice={choice}
                disabled={this.props.disabled}
                key={choice.hash}
                onChange={this.onChange}
                onDelete={this.onDelete}
              />
            )
          })}
        </ul>
        <button
          className="btn btn-default btn-sm"
          disabled={this.props.disabled}
          onClick={this.onAdd}
          type="button"
        >
          {pgettext("thread poll", "Add choice")}
        </button>
      </div>
    )
  }
}

export class PollChoice extends React.Component {
  onChange = (event) => {
    this.props.onChange(this.props.choice.hash, event.target.value)
  }

  onDelete = () => {
    const deleteItem =
      this.props.choice.label.length === 0
        ? true
        : window.confirm(
            pgettext(
              "thread poll",
              "Are you sure you want to remove this choice?"
            )
          )
    if (deleteItem) {
      this.props.onDelete(this.props.choice.hash)
    }
  }

  render() {
    return (
      <li className="list-group-item">
        <button
          className="btn"
          disabled={!this.props.canDelete || this.props.disabled}
          onClick={this.onDelete}
          title={pgettext("thread poll", "Remove this choice")}
          type="button"
        >
          <span className="material-icon">close</span>
        </button>
        <input
          disabled={this.props.disabled}
          maxLength="255"
          placeholder={pgettext("thread poll", "Poll choice")}
          type="text"
          onChange={this.onChange}
          value={this.props.choice.label}
        />
      </li>
    )
  }
}
