interface City {
  name: string;
}

export interface Building {
    name: string;
    floors: number;
    height: number;
    id: string;
    city: City;
    status: string;
}
