import React from "react"
import ClickTrap from "../ClickTrap"

interface IResetScrollOnNavProps {
  children: React.ReactNode
  selector?: string
}

const ResetScrollOnNav: React.FC<IResetScrollOnNavProps> = ({
  children,
  selector,
}) => (
  <ClickTrap
    onClick={() => {
      if (selector) {
        const element = document.querySelector(selector)
        if (element) {
          const offset =
            element.getBoundingClientRect().top +
            document.documentElement.scrollTop
          console.log(offset)
          window.scrollTo(0, offset - 10)
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
