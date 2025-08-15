import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Hotel {
  id?: number;
  name: string;
  location: string;
  rating: number;
  image?: string;
}

@Injectable({
  providedIn: 'root'
})
export class HotelService {
  private apiUrl = `${environment.apiUrl}/hotels`;

  constructor(private http: HttpClient) {}

  getHotels(): Observable<Hotel[]> {
    return this.http.get<Hotel[]>(this.apiUrl);
  }

  getHotelById(id: number): Observable<Hotel> {
    return this.http.get<Hotel>(`${this.apiUrl}/${id}`);
  }

  createHotel(hotel: Hotel): Observable<any> {
    return this.http.post(this.apiUrl, hotel);
  }

  updateHotel(id: number, hotel: Partial<Hotel>): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, hotel);
  }

  deleteHotel(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`);
  }
}
