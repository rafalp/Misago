import { ApolloProvider, useQuery } from "@apollo/react-hooks";
import ApolloClient, { gql } from "apollo-boost";
import React, { Suspense } from "react";

const client = new ApolloClient({
  uri: "/graphql/"
});

const App: React.FC = () => {
  return (
    <ApolloProvider client={client}>
      <GraphQLTest />
    </ApolloProvider>
  );
};

const Navbar = React.lazy(() => import("./Navbar"));

const INITIAL_DATA = gql`
  query InitialData {
    auth {
      id
      name
      avatars {
        size
        url
      }
    }
    settings {
      forumName
    }
  }
`;

interface IAvatar {
  size: number;
  url: string;
}

interface ISiteSettings {
  auth: {
    id: string;
    name: string;
    avatars: Array<IAvatar>;
  };
  settings: {
    forumName: string;
  };
}

const GraphQLTest: React.FC = () => {
  const { loading, data } = useQuery<ISiteSettings>(INITIAL_DATA);

  return (
    <div>
      <Suspense fallback={<div>Loading...</div>}>
        <Navbar />
        <div>{loading ? "..." : (data && data.settings.forumName)}</div>
      </Suspense>
    </div>
  );
};

export default App;
