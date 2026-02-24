import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class IotService {
  private path: string = "http://localhost:5050"

  constructor(private httpClient: HttpClient) { }

  sendDMSPassword(typed_password: string): Observable<any> {
    const body = { password: typed_password };
    return this.httpClient.post(`${this.path}/dms_input`, body);
  }

  setRGB(number: string): Observable<any>{
    const body = { selected_number: number};
    return this.httpClient.post(`${this.path}/set_rgb`, body);
  }

  setKitchenTimer(number: number): Observable<any>{
    const body = { total_seconds: number};
    return this.httpClient.post(`${this.path}/start_kitchen_timer`, body);
  }

  addToKitchenTimer(added_seconds: number): Observable<any>{
    const body = { seconds_to_add: added_seconds};
    return this.httpClient.post(`${this.path}/add_to_kitchen_timer`, body);
  }

  getSystemStatus(): Observable<any>{
    return this.httpClient.get(`${this.path}/system_status`);
  }
}
