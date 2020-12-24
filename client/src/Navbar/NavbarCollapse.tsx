import { t } from "@lingui/macro"
import className from "classnames"
import React from "react"
import Avatar from "../UI/Avatar"
import { User } from "./Navbar.types"

interface NavbarCollapseProps {
  children: React.ReactNode
  user?: User | null
}

const NavbarCollapse: React.FC<NavbarCollapseProps> = ({ children, user }) => {
  const [isOpen, updateOpen] = React.useState(false)
  const button = React.useRef<HTMLButtonElement | null>(null)

  React.useEffect(() => {
    const eventHandler = (event: Event) => {
      if (!isOpen) return
      if (!(event.target instanceof Element)) return
      if (button.current === event.target) return
      if (button.current?.contains(event.target)) return

      updateOpen(false)
    }

    window.document.addEventListener("click", eventHandler)

    return () => window.document.removeEventListener("click", eventHandler)
  }, [isOpen])

  return (
    <>
      <button
        className={className("navbar-toggler", {
          "navbar-toggler-user": user,
        })}
        ref={button}
        type="button"
        aria-controls="navbarToggle"
        aria-expanded={isOpen ? "true" : "false"}
        aria-label={t({ id: "navbar.toggle", message: "Toggle navigation" })}
        onClick={() => updateOpen((state) => !state)}
      >
        {user ? (
          <Avatar size={30} user={user} />
        ) : (
          <span className="navbar-toggler-icon"></span>
        )}
      </button>
      <div
        className={className("collapse", "navbar-collapse", {
          show: isOpen,
        })}
        id="navbarToggle"
      >
        {children}
      </div>
    </>
  )
}

export default NavbarCollapse
