import ApolloClient, { gql } from "apollo-boost"
import React from "react"
import ReactDOM from "react-dom"
import { ApolloProvider, Query } from "react-apollo"

const initVersionCheck = ({ elementId, errorMessage, loadingMessage, uri }) => {
  const element = document.getElementById(elementId)
  if (!element) console.error("Element with id " + element + "doesn't exist!")

  const client = new ApolloClient({
    credentials: "same-origin",
    uri: uri
  })

  ReactDOM.render(
    <ApolloProvider client={client}>
      <VersionCheck
        errorMessage={errorMessage}
        loadingMessage={loadingMessage}
      />
    </ApolloProvider>,
    element
  )
}

const getVersion = gql`
  query getVersion {
    version {
      status
      message
      description
    }
  }
`

const VersionCheck = ({ errorMessage, loadingMessage }) => {
  return (
    <Query query={getVersion}>
      {({ loading, error, data }) => {
        if (loading) return <Spinner {...loadingMessage} />
        if (error) return <Error {...errorMessage} />

        return <CheckMessage {...data.version} />
      }}
    </Query>
  )
}

const Spinner = ({ description, message }) => (
  <div className="media media-admin-check">
    <div className="media-check-icon">
      <div className="spinner-border" role="status">
        <span className="sr-only">Loading...</span>
      </div>
    </div>
    <div className="media-body">
      <h5>{message}</h5>
      {description}
    </div>
  </div>
)

const Error = ({ description, message }) => (
  <div className="media media-admin-check">
    <div className="media-check-icon media-check-icon-danger">
      <span className="fas fa-times" />
    </div>
    <div className="media-body">
      <h5>{message}</h5>
      {description}
    </div>
  </div>
)

const CheckMessage = ({ description, message, status }) => (
  <div className="media media-admin-check">
    <CheckIcon status={status} />
    <div className="media-body">
      <h5>{message}</h5>
      {description}
    </div>
  </div>
)

const CheckIcon = ({ status }) => {
  let className = "media-check-icon media-check-icon-"
  if (status === "SUCCESS") className += "success"
  if (status === "WARNING") className += "warning"
  if (status === "ERROR") className += "danger"

  return (
    <div className={className}>
      <CheckIconImage status={status} />
    </div>
  )
}

const CheckIconImage = ({ status }) => {
  if (status === "SUCCESS") return <span className="fas fa-check" />
  if (status === "WARNING") return <span className="fas fa-question" />
  if (status === "ERROR") return <span className="fas fa-times" />

  return null
}

export default initVersionCheck
