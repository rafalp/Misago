import React from "react"
import ReactDOM from "react-dom"

const initColorpicker = ({ elementId }) => {
  const element = document.getElementById(elementId)
  if (!element) console.error("Element with id " + element + "doesn't exist!")

  const name = element.name
  const value = element.value

  const container = document.createElement("div")
  element.parentNode.insertBefore(container, element)
  element.remove()

  ReactDOM.render(<ColorPicker name={name} value={value} />, container)
}

class ColorPicker extends React.Component {
  state = { value: this.props.value }

  onChange = ({ target }) => {
    this.setState({ value: target.value })
  }

  render() {
    return (
      <div className="row">
        <div className="col-auto pr-0">
          <input
            type="color"
            className="form-control"
            style={{width: "48px"}}
            value={cleanColor(this.state.value)}
            onChange={this.onChange}
          />
        </div>
        <div className="col">
          <input
            type="text"
            className="form-control"
            name={this.props.name}
            value={this.state.value}
            onChange={this.onChange}
          />
        </div>
      </div>
    )
  }
}

const color = /^#[0-9a-fA-F]{6}$/

const cleanColor = (value) => {
  return color.test(value) ? value : "#ffffff"
}

export default initColorpicker
