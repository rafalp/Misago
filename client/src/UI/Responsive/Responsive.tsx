import classNames from "classnames"
import React from "react"

interface IResponsiveProps {
  children: React.ReactNode
  className?: string | null
  desktop?: boolean
  tablet?: boolean
  mobile?: boolean
}

const Responsive: React.FC<IResponsiveProps> = ({
  children,
  className,
  desktop,
  tablet,
  mobile,
}) => (
  <div
    className={classNames(className, {
      "d-none d-md-block": !mobile && tablet && desktop,
      "d-md-none d-lg-block": mobile && !tablet && desktop,
      "d-lg-none": mobile && tablet && !desktop,
      "d-md-none": mobile && !tablet && !desktop,
      "d-none d-lg-block": !mobile && !tablet && desktop,
      "d-none d-md-block d-lg-none": !mobile && tablet && !desktop,
    })}
  >
    {children}
  </div>
)

export default Responsive
