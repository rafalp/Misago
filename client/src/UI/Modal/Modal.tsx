import classnames from "classnames"
import React from "react"
import ModalBacktrop from "./ModalBacktrop"
import useTransition from "./useTransition"

interface ModalProps {
  children: React.ReactNode
  isOpen: boolean
  resistant?: boolean
  close: () => void
}

const Modal: React.FC<ModalProps> = ({
  children,
  isOpen,
  resistant = false,
  close,
}) => {
  const { display, fade } = useTransition(isOpen)
  if (!display) return null

  return (
    <div onClick={resistant ? undefined : close}>
      <div
        className={classnames("modal", "d-block", "fade", { show: fade })}
        tabIndex={-1}
        role="dialog"
        aria-hidden={fade ? "false" : "true"}
        onKeyDown={({ keyCode }) => {
          if (keyCode === 27) close()
        }}
        onSubmit={(event) => {
          // Prevent form submit events from propagating from modals
          // Used when form opens modals containing forms
          event.stopPropagation()
        }}
      >
        {children}
      </div>
      <ModalBacktrop fade={fade} onClick={resistant ? undefined : close} />
    </div>
  )
}

export default Modal
