import { gql } from 'apollo-boost';

export const BUILDINGS = gql`
  {
    buildings {
      id
      floors
      height
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
