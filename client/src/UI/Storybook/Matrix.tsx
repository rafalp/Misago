import React from "react"

interface MatrixProps {
  items: Array<
    Array<{
      name: string
      component: React.ReactElement
    }>
  >
}

const Matrix: React.FC<MatrixProps> = ({ items }) => (
  <>
    {items.map((cols, i) => (
      <div className="row m-4" key={i}>
        {cols.map(({ name, component }, l) => (
          <div className="col" key={l}>
            <div className="pb-2">
              <strong>{`${name}:`}</strong>
            </div>
            {component}
          </div>
        ))}
      </div>
    ))}
  </>
)

export default Matrix
