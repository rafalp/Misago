import React from "react"
import PageContainer from "../../PageContainer"
import UsersNav from "../UsersNav"

export default class extends React.Component {
  getEmptyMessage() {
    return interpolate(
      npgettext(
        "top posters empty",
        "No users have posted any new messages during last %(days)s day.",
        "No users have posted any new messages during last %(days)s days.",
        this.props.trackedPeriod
      ),
      { days: this.props.trackedPeriod },
      true
    )
  }

  render() {
    return (
      <div className="active-posters-list">
        <PageContainer>
          <UsersNav
            baseUrl={misago.get("USERS_LIST_URL")}
            page={this.props.page}
            pages={misago.get("USERS_LISTS")}
          />
          <p className="lead">{this.getEmptyMessage()}</p>
        </PageContainer>
      </div>
    )
  }
}
