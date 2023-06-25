import React from "react"
import ListItem from "misago/components/users/active-posters/list-item"
import PageContainer from "../../PageContainer"
import UsersNav from "../UsersNav"

export default class extends React.Component {
  getLeadMessage() {
    let message = npgettext(
      "top posters list",
      "%(posters)s top poster from last %(days)s days.",
      "%(posters)s top posters from last %(days)s days.",
      this.props.count
    )

    return interpolate(
      message,
      {
        posters: this.props.count,
        days: this.props.trackedPeriod,
      },
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
          <p className="lead">{this.getLeadMessage()}</p>

          <div className="active-posters ui-ready">
            <ul className="list-group">
              {this.props.users.map((user, i) => {
                return (
                  <ListItem
                    user={user}
                    rank={user.rank}
                    counter={i + 1}
                    key={user.id}
                  />
                )
              })}
            </ul>
          </div>
        </PageContainer>
      </div>
    )
  }
}
