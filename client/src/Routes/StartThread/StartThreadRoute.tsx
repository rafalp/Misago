import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import React from "react"
import { CategoriesContext } from "../../Context"
import { RouteContainer } from "../../UI"
import { IMutationError } from "../../types"

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
      }
    }
  }
`

interface IStartThreadMutationData {
  login: {
    errors: Array<IMutationError> | null
    user: {
      id: string
      name: string
    } | null
    token: string | null
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
  const categories = React.useContext(CategoriesContext)
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
          {categories.map(({ children, id, name }) => (
            <React.Fragment key={id}>
              <option value={id}>{name}</option>
              {children.map(({ id, name }) => (
                <option key={id} value={id}>{`- - ${name}`}</option>
              ))}
            </React.Fragment>
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

          const data = await postThread({ variables: { input } })
          console.log(data)
        }}
      >
        Submit
      </button>
      <br />
    </RouteContainer>
  )
}

export default StartThreadRoute
