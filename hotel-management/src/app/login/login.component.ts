import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';
@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  onLogin() {
  this.http.post<any>(`${environment.apiUrl}/login`, {
    username: this.username,
    password: this.password
  }).subscribe({
    next: (res) => {
      if (res.success) {
        localStorage.setItem('isLoggedIn', 'true');
        this.router.navigate(['/hotels']);
      } else {
        this.errorMessage = res.message;
      }
    },
    error: () => {
      this.errorMessage = "Login failed!";
    }
  });
}

}
