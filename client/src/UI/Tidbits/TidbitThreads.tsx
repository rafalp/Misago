import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"

interface ITidbitThreadsProps {
  threads: number
}

const TidbitThreads: React.FC<ITidbitThreadsProps> = ({ threads }) => (
  <TidbitItem className="tidbit-threads">
    <Plural
      id="tidbit.threads"
      value={threads}
      one={<Trans>{Number(threads).toLocaleString("en")} thread</Trans>}
      few={<Trans>{Number(threads).toLocaleString("en")} threads</Trans>}
      other={<Trans>{Number(threads).toLocaleString("en")} threads</Trans>}
    />
  </TidbitItem>
)

export default TidbitThreads