import React from "react"
import {
  PageHeader,
  PageHeaderBanner,
  PageHeaderContainer,
} from "../PageHeader"

const Header = ({ backendName }) => {
  const pageTitleTpl = pgettext("social auth title", "Sign in with %(backend)s")
  const pageTitle = interpolate(pageTitleTpl, { backend: backendName }, true)

  return (
    <PageHeaderContainer>
      <PageHeader styleName="social-auth">
        <PageHeaderBanner styleName="social-auth">
          <h1>{pageTitle}</h1>
        </PageHeaderBanner>
      </PageHeader>
    </PageHeaderContainer>
  )
}

export default Header
