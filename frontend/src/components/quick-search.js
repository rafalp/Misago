import React from "react"

export default class extends React.Component {
  getClassName() {
    if (this.props.className) {
      return "form-search " + this.props.className
    } else {
      return "form-search"
    }
  }

  render() {
    return (
      <div className={this.getClassName()}>
        <input
          type="text"
          className="form-control"
          value={this.props.value}
          onChange={this.props.onChange}
          placeholder={
            this.props.placeholder ||
            pgettext("quick search placeholder", "Search...")
          }
        />
        <span className="material-icon">search</span>
      </div>
    )
  }
}
