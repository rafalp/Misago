import { Trans } from "@lingui/macro"
import React from "react"
import Error from "./Error"

interface INotFoundErrorProps {
  className: string
  header?: React.ReactNode
  message?: React.ReactNode
}

const NotFoundError: React.FC<INotFoundErrorProps> = ({
  className,
  header,
  message,
}) => (
  <Error
    className={className}
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
          The link you've followed may be broken, or the page has been moved or
          deleted.
        </Trans>
      )
    }
  />
)

export default NotFoundError
