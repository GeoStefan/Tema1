import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Rocket } from './rocket';

const httpOptions = {
  headers: new HttpHeaders({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  })
};

@Injectable({
  providedIn: 'root'
})
export class WebApisService {

  private convertUrl = 'http://localhost:8000/convert';
  private rocketUrl = 'http://localhost:8000/rocket';
  private qrUrl = 'http://localhost:8000/qr';
  private metricsUrl = 'http://localhost:8000/metrics';

  constructor(private http: HttpClient) {
  }

  public getEurToRon(amount: number) {
    return this.http.get<any>(this.convertUrl, { params: { amount: amount.toString() } }).toPromise();
  }

  public getRocket(rocketId: string) {
    const url = this.rocketUrl + '/' + rocketId;
    return this.http.get<Rocket>(url).toPromise();
  }

  public generateQr(data: string, size: number) {
    const dim = size.toString() + 'x' + size.toString();
    return this.http.post<{qr: any}>(this.qrUrl, { 'data': data, 'size': dim }, httpOptions).toPromise();
  }

  public getMetrics() {
    return this.http.get<any>(this.metricsUrl).toPromise();
  }
}
