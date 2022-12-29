import React from "react"
import PageHeader from "./PageHeader"
import PageHeaderBanner from "./PageHeaderBanner"
import PageHeaderContainer from "./PageHeaderContainer"
import PageHeaderDetails from "./PageHeaderDetails"

const PageHeaderPlain = ({ styleName, header, message }) => (
  <PageHeaderContainer>
    <PageHeader styleName={styleName}>
      <PageHeaderBanner styleName={styleName}>
        <h1>{header}</h1>
      </PageHeaderBanner>
      {message && (
        <PageHeaderDetails styleName={styleName}>{message}</PageHeaderDetails>
      )}
    </PageHeader>
  </PageHeaderContainer>
)

export default PageHeaderPlain
