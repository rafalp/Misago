import { Plural } from "@lingui/macro"
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
      one={"# thread"}
      other={"# threads"}
    />
  </TidbitItem>
)

export default TidbitThreads