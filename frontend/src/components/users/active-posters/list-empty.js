import React from "react"
import PageContainer from "../../PageContainer"

export default class extends React.Component {
  getEmptyMessage() {
    return interpolate(
      gettext(
        "No users have posted any new messages during last %(days)s days."
      ),
      { days: this.props.trackedPeriod },
      true
    )
  }

  render() {
    return (
      <div className="active-posters-list">
        <PageContainer>
          <p className="lead">{this.getEmptyMessage()}</p>
        </PageContainer>
      </div>
    )
  }
}
