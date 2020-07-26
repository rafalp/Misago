import React from "react"
import { useFormContext } from "react-hook-form"
import { useFieldContext, useSelection } from "../../../../UI"
import { IMutationError } from "../../../../types"
import { IPost } from "../../Thread.types"
import ThreadPostsModerationSelectedPostsListItem from "./ThreadPostsModerationSelectedPostsListItem"

interface IThreadPostsModerationSelectedPostsListProps {
  errors?: Record<string, IMutationError>
  posts: Array<IPost>
  messages?: {
    [type: string]: React.ReactNode
  } | null
}

const ThreadPostsModerationSelectedPostsList: React.FC<IThreadPostsModerationSelectedPostsListProps> = ({
  errors,
  posts,
  messages,
}) => {
  const context = useFieldContext()
  const name = context ? context.name : undefined

  const { register, unregister, setValue } = useFormContext() || {}
  const { change, selection, selected } = useSelection<IPost>(posts, posts)

  React.useEffect(() => {
    if (register && unregister) {
      register({ name: "posts" })
      return () => unregister("posts")
    }
  }, [register, unregister])

  React.useEffect(() => {
    if (name && setValue) {
      setValue("posts", selected)
    }
  }, [name, setValue, selected])

  return (
    <ul className="selected-items selected-posts">
      {posts.map((post) => (
        <ThreadPostsModerationSelectedPostsListItem
          disabled={context && context.disabled}
          error={errors && errors[post.id]}
          id={context && `${context.id}_${context.name}`}
          key={post.id}
          selected={selection[post.id]}
          post={post}
          messages={messages}
          changeSelection={change}
        />
      ))}
    </ul>
  )
}

export default ThreadPostsModerationSelectedPostsList
