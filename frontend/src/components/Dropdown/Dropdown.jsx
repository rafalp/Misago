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

  componentDidUpdate(prevProps, prevState) {
    const didUpdate = prevState.isOpen !== this.state.isOpen
    if (didUpdate) {
      if (this.state.isOpen && this.props.onOpen) {
        this.props.onOpen(this.root)
      }

      if (!this.state.isOpen && this.props.onClose) {
        this.props.onClose(this.root)
      }
    }
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

    return (
      <div
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
      </div>
    )
  }
}

function ariaProps(isOpen) {
  return {
    "aria-haspopup": "true",
    "aria-expanded": isOpen ? "true" : "false",
  }
}
