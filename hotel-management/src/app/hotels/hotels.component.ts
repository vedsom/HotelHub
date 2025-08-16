import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HotelService, Hotel } from '../services/hotel.service';

@Component({
  selector: 'app-hotels',
  templateUrl: './hotels.component.html',
  styleUrls: ['./hotels.component.css']
})
export class HotelsComponent implements OnInit {
  hotels: Hotel[] = [];
  selectedTab: string = 'view';
  newHotel: Hotel = { name: '', location: '', rating: 0, image: '' };
  editHotelData: Hotel | null = null;

  constructor(private hotelService: HotelService, private router: Router) {}

  ngOnInit() {
    this.loadHotels();
  }

  setTab(tab: string) {
    this.selectedTab = tab;
    if (tab === 'view') {
      this.loadHotels();
    }
  }

  loadHotels() {
    this.hotelService.getHotels().subscribe(data => {
      this.hotels = data;
    });
  }

  startEdit(hotel: Hotel) {
    this.editHotelData = { ...hotel }; // Make a copy
    this.selectedTab = 'edit';
  }

  addHotel() {
    if (!this.newHotel.name || !this.newHotel.location || !this.newHotel.rating) {
      alert('All fields are required');
      return;
    }
    this.hotelService.createHotel(this.newHotel).subscribe(() => {
      alert('Hotel added');
      this.newHotel = { name: '', location: '', rating: 0, image: '' };
      this.setTab('view');
    });
  }

  updateHotel() {
    if (!this.editHotelData?.id) {
      alert('Invalid hotel');
      return;
    }
    this.hotelService.updateHotel(this.editHotelData.id, this.editHotelData).subscribe(() => {
      alert('Hotel updated');
      this.editHotelData = null;
      this.setTab('view');
    });
  }

  deleteHotel(id: number) {
    if (!id) {
      alert('Invalid hotel ID');
      return;
    }
    this.hotelService.deleteHotel(id).subscribe(() => {
      alert('Hotel deleted');
      this.setTab('view');
    });
  }

  logout() {
    localStorage.removeItem('isLoggedIn'); // Clear login status
    this.router.navigate(['/login']);      // Redirect to login page
  }
}
