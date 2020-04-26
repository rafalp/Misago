import React from "react"

const INTERVAL = 1000
const INTERVAL_DESKTOP = 600
const BREAKPOINT = 768

interface IViewportEventProps {
  children?: React.ReactNode
  className?: string
  desktopOnly?: boolean
  disabled?: boolean
  oneTime?: boolean
  onEnter?: () => void
}

const ViewportEvent: React.FC<IViewportEventProps> = ({
  children,
  className,
  desktopOnly,
  disabled,
  oneTime,
  onEnter,
}) => {
  const container = React.useRef<HTMLDivElement>(null)

  React.useEffect(() => {
    if (disabled || !onEnter || !container.current) return

    const poll = window.setInterval(
      () => {
        if (desktopOnly && window.innerWidth < BREAKPOINT) return

        const rect =
          container.current && container.current.getBoundingClientRect()

        if (rect && rect.bottom > 0 && rect.bottom <= window.innerHeight) {
          onEnter()
          if (oneTime) window.clearInterval(poll)
        }
      },
      desktopOnly ? INTERVAL_DESKTOP : INTERVAL
    )

    return () => window.clearInterval(poll)
  }, [desktopOnly, disabled, oneTime, onEnter])

  return (
    <div className={className} ref={container}>
      {children}
    </div>
  )
}

export default ViewportEvent
