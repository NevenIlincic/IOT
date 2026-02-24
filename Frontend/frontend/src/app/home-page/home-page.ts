import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { IotService } from '../../services/iot-service';
import { interval, startWith, Subscription, switchMap } from 'rxjs';

@Component({
  selector: 'app-home-page',
  imports: [CommonModule],
  templateUrl: './home-page.html',
  styleUrl: './home-page.css',
})
export class HomePage {
  private readonly apiUrl = 'http://localhost:5050'; // IP adresa tvog Flask servera

  // Stanja za prikaz na dashboardu
  public systemArmed: boolean = false;
  public alarmActive: boolean = false;
  public peopleInside: number = 0;

  private statusSubscription?: Subscription;
  public systemStatus: any = {
    alarm_state: "NOT_ACTIVE",
    num_people: 0
  }; // Ovde čuvamo podatke sa Flask


  constructor(private iotService: IotService) { }

 ngOnInit(): void {
    this.statusSubscription = interval(5000).pipe(
      startWith(0),
      switchMap(() => this.iotService.getSystemStatus())
    ).subscribe({
      next: (data) => {
        this.systemStatus = data;
        console.log('Status refreshed:', data);
      },
      error: (err) => console.error('Greška pri osvežavanju:', err)
    });
  }

  ngOnDestroy(): void {
    if (this.statusSubscription) {
      this.statusSubscription.unsubscribe();
    }
  }

  // 1. Slanje PIN koda (DMS)
  sendPin(pin: string): void {
    if (pin.length !== 4) {
      alert("PIN must be 4 digits!");
      return;
    }
    this.iotService.sendDMSPassword(pin).subscribe({
      next: (value: any) => {
        console.log("POSLATO");
      }
    });
  }

  setTimer(minutes: string, seconds: string): void {
    const m = parseInt(minutes) || 0;
    const s = parseInt(seconds) || 0;

    // Preračunavamo u ukupne sekunde
    const totalSeconds = (m * 60) + s;

    if (totalSeconds <= 0) {
      alert("Please enter a valid time.");
      return;
    }

    console.log(`Setting timer for ${m}m ${s}s (${totalSeconds} total seconds)`);

    this.iotService.setKitchenTimer(totalSeconds).subscribe({
      next: (value: any) => {
        console.log("TIMER STARTOVAN!");
      }
    });
  }

  // 3. Podešavanje inkrementa za BTN (N sekundi)
  setN(nValue: number): void {
    this.iotService.addToKitchenTimer(nValue).subscribe({
      next: (value: any) => {
        console.log(`DODATO ${nValue} SEKUNDI`);
      }
    });
  }

  setRGBByColor(number: string): void {
    this.iotService.setRGB(number).subscribe({
      next: (value: any) => {
        console.log("POSLATA RGB KOMANDA!");
      }
    });
  }
  setRGB(event: any): void {
    // event.target je zapravo tvoj <input> element
    // event.target.value je string u HEX formatu, npr. "#ff0000" (crvena)
    const color = event.target.value;

    console.log("Izabrana boja iz inputa:", color);

    // this.http.post(`${this.apiUrl}/set_rgb`, { color: color, mode: 'on' }).subscribe();
  }
  toggleRGB(turnOn: boolean): void {
    // const mode = turnOn ? 'on' : 'off';
    // this.http.post(`${this.apiUrl}/set_rgb`, { mode: mode }).subscribe({
    //   next: (res) => console.log('RGB toggled', res)
    // });
  }

  // Pomoćna funkcija za osvežavanje stanja sistema
  refreshStatus(): void {
    // // Pretpostavka: imaš rutu koja vraća trenutno stanje svih senzora
    // this.http.get<any>(`${this.apiUrl}/system_status`).subscribe(status => {
    //   this.systemArmed = status.is_armed;
    //   this.alarmActive = status.alarm_on;
    //   this.peopleInside = status.people_count;
    // });
  }
}
