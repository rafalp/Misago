import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"
import TidbitNumber from "./TidbitNumber"

interface ITidbitRepliesProps {
  value: number
}

const TidbitReplies: React.FC<ITidbitRepliesProps> = ({ value }) => (
  <TidbitItem className="tidbit-replies">
    <Plural
      id="tidbit.replies"
      value={value}
      one={
        <Trans>
          <TidbitNumber>#</TidbitNumber> reply
        </Trans>
      }
      other={
        <Trans>
          <TidbitNumber>#</TidbitNumber> replies
        </Trans>
      }
    />
  </TidbitItem>
)

export default TidbitReplies
