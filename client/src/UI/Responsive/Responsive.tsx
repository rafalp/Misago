import classNames from "classnames"
import React from "react"

interface IResponsiveProps {
  children: React.ReactNode
  className?: string | null
  desktop?: boolean
  tablet?: boolean
  mobile?: boolean
  landscape?: boolean
  portrait?: boolean
}

const Responsive: React.FC<IResponsiveProps> = ({
  children,
  className,
  desktop: lg,
  tablet: md,
  mobile: sm,
  landscape: s,
  portrait: xs,
}) => (
  <div
    className={classNames(className, {
      "d-none": !xs && (s || md || lg),

      "d-sm-none": xs && !(s || sm),
      "d-sm-block": !xs && (s || sm),

      "d-md-block": !(s || sm) && md,
      "d-md-none": (s || sm) && !md,

      "d-lg-block": !md && lg,
      "d-lg-none": md && !lg,
    })}
  >
    {children}
  </div>
)

export default Responsive
