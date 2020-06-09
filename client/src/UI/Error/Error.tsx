import { Trans } from "@lingui/macro"
import React from "react"
import ErrorMessage from "./ErrorMessage"

interface IErrorProps {
  className: string
  header?: React.ReactNode | null
  message?: React.ReactNode | null
}

const Error: React.FC<IErrorProps> = ({ className, header, message }) => (
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
      </div>
    </div>
  </div>
)

export default Error
