import { ApolloProvider, useQuery } from '@apollo/react-hooks';
import ApolloClient, { gql } from 'apollo-boost';
import React from 'react';

const client = new ApolloClient({
  uri: '/graphql/',
});

const App: React.FC = () => {
  return (
    <ApolloProvider client={client}>
      <GraphQLTest />
    </ApolloProvider>
  );
}

const SITE_SETTINGS = gql`
  query SiteSettings {
    settings {
      forumName
    }
  }
`;

interface ISiteSettings {
  settings: {
    forumName: string
  }
};

const GraphQLTest: React.FC = () => {
  const { loading, data } = useQuery<ISiteSettings>(SITE_SETTINGS);

  if (loading) return <div>...</div>;
  if (!data) return <div>nope!</div>;
  return <div>{data.settings.forumName}</div>
}

export default App;
