import { Trans } from "@lingui/macro"
import classNames from "classnames"
import React from "react"
import PageContainer from "../PageContainer"
import PageTitle from "../PageTitle"

interface IPageErrorProps {
  className?: string | null
  header?: React.ReactNode | null
  message?: React.ReactNode | null
}

const PageError: React.FC<IPageErrorProps> = ({
  className,
  header,
  message,
}) => (
  <PageContainer className={classNames("page-error-container", className)}>
    <PageTitle />
    <div className="page-error">
      <div className="page-error-body">
        <div className="page-error-icon" />
        <div className="page-error-message">
          <h1>
            {header || (
              <Trans id="page_error.title">
                Requested page could not be displayed due to an error.
              </Trans>
            )}
          </h1>
          <p>
            {message || (
              <Trans id="page_crashed_error.message">
                An unexpected error has occurred during displaying of this
                page.
              </Trans>
            )}
          </p>
        </div>
      </div>
    </div>
  </PageContainer>
)

export default PageError
