import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"
import { ButtonDark } from "../../../UI/Button"
import { useThreadReplyContext } from "../ThreadReply"
import getQuoteSelection from "./getQuoteSelection"

interface ThreadQuoteSelectionProps {
  children: React.ReactNode
}

const ThreadQuoteSelection: React.FC<ThreadQuoteSelectionProps> = ({
  children,
}) => {
  const user = useAuthContext()
  const reply = useThreadReplyContext()

  const [range, setRange] = React.useState<Range | null>(null)
  const [rect, setRect] = React.useState<DOMRect | null>(null)
  const ref = React.useRef<HTMLDivElement | null>(null)
  const [init, setInit] = React.useState(false)

  React.useEffect(() => {
    if (range) {
      setRect(range.getBoundingClientRect())
    } else {
      setRect(null)
    }
  }, [range, setRect])

  const selected = React.useCallback(() => {
    if (ref.current) {
      const range = getQuoteSelection(ref.current)
      setRange(range || null)
    }
  }, [ref, setRange])

  React.useEffect(() => {
    if (user && init && ref.current) {
      ref.current.addEventListener("mouseup", selected)
      return () => {
        ref.current?.removeEventListener("mouseup", selected)
      }
    }
  }, [user, init, ref, selected])

  return (
    <div
      ref={(element) => {
        if (element) {
          ref.current = element
          setInit(true)
        }
      }}
    >
      {children}
      {rect && (
        <div
          className="quote-control"
          style={{
            position: "absolute",
            left: rect.left + window.scrollX,
            top: rect.bottom + window.scrollY,
          }}
        >
          <ButtonDark
            icon="fas fa-quote-left"
            text={<Trans id="quote_selected">Quote</Trans>}
            small
            onClick={() => {
              if (reply && range) reply.quote(range)
              setRange(null)
              setRect(null)
            }}
          />
        </div>
      )}
    </div>
  )
}

export default ThreadQuoteSelection
