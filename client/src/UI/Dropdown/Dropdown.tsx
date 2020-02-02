import { Instance, createPopper } from "@popperjs/core"
import classNames from "classnames"
import React from "react"
import portal from "../../portal"

interface IToggleArgs {
  ref: React.MutableRefObject<HTMLButtonElement>
  close: () => void
  toggle: () => void
}

interface IDropdownProps {
  className?: string | null
  menu: React.ReactNode
  leftAligned?: boolean
  toggle: (args: IToggleArgs) => React.ReactNode
}

const Dropdown: React.FC<IDropdownProps> = ({ className, menu, leftAligned, toggle }) => {
  const [isOpen, updateOpen] = React.useState(false)
  const button = React.useRef<HTMLButtonElement>()
  const dropdown = React.useRef<HTMLDivElement | null>(null)

  React.useLayoutEffect(() => {
    if (!button.current || !dropdown.current) return
    const eventHandler = (event: Event) => {
      if (!isOpen) return
      if (!(event.target instanceof Element)) return
      if (button.current === event.target) return
      if (button.current?.contains(event.target)) return

      updateOpen(false)
    }

    window.document.addEventListener("click", eventHandler)

    let popper: Instance | null = createPopper(
      button.current,
      dropdown.current,
      {
        placement: leftAligned ? "bottom-start" : "bottom-end",
      }
    )

    return () => {
      if (popper) {
        window.document.removeEventListener("click", eventHandler)
        popper.destroy()
        popper = null
      }
    }
  }, [isOpen, leftAligned])

  return (
    <>
      {toggle({
        ref: button,
        close: () => updateOpen(false),
        toggle: () => updateOpen(state => !state),
      })}
      {isOpen && portal(
        <div className={classNames("dropdown-menu show", className )} ref={dropdown}>
          {menu}
        </div>
      )}
    </>
  )
}

export default Dropdown
