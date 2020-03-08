interface City {
  name: string;
  latitude: number;
  longitude: number;
}

export interface Building {
    name: string;
    floors: number;
    height: number;
    id: string;
    city: City;
    status: string;
}
