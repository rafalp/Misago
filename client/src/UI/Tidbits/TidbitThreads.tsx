import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"
import TidbitNumber from "./TidbitNumber"

interface TidbitThreadsProps {
  value: number
}

const TidbitThreads: React.FC<TidbitThreadsProps> = ({ value }) => (
  <TidbitItem className="tidbit-threads">
    <Plural
      id="tidbit.threads"
      value={value}
      one={
        <Trans>
          <TidbitNumber>#</TidbitNumber> thread
        </Trans>
      }
      other={
        <Trans>
          <TidbitNumber>#</TidbitNumber> threads
        </Trans>
      }
    />
  </TidbitItem>
)

export default TidbitThreads
