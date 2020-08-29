import { Trans } from "@lingui/macro"
import React from "react"
import TidbitIcon from "./TidbitIcon"
import TidbitItem from "./TidbitItem"

const TidbitClosed: React.FC = () => (
  <TidbitItem className="tidbit-closed">
    <TidbitIcon icon="fas fa-lock" />
    <Trans id="tidbit.closed">Closed</Trans>
  </TidbitItem>
)

export default TidbitClosed
