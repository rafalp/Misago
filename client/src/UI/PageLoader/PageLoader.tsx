import React from "react"
import PageContainer from "../PageContainer"
import PageTitle from "../PageTitle"
import Spinner from "../Spinner"

const PageLoader: React.FC = () => (
  <PageContainer className="page-loader-container">
    <PageTitle />
    <div className="container-fluid">
      <div className="page-loader">
        <div className="page-loader-body">
          <Spinner />
        </div>
      </div>
    </div>
  </PageContainer>
)

export default PageLoader
