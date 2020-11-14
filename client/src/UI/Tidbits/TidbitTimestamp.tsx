import { useLingui } from "@lingui/react"
import { Link } from "react-router-dom"
import React from "react"
import Timestamp from "../Timestamp"
import { formatDate } from "../formats"
import TidbitItem from "./TidbitItem"

interface ITidbitTimestampProps {
  date: Date
  url?: string
}

const TidbitTimestamp: React.FC<ITidbitTimestampProps> = ({ date, url }) => {
  const { i18n } = useLingui()
  const locale = i18n.locale

  return (
    <TidbitItem className="tidbit-date" title={formatDate(date, locale)}>
      {url ? (
        <Link to={url}>
          <Timestamp date={date} locale={locale} />
        </Link>
      ) : (
        <Timestamp date={date} locale={locale} />
      )}
    </TidbitItem>
  )
}

export default TidbitTimestamp
