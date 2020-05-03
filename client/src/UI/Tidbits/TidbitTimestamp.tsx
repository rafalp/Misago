import { I18n } from "@lingui/react"
import { Link } from "react-router-dom"
import React from "react"
import Timestamp from "../Timestamp"
import { formatDate } from "../formats"
import TidbitItem from "./TidbitItem"

interface ITidbitTimestampProps {
  date: Date
  url?: string
}

const TidbitTimestamp: React.FC<ITidbitTimestampProps> = ({ date, url }) => (
  <I18n>
    {({ i18n: { language } }) => (
      <TidbitItem className="tidbit-date" title={formatDate(date, language)}>
        {url ? (
          <Link to={url}>
            <Timestamp date={date} language={language} />
          </Link>
        ) : (
          <Timestamp date={date} language={language} />
        )}
      </TidbitItem>
    )}
  </I18n>
)

export default TidbitTimestamp
