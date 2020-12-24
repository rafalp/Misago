import React from "react"

interface ClickTrapProps {
  className?: string
  children?: React.ReactNode
  onClick: () => void
}

const ClickTrap: React.FC<ClickTrapProps> = ({
  className,
  children,
  onClick,
}) => {
  const ref = React.useRef<HTMLDivElement>(null)
  React.useEffect(() => {
    if (!ref.current) return

    const element = ref.current
    const clickHandler = (event: MouseEvent) => {
      if (event.target instanceof HTMLAnchorElement) {
        window.setTimeout(onClick, 0)
        return
      }

      let parent = (event.target as HTMLElement).parentNode
      while (parent !== null) {
        if (parent instanceof HTMLAnchorElement) {
          window.setTimeout(onClick, 0)
          return
        }
        parent = parent.parentNode
      }
    }

    element.addEventListener("click", clickHandler)
    return () => element.removeEventListener("click", clickHandler)
  }, [onClick])

  return (
    <div className={className} ref={ref}>
      {children}
    </div>
  )
}

export default ClickTrap
