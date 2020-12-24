import { Trans } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import { Link } from "react-router-dom"
import React from "react"
import * as urls from "../../urls"
import Timestamp from "../Timestamp"
import { formatDate } from "../formats"
import TidbitItem from "./TidbitItem"

interface TidbitActivityTimestampProps {
  date: Date
  url?: string
}

interface TidbitActivityUserProps {
  user?: {
    id: string
    slug: string
    name: string
  } | null
  userName: string
}

interface TidbitActivityProps
  extends TidbitActivityTimestampProps,
    TidbitActivityUserProps {}

const TidbitActivityTimestamp: React.FC<TidbitActivityTimestampProps> = ({
  date,
  url,
}) => {
  const { i18n } = useLingui()
  const locale = i18n.locale

  if (url) {
    return (
      <Link
        className="tidbit-activity-timestamp"
        to={url}
        title={formatDate(date, locale)}
      >
        <Timestamp date={date} locale={locale} prefixed />
      </Link>
    )
  }

  return (
    <span
      className="tidbit-activity-timestamp"
      title={formatDate(date, locale)}
    >
      <Timestamp date={date} locale={locale} prefixed />
    </span>
  )
}

const TidbitActivityUser: React.FC<TidbitActivityUserProps> = ({
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

const TidbitActivityLastReply: React.FC<TidbitActivityProps> = ({
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
        {poster} {timestamp}
      </Trans>
    </TidbitItem>
  )
}

const TidbitActivityStart: React.FC<TidbitActivityProps> = ({
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
        {poster} {timestamp}
      </Trans>
    </TidbitItem>
  )
}

export { TidbitActivityLastReply, TidbitActivityStart }
