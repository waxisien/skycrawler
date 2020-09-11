import { gql } from 'apollo-boost';

export const BUILDINGS = gql`
  {
    buildings {
      id
      floors
      height
      link
      name
      city {
        name
        latitude
        longitude
      }
      status
    }
  }
`;
