import ApolloClient from 'apollo-boost';
import gql from 'graphql-tag';

export const client = new ApolloClient({
  uri: 'http://localhost:5000/graphql',
});

export const graphqlTest = () =>
  client
    .query({
      query: gql`
        {
          buildings {
            id
            name
            city {
              id
              name
            }
          }
        }
        `
    })
    .then(result => console.log(result));
