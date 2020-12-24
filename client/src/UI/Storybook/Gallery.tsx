import React from "react"

interface GalleryProps {
  items: Array<{
    name: string
    component: React.ReactElement
  }>
}

const Gallery: React.FC<GalleryProps> = ({ items }) => (
  <div className="row m-0 p-1">
    {items.map(({ name, component }, i) => (
      <div className="col-3 p-3" key={i}>
        <div className="pb-2">
          <strong>{`${name}:`}</strong>
        </div>
        {component}
      </div>
    ))}
  </div>
)

export default Gallery
