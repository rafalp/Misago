import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from '@apollo/client';
import React from "react"
import ReactDOM from "react-dom"
import Chart from "react-apexcharts"
import moment from "moment"

const initAnalytics = ({ elementId, errorMessage, labels, title, uri }) => {
  const element = document.getElementById(elementId)
  if (!element) console.error("Element with id " + element + "doesn't exist!")

  const client = new ApolloClient({
    credentials: "same-origin",
    uri: uri,
    cache: new InMemoryCache(),
  })

  ReactDOM.render(
    <ApolloProvider client={client}>
      <Analytics errorMessage={errorMessage} labels={labels} title={title} />
    </ApolloProvider>,
    element
  )
}

const getAnalytics = gql`
  query getAnalytics($span: Int!) {
    analytics(span: $span) {
      users {
        ...data
      }
      userDeletions {
        ...data
      }
      threads {
        ...data
      }
      posts {
        ...data
      }
      attachments {
        ...data
      }
      dataDownloads {
        ...data
      }
    }
  }

  fragment data on AnalyticsData {
    current
    currentCumulative
    previous
    previousCumulative
  }
`

function Analytics({ errorMessage, labels, title }) {
  const [span, setSpan] = React.useState(30)
  const { loading, error, data } = useQuery(getAnalytics, { variables: { span }})

  return (
    <div className="card card-admin-info">
      <div className="card-body">
        <div className="row align-items-center">
          <div className="col">
            <h4 className="card-title">{title}</h4>
          </div>
          <div className="col-auto">
            <SpanPicker span={span} setSpan={setSpan} />
          </div>
        </div>
      </div>
      {(() => {
        if (loading) return <Spinner />
        if (error) return <Error message={errorMessage} />

        const { analytics } = data

        return (
          <>
            <AnalyticsItem
              data={analytics.threads}
              name={labels.threads}
              span={span}
            />
            <AnalyticsItem
              data={analytics.posts}
              name={labels.posts}
              span={span}
            />
            <AnalyticsItem
              data={analytics.attachments}
              name={labels.attachments}
              span={span}
            />
            <AnalyticsItem
              data={analytics.users}
              name={labels.users}
              span={span}
            />
            <AnalyticsItem
              data={analytics.userDeletions}
              name={labels.userDeletions}
              negative={true}
              span={span}
            />
            <AnalyticsItem
              data={analytics.dataDownloads}
              name={labels.dataDownloads}
              span={span}
            />
          </>
        )
      })()}
    </div>
  )
}

const SpanPicker = ({ span, setSpan }) => (
  <div>
    {[30, 90, 180, 360].map(choice => (
      <button
        key={choice}
        className={
          choice === span
            ? "btn btn-primary btn-sm ml-3"
            : "btn btn-light btn-sm ml-3"
        }
        type="button"
        onClick={() => setSpan(choice)}
      >
        {choice}
      </button>
    ))}
  </div>
)

const Spinner = () => (
  <div className="card-body border-top">
    <div className="text-center py-5">
      <div className="spinner-border text-light" role="status">
        <span className="sr-only">Loading...</span>
      </div>
    </div>
  </div>
)

const Error = ({ message }) => (
  <div className="card-body border-top">
    <div className="text-center py-5">{message}</div>
  </div>
)

const CURRENT = "C"
const PREVIOUS = "P"
const CURRENT_SERIES = 0

const AnalyticsItem = ({ data, legend, name, negative, span }) => {
  const options = {
    legend: {
      show: false
    },
    chart: {
      animations: {
        enabled: false
      },
      parentHeightOffset: 0,
      toolbar: {
        show: false
      }
    },
    colors: ["#6554c0", "#b3d4ff"],
    grid: {
      padding: {
        top: 0
      }
    },
    stroke: {
      width: 2
    },
    tooltip: {
      x: {
        show: false
      },
      y: {
        title: {
          formatter: function(series, { dataPointIndex }) {
            const now = moment()
            if (series === PREVIOUS) now.subtract(span, "days")
            now.subtract(span - dataPointIndex - 1, "days")
            return now.format("ll")
          }
        },
        formatter: function(value, { dataPointIndex, seriesIndex }) {
          if (seriesIndex === CURRENT_SERIES) {
            return data.current[dataPointIndex]
          }
          return data.previous[dataPointIndex]
        }
      }
    },
    xaxis: {
      axisBorder: {
        show: false
      },
      axisTicks: {
        show: false
      },
      labels: {
        show: false
      },
      categories: [],
      tooltip: {
        enabled: false
      }
    },
    yaxis: {
      tickAmount: 2,
      max: m => m || 1,
      show: false
    }
  }

  const series = [
    { name: CURRENT, data: data.currentCumulative },
    { name: PREVIOUS, data: data.previousCumulative }
  ]

  return (
    <div className="card-body border-top pb-1">
      <h5 className="m-0">{name}</h5>
      <div className="row align-items-center">
        <div className="col-auto">
          <Summary data={data} negative={negative} />
        </div>
        <div className="col">
          <ChartContainer>
            {({ width }) =>
              width > 1 && (
                <Chart
                  options={options}
                  series={series}
                  type="line"
                  width={width}
                  height={140}
                />
              )
            }
          </ChartContainer>
        </div>
      </div>
    </div>
  )
}

const Summary = ({ data, negative }) => {
  const current = data.current.reduce((a, b) => a + b)
  const previous = data.previous.reduce((a, b) => a + b)
  const diff = current - previous

  let color = "text-light"
  let icon = "fas fa-equals"

  if (negative) {
    if (diff > 0) color = "text-danger"
    if (diff < 0) color = "text-success"
  } else {
    if (diff > 0) color = "text-success"
    if (diff < 0) color = "text-danger"
  }

  if (diff > 0) {
    icon = "fas fa-chevron-up"
  }
  if (diff < 0) {
    icon = "fas fa-chevron-down"
  }

  return (
    <div className="card-admin-analytics-summary">
      <div>{current}</div>
      <small className={color}>
        <span className={icon} /> {Math.abs(diff)}
      </small>
    </div>
  )
}

class ChartContainer extends React.Component {
  state = { width: 1, height: 1 }
  element = React.createRef()

  componentDidMount() {
    this.timer = window.setInterval(this.updateSize, 3000)
    this.updateSize()
  }

  componentWillUnmount() {
    window.clearInterval(this.timer)
  }

  updateSize = () => {
    this.setState({
      width: this.element.current.clientWidth,
      height: this.element.current.clientHeight
    })
  }

  render() {
    return (
      <div className="card-admin-analytics-chart" ref={this.element}>
        {this.props.children(this.state)}
      </div>
    )
  }
}

export default initAnalytics
