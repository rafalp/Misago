import { Trans } from "@lingui/macro"
import React from "react"

interface IErrorProps {
  className: string
  header?: React.ReactNode | null
  message?: React.ReactNode | null
}

const Error: React.FC<IErrorProps> = ({
  className,
  header,
  message,
}) => (
    <div className={className + "-error"}>
      <div className={className + "-error-body"}>
        <div className={className + "-error-icon"} />
        <div className={className + "-error-message"}>
          <h1>
            {header || (
              <Trans id="generic_error.title">
                Requested page could not be displayed.
              </Trans>
            )}
          </h1>
          <p>
            {message || (
              <Trans id="generic_error.message">
                An unexpected error has occurred.
              </Trans>
            )}
          </p>
        </div>
      </div>
    </div>
)

export default Error
