import { StringValueNode } from "graphql";

interface ICity {
  name: string;
}

export interface IBuilding {
    name: string;
    floors: number;
    height: number;
    id: string;
    city: ICity;
    status: string;
}
