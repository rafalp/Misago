import React from "react"
import Tribute from "tributejs"
import useSearchUsersQuery from "./useSearchUsersQuery"

interface IEditorMentionsProps {
  children: React.ReactNode
  name: string
}

const EditorMentions: React.FC<IEditorMentionsProps> = ({
  children,
  name,
}) => {
  const container = React.useRef<HTMLDivElement>(null)
  const element = container.current
  const tribute = React.useRef<Tribute<any> | null>(null)

  const searchUsers = useSearchUsersQuery()

  React.useEffect(() => {
    if (!element || tribute.current) return

    const textarea = element.querySelector("textarea")
    if (!textarea) return

    tribute.current = new Tribute({
      collection: [
        {
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
    })

    tribute.current.attach(textarea)

    return () => {
      if (tribute.current) tribute.current.detach(textarea)
    }
  }, [element, name, searchUsers])

  return <div ref={container}>{children}</div>
}

export default EditorMentions
