interface City {
  latitude: number;
  longitude: number;
  name: string;
}

export interface Building {
  city: City;
  floors: number;
  height: number;
  id: string;
  link: string;
  name: string;
  status: string;
}
