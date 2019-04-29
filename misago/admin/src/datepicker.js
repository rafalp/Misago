import React from "react"
import ReactDOM from "react-dom"
import moment from "moment"

// 2019-03-22T22:17:12+00:00
const initDatepicker = ({ elementId, never, setDate }) => {
  const element = document.getElementById(elementId)
  if (!element) console.error("Element with id " + element + "doesn't exist!")

  element.type = "hidden"

  const name = element.name
  const value = element.value.length ? moment(element.value) : null
  if (value) value.local()
  const required = element.required

  const container = document.createElement("div")
  element.parentNode.insertBefore(container, element)
  element.remove()

  ReactDOM.render(
    <DatePicker
      name={name}
      never={never}
      value={value}
      required={required}
      setDate={setDate}
    />,
    container
  )
}

class DatePicker extends React.Component {
  state = {
    defaultValue: this.props.value,
    value: this.props.value
  }

  setNever = () => {
    this.setState({ value: null })
  }

  setInitialValue = () => {
    this.setState(({ defaultValue, value }) => {
      if (defaultValue) return { value: defaultValue }

      const newValue = moment()
      newValue.add(1, "hour")
      return { value: newValue }
    })
  }

  setValue = value => {
    this.setState({ value })
  }

  render() {
    const { name, never, required, setDate } = this.props
    const { defaultValue, value } = this.state

    return (
      <div onBlur={this.handleBlur} onFocus={this.handleFocus}>
        <input type="hidden" name={name} value={value ? value.format() : ""} />
        <div>
          <button
            className={getButtonClassName(value === null)}
            type="button"
            onClick={this.setNever}
          >
            {never}
          </button>
          <button
            className={getButtonClassName(value !== null) + " ml-3"}
            type="button"
            onClick={this.setInitialValue}
          >
            {value ? value.format("L LT") : setDate}
          </button>
        </div>
        <Input value={value} onChange={this.setValue} />
      </div>
    )
  }
}

const getButtonClassName = active => {
  if (active) return "btn btn-outline-primary btn-sm"
  return "btn btn-outline-secondary btn-sm"
}

const Input = ({ value, onChange }) => {
  if (!value) return null

  return (
    <div className="row mt-3">
      <div className="col-auto">
        <SelectMonth value={value} onChange={onChange} />
      </div>
      <div className="col-auto">
        <SelectTime value={value} onChange={onChange} />
      </div>
    </div>
  )
}

const weeks = [1, 2, 3, 4, 5, 6]
const days = [1, 2, 3, 4, 5, 6, 7]

class SelectMonth extends React.Component {
  decreaseMonth = () => {
    this.setState((_, props) => {
      const value = props.value.clone()
      value.subtract(1, "month")
      props.onChange(value)
    })
  }

  increaseMonth = () => {
    this.setState((_, props) => {
      const value = props.value.clone()
      value.add(1, "month")
      props.onChange(value)
    })
  }

  render() {
    const { value, onChange } = this.props

    const calendar = value.clone()
    const startOfMonth = calendar.startOf("month").isoWeekday()

    calendar.date(1)
    calendar.hour(value.hour())
    calendar.minute(value.minute())
    calendar.subtract(startOfMonth + 1, "day")

    return (
      <div className="control-month-picker">
        <div className="row align-items-center">
          <div className="col-auto text-center">
            <button
              className="btn btn-block py-1 px-3"
              type="button"
              onClick={this.decreaseMonth}
            >
              <span className="fas fa-chevron-left" />
            </button>
          </div>
          <div className="col text-center font-weight-bold">
            {value.format("MMMM YYYY")}
          </div>
          <div className="col-auto text-center">
            <button
              className="btn btn-block py-1 px-3"
              type="button"
              onClick={this.increaseMonth}
            >
              <span className="fas fa-chevron-right" />
            </button>
          </div>
        </div>
        <div className="row align-items-center m-0">
          {moment.weekdaysMin(false).map((label, i) => (
            <div
              className={
                "col text-center px-1 " +
                (i === 0 ? "text-danger" : "text-muted")
              }
              key={label}
            >
              {label}
            </div>
          ))}
        </div>
        {weeks.map(w => (
          <div className="row align-items-center m-0" key={w}>
            {days.map(d => {
              calendar.add(1, "day")
              const day = calendar.clone()
              const active = day.format("D M Y") === value.format("D M Y")

              return (
                <div className={"col text-center px-1"} key={d}>
                  <button
                    className={
                      "btn btn-sm btn-block px-0" +
                      (active ? " btn-primary" : "")
                    }
                    type="button"
                    onClick={() => onChange(day)}
                    disabled={day.month() !== value.month()}
                  >
                    {day.format("D")}
                  </button>
                </div>
              )
            })}
          </div>
        ))}
      </div>
    )
  }
}

class SelectTime extends React.Component {
  handleHourChange = ({ target }) => {
    const { value: time } = target
    if (!time.match(/^[0-2][0-9]?[0-9]?$/)) return

    this.setState((_, props) => {
      const value = props.value.clone()
      let hour = time
      if (hour.length === 3) {
        hour = hour.substring(1, 3)
        if (parseInt(hour[0]) > 2) {
          hour = "2" + hour[1]
        }
      }
      value.hour(hour)
      props.onChange(value)
    })
  }

  handleMinuteChange = ({ target }) => {
    const { value: time } = target
    if (!time.match(/^[0-5][0-9]?[0-9]?$/)) return

    this.setState((_, props) => {
      const value = props.value.clone()
      let minute = time
      if (minute.length === 3) {
        minute = minute.substring(1, 3)
        if (parseInt(minute[0]) > 5) {
          minute = "5" + minute[1]
        }
      }
      value.minute(minute)
      props.onChange(value)
    })
  }

  render() {
    return (
      <div className="control-time-picker">
        <div className="row align-items-center m-0">
          <div className="col px-0">
            <input
              className="form-control text-center"
              placeholder="00"
              type="text"
              value={this.props.value.format("HH")}
              onChange={this.handleHourChange}
            />
          </div>
          <div className="col-auto px-0">
            <span>:</span>
          </div>
          <div className="col px-0">
            <input
              className="form-control text-center"
              placeholder="00"
              type="text"
              value={this.props.value.format("mm")}
              onChange={this.handleMinuteChange}
            />
          </div>
        </div>
      </div>
    )
  }
}

export default initDatepicker
