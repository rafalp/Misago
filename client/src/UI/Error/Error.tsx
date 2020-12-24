import { Trans } from "@lingui/macro"
import React from "react"
import ErrorMessage from "./ErrorMessage"

interface ErrorProps {
  className: string
  header?: React.ReactNode
  message?: React.ReactNode
  action?: React.ReactNode
}

const Error: React.FC<ErrorProps> = ({
  action,
  className,
  header,
  message,
}) => (
  <div className={className + "-error"}>
    <div className={className + "-error-body"}>
      <div className={className + "-error-icon"} />
      <div className={className + "-error-message"}>
        <p className="lead">
          {header || (
            <Trans id="generic_error.title">
              Requested page could not be displayed.
            </Trans>
          )}
        </p>
        <p>{message || <ErrorMessage />}</p>
        {action && <div className={className + "-error-action"}>{action}</div>}
      </div>
    </div>
  </div>
)

export default Error
