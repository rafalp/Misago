import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"
import TidbitNumber from "./TidbitNumber"

interface ITidbitThreadsProps {
  threads: number
}

const TidbitThreads: React.FC<ITidbitThreadsProps> = ({ threads }) => (
  <TidbitItem className="tidbit-threads">
    <Plural
      id="tidbit.threads"
      value={threads}
      one={<Trans><TidbitNumber>#</TidbitNumber> thread</Trans>}
      other={<Trans><TidbitNumber>#</TidbitNumber> threads</Trans>}
    />
  </TidbitItem>
)

export default TidbitThreads