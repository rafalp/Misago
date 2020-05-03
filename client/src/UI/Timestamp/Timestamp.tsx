import { Plural, Trans } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { formatDateShort } from "../formats"

interface ITimestampProps {
  date: Date
  language?: string
}

const Timestamp: React.FC<ITimestampProps> = ({ date, language }) => {
  const now = new Date()
  const diff = (now.getTime() - date.getTime()) / 1000

  // Test future dates with 15s offset for small
  // clock differences between client and user
  if (diff > -15) {
    if (diff < 90) {
      return <Trans id="time.moment_ago">a moment ago</Trans>
    }

    if (diff < 3600) {
      return (
        <Plural
          id="time.minutes_ago"
          value={Math.floor(diff / 60)}
          one="# minute ago"
          other="# minutes ago"
        />
      )
    }

    if (diff < 3600 * 24) {
      return (
        <Plural
          id="time.hours_ago"
          value={Math.floor(diff / 3600)}
          one="# hour ago"
          other="# hours ago"
        />
      )
    }

    if (diff < 3600 * 24 * 6) {
      return (
        <Plural
          id="time.days_ago"
          value={Math.floor(diff / (24 * 3600))}
          one="# day ago"
          other="# days ago"
        />
      )
    }
  } else {
    if (diff > -90) {
      return <Trans id="time.in_moment">in a moment</Trans>
    }

    if (diff > -3600) {
      return (
        <Plural
          id="time.in_minutes"
          value={Math.floor(diff / 60) * -1}
          one="in # minute"
          other="in # minutes"
        />
      )
    }

    if (diff > -3600 * 24) {
      return (
        <Plural
          id="time.in_hours"
          value={Math.floor(diff / 3600) * -1}
          one="in # hour"
          other="in # hours"
        />
      )
    }

    if (diff > -3600 * 24 * 6) {
      return (
        <Plural
          id="time.in_days"
          value={Math.floor(diff / (24 * 3600)) * -1}
          one="in # day"
          other="in # days"
        />
      )
    }

    if (language) {
      return <Trans id="time.on">on {formatDateShort(date, language)}</Trans>
    }

    return (
      <I18n>
        {({ i18n: { language } }) => (
          <Trans id="time.on">on {formatDateShort(date, language)}</Trans>
        )}
      </I18n>
    )
  }

  if (language) {
    return <>{formatDateShort(date, language)}</>
  }

  return (
    <I18n>{({ i18n: { language } }) => formatDateShort(date, language)}</I18n>
  )
}

export default Timestamp
