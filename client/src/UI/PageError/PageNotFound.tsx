import { Trans } from "@lingui/macro"
import React from "react"
import PageError from "./PageError"

interface IPageNotFoundProps {
  header?: React.ReactNode | null
  message?: React.ReactNode | null
}

const PageNotFound: React.FC<IPageNotFoundProps> = ({ header, message }) => (
  <PageError
    className="page-not-found"
    header={
      header || (
        <Trans id="not_found_error.title">
          Requested page could not be found.
        </Trans>
      )
    }
    message={
      message || (
        <Trans id="not_found_error.message">
          The link you followed was incorrect or the page has been moved or
          deleted.
        </Trans>
      )
    }
  />
)

export default PageNotFound
