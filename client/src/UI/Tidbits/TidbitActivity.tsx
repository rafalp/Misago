import { Trans } from "@lingui/macro"
import { I18n } from "@lingui/react"
import { Link } from "react-router-dom"
import React from "react"
import * as urls from "../../urls"
import Timestamp from "../Timestamp"
import { formatDate } from "../formats"
import TidbitItem from "./TidbitItem"

interface ITidbitActivityTimestampProps {
  date: Date
  url?: string
}

interface ITidbitActivityUserProps {
  user?: {
    id: string
    slug: string
    name: string
  } | null
  userName: string
}

interface ITidbitActivityProps
  extends ITidbitActivityTimestampProps,
    ITidbitActivityUserProps {}

const TidbitActivityTimestamp: React.FC<ITidbitActivityTimestampProps> = ({
  date,
  url,
}) => (
  <I18n>
    {({ i18n: { language } }) =>
      url ? (
        <Link
          className="tidbit-activity-timestamp"
          to={url}
          title={formatDate(date, language)}
        >
          <Timestamp date={date} language={language} prefixed />
        </Link>
      ) : (
        <span
          className="tidbit-activity-timestamp"
          title={formatDate(date, language)}
        >
          <Timestamp date={date} language={language} prefixed />
        </span>
      )
    }
  </I18n>
)

const TidbitActivityUser: React.FC<ITidbitActivityUserProps> = ({
  user,
  userName,
}) =>
  user ? (
    <Link className="tidbit-activity-user" to={urls.user(user)}>
      {user.name}
    </Link>
  ) : (
    <span className="tidbit-activity-user">{userName}</span>
  )

const TidbitActivityLastReply: React.FC<ITidbitActivityProps> = ({
  date,
  url,
  user,
  userName,
}) => {
  const poster = <TidbitActivityUser user={user} userName={userName} />
  const timestamp = <TidbitActivityTimestamp date={date} url={url} />

  return (
    <TidbitItem className="tidbit-last-reply">
      <Trans id="tidbit.activity">
        By {poster} {timestamp}
      </Trans>
    </TidbitItem>
  )
}

const TidbitActivityStart: React.FC<ITidbitActivityProps> = ({
  date,
  url,
  user,
  userName,
}) => {
  const poster = <TidbitActivityUser user={user} userName={userName} />
  const timestamp = <TidbitActivityTimestamp date={date} url={url} />

  return (
    <TidbitItem className="tidbit-start">
      <Trans id="tidbit.activity">
        By {poster} {timestamp}
      </Trans>
    </TidbitItem>
  )
}

export { TidbitActivityLastReply, TidbitActivityStart }
