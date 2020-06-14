import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import React from "react"
import { useHistory } from "react-router-dom"
import { useCategoriesListContext } from "../../Context"
import { RouteContainer } from "../../UI"
import { IMutationError } from "../../types"
import * as urls from "../../urls"

const POST_THREAD = gql`
  mutation PostThread($input: PostThreadInput!) {
    postThread(input: $input) {
      errors {
        location
        message
        type
      }
      thread {
        id
        title
        slug
      }
    }
  }
`

interface IStartThreadMutationData {
  postThread: {
    errors: Array<IMutationError> | null
    thread: {
      id: string
      title: string
      slug: string
    } | null
  }
}

interface IStartThreadMutationValues {
  input: {
    category: string
    title: string
    body: string
  }
}

const StartThreadRoute: React.FC = () => {
  const history = useHistory()
  const categories = useCategoriesListContext()
  const [category, setCategory] = React.useState("")
  const [title, setTitle] = React.useState("")
  const [body, setBody] = React.useState("")

  const [postThread] = useMutation<
    IStartThreadMutationData,
    IStartThreadMutationValues
  >(POST_THREAD, { errorPolicy: "all" })

  return (
    <RouteContainer>
      <br />
      <div>
        <label>Category:</label>
        <select
          className="form-control"
          value={category}
          onChange={({ target }) => setCategory(target.value)}
        >
          <option value="">Select category</option>
          {categories.map(({ depth, category: { id, name } }) => (
            <option value={id}>{depth ? "-   " + name : name}</option>
          ))}
        </select>
      </div>
      <br />
      <div>
        <label>Title:</label>
        <input
          className="form-control"
          type="text"
          value={title}
          onChange={({ target }) => setTitle(target.value)}
        />
      </div>
      <br />
      <div>
        <label>Post:</label>
        <textarea
          className="form-control"
          rows={10}
          value={body}
          onChange={({ target }) => setBody(target.value)}
        />
      </div>
      <br />
      <button
        type="button"
        onClick={async () => {
          const input = {
            body,
            category,
            title,
          }

          try {
            const result = await postThread({ variables: { input } })
            if (result.data?.postThread?.thread) {
              history.push(urls.thread(result.data?.postThread?.thread))
            }
          } catch (error) {
            // do nothing when postThread throws
            return
          }
        }}
      >
        Submit
      </button>
      <br />
    </RouteContainer>
  )
}

export default StartThreadRoute
