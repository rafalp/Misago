import React from "react"

export default function (props) {
  return (
    <ul className="list-unstyled poll-select-choices">
      {props.choices.map((choice) => {
        return (
          <ChoiceSelect
            choice={choice}
            key={choice.hash}
            toggleChoice={props.toggleChoice}
          />
        )
      })}
    </ul>
  )
}

export class ChoiceSelect extends React.Component {
  onClick = () => {
    this.props.toggleChoice(this.props.choice.hash)
  }

  render() {
    return (
      <li className="poll-select-choice">
        <button
          className={this.props.choice.selected ? "btn btn-selected" : "btn"}
          onClick={this.onClick}
          type="button"
        >
          <span className="material-icon">
            {this.props.choice.selected
              ? "check_box"
              : "check_box_outline_blank"}
          </span>
          <strong>{this.props.choice.label}</strong>
        </button>
      </li>
    )
  }
}
