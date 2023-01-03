import React from "react"
import { connect } from "react-redux"
import { SideNav, CompactNav } from "misago/components/options/navs"
import DeleteAccount from "misago/components/options/delete-account"
import EditDetails from "misago/components/options/edit-details"
import DownloadData from "misago/components/options/download-data"
import ChangeForumOptions from "misago/components/options/forum-options"
import ChangeUsername from "misago/components/options/change-username/root"
import ChangeSignInCredentials from "misago/components/options/sign-in-credentials/root"
import WithDropdown from "misago/components/with-dropdown"
import misago from "misago/index"
import { FlexRow, FlexRowCol, FlexRowSection } from "../FlexRow"
import PageContainer from "../PageContainer"
import {
  PageHeader,
  PageHeaderBanner,
  PageHeaderContainer,
} from "../PageHeader"

export default class extends WithDropdown {
  render() {
    const page = misago.get("USER_OPTIONS").filter((page) => {
      const url = misago.get("USERCP_URL") + page.component + "/"
      return this.props.location.pathname.substr(0, url.length) === url
    })[0]

    return (
      <div className="page page-options">
        <PageHeaderContainer>
          <PageHeader styleName="options">
            <PageHeaderBanner styleName="options">
              <FlexRow>
                <FlexRowSection auto>
                  <FlexRowCol auto>
                    <h1>{gettext("Change your options")}</h1>
                  </FlexRowCol>
                  <FlexRowCol className="hidden-xs hidden-md hidden-lg" shrink>
                    <div className="dropdown">
                      <button
                        type="button"
                        className="btn btn-default btn-outline btn-icon dropdown-toggle"
                        title={gettext("Menu")}
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                      >
                        <span className="material-icon">menu</span>
                      </button>
                      <CompactNav
                        className="dropdown-menu dropdown-menu-right"
                        baseUrl={misago.get("USERCP_URL")}
                        options={misago.get("USER_OPTIONS")}
                      />
                    </div>
                  </FlexRowCol>
                </FlexRowSection>
                <FlexRowSection className="hidden-sm hidden-md hidden-lg">
                  <FlexRowCol>
                    <div className="dropdown">
                      <button
                        type="button"
                        className="btn btn-default btn-outline btn-block dropdown-toggle"
                        data-toggle="dropdown"
                        aria-haspopup="true"
                        aria-expanded="false"
                      >
                        <span className="material-icon">{page.icon}</span>
                        {page.name}
                      </button>
                      <CompactNav
                        className="dropdown-menu"
                        baseUrl={misago.get("USERCP_URL")}
                        options={misago.get("USER_OPTIONS")}
                      />
                    </div>
                  </FlexRowCol>
                </FlexRowSection>
              </FlexRow>
            </PageHeaderBanner>
          </PageHeader>
        </PageHeaderContainer>
        <PageContainer>
          <div className="row">
            <div className="col-md-3 hidden-xs hidden-sm">
              <SideNav
                baseUrl={misago.get("USERCP_URL")}
                options={misago.get("USER_OPTIONS")}
              />
            </div>
            <div className="col-md-9">{this.props.children}</div>
          </div>
        </PageContainer>
      </div>
    )
  }
}

export function select(store) {
  return {
    tick: store.tick.tick,
    user: store.auth.user,
    "username-history": store["username-history"],
  }
}

export function paths() {
  const paths = [
    {
      path: misago.get("USERCP_URL") + "forum-options/",
      component: connect(select)(ChangeForumOptions),
    },
    {
      path: misago.get("USERCP_URL") + "edit-details/",
      component: connect(select)(EditDetails),
    },
    {
      path: misago.get("USERCP_URL") + "change-username/",
      component: connect(select)(ChangeUsername),
    },
    {
      path: misago.get("USERCP_URL") + "sign-in-credentials/",
      component: connect(select)(ChangeSignInCredentials),
    },
  ]

  if (misago.get("ENABLE_DOWNLOAD_OWN_DATA")) {
    paths.push({
      path: misago.get("USERCP_URL") + "download-data/",
      component: connect(select)(DownloadData),
    })
  }

  if (misago.get("ENABLE_DELETE_OWN_ACCOUNT")) {
    paths.push({
      path: misago.get("USERCP_URL") + "delete-account/",
      component: connect(select)(DeleteAccount),
    })
  }

  return paths
}
