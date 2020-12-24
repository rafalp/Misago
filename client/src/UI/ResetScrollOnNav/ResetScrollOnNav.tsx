import React from "react"
import ClickTrap from "../ClickTrap"

interface ResetScrollOnNavProps {
  children: React.ReactNode
  selector?: string
}

const ResetScrollOnNav: React.FC<ResetScrollOnNavProps> = ({
  children,
  selector,
}) => (
  <ClickTrap
    onClick={() => {
      if (selector) {
        const element = document.querySelector(selector)
        if (element) {
          const top = element.getBoundingClientRect().top
          const scroll = document.documentElement.scrollTop
          window.scrollTo(0, top + scroll - 10)
        } else {
          window.scrollTo(0, 0)
        }
      } else {
        window.scrollTo(0, 0)
      }
    }}
  >
    {children}
  </ClickTrap>
)

export default ResetScrollOnNav
