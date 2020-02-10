import React from "react"
import PageContainer from "../PageContainer"
import PageTitle from "../PageTitle"

interface IPageErrorProps {
  className?: string | null
  header: React.ReactNode
  message: React.ReactNode
}

const PageError: React.FC<IPageErrorProps> = ({
  className,
  header,
  message,
}) => (
  <PageContainer className={className}>
    <PageTitle />
    <div className="page-error">
      <div className="page-error-body">
        <div className="page-error-icon" />
        <div className="page-error-message">
          <h1>{header}</h1>
          <p>{message}</p>
        </div>
      </div>
    </div>
  </PageContainer>
)

export default PageError
