import * as React from 'react';
import { ApolloProvider } from '@apollo/react-hooks';

import { client } from './lib/graphql';
import Buildings from './Buildings';

const App = () => (
  <ApolloProvider client={client}>
    <Buildings/>
  </ApolloProvider>
)

export default App;
