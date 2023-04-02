import { withParams } from "react-router-dom"

export function withParams(Component) {
  return props => <Component {...props} params={useParams()} />;
}