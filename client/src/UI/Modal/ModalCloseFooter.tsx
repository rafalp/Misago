import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonPrimary } from "../Button"
import ModalFooter from "./ModalFooter"

interface ModalFooterProps {
  className?: string
  close: () => void
}

const ModalCloseFooter: React.FC<ModalFooterProps> = ({
  className,
  close,
}) => (
  <ModalFooter className={className}>
    <ButtonPrimary
      text={<Trans id="close">Close</Trans>}
      onClick={close}
      responsive
    />
  </ModalFooter>
)

export default ModalCloseFooter
