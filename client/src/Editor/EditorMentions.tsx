import React from "react"
import Tribute from "tributejs"
import useSearchUsersQuery from "./useSearchUsersQuery"

interface IEditorMentionsProps {
  children: React.ReactNode
  mocks?: Array<{
    key: string
    value: string
  }>
}

const EditorMentions: React.FC<IEditorMentionsProps> = ({
  children,
  mocks,
}) => {
  const [initialized, setInitialized] = React.useState(false)
  const container = React.useRef<HTMLDivElement | null>(null)
  const tribute = React.useRef<Tribute<any> | null>(null)

  const searchUsers = useSearchUsersQuery()
  const element = container.current

  React.useEffect(() => {
    if (!initialized || !element || tribute.current) return

    const textarea = element.querySelector("textarea")
    if (!textarea) return

    tribute.current = new Tribute({
      values: mocks,
      collection: mocks ? [] : [
        mocks || {
          values: (text, cb) => {
            searchUsers(text)
              .then((results) =>
                results.map((user) => {
                  return {
                    key: user.fullName
                      ? `${user.fullName} (${user.name})`
                      : user.name,
                    value: user.name,
                  }
                })
              )
              .then(cb)
          },
        },
      ],
      noMatchTemplate: function () {
        return '<span style:"visibility: hidden;"></span>'
      },
      requireLeadingSpace: false,
    })

    tribute.current.attach(textarea)

    return () => {
      if (tribute.current) tribute.current.detach(textarea)
    }
  }, [initialized, element, mocks, searchUsers])

  return (
    <div
      ref={(element) => {
        if (element) {
          container.current = element
          setInitialized(true)
        }
      }}
    >
      {children}
    </div>
  )
}

export default EditorMentions
