import { Trans } from "@lingui/macro"
import React from "react"
import TidbitItem from "./TidbitItem"

const TidbitClosed: React.FC = () => (
  <TidbitItem className="tidbit-closed">
    <Trans id="tidbit.closed">Closed</Trans>
  </TidbitItem>
)

export default TidbitClosed
