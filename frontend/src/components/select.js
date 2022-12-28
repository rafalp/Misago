import React from "react"

export default class extends React.Component {
  getChoice() {
    let choice = null
    this.props.choices.map((item) => {
      if (item.value === this.props.value) {
        choice = item
      }
    })
    return choice
  }

  getIcon() {
    return this.getChoice().icon
  }

  getLabel() {
    return this.getChoice().label
  }

  change = (value) => {
    return () => {
      this.props.onChange({
        target: {
          value: value,
        },
      })
    }
  }

  render() {
    return (
      <div className="btn-group btn-select-group">
        <button
          type="button"
          className="btn btn-select dropdown-toggle"
          id={this.props.id || null}
          data-toggle="dropdown"
          aria-haspopup="true"
          aria-expanded="false"
          aria-describedby={this.props["aria-describedby"] || null}
          disabled={this.props.disabled || false}
        >
          <Icon icon={this.getIcon()} />
          {this.getLabel()}
        </button>
        <ul className="dropdown-menu">
          {this.props.choices.map((item, i) => {
            return (
              <li key={i}>
                <button
                  type="button"
                  className="btn-link"
                  onClick={this.change(item.value)}
                >
                  <Icon icon={item.icon} />
                  {item.label}
                </button>
              </li>
            )
          })}
        </ul>
      </div>
    )
  }
}

export function Icon({ icon }) {
  if (!icon) return null

  return <span className="material-icon">{icon}</span>
}
