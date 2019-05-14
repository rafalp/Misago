import React from "react"
import ReactDOM from "react-dom"
import moment from "moment"

const initDatepicker = ({ elementId, never, setDate }) => {
  const element = document.getElementById(elementId)
  if (!element) console.error("Element with id " + element + "doesn't exist!")

  element.type = "hidden"

  const name = element.name
  const value = element.value.length ? moment(element.value) : null
  if (value) value.local()

  const container = document.createElement("div")
  element.parentNode.insertBefore(container, element)
  element.remove()

  ReactDOM.render(
    <DatePicker name={name} never={never} value={value} setDate={setDate} />,
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
    const { name, never, setDate } = this.props
    const { value } = this.state

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
    const startOfMonth = value
      .clone()
      .startOf("month")
      .isoWeekday()

    const calendar = value.clone()
    calendar.date(1)
    calendar.hour(value.hour())
    calendar.minute(value.minute())
    calendar.subtract(startOfMonth + 1, "day")

    return (
      <div className="control-month-picker">
        <CalendarHeader
          decreaseMonth={this.decreaseMonth}
          increaseMonth={this.increaseMonth}
          value={value}
        />
        <WeekdaysNames />
        {weeks.map(w => (
          <div className="row align-items-center m-0" key={w}>
            {days.map(d => (
              <Weekday
                calendar={calendar}
                key={d}
                value={value}
                onSelect={onChange}
              />
            ))}
          </div>
        ))}
      </div>
    )
  }
}

const CalendarHeader = ({ decreaseMonth, increaseMonth, value }) => (
  <div className="row align-items-center">
    <div className="col-auto text-center">
      <button
        className="btn btn-block py-1 px-3"
        type="button"
        onClick={decreaseMonth}
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
        onClick={increaseMonth}
      >
        <span className="fas fa-chevron-right" />
      </button>
    </div>
  </div>
)

const WeekdaysNames = () => (
  <div className="row align-items-center m-0">
    {moment.weekdaysMin(false).map((name, i) => (
      <div
        className={
          "col text-center px-1 " + (i === 0 ? "text-danger" : "text-muted")
        }
        key={name}
      >
        {name}
      </div>
    ))}
  </div>
)

const Weekday = ({ calendar, value, onSelect }) => {
  calendar.add(1, "day")
  const day = calendar.clone()
  const active = day.format("D M Y") === value.format("D M Y")

  return (
    <div className={"col text-center px-1"}>
      <button
        className={"btn btn-sm btn-block px-0" + (active ? " btn-primary" : "")}
        type="button"
        onClick={() => onSelect(day)}
        disabled={day.month() !== value.month()}
      >
        {day.format("D")}
      </button>
    </div>
  )
}

class SelectTime extends React.Component {
  handleHourChange = ({ target }) => {
    const { value: time } = target
    if (!time.match(/^[0-2][0-9]?[0-9]?$/)) return

    this.setState((_, props) => {
      const hour = cleanTimeValue(time, 2)
      const value = props.value.clone()
      value.hour(hour)
      props.onChange(value)
    })
  }

  handleMinuteChange = ({ target }) => {
    const { value: time } = target
    if (!time.match(/^[0-5][0-9]?[0-9]?$/)) return

    this.setState((_, props) => {
      const minute = cleanTimeValue(time, 5)
      const value = props.value.clone()
      value.minute(minute)
      props.onChange(value)
    })
  }

  render() {
    return (
      <div className="control-time-picker">
        <div className="row align-items-center m-0">
          <div className="col px-0">
            <TimeInput
              format="HH"
              value={this.props.value}
              onChange={this.handleHourChange}
            />
          </div>
          <div className="col-auto px-0">
            <span>:</span>
          </div>
          <div className="col px-0">
            <TimeInput
              format="mm"
              value={this.props.value}
              onChange={this.handleMinuteChange}
            />
          </div>
        </div>
      </div>
    )
  }
}

const cleanTimeValue = (time, maxFirstDigit) => {
  let value = time
  if (value.length === 3) {
    value = value.substring(1, 3)
    if (parseInt(value[0]) > maxFirstDigit) {
      value = maxFirstDigit + "" + value[1]
    }
  }
  return value
}

const TimeInput = ({ format, value, onChange }) => (
  <input
    className="form-control text-center"
    placeholder="00"
    type="text"
    value={value.format(format)}
    onChange={onChange}
  />
)

export default initDatepicker
