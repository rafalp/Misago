import { Plural, Trans } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import React from "react"
import { formatDateShort, formatTime } from "../formats"

interface TimestampProps {
  date: Date
  locale?: string
  prefixed?: boolean
}

const Timestamp: React.FC<TimestampProps> = ({ date, locale, prefixed }) => {
  const { i18n } = useLingui()

  const now = new Date()
  const diff = (now.getTime() - date.getTime()) / 1000

  const [state, setState] = React.useState<{} | null>(null)
  const update = React.useCallback(() => setState({}), [])

  React.useEffect(() => {
    // Update "x minutes" every 50s
    if (Math.abs(diff) < 3600) {
      const timeout = window.setTimeout(update, 50 * 1000)
      return () => window.clearTimeout(timeout)
    }

    // Update "x hours" every 20 minutes
    if (Math.abs(diff) < 3600 * 12) {
      const timeout = window.setTimeout(update, 20 * 60 * 1000)
      return () => window.clearInterval(timeout)
    }

    // Update "x days" every 40 minutes
    if (Math.abs(diff) < 3600 * 24 * 6) {
      const timeout = window.setTimeout(update, 40 * 60 * 1000)
      return () => window.clearInterval(timeout)
    }
  }, [diff, state, update])

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

    if (diff < 3600 * 12) {
      return (
        <Plural
          id="time.hours_ago"
          value={Math.floor(diff / 3600)}
          one="# hour ago"
          other="# hours ago"
        />
      )
    }

    if (diff < 3600 * 48) {
      if (now.getDay() === date.getDay()) {
        return (
          <Trans id="time.today">
            today at {formatTime(date, locale || i18n.locale)}
          </Trans>
        )
      }

      return (
        <Trans id="time.yesterday">
          yesterday at {formatTime(date, locale || i18n.locale)}
        </Trans>
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
  }

  if (prefixed) {
    if (locale) {
      return <Trans id="time.on">on {formatDateShort(date, locale)}</Trans>
    }

    return (
      <Trans id="time.on">
        on {formatDateShort(date, locale || i18n.locale)}
      </Trans>
    )
  }

  if (locale) {
    return <>{formatDateShort(date, locale)}</>
  }

  return <>{formatDateShort(date, locale || i18n.locale)}</>
}

export default Timestamp
