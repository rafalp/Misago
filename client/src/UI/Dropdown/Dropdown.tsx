import { Instance, createPopper } from "@popperjs/core"
import classnames from "classnames"
import React from "react"
import portal from "../portal"

interface IToggleArgs {
  ref: React.MutableRefObject<HTMLButtonElement | null>
  close: () => void
  toggle: () => void
}

interface IMenuArgs {
  close: () => void
}

interface DropdownProps {
  className?: string | null
  resistant?: boolean
  placement?:
    | "bottom"
    | "bottom-end"
    | "bottom-start"
    | "top"
    | "top-start"
    | "top-end"
    | "left"
    | "right"
  toggle: (args: IToggleArgs) => React.ReactNode
  menu: (args: IMenuArgs) => React.ReactNode
}

const Dropdown: React.FC<DropdownProps> = ({
  className,
  menu,
  placement,
  resistant,
  toggle,
}) => {
  const [isOpen, updateOpen] = React.useState(false)
  const button = React.useRef<HTMLButtonElement | null>(null)
  const dropdown = React.useRef<HTMLDivElement | null>(null)

  React.useLayoutEffect(() => {
    if (!button.current || !dropdown.current) return
    const eventHandler = (event: Event) => {
      if (!isOpen) return
      if (!(event.target instanceof Element)) return
      if (button.current === event.target) return
      if (button.current?.contains(event.target)) return
      if (resistant && dropdown.current === event.target) return
      if (resistant && dropdown.current?.contains(event.target)) return

      updateOpen(false)
    }

    window.document.addEventListener("click", eventHandler)

    let popper: Instance | null = createPopper(
      button.current,
      dropdown.current,
      {
        placement: placement || "bottom-end",
      }
    )

    return () => {
      window.document.removeEventListener("click", eventHandler)

      if (popper) {
        popper.destroy()
        popper = null
      }
    }
  }, [isOpen, placement, resistant])

  return (
    <>
      {toggle({
        ref: button,
        close: () => updateOpen(false),
        toggle: () => updateOpen((state) => !state),
      })}
      {isOpen &&
        portal(
          <div
            className={classnames("dropdown-menu show", className)}
            ref={dropdown}
          >
            {menu({ close: () => updateOpen(false) })}
          </div>
        )}
    </>
  )
}

export default Dropdown
