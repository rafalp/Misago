import React from "react"
import { dateRelative, dateRelativeShort, fullDateTime } from "../../formats"

class Timestamp extends React.Component {
  constructor(props) {
    super(props)

    this.state = { tick: 0 }
    this.date = new Date(props.datetime)
    this.timeout = null
  }

  componentDidMount() {
    this.scheduleNextUpdate()
  }

  componentWillUnmount() {
    if (this.timeout) {
      window.clearTimeout(this.timeout)
    }
  }

  scheduleNextUpdate = () => {
    const now = new Date()
    const diff = Math.ceil(Math.abs(Math.round((this.date - now) / 1000)))

    if (diff < 3600) {
      this.timeout = window.setTimeout(
        () => {
          this.setState(tick)
          this.scheduleNextUpdate()
        },
        50 * 1000 // Update every 50 seconds
      )
    } else if (diff < 3600 * 24) {
      this.timeout = window.setTimeout(
        () => {
          this.setState(tick)
        },
        40 * 60 * 1000 // Update every 40 minutes
      )
    }
  }

  render() {
    const displayed = this.props.narrow
      ? dateRelativeShort(this.date)
      : dateRelative(this.date)

    return (
      <attr
        title={
          this.props.title
            ? this.props.title.replace(
                "%(timestamp)s",
                fullDateTime.format(this.date)
              )
            : fullDateTime.format(this.date)
        }
      >
        {displayed}
      </attr>
    )
  }
}

function tick(state) {
  return { tick: state.tick + 1 }
}

export default Timestamp
