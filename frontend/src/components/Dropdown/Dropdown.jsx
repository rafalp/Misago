import classnames from "classnames"
import React from "react"

export default class Dropdown extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isOpen: false,
    }

    this.root = null
    this.dropdown = null
  }

  componentDidMount() {
    window.addEventListener("click", this.handleClick)
  }

  componentWillUnmount() {
    window.removeEventListener("click", this.handleClick)
  }

  handleClick = (event) => {
    if (
      this.state.isOpen &&
      (!this.root.contains(event.target) ||
        (this.menu.contains(event.target) && event.target.closest("a")))
    ) {
      this.setState({ isOpen: false })
    }
  }

  toggle = () => {
    this.setState((prevState) => {
      return { isOpen: !prevState.isOpen }
    })
  }

  close = () => {
    this.setState({ isOpen: false })
  }

  render() {
    const { isOpen } = this.state
    const RootElement = this.props.listItem ? "li" : "div"

    return (
      <RootElement
        id={this.props.id}
        className={classnames(
          "dropdown",
          { open: isOpen },
          this.props.className
        )}
        ref={(element) => {
          if (element && !this.element) {
            this.root = element
          }
        }}
      >
        {this.props.toggle({
          isOpen,
          toggle: this.toggle,
          aria: ariaProps(isOpen),
        })}
        <div
          className={classnames(
            "dropdown-menu",
            { "dropdown-menu-right": this.props.menuAlignRight },
            this.props.menuClassName
          )}
          ref={(element) => {
            if (element && !this.menu) {
              this.menu = element
            }
          }}
          role="menu"
        >
          {this.props.children({ isOpen, close: this.close })}
        </div>
      </RootElement>
    )
  }
}

function ariaProps(isOpen) {
  return {
    "aria-haspopup": "true",
    "aria-expanded": isOpen ? "true" : "false",
  }
}
