import { Plural, Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"
import TidbitNumber from "./TidbitNumber"

interface ITidbitMembersProps {
  value: number
}

const TidbitMembers: React.FC<ITidbitMembersProps> = ({ value }) => (
  <TidbitItem className="tidbit-members">
    <Plural
      id="tidbit.members"
      value={value}
      one={
        <Trans>
          <TidbitNumber>#</TidbitNumber> member
        </Trans>
      }
      other={
        <Trans>
          <TidbitNumber>#</TidbitNumber> members
        </Trans>
      }
    />
  </TidbitItem>
)

export default TidbitMembers
