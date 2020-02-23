import { StringValueNode } from "graphql";

interface ICity {
  name: string;
}

export interface IBuilding {
    name: string;
    height: number;
    id: string;
    city: ICity;
}
